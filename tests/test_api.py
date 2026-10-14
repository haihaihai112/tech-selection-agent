import asyncio
import os
import socket
import subprocess
import sys
import time

import httpx

from selection_agent.api import create_app
from selection_agent.config import Settings


async def poll(client, task_id):
    for _ in range(150):
        result = (await client.get('/v1/tasks/' + task_id)).json()
        if result['status'] not in {'queued', 'working'}:
            return result
        await asyncio.sleep(0.03)
    raise TimeoutError('task did not finish')


async def test_api_full_revision_evidence_export_and_errors(tmp_path):
    app = create_app(Settings(runtime=tmp_path, mode='fixture'), with_ui=False)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post('/v1/research', json={'query': '比较向量数据库'})
        assert response.status_code == 202
        task_id = response.json()['id']
        task = await poll(client, task_id)
        assert task['status'] == 'input_required'
        answer = await client.post('/v1/tasks/' + task_id + '/answers', json={'answer': '本地部署，使用PostgreSQL'})
        assert answer.json()['id'] == task_id
        task = await poll(client, task_id)
        assert task['status'] == 'completed'
        report_id = task['report_id']
        report = (await client.get('/v1/reports/' + report_id)).json()
        eid = report['claims'][0]['evidence_ids'][0]
        evidence = (await client.get('/v1/evidence/' + eid)).json()
        assert evidence['evidence']['text'] in evidence['snapshot_text']
        revision = (await client.post('/v1/reports/' + report_id + '/revisions', json={'base_version': 1, 'query': '优先维护成本'})).json()
        assert (await poll(client, revision['id']))['status'] == 'completed'
        exported = await client.get('/v1/reports/' + report_id + '/export', params={'version': 1})
        assert exported.text == report['markdown'] and '第 1 版' in exported.text
        assert (await client.post('/v1/reports/' + report_id + '/revisions', json={'base_version': 1, 'query': 'stale'})).status_code == 409
        assert (await client.get('/v1/evidence/missing')).status_code == 404
        assert (await client.post('/v1/research', json={'query': ''})).status_code == 422
    await app.state.engine.close()


async def test_flowchart_endpoints_return_task_and_report_views(tmp_path):
    app = create_app(Settings(runtime=tmp_path, mode='fixture'), with_ui=False)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post('/v1/research', json={
            'query': '本地部署，使用PostgreSQL', 'allow_unknown': True,
        })
        task = await poll(client, response.json()['id'])
        task_graph = await client.get('/v1/tasks/' + task['id'] + '/flowchart')
        assert task_graph.status_code == 200
        assert task_graph.json()['status'] == task['status']
        assert task_graph.json()['graph']['nodes']
        assert task_graph.json()['mermaid'].startswith('flowchart TD')

        report_graph = await client.get('/v1/reports/' + task['report_id'] + '/flowchart', params={'version': 1})
        assert report_graph.status_code == 200
        assert report_graph.json()['version'] == 1
        assert report_graph.json()['graph']['status'] == task['status']
        assert (await client.get('/v1/tasks/missing/flowchart')).status_code == 404
        assert (await client.get('/v1/reports/missing/flowchart')).status_code == 404
        assert (await client.get('/v1/reports/' + task['report_id'] + '/flowchart', params={'version': 9})).status_code == 404
    await app.state.engine.close()


async def test_project_api_exposes_options_and_architecture_versions(tmp_path):
    app = create_app(Settings(runtime=tmp_path, mode='fixture'), with_ui=False)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
        created = await client.post('/v1/projects', json={'goal': '个人知识库', 'allow_unknown': True})
        assert created.status_code == 201
        project = created.json()
        layer = project['options']['layers'][0]
        started = await client.post(f"/v1/projects/{project['id']}/layers/{layer['id']}/research")
        assert started.status_code == 202
        task = await poll(client, started.json()['id'])
        assert task['status'] == 'completed'
        selections = {}
        for item in project['options']['layers']:
            if item['id'] == layer['id']:
                current_task = task
            else:
                response = await client.post(f"/v1/projects/{project['id']}/layers/{item['id']}/research")
                current_task = await poll(client, response.json()['id'])
            selections[item['id']] = {'product': item['candidates'][0]['product'],
                                      'report_id': current_task['report_id'], 'report_version': 1}
        confirmed = await client.post(f"/v1/projects/{project['id']}/confirm", json={'selections': selections})
        assert confirmed.status_code == 200
        assert confirmed.json()['version'] == 1
        diagram = await client.get(f"/v1/projects/{project['id']}/architecture")
        assert diagram.status_code == 200 and diagram.json()['svg'].startswith('<svg')
        old = await client.get(f"/v1/projects/{project['id']}/architecture", params={'version': 1})
        assert old.json() == diagram.json()
        assert (await client.get('/v1/projects/missing')).status_code == 404
    await app.state.engine.close()


def test_actual_http_process_survives_restart_with_reports(tmp_path):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    env = {**os.environ, 'SELECTION_RUNTIME': str(tmp_path), 'AGENT_MODE': 'fixture', 'PYTHONUTF8': '1'}
    base = f'http://127.0.0.1:{port}'
    log = (tmp_path / 'server.log').open('w', encoding='utf-8')
    process = None
    def start():
        child = subprocess.Popen([sys.executable, '-m', 'selection_agent.cli', '--fixture', '--no-ui', '--port', str(port)],
            env=env, stdout=log, stderr=subprocess.STDOUT)
        for _ in range(100):
            if child.poll() is not None:
                raise RuntimeError('server failed: ' + (tmp_path / 'server.log').read_text(encoding='utf-8'))
            try:
                if httpx.get(base + '/health', timeout=1).status_code == 200:
                    return child
            except httpx.HTTPError:
                pass
            time.sleep(0.1)
        child.terminate()
        raise TimeoutError('startup')
    try:
        process = start()
        with httpx.Client(base_url=base, timeout=10) as client:
            task = client.post('/v1/research', json={'query': '本地部署，使用PostgreSQL'}).json()
            for _ in range(100):
                value = client.get('/v1/tasks/' + task['id']).json()
                if value['status'] not in {'queued', 'working'}:
                    break
                time.sleep(0.1)
            assert value['status'] == 'completed'
            report = client.get('/v1/reports/' + task['report_id']).json()
        process.terminate()
        process.wait(timeout=10)
        process = start()
        restored = httpx.get(base + '/v1/reports/' + task['report_id']).json()
        assert restored == report and restored['claims']
    finally:
        if process and process.poll() is None:
            process.terminate()
            process.wait(timeout=10)
        log.close()
