import asyncio
import json
from datetime import datetime, timedelta, timezone

import pytest

from selection_agent.catalog import CATALOG
from selection_agent.config import Settings
from selection_agent.engine import Conflict, Engine
from selection_agent.fixture import fixture_document, call
from selection_agent.llm import Model
from selection_agent.models import AnswerInput, ResearchInput, RevisionInput


async def run(engine, request):
    task = engine.submit(request)
    await engine.jobs[task['id']]
    return engine.db.get('tasks', task['id'])


@pytest.mark.parametrize('group', list(CATALOG))
async def test_three_groups_complete_with_traceable_facts(tmp_path, group):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'))
    task = await run(engine, ResearchInput(query='比较产品，未知条件暂不确定', group=group, allow_unknown=True))
    assert task['status'] == 'completed', task.get('error')
    report = engine.report(task['report_id'])
    assert len(report['claims']) == 15 and not report['unresolved']
    assert all(c['status'] == 'supported' for c in report['claims'])
    assert '测试替身' in report['markdown'] and all(s['source_type'] == 'fixture' for s in report['sources'])
    assert report['usage']['search_calls'] == report['usage']['read_calls'] == 3
    for claim in report['claims']:
        for eid in claim['evidence_ids']:
            assert engine.db.get('evidence', eid)['session_id'] == task['session_id']


async def test_clarify_continue_same_task_and_restart(tmp_path):
    config = Settings(runtime=tmp_path, mode='fixture')
    engine = Engine(config)
    task = await run(engine, ResearchInput(query='比较向量数据库'))
    assert task['status'] == 'input_required'
    assert task['usage']['search_calls'] == 0
    restored = Engine(config)
    result = restored.answer(task['id'], AnswerInput(answer='本地部署，已经使用PostgreSQL'))
    assert result['id'] == task['id']
    await restored.jobs[task['id']]
    current = restored.db.get('tasks', task['id'])
    assert current['status'] == 'completed'
    assert current['brief']['constraints']['已有技术栈'] == 'PostgreSQL'


async def test_revision_reuses_facts_preserves_versions_and_rejects_stale_base(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'))
    task = await run(engine, ResearchInput(query='本地部署，优先维护成本', allow_unknown=True))
    original = engine.report(task['report_id'])
    revised = engine.revise(task['report_id'], RevisionInput(base_version=1, query='已经使用PostgreSQL'))
    await engine.jobs[revised['id']]
    report = engine.report(task['report_id'])
    assert report['version'] == 2
    assert report['usage']['search_calls'] == report['usage']['read_calls'] == 0
    assert report['changes']['reused_snapshots'] == 3
    assert report['changes']['condition_changes']['已有技术栈']['after'] == 'PostgreSQL'
    assert report['changes']['judgments_changed']
    assert not report['changes']['added_facts']
    assert engine.report(task['report_id'], 1) == original
    with pytest.raises(Conflict):
        engine.revise(task['report_id'], RevisionInput(base_version=1, query='过期修改'))


async def test_force_refresh_and_cross_session_do_not_reuse(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'))
    task = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL'))
    revision = engine.revise(task['report_id'], RevisionInput(base_version=1, query='重新读取资料', force_refresh=True))
    await engine.jobs[revision['id']]
    assert engine.report(task['report_id'])['usage']['read_calls'] == 3
    other = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL'))
    assert other['session_id'] != task['session_id']
    assert other['usage']['read_calls'] == 3 and other['usage']['reused_snapshots'] == 0


async def test_expired_sensitive_evidence_is_fetched_again(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'))
    task = await run(engine, ResearchInput(query='研究报告需要正文', group='search_apis'))
    old = engine.report(task['report_id'])
    assert old
    for source in old['sources']:
        source['retrieved_at'] = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        engine.db.put('sources', source['id'], source)
    revision = engine.revise(task['report_id'], RevisionInput(base_version=1, query='重新检查费用'))
    await engine.jobs[revision['id']]
    assert engine.report(task['report_id'])['usage']['read_calls'] == 3


async def test_one_researcher_failure_preserves_others_and_targets_repairs(tmp_path):
    async def loader(product, url):
        if product == 'Qdrant':
            raise TimeoutError('upstream failed')
        return fixture_document(product, url)
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'), loader=loader)
    task = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL'))
    assert task['status'] == 'partial'
    report = engine.report(task['report_id'])
    assert len([c for c in report['claims'] if c['status'] == 'supported']) == 10
    assert {g['product'] for g in report['unresolved']} == {'Qdrant'}
    repairs = [t for t in task['trace'] if t['operation'] == 'research_round' and t['round'] > 0]
    assert repairs and len(repairs) <= 2
    assert all(set(r['targets']) == {'Qdrant'} for r in repairs)
    assert all(v <= 8 for v in task['research_steps'].values())


async def test_search_and_read_budgets_are_global_under_parallelism(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture', search_limit=1, read_limit=1))
    task = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL'))
    assert task['status'] == 'partial'
    assert task['usage']['search_calls'] <= 1 and task['usage']['read_calls'] <= 1
    assert engine.report(task['report_id'])['unresolved']


async def test_requested_version_without_evidence_is_not_asserted(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'))
    task = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL', requested_versions={'Qdrant': 'v99.99'}))
    assert task['status'] == 'partial'
    report = engine.report(task['report_id'])
    assert all(c['status'] != 'supported' for c in report['claims'] if c['product'] == 'Qdrant')


async def test_cancel_waiting_and_active_and_restart_records(tmp_path):
    config = Settings(runtime=tmp_path, mode='fixture')
    engine = Engine(config)
    waiting = await run(engine, ResearchInput(query='比较数据库'))
    assert (await engine.cancel(waiting['id']))['status'] == 'canceled'
    with pytest.raises(Conflict):
        engine.answer(waiting['id'], AnswerInput(answer='本地部署'))
    async def slow_loader(product, url):
        await asyncio.sleep(5)
        return fixture_document(product, url)
    engine.loader = slow_loader
    active = engine.submit(ResearchInput(query='本地部署，使用PostgreSQL'))
    await asyncio.sleep(0.05)
    assert (await engine.cancel(active['id']))['status'] == 'canceled'
    engine.db.put('tasks', 'crashed', {'id': 'crashed', 'status': 'working'})
    restored = Engine(config)
    assert restored.db.get('tasks', 'crashed')['status'] == 'interrupted'


async def test_timeout_retains_successful_researcher_evidence(tmp_path):
    async def slow_one(product, url):
        if product == 'Qdrant':
            await asyncio.sleep(5)
        return fixture_document(product, url)
    engine = Engine(Settings(runtime=tmp_path, mode='fixture', task_timeout=0.5), loader=slow_one)
    task = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL'))
    assert task['status'] == 'partial'
    assert len(task['snapshot_ids']) == 2 and len(task['claims']) == 10
    assert engine.report(task['report_id'])['unresolved']


class InvalidWriter(Model):
    async def respond(self, stage, messages, tools, context=None):
        result = await super().respond(stage, messages, tools, context)
        if stage == 'write':
            args = json.loads(result['tool_calls'][0]['function']['arguments'])
            args['judgments'][0]['claim_ids'] = ['forged-id']
            result['tool_calls'][0]['function']['arguments'] = json.dumps(args)
        return result


async def test_forged_writer_reference_does_not_publish_success(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'), model_factory=InvalidWriter)
    task = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL'))
    assert task['status'] == 'failed'
    assert engine.report(task['report_id']) is None


async def test_concurrent_sessions_usage_is_isolated(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'))
    a, b = await asyncio.gather(run(engine, ResearchInput(query='本地部署，使用PostgreSQL')),
                                run(engine, ResearchInput(query='本地部署，使用PostgreSQL')))
    assert a['status'] == b['status'] == 'completed'
    assert a['usage']['read_calls'] == b['usage']['read_calls'] == 3
    assert set(a['snapshot_ids']).isdisjoint(b['snapshot_ids'])


class TruncatedWriter(Model):
    async def respond(self, stage, messages, tools, context=None):
        if stage == 'write':
            raise ValueError('模型输出被Token上限截断')
        return await super().respond(stage, messages, tools, context)


async def test_truncation_does_not_publish_success(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'), model_factory=TruncatedWriter)
    task = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL'))
    assert task['status'] == 'failed' and not engine.report(task['report_id'])
    assert task['claims'] and task['snapshot_ids']


class SearchHappyModel(Model):
    async def respond(self, stage, messages, tools, context=None):
        if stage == 'research' and len(tools) > 1:
            observations = [json.loads(m['content']) for m in messages if m['role'] == 'tool']
            if any(r.get('evidence') for r in observations):
                await self.usage.model({})
                return call('search', {'query': context['product'] + ' extra docs'})
        return await super().respond(stage, messages, tools, context)


async def test_research_reserves_final_native_submission(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'), model_factory=SearchHappyModel)
    task = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL'))
    assert task['status'] == 'completed'
    assert all(v == 4 for v in task['research_steps'].values())
    assert len(engine.report(task['report_id'])['claims']) == 15


async def test_valid_citation_cannot_authorize_unsupported_recommendation(tmp_path):
    class UnsupportedWriter(Model):
        async def respond(self, stage, messages, tools, context=None):
            result = await super().respond(stage, messages, tools, context)
            if stage == 'write':
                args = json.loads(result['tool_calls'][0]['function']['arguments'])
                args['judgments'][0]['reasoning'] = '该产品免费而且性能最高，尽管引用未提供这些事实。'
                result['tool_calls'][0]['function']['arguments'] = json.dumps(args)
            return result
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'), model_factory=UnsupportedWriter)
    task = await run(engine, ResearchInput(query='本地部署，使用PostgreSQL'))
    assert task['status'] == 'failed' and engine.report(task['report_id']) is None
    assert task['claims'] and task['snapshot_ids']
