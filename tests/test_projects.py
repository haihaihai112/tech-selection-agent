import pytest
from pydantic import ValidationError

from selection_agent.config import Settings
from selection_agent.engine import Conflict, Engine
from selection_agent.models import ResearchInput, RevisionInput
from selection_agent.projects import ProjectInput, ProjectService, ConfirmationInput


async def researched(service, project, layer_id):
    task = service.research(project['id'], layer_id)
    await service.engine.jobs[task['id']]
    return service.engine.db.get('tasks', task['id'])


async def test_goal_to_comparison_selection_and_immutable_project_diagram(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'))
    service = ProjectService(engine)
    project = await service.create(ProjectInput(goal='个人知识库', allow_unknown=True))
    assert project['status'] == 'options_ready'
    assert project['mode'] == 'fixture'
    assert project['architecture_version'] == 0
    assert project['options']['layers']
    assert service.architecture(project['id']) is None
    first_layer = project['options']['layers'][0]
    task = await researched(service, project, first_layer['id'])
    assert task['status'] == 'completed', task.get('error')
    report = engine.report(task['report_id'])
    assert report['brief']['products'] == [c['product'] for c in first_layer['candidates']]
    assert all(c['status'] == 'supported' for c in report['claims'])

    selections = {}
    for layer in project['options']['layers']:
        t = task if layer['id'] == first_layer['id'] else await researched(service, project, layer['id'])
        selections[layer['id']] = {'product': layer['candidates'][0]['product'],
                                   'report_id': t['report_id'], 'report_version': 1}
    confirmed = service.confirm(project['id'], ConfirmationInput(selections=selections))
    assert confirmed['version'] == 1
    assert confirmed['graph']['kind'] == 'project'
    assert '条件澄清' not in confirmed['mermaid']
    assert '合成' in confirmed['notice']
    assert confirmed['svg'].startswith('<svg')
    assert confirmed['choices'][0]['evidence_ids']
    assert all(c['product'] in confirmed['mermaid'] for c in confirmed['choices'])
    changed = dict(selections)
    changed[first_layer['id']] = {**changed[first_layer['id']], 'product': first_layer['candidates'][1]['product']}
    second = service.confirm(project['id'], ConfirmationInput(base_version=1, selections=changed))
    assert second['version'] == 2 and second['choices'][0]['product'] != confirmed['choices'][0]['product']
    assert service.architecture(project['id'], 1) == confirmed
    with pytest.raises(Conflict):
        service.confirm(project['id'], ConfirmationInput(base_version=1, selections=changed))
    await engine.close()


async def test_confirmation_rejects_unresearched_wrong_product_and_foreign_reports(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'))
    service = ProjectService(engine)
    p = await service.create(ProjectInput(goal='项目', allow_unknown=True))
    with pytest.raises(ValueError):
        service.confirm(p['id'], ConfirmationInput(selections={}))
    selections = {}
    for layer in p['options']['layers']:
        t = await researched(service, p, layer['id'])
        selections[layer['id']] = {'product': layer['candidates'][0]['product'],
                                   'report_id': t['report_id'], 'report_version': 1}
    first = next(iter(selections))
    invalid = {**selections, first: {**selections[first], 'product': 'invented'}}
    with pytest.raises(ValueError):
        service.confirm(p['id'], ConfirmationInput(selections=invalid))
    other = await service.create(ProjectInput(goal='其他项目', allow_unknown=True))
    with pytest.raises(ValueError):
        service.confirm(other['id'], ConfirmationInput(selections=selections))
    invalid = {**selections, first: {**selections[first], 'report_version': 99}}
    with pytest.raises(ValueError):
        service.confirm(p['id'], ConfirmationInput(selections=invalid))
    assert service.architecture(p['id']) is None
    await engine.close()


def test_custom_catalog_is_required_and_bounds_candidates():
    with pytest.raises(ValidationError):
        ResearchInput(query='goal', group='custom')
    with pytest.raises(ValidationError):
        ResearchInput(query='goal', group='custom', custom_catalog={
            'title': '框架', 'products': ['A', 'B', 'C', 'D'], 'dimensions': ['部署'], 'questions': [],
        })


async def test_custom_catalog_report_revision_uses_same_scope(tmp_path):
    engine = Engine(Settings(runtime=tmp_path, mode='fixture'))
    task = engine.submit(ResearchInput(query='目标', group='custom', allow_unknown=True,
                                     custom_catalog={'title': 'Web 框架', 'products': ['FastAPI', 'Flask'],
                                                     'dimensions': ['部署方式', '维护要求'], 'questions': []}))
    await engine.jobs[task['id']]
    current = engine.db.get('tasks', task['id'])
    assert current['status'] == 'completed'
    revised = engine.revise(task['report_id'], RevisionInput(base_version=1, query='使用PostgreSQL', allow_unknown=True))
    await engine.jobs[revised['id']]
    report = engine.report(task['report_id'])
    assert report['version'] == 2
    assert report['brief']['products'] == ['FastAPI', 'Flask']
    assert report['usage']['read_calls'] == 0
    await engine.close()
