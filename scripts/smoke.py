"""Exercise clarification -> report -> revision -> evidence -> export over actual HTTP."""
import argparse
import json
import time
from pathlib import Path

import httpx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default='http://127.0.0.1:8050')
    parser.add_argument('--output', default='reports/http-smoke.json')
    args = parser.parse_args()
    with httpx.Client(base_url=args.base, timeout=30) as client:
        def post(url, payload):
            response = client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        def poll(task_id):
            deadline = time.monotonic() + 330
            while time.monotonic() < deadline:
                task = client.get('/v1/tasks/' + task_id).json()
                if task['status'] not in {'queued', 'working'}:
                    return task
                time.sleep(0.25)
            raise TimeoutError('task')
        health = client.get('/health').json()
        first = post('/v1/research', {'query': '为个人知识库比较三款向量数据库，优先维护成本。'})
        waiting = poll(first['id'])
        assert waiting['status'] == 'input_required', waiting
        post('/v1/tasks/' + first['id'] + '/answers', {'answer': '本地部署，其他条件暂不确定。', 'allow_unknown': True})
        completed = poll(first['id'])
        assert completed['status'] in {'completed', 'partial'} and completed.get('report_version')
        old = client.get('/v1/reports/' + first['report_id'], params={'version': 1}).json()
        revision = post('/v1/reports/' + first['report_id'] + '/revisions',
                        {'base_version': 1, 'query': '我已经使用PostgreSQL', 'allow_unknown': True})
        revised = poll(revision['id'])
        assert revised['status'] in {'completed', 'partial'}
        new = client.get('/v1/reports/' + first['report_id']).json()
        assert new['version'] == 2
        assert client.get('/v1/reports/' + first['report_id'], params={'version': 1}).json() == old
        exported = client.get('/v1/reports/' + first['report_id'] + '/export', params={'version': 2})
        assert exported.text == new['markdown']
        evidence = []
        if new['claims']:
            eid = new['claims'][0]['evidence_ids'][0]
            item = client.get('/v1/evidence/' + eid).json()
            assert item['evidence']['text'] in item['snapshot_text']
            evidence.append(item)
        result = {'health': health, 'tasks': [waiting, completed, revised], 'reports': [old, new],
                  'evidence_sample': evidence, 'assertions_passed': True,
                  'note': 'HTTP闭环验证；模型模式以health为准，不将fixture当作真实模型能力。'}
        target = Path(args.output)
        target.parent.mkdir(exist_ok=True, parents=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Saved {target}; task={revised["id"]}; report={new["report_id"]}; version={new["version"]}')


if __name__ == '__main__':
    main()
