from __future__ import annotations

import asyncio
import time
import uuid
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from .catalog import catalog_for_request
from .db import Store
from .llm import Model, ModelUnavailable
from .models import ResearchBrief, ResearchInput, ReportVersion, SourceSnapshot, VerifiedClaim, now
from .research import gaps_for, research_product, verify_claims
from .reporting import diff, judgments, render
from .sources import Sources
from .usage import Usage

TERMINAL = {'completed', 'partial', 'failed', 'canceled', 'interrupted'}


class Conflict(Exception):
    pass


class GraphState(TypedDict):
    run: object


class Run:
    def __init__(self, engine, task):
        self.engine, self.config, self.db, self.task = engine, engine.config, engine.db, task
        self.started = time.monotonic()
        self.previous_seconds = task.get('active_seconds', 0)
        self.trace = task.get('trace', [])
        self.usage = Usage(self.config, task.get('usage_counters'))
        self.model = engine.model_factory(self.config, self.usage)
        self.sources = Sources(self.config, self.db, task['session_id'], self.usage, self.trace, self.save,
                               loader=engine.loader, searcher=engine.searcher,
                               fixture_dimensions=((task.get('input') or {}).get('custom_catalog') or {}).get('dimensions'))
        self.brief = ResearchBrief.model_validate(task['brief']) if task.get('brief') else None
        self.claims = [VerifiedClaim.model_validate(c) for c in task.get('claims', [])]
        self.steps = task.get('research_steps', {})
        self.round = task.get('repair_round', 0)
        self.gaps = {}
        self.previous = self.db.get('reports', f'{task["report_id"]}:{task["base_version"]}') if task.get('base_version') else None

    def save(self, checkpoint=None):
        if checkpoint:
            self.task['checkpoint'] = checkpoint
        self.task.update(trace=self.trace, usage=self.usage.snapshot(), usage_counters=dict(self.usage.values),
                         brief=self.brief.model_dump() if self.brief else None,
                         claims=[c.model_dump() for c in self.claims], research_steps=self.steps,
                         repair_round=self.round, active_seconds=self.previous_seconds + time.monotonic() - self.started,
                         snapshot_ids=sorted(self.sources.snapshot_ids), evidence_ids=sorted(self.sources.allowed_evidence),
                         summary_only_ids=sorted(self.sources.summary_ids),
                         updated_at=now())
        self.db.put('tasks', self.task['id'], self.task)


class Engine:
    def __init__(self, config, model_factory=Model, loader=None, searcher=None):
        self.config, self.model_factory = config, model_factory
        self.loader, self.searcher = loader, searcher
        self.db = Store(config.runtime / 'research.sqlite')
        self.jobs, self.locks = {}, {}
        for task in self.db.all('tasks'):
            if task['status'] in {'queued', 'working'}:
                task.update(status='interrupted', error='服务重启；未静默重跑付费请求。请重新发起研究。')
                self.db.put('tasks', task['id'], task)
        graph = StateGraph(GraphState)
        graph.add_node('clarify', self.clarify)
        graph.add_node('research', self.research)
        graph.add_node('verify', self.verify)
        graph.add_node('write', self.write)
        graph.add_edge(START, 'clarify')
        graph.add_conditional_edges('clarify', lambda s: 'end' if s['run'].task['status'] == 'input_required' else 'research',
                                    {'end': END, 'research': 'research'})
        graph.add_edge('research', 'verify')
        graph.add_conditional_edges('verify', self.after_verify, {'research': 'research', 'write': 'write'})
        graph.add_edge('write', END)
        self.graph = graph.compile()

    def require_idle(self, session_id):
        if any(t['session_id'] == session_id and t['status'] in {'queued', 'working'} for t in self.db.all('tasks')):
            raise Conflict('当前会话已有运行中的任务，请等待或取消后继续。')

    def submit(self, request: ResearchInput, report_id=None, base_version=None):
        sid = request.session_id or uuid.uuid4().hex
        if request.session_id and not self.db.get('sessions', sid):
            raise KeyError('session not found')
        self.require_idle(sid)
        request = request.model_copy(update={'session_id': sid})
        if not self.db.get('sessions', sid):
            self.db.put('sessions', sid, {'id': sid, 'created_at': now()})
        task = {'id': uuid.uuid4().hex, 'session_id': sid, 'input': request.model_dump(),
                'report_id': report_id or uuid.uuid4().hex, 'base_version': base_version, 'status': 'queued',
                'created_at': now(), 'trace': [], 'usage': {}, 'model_mode': self.config.mode,
                'brief': None, 'claims': [], 'active_seconds': 0, 'error': None}
        self.db.put('tasks', task['id'], task)
        self.launch(task['id'])
        return task

    def launch(self, task_id):
        self.jobs[task_id] = asyncio.create_task(self.run(task_id))

    def answer(self, task_id, answer):
        task = self.db.get('tasks', task_id)
        if not task:
            raise KeyError('task not found')
        if task['status'] != 'input_required':
            raise Conflict('只有等待补充条件的任务可以继续。')
        self.require_idle(task['session_id'])
        task['answer'] = task.get('answer', '') + '\n' + answer.answer
        task['input']['allow_unknown'] = answer.allow_unknown or task['input']['allow_unknown']
        task['status'] = 'queued'
        self.db.put('tasks', task_id, task)
        self.launch(task_id)
        return task

    def report(self, report_id, version=None):
        latest = self.db.get('report_heads', report_id)
        if not latest:
            return None
        return self.db.get('reports', f'{report_id}:{version or latest["version"]}')

    def revise(self, report_id, request):
        old = self.report(report_id)
        if not old:
            raise KeyError('report not found')
        if old['version'] != request.base_version:
            raise Conflict('基础报告版本已变化，请读取最新报告。')
        original = self.db.get('tasks', old['task_id'])['input']
        new = ResearchInput(**{**original, 'query': original['query'] + '\n用户修改条件：' + request.query,
            'allow_unknown': request.allow_unknown, 'force_refresh': request.force_refresh,
            'requested_versions': {**old['brief']['requested_versions'], **request.requested_versions}})
        return self.submit(new, report_id, request.base_version)

    async def cancel(self, task_id):
        task = self.db.get('tasks', task_id)
        if not task:
            raise KeyError('task not found')
        if task['status'] in TERMINAL:
            return task
        job = self.jobs.get(task_id)
        if job and not job.done():
            job.cancel()
            await asyncio.gather(job, return_exceptions=True)
        task = self.db.get('tasks', task_id)
        task.update(status='canceled', error='用户取消，已采集记录保留。')
        self.db.put('tasks', task_id, task)
        return task

    async def close(self):
        jobs = list(self.jobs.values())
        for job in jobs:
            job.cancel()
        await asyncio.gather(*jobs, return_exceptions=True)

    async def run(self, task_id):
        task = self.db.get('tasks', task_id)
        run = None
        try:
            async with self.locks.setdefault(task['session_id'], asyncio.Lock()):
                task['status'] = 'working'
                run = Run(self, task)
                run.save('starting')
                remaining = max(0.01, self.config.task_timeout - run.previous_seconds)
                async with asyncio.timeout(remaining):
                    await self.graph.ainvoke({'run': run}, config={'recursion_limit': 16})
        except asyncio.CancelledError:
            if run:
                run.task.update(status='interrupted', error='处理被中断；已采集记录保留。')
                run.save()
            raise
        except TimeoutError:
            if run:
                run.task.update(status='partial', error='已达到主动处理时限；已核验资料和缺口已保留，未继续调用。')
                if run.brief:
                    await self.persist_report(run, [], partial=True)
                run.save('timeout')
        except Exception as exc:
            if run:
                run.task.update(status='failed', error='处理失败：' + type(exc).__name__)
                if isinstance(exc, ModelUnavailable):
                    run.task.update(error=str(exc), provider_code=exc.code, http_status=exc.status_code)
                run.trace.append({'operation': 'task', 'status': 'error', 'error_type': type(exc).__name__})
                run.save()
        finally:
            self.jobs.pop(task_id, None)

    async def clarify(self, state):
        run = state['run']
        request = run.task['input']
        catalog = catalog_for_request(request)
        previous = run.brief.model_dump() if run.brief else run.previous['brief'] if run.previous else None
        brief = await run.model.structured('brief',
            '将用户明确条件转为研究任务。保留先前条件，但用户新条件明确修改同一项时以新条件为准。'
            '不要猜测预算、数据规模、已有技术栈、部署方式。影响判断的缺失条件用questions追问，最多两问。'
            'allow_unknown=true时不再追问，缺失项进入unknowns，生成条件式研究。'
            '使用输入catalog的全部products和dimensions，不增减；requested_versions来自显式输入。'
            '用户自然语言指定的版本要求也应补入requested_versions，无法定位则追问。',
            {'input': request, 'answer': run.task.get('answer', ''), 'previous': previous, 'catalog': catalog}, ResearchBrief)
        if brief.group != request['group'] or brief.products != catalog['products'] or brief.dimensions != catalog['dimensions']:
            raise ValueError('研究范围不符合产品目录')
        if set(brief.requested_versions) - set(brief.products):
            raise ValueError('版本要求包含未知产品')
        brief.requested_versions.update(request['requested_versions'])
        if request['allow_unknown']:
            brief.unknowns = list(dict.fromkeys(brief.unknowns + brief.questions))
            brief.questions = []
        run.brief = brief
        if brief.questions:
            run.task['status'] = 'input_required'
        run.trace.append({'operation': 'clarify', 'status': run.task['status'], 'questions': brief.questions})
        run.save('clarify')
        return state

    async def research(self, state):
        run = state['run']
        targets = run.gaps or {p: run.brief.dimensions for p in run.brief.products}
        if run.round == 0 and run.previous and not run.task['input']['force_refresh']:
            # Reuse facts separately from user-conditioned recommendations; freshness checked per snapshot.
            for raw in run.previous['claims']:
                if raw['status'] != 'supported':
                    continue
                claim = VerifiedClaim.model_validate(raw)
                source_ids = {self.db.get('evidence', eid)['snapshot_id'] for eid in claim.evidence_ids}
                sensitive = claim.dimension in {'计费方式', '接口限制'}
                rows = [self.db.get('sources', sid) for sid in source_ids]
                if all(s and run.sources.usable(s, claim.product, run.brief.requested_versions.get(claim.product),
                                               sensitive, False) for s in rows):
                    for s in rows:
                        if s['id'] not in run.sources.snapshot_ids:
                            run.usage.values['reused_snapshots'] += 1
                        run.sources.expose(s)
                    run.claims.append(claim)
            targets = gaps_for(run.brief, run.claims)
        run.trace.append({'operation': 'research_round', 'round': run.round, 'targets': targets, 'status': 'working'})
        run.save('research')
        async def collect(product, dims):
            result = await research_product(run.model, run.sources, run.brief, product, dims,
                self.config, run.steps, run.task['input']['force_refresh'])
            # Identical facts are not counted twice when a repair reads the same source again.
            existing = {(c.product, c.dimension, c.text, tuple(c.evidence_ids)) for c in run.claims}
            run.claims.extend(c for c in result if (c.product, c.dimension, c.text, tuple(c.evidence_ids)) not in existing)
            run.save('researcher_finished')
        results = await asyncio.gather(*(collect(product, dims) for product, dims in targets.items()), return_exceptions=True)
        for result in results:
            if isinstance(result, BaseException):
                run.trace.append({'operation': 'researcher', 'status': 'error', 'error_type': type(result).__name__})
        fatal = next((r for r in results if isinstance(r, ModelUnavailable)), None)
        if fatal:
            raise fatal
        run.save('researched')
        return state

    async def verify(self, state):
        run = state['run']
        run.claims = await verify_claims(run.model, run.sources, run.brief, run.claims)
        run.gaps = gaps_for(run.brief, run.claims)
        run.save('verified')
        return state

    def after_verify(self, state):
        run = state['run']
        if run.gaps and run.round < self.config.repair_rounds and any(
                run.steps.get(p, 0) < self.config.research_steps for p in run.gaps) and (
                run.usage.values['search_calls'] < self.config.search_limit or run.usage.values['read_calls'] < self.config.read_limit):
            run.round += 1
            return 'research'
        return 'write'

    async def write(self, state):
        run = state['run']
        decisions = await judgments(run.model, run.brief, run.claims)
        await self.persist_report(run, decisions, partial=bool(run.gaps))
        run.save('reported')
        return state

    async def persist_report(self, run, decisions, partial=False):
        # Never publish candidate claims left mid-verification as supported.
        version = (run.task.get('base_version') or 0) + 1
        unresolved = [{'product': p, 'dimension': d, 'reason': '没有足够的无冲突原文证据；不据此判定不支持。'}
                      for p, dims in gaps_for(run.brief, run.claims).items() for d in dims]
        sources = [SourceSnapshot.model_validate(self.db.get('sources', sid)) for sid in sorted(run.sources.snapshot_ids)]
        full_urls = {s.url for s in sources}
        sources.extend(SourceSnapshot.model_validate(self.db.get('sources', sid)) for sid in sorted(run.sources.summary_ids)
                       if self.db.get('sources', sid)['url'] not in full_urls)
        markdown = render(run.brief, run.claims, decisions, unresolved, sources, version, self.config.mode)
        report = ReportVersion(report_id=run.task['report_id'], version=version, task_id=run.task['id'],
            session_id=run.task['session_id'], model_mode=self.config.mode, brief=run.brief,
            claims=run.claims, judgments=decisions, unresolved=unresolved, sources=sources,
            previous_version=run.task.get('base_version'), usage=run.usage.snapshot(), markdown=markdown,
            changes=diff(run.previous, run.brief, run.claims, decisions, markdown, run.usage.values['reused_snapshots']))
        with self.db.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            head = self.db.get('report_heads', report.report_id, db)
            if head and head['version'] != run.task.get('base_version'):
                raise Conflict('报告基础版本已变化')
            self.db.put('reports', f'{report.report_id}:{version}', report.model_dump(), db)
            self.db.put('report_heads', report.report_id, {'version': version}, db)
        run.task.update(status='partial' if partial else 'completed', report_version=version)
