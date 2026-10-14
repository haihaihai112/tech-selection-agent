"""Deterministic TEST DOUBLE. No factual product capability or price is asserted here."""
import json
import re
import uuid
from urllib.parse import quote

from .catalog import CATALOG


def call(name, args):
    return {'role': 'assistant', 'content': '', 'tool_calls': [{'id': 'fixture-' + uuid.uuid4().hex,
        'type': 'function', 'function': {'name': name, 'arguments': json.dumps(args, ensure_ascii=False)}}]}


def fixture_search(product):
    return [{'url': 'https://fixtures.example.org/' + quote(product, safe='') + '/documentation',
             'title': '测试替身资料：' + product, 'summary': '测试摘要，不能作为真实产品能力的依据。'}]


def fixture_document(product, url, custom_dimensions=None):
    group = next((g for g in CATALOG.values() if product in g['products']), None)
    if group is None:
        group = {'dimensions': custom_dimensions or ['部署方式', '维护要求']}
    lines = []
    for dimension in group['dimensions']:
        value = f'【测试设定】{product}的{dimension}应根据用户条件进一步检查；不代表真实产品事实。'
        lines.append(f'{dimension}：{value}')
    return '\n\n'.join(lines), {'title': '合成测试文档：' + product,
                                'document_version': 'fixture-1', 'published_at': None}


def respond(stage, messages, tools, context):
    if stage == 'summary_ablation':
        return call('emit', {'facts': [line for text in context['summaries'] for line in text.splitlines()]})
    if stage == 'brief':
        previous = context.get('previous') or {}
        group = context['input']['group']
        catalog = context.get('catalog') or CATALOG.get(group)
        question_bank = catalog.get('questions') or ['部署要求', '主要技术约束']
        text = context['input']['query'] + '\n' + context.get('answer', '')
        constraints = dict(previous.get('constraints', {}))
        if re.search(r'PostgreSQL|postgres|PG数据库', text, re.I):
            constraints['已有技术栈'] = 'PostgreSQL'
        if any(w in text for w in ('本地', '自托管', '离线')):
            constraints['部署要求'] = '本地或自托管'
        elif '托管服务' in text:
            constraints['部署要求'] = '托管服务'
        if '研究报告' in text:
            constraints['使用场景'] = '研究报告'
        if '正文' in text:
            constraints['内容要求'] = '正文'
        if any(w in text for w in ('PDF', 'pdf', '文档')):
            constraints['文档类型'] = '用户提及的文档类型'
        questions = []
        if group in {'vector_databases', 'rag_platforms'} and '部署要求' not in constraints:
            questions.append(question_bank[0])
        other = {'vector_databases': '已有技术栈', 'search_apis': '内容要求', 'rag_platforms': '文档类型'}.get(group)
        if other is None and catalog.get('dimensions'):
            other = catalog['dimensions'][0]
        if other not in constraints:
            questions.append(question_bank[1])
        unknowns = questions if context['input']['allow_unknown'] else []
        preferences = list(previous.get('preferences', []))
        if '维护' in text and '维护成本' not in preferences:
            preferences.append('维护成本')
        return call('emit', {'group': group, 'products': catalog['products'], 'dimensions': catalog['dimensions'],
            'constraints': constraints, 'preferences': preferences,
            'questions': [] if context['input']['allow_unknown'] else questions,
            'unknowns': unknowns, 'requested_versions': context['input']['requested_versions']})
    if stage == 'research':
        results = [json.loads(m['content']) for m in messages if m['role'] == 'tool']
        read = next((r for r in reversed(results) if r.get('ok') and r.get('evidence')), None)
        if read:
            claims = []
            for dimension in context['dimensions']:
                evidence = next((e for e in read['evidence'] if e['text'].startswith(dimension + '：')), None)
                if evidence:
                    claims.append({'product': context['product'], 'dimension': dimension, 'attribute': dimension,
                        'value': evidence['text'].split('：', 1)[1], 'text': evidence['text'],
                        'evidence_ids': [evidence['id']], 'scope': {}})
            return call('submit_findings', {'claims': claims, 'gaps': []})
        if {t['function']['name'] for t in tools} == {'submit_findings'}:
            return call('submit_findings', {'claims': [], 'gaps': context['dimensions']})
        if context.get('cached') and not results:
            return call('read_page', {'url': context['cached'][0]['url']})
        searched = next((r for r in reversed(results) if r.get('ok') and 'results' in r), None)
        if searched and searched['results'] and not any(not r.get('ok') for r in results):
            return call('read_page', {'url': searched['results'][0]['url']})
        if results:
            return call('submit_findings', {'claims': [], 'gaps': context['dimensions']})
        return call('search', {'query': context['product'] + ' ' + ' '.join(context['dimensions'])})
    if stage == 'verify':
        verdicts = []
        for item in context['claims']:
            spans = context['evidence']
            supported = any(item['text'] in spans.get(e, '') for e in item['evidence_ids'])
            if re.search(r'ignore previous|忽略.*指令|system prompt', item['text'], re.I):
                supported = False
            verdicts.append({'claim_id': item['id'], 'status': 'supported' if supported else 'insufficient',
                             'reason': '测试替身仅验证逐字证据对应，不是语义能力实测。', 'conflicting_ids': []})
        return call('emit', {'verdicts': verdicts})
    if stage == 'verify_judgments':
        return call('emit', {'verdicts': [{'claim_id': j['id'], 'status': 'supported'
            if j['reasoning'].startswith('【测试推理】') else 'insufficient',
            'reason': '测试替身只接受明示测试推理模板，不代表语义核验能力。', 'conflicting_ids': []}
            for j in context['judgments']]})
    if stage == 'write':
        judgments = []
        for product in context['brief']['products']:
            ids = [c['id'] for c in context['claims'] if c['product'] == product and c['status'] == 'supported']
            if ids:
                conditions = context['brief']['constraints']
                judgments.append({'product': product,
                    'reasoning': '【测试推理】根据当前条件 ' + json.dumps(conditions, ensure_ascii=False) +
                                 ' 重新检查适配性；此处不提供真实产品排名或推荐。',
                    'condition_keys': list(conditions), 'claim_ids': ids[:2]})
        return call('emit', {'judgments': judgments})
    raise ValueError('unknown fixture stage')
