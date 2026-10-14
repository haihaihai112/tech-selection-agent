"""Run actual Gradio callbacks over HTTP; not a browser visual inspection."""
import json
import time
from pathlib import Path

from gradio_client import Client


def main():
    client = Client('http://127.0.0.1:8050/ui/', verbose=False)
    history = []
    def poll(task_id):
        for _ in range(90):
            result = client.predict(task_id, api_name='/poll')
            if not result[1].startswith(('等待处理', '正在研究')):
                return result
            time.sleep(0.3)
        raise TimeoutError('Gradio task')
    initial = client.predict('比较三种向量数据库', 'vector_databases', False, api_name='/start')
    waiting = poll(initial[0])
    assert waiting[1].startswith('请补充条件')
    client.predict(initial[0], '本地部署，其他条件暂不确定', True, api_name='/answer')
    first = poll(initial[0])
    assert first[1].startswith('报告已生成') and '合成' in first[2]
    revised = client.predict(first[3], 1, '已使用PostgreSQL', False, True, api_name='/revise')
    second = poll(revised[0])
    assert second[4] == 2 and 'PostgreSQL' in second[2]
    evidence_id = second[5]['value'] if isinstance(second[5], dict) else second[5]
    evidence = client.predict(evidence_id, api_name='/evidence')
    assert evidence[0] and 'fixture' in evidence[1]
    exported = client.predict(first[3], 1, api_name='/export')
    assert Path(exported).read_text(encoding='utf-8') == first[2]
    restored = client.predict(first[0], api_name='/restore')
    assert restored[2] == first[2]
    pending = client.predict('比较数据库', 'vector_databases', False, api_name='/start')
    poll(pending[0])
    assert 'canceled' in client.predict(pending[0], api_name='/cancel')
    history.extend([waiting, first, second])
    Path('reports/ui-smoke.json').write_text(json.dumps({'mode': 'fixture', 'passed': True,
        'checks': ['clarification', 'resume', 'timer_poll', 'revision', 'evidence', 'old_version_export', 'restore', 'cancel'],
        'visual_inspection': False, 'outputs': history}, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Gradio callbacks passed; visual inspection not performed.')


if __name__ == '__main__':
    main()
