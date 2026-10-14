from __future__ import annotations

import asyncio
import hashlib
import io
import ipaddress
import re
import socket
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlsplit, urlunsplit

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

from .catalog import is_official
from .models import EvidenceSpan, SourceSnapshot
from .usage import BudgetExceeded


class SourceError(Exception):
    pass


def canonical_url(url):
    parts = urlsplit(url)
    if parts.scheme not in {'http', 'https'} or not parts.hostname or parts.username or parts.password:
        raise SourceError('只允许不含凭据的公开HTTP(S)地址')
    if parts.port not in {None, 80, 443}:
        raise SourceError('不支持此端口')
    if parts.hostname.lower() in {'localhost', 'localhost.localdomain'} or parts.hostname.endswith('.local'):
        raise SourceError('禁止读取本机或内部地址')
    try:
        address = ipaddress.ip_address(parts.hostname)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise SourceError('禁止读取非公开IP地址')
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path or '/', parts.query, ''))


async def public_addresses(host, port):
    rows = await asyncio.get_running_loop().getaddrinfo(host, port, type=socket.SOCK_STREAM)
    addresses = list(dict.fromkeys(row[4][0] for row in rows))
    if not addresses or any(not ipaddress.ip_address(ip).is_global for ip in addresses):
        raise SourceError('目标解析到非公开网络地址')
    return addresses


class PublicTransport(httpx.AsyncBaseTransport):
    """Pin the resolved public IP, preserving TLS SNI and Host (including every redirect)."""
    def __init__(self):
        self.inner = httpx.AsyncHTTPTransport(retries=0)

    async def handle_async_request(self, request):
        host = request.url.host
        addresses = await public_addresses(host, request.url.port or (443 if request.url.scheme == 'https' else 80))
        # IPv4 first avoids unavailable IPv6 routes on common local development setups.
        addresses.sort(key=lambda ip: ':' in ip)
        pinned = httpx.Request(request.method, request.url.copy_with(host=addresses[0]),
            headers=request.headers, stream=request.stream,
            extensions={**request.extensions, 'sni_hostname': host})
        return await self.inner.handle_async_request(pinned)

    async def aclose(self):
        await self.inner.aclose()


def extract_document(body: bytes, content_type: str, url: str):
    metadata = {'title': url, 'published_at': None, 'document_version': None, 'original_url': None}
    if 'pdf' in content_type or body[:5] == b'%PDF-':
        reader = PdfReader(io.BytesIO(body))
        if reader.is_encrypted:
            raise SourceError('不读取加密PDF')
        text = '\n\n'.join(page.extract_text() or '' for page in reader.pages[:80])
        if len(text.strip()) < 30:
            raise SourceError('PDF无可用文本层，首版不包含OCR')
        if reader.metadata:
            metadata['title'] = str(reader.metadata.title or url)
    elif 'html' in content_type:
        soup = BeautifulSoup(body, 'html.parser')
        if soup.title:
            metadata['title'] = soup.title.get_text(' ', strip=True)
        for selector in ('meta[property="article:published_time"]', 'meta[name="date"]'):
            item = soup.select_one(selector)
            if item and item.get('content'):
                metadata['published_at'] = item['content']
                break
        version = soup.select_one('meta[name="version"]')
        if version:
            metadata['document_version'] = version.get('content')
        canonical = soup.select_one('link[rel="canonical"]')
        if canonical and canonical.get('href'):
            try:
                metadata['original_url'] = canonical_url(urljoin(url, canonical['href']))
            except SourceError:
                pass
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript', 'form']):
            tag.decompose()
        main = soup.find('main') or soup.find('article') or soup.body or soup
        block_tags = {'p', 'li', 'pre', 'tr', 'h1', 'h2', 'h3', 'h4', 'blockquote'}
        blocks = [node.get_text(' ', strip=True) for node in main.find_all(list(block_tags))
                  if not any(parent.name in block_tags for parent in node.parents if parent is not main)]
        text = '\n\n'.join(blocks) if blocks else main.get_text('\n', strip=True)
    elif content_type.startswith('text/'):
        text = body.decode('utf-8', errors='replace')
    else:
        raise SourceError('不支持的内容类型，只读取HTML、文本和文本型PDF')
    text = text.replace('\x00', '').strip()[:200_000]
    if len(text) < 30:
        raise SourceError('正文不足或页面需要客户端渲染')
    return text, metadata


async def fetch_document(url, transport=None):
    target = canonical_url(url)
    async with httpx.AsyncClient(transport=transport or PublicTransport(), timeout=20,
                                 follow_redirects=False, trust_env=False) as client:
        for _ in range(5):
            canonical_url(target)
            async with client.stream('GET', target, headers={'User-Agent': 'TechSelectionResearch/0.1'}) as response:
                if response.status_code in {301, 302, 303, 307, 308}:
                    target = canonical_url(urljoin(target, response.headers.get('location', '')))
                    continue
                if response.status_code in {401, 403, 407}:
                    raise SourceError('页面需要授权或拒绝读取')
                if response.status_code >= 400:
                    raise SourceError(f'页面返回HTTP {response.status_code}')
                chunks, size = [], 0
                async for chunk in response.aiter_bytes():
                    size += len(chunk)
                    if size > 5_000_000:
                        raise SourceError('文档超过5MB读取上限')
                    chunks.append(chunk)
                text, metadata = await asyncio.to_thread(extract_document, b''.join(chunks),
                    response.headers.get('content-type', ''), target)
                return text, {**metadata, 'final_url': target}
    raise SourceError('重定向次数超过上限')


def paragraphs(text):
    return [part[start:start + 1600] for part in re.split(r'\n+', text) if part.strip()
            for start in range(0, len(part), 1600)]


class Sources:
    def __init__(self, config, db, session_id, usage, trace, persist=None, loader=None, searcher=None,
                 fixture_dimensions=None):
        self.config, self.db, self.session_id = config, db, session_id
        self.usage, self.trace, self.persist = usage, trace, persist
        self.loader, self.searcher, self.fixture_dimensions = loader, searcher, fixture_dimensions
        self.snapshot_ids = set()
        self.summary_ids = set()
        self.allowed_evidence = set()
        self.searched = {}
        self.fresh = {}

    def record(self, operation, product, status, began, **extra):
        self.trace.append({'operation': operation, 'product': product, 'status': status,
                           'elapsed_ms': round((time.perf_counter() - began) * 1000, 2), **extra})
        if self.persist:
            self.persist()

    async def search(self, product, query):
        began = time.perf_counter()
        await self.usage.reserve('search')
        try:
            if self.searcher:
                rows = await self.searcher(product, query)
            elif self.config.mode == 'fixture':
                from .fixture import fixture_search
                rows = fixture_search(product)
            else:
                if not self.config.tavily_key:
                    raise SourceError('未配置TAVILY_API_KEY')
                async with httpx.AsyncClient(timeout=20, transport=httpx.AsyncHTTPTransport(local_address='0.0.0.0')) as client:
                    response = await client.post('https://api.tavily.com/search', json={
                        'api_key': self.config.tavily_key, 'query': query, 'search_depth': 'basic',
                        'max_results': 5, 'include_answer': False, 'include_raw_content': False})
                    response.raise_for_status()
                    rows = [{'url': r['url'], 'title': r.get('title', ''), 'summary': r.get('content', '')}
                            for r in response.json().get('results', [])]
            good = []
            for row in rows:
                try:
                    url = canonical_url(row['url'])
                except (SourceError, ValueError):
                    continue
                clean = {'url': url, 'title': row.get('title', '')[:300], 'summary': row.get('summary', '')[:1500],
                         'official': is_official(product, url), 'status': 'summary_only'}
                self.searched[(product, url)] = clean
                # Search summaries are retained for audit, never become evidence spans.
                key = hashlib.sha256(f'{self.session_id}:{product}:{url}:summary'.encode()).hexdigest()[:24]
                source = SourceSnapshot(id=key, session_id=self.session_id, product=product, url=url,
                    title=clean['title'], source_type='fixture' if self.config.mode == 'fixture' else
                    'official' if clean['official'] else 'third_party', model_mode=self.config.mode,
                    status='summary_only', summary=clean['summary'])
                self.db.put('sources', key, source.model_dump())
                self.summary_ids.add(key)
                good.append(clean)
            good.sort(key=lambda r: not r['official'])
            self.record('search', product, 'ok', began, count=len(good))
            return {'ok': True, 'results': good}
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.usage.values['failed_calls'] += 1
            self.record('search', product, 'error', began, error_type=type(exc).__name__)
            return {'ok': False, 'error': '搜索失败：' + type(exc).__name__}

    def usable(self, source, product, version, sensitive, refresh):
        if refresh or source['session_id'] != self.session_id or source['product'] != product:
            return False
        if source['status'] != 'fulltext' or source['model_mode'] != self.config.mode:
            return False
        if source.get('requested_version') != version:
            return False
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(source['retrieved_at'])).total_seconds()
        return 0 <= age < (3600 if sensitive or source.get('sensitive') else 86400)

    def expose(self, source):
        spans = [e for e in self.db.all('evidence') if e['snapshot_id'] == source['id']]
        terms = re.compile(r'install|deploy|docker|postgres|filter|index|license|pricing|price|quota|limit|cluster|scale|'
                           r'workflow|model|document|api|content|source|版本|部署|检索|许可|计费|接口|工作流', re.I)
        ranked = sorted(spans, key=lambda e: (-len(terms.findall(e['text'])), e['paragraph']))
        chosen, size = [], 0
        for span in ranked:
            if len(chosen) >= 16 or size + len(span['text']) > 16000:
                break
            chosen.append(span)
            size += len(span['text'])
        chosen.sort(key=lambda e: e['paragraph'])
        self.snapshot_ids.add(source['id'])
        self.allowed_evidence.update(e['id'] for e in chosen)
        return {'ok': True, 'snapshot': source, 'evidence': chosen,
                'total_paragraphs': len(spans), 'note': '展示限长的相关段落；完整快照保留在来源存储中。'}

    def cached(self, product, version=None, sensitive=False, refresh=False):
        rows = [s for s in self.db.all('sources') if self.usable(s, product, version, sensitive, refresh)]
        newest = {}
        for s in sorted(rows, key=lambda r: r['retrieved_at']):
            newest[s['url']] = s
        return list(newest.values())

    async def read(self, product, url, version=None, sensitive=False, refresh=False):
        began = time.perf_counter()
        try:
            url = canonical_url(url)
            fresh_key = (product, url, version)
            cached = next((s for s in self.cached(product, version, sensitive, refresh) if s['url'] == url), None)
            cached = self.fresh.get(fresh_key) or cached
            if cached:
                if cached['id'] not in self.snapshot_ids:
                    self.usage.values['reused_snapshots'] += 1
                self.record('read_page', product, 'reused', began, snapshot_id=cached['id'])
                return self.expose(cached)
            await self.usage.reserve('read')
            if self.loader:
                text, metadata = await self.loader(product, url)
            elif self.config.mode == 'fixture':
                from .fixture import fixture_document
                text, metadata = fixture_document(product, url, self.fixture_dimensions)
            else:
                text, metadata = await fetch_document(url)
            digest = hashlib.sha256(text.encode()).hexdigest()
            source_id = hashlib.sha256(f'{self.session_id}:{product}:{url}:{time.time_ns()}'.encode()).hexdigest()[:24]
            same_content = next((s for s in self.db.all('sources') if s['session_id'] == self.session_id and
                s.get('content_hash') == digest and s['status'] == 'fulltext'), None)
            path = self.config.runtime / 'snapshots' / (digest + '.txt')
            path.parent.mkdir(exist_ok=True)
            path.write_text(text, encoding='utf-8')
            source = SourceSnapshot(id=source_id, session_id=self.session_id, product=product, url=url,
                title=metadata.get('title') or url, source_type='fixture' if self.config.mode == 'fixture' else
                'official' if is_official(product, metadata.get('final_url', url)) else 'third_party',
                published_at=metadata.get('published_at'), document_version=metadata.get('document_version'),
                requested_version=version, content_hash=digest, content_path=path.name,
                original_url=metadata.get('original_url'), duplicate_of=same_content['id'] if same_content else None,
                sensitive=sensitive or bool(re.search(r'price|quota|pricing|套餐|计费|额度|价格', text, re.I)),
                model_mode=self.config.mode)
            self.db.put('sources', source_id, source.model_dump())
            for index, part in enumerate(paragraphs(text)):
                evidence = EvidenceSpan(id=f'E-{source_id}-{index}', snapshot_id=source_id,
                    session_id=self.session_id, product=product, paragraph=index, text=part)
                self.db.put('evidence', evidence.id, evidence.model_dump())
            self.fresh[fresh_key] = source.model_dump()
            self.record('read_page', product, 'ok', began, snapshot_id=source_id)
            return self.expose(source.model_dump())
        except asyncio.CancelledError:
            raise
        except BudgetExceeded:
            raise
        except Exception as exc:
            self.usage.values['failed_calls'] += 1
            # Do not expose HTTP exceptions containing URLs, tokens or proxy credentials.
            self.record('read_page', product, 'error', began, error_type=type(exc).__name__)
            return {'ok': False, 'status': 'summary_only', 'error': '原文无法读取：' + type(exc).__name__}
