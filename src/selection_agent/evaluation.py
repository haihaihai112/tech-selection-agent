"""Offline deterministic scenario harness. Results measure mechanisms, not model ability."""
import json
import time
from pathlib import Path

from .catalog import CATALOG
from .config import Settings
from .engine import Engine
from .fixture import fixture_document
from .llm import Model
from .models import AnswerInput, ResearchInput, RevisionInput
from .models import StrictModel
from .db import Store
from .sources import Sources
from .usage import Usage


class PerturbedModel(Model):
    async def respond(self, stage, messages, tools, context=None):
        result = await super().respond(stage, messages, tools, context)
        if stage == 'research' and result.get('tool_calls'):
            function = result['tool_calls'][0]['function']
            if function['name'] == 'submit_findings':
                payload = json.loads(function['arguments'])
                if payload['claims']:
                    payload['claims'][0]['text'] = 'This unsupported statement is not in the cited original text.'
                function['arguments'] = json.dumps(payload)
        return result


async def finish(engine, task):
    job = engine.jobs.get(task['id'])
    if job:
        await job
    return engine.db.get('tasks', task['id'])


async def run_scenario(case, root):
    began = time.perf_counter()
    group, kind = case['group'], case['kind']
    config = Settings(runtime=Path(root) / case['id'], mode='fixture',
                      search_limit=1 if kind == 'budget' else 18, read_limit=1 if kind == 'budget' else 24)
    async def loader(product, url):
        if kind == 'unreadable' and product == CATALOG[group]['products'][1]:
            raise TimeoutError('injected source failure')
        return fixture_document(product, url)
    engine = Engine(config, model_factory=PerturbedModel if kind == 'unsupported' else Model, loader=loader)
    tasks, checks = [], []
    try:
        request = ResearchInput(group=group, query=case.get('query', '比较候选产品，未知条件暂不确定。'),
                                allow_unknown=kind != 'clarification')
        if kind == 'version':
            request.requested_versions = {CATALOG[group]['products'][0]: 'unavailable-v99'}
        task = await finish(engine, engine.submit(request))
        tasks.append(task)
        if kind == 'clarification':
            assert task['status'] == 'input_required'
            assert task['usage']['search_calls'] == 0
            resumed = await finish(engine, engine.answer(task['id'], AnswerInput(answer='未知条件先保留', allow_unknown=True)))
            assert resumed['id'] == task['id'] and resumed['status'] == 'completed'
            tasks.append(resumed)
            checks.append('same_task_clarification_and_resume')
        elif kind in {'revision', 'unchanged', 'refresh'}:
            assert task['status'] == 'completed'
            original = engine.report(task['report_id'], 1)
            change = '我已经使用PostgreSQL，优先维护成本' if kind == 'revision' else '保持原条件，重新判断'
            revised = await finish(engine, engine.revise(task['report_id'], RevisionInput(
                base_version=1, query=change, allow_unknown=True, force_refresh=kind == 'refresh')))
            tasks.append(revised)
            assert revised['status'] == 'completed'
            report = engine.report(task['report_id'])
            assert report['version'] == 2 and engine.report(task['report_id'], 1) == original
            assert report['usage']['read_calls'] == (3 if kind == 'refresh' else 0)
            if kind == 'revision':
                assert report['changes']['condition_changes']
            if kind == 'unchanged':
                assert not report['changes']['condition_changes']
                assert not report['changes']['judgments_changed']
            checks.append('immutable_versions_and_expected_reuse')
        elif kind in {'budget', 'unreadable', 'unsupported', 'version'}:
            assert task['status'] == 'partial'
            report = engine.report(task['report_id'])
            assert report['unresolved']
            assert task['usage']['search_calls'] <= config.search_limit
            assert task['usage']['read_calls'] <= config.read_limit
            if kind == 'unreadable':
                assert len([c for c in report['claims'] if c['status'] == 'supported']) == 10
                assert any(s['status'] == 'summary_only' for s in report['sources'])
            if kind == 'unsupported':
                assert all(c['status'] == 'insufficient' for c in report['claims'] if c['text'].startswith('This unsupported'))
            checks.append('observable_partial_result_without_unsupported_facts')
        elif kind == 'recovery':
            assert task['status'] == 'completed'
            before = engine.report(task['report_id'])
            await engine.close()
            engine = Engine(config)
            assert engine.report(task['report_id']) == before
            checks.append('report_survives_engine_restart')
        else:
            assert task['status'] == 'completed'
            report = engine.report(task['report_id'])
            assert len(report['claims']) == 15 and not report['unresolved']
            checks.append('three_product_comparison_with_fulltext_evidence')
        return {'case': case, 'passed': True, 'assertions': checks,
                'elapsed_seconds': round(time.perf_counter() - began, 4), 'tasks': tasks,
                'reports': [engine.report(t['report_id'], t.get('report_version')) for t in tasks if t.get('report_version')]}
    except Exception as exc:
        return {'case': case, 'passed': False, 'error_type': type(exc).__name__, 'tasks': tasks,
                'elapsed_seconds': round(time.perf_counter() - began, 4)}
    finally:
        await engine.close()


async def reuse_ablation(root):
    config = Settings(runtime=Path(root), mode='fixture')
    engine = Engine(config)
    first = await finish(engine, engine.submit(ResearchInput(query='本地部署，已有技术栈暂不明确', allow_unknown=True)))
    results = []
    for base, refresh in [(1, False), (2, True)]:
        start = time.perf_counter()
        task = await finish(engine, engine.revise(first['report_id'], RevisionInput(base_version=base,
            query='已经使用PostgreSQL', allow_unknown=True, force_refresh=refresh)))
        report = engine.report(first['report_id'])
        results.append({'condition': 'full_refresh' if refresh else 'reuse', 'status': task['status'],
                        'elapsed_seconds': round(time.perf_counter() - start, 4), 'usage': task['usage'],
                        'supported_facts': sum(c['status'] == 'supported' for c in report['claims']),
                        'unresolved_count': len(report['unresolved']), 'report': report})
    await engine.close()
    return {'mode': 'fixture', 'note': '真实执行本地流程的单次测量，不代表真实模型速度或语义质量。', 'runs': results}


class BaselineOutput(StrictModel):
    facts: list[str]


async def evidence_ablation(root):
    """Two actual paths over controlled paired summaries/fulltexts; no fabricated live score."""
    group = CATALOG['vector_databases']
    truth = {}
    for product in group['products']:
        truth[product] = []
        for index, dimension in enumerate(group['dimensions']):
            truth[product].append(f'{dimension}：测试设定下，{product}的属性{index}仅适用于版本v1，不适用于版本v2。')
    async def searcher(product, query):
        # Deliberately omit a scope qualification in the first snippet; known controlled failure.
        summaries = [s.replace('仅适用于版本v1，不适用于版本v2', '适用于所有版本') if i == 0 else s
                     for i, s in enumerate(truth[product])]
        return [{'url': f'https://ablation.example.org/{product}', 'title': '测试设定来源', 'summary': '\n'.join(summaries)}]
    async def loader(product, url):
        return '\n\n'.join(truth[product]), {'title': '受控测试原文'}
    config = Settings(runtime=Path(root) / 'summary', mode='fixture')
    usage = Usage(config)
    sources = Sources(config, Store(config.runtime / 'research.sqlite'), 'ablation', usage, [], searcher=searcher)
    began = time.perf_counter()
    snippets = []
    for product in group['products']:
        data = await sources.search(product, product)
        snippets.extend(s['summary'] for s in data['results'])
    baseline = await Model(config, usage).structured('summary_ablation', '仅根据摘要生成报告事实。',
                                                    {'summaries': snippets}, BaselineOutput)
    known_truth = {text for values in truth.values() for text in values}
    baseline_result = {'path': 'summary_only', 'facts': baseline.facts,
        'matches_annotated_fixture_truth': sum(f in known_truth for f in baseline.facts),
        'elapsed_seconds': round(time.perf_counter() - began, 4), 'usage': usage.snapshot()}
    engine = Engine(Settings(runtime=Path(root) / 'fulltext', mode='fixture'), loader=loader, searcher=searcher)
    began = time.perf_counter()
    task = await finish(engine, engine.submit(ResearchInput(query='比较三款数据库', allow_unknown=True)))
    report = engine.report(task['report_id'])
    facts = [c['text'] for c in report['claims'] if c['status'] == 'supported']
    fulltext_result = {'path': 'fulltext_and_verification', 'facts': facts,
        'matches_annotated_fixture_truth': sum(f in known_truth for f in facts),
        'elapsed_seconds': round(time.perf_counter() - began, 4), 'usage': task['usage'], 'report': report}
    await engine.close()
    return {'mode': 'fixture', 'note': '人为注入摘要丢失版本限定的受控实验。按预先构造的事实逐字检查，不是模型语义评分。',
            'runs': [baseline_result, fulltext_result]}
