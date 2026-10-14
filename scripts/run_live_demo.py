"""A real bounded research + revision run. Uses explicit local credential file without copying it."""
import argparse
import asyncio
import json
from pathlib import Path

from check_live import live_settings
from selection_agent.engine import Engine
from selection_agent.models import ResearchInput, RevisionInput, now


async def wait(engine, task):
    previous = None
    while True:
        current = engine.db.get('tasks', task['id'])
        state = (current['status'], current.get('checkpoint'), len(current.get('trace', [])))
        if state != previous:
            print(json.dumps({'task_id': task['id'], 'status': state[0], 'stage': state[1],
                              'operations': state[2]}, ensure_ascii=False), flush=True)
            previous = state
        if current['status'] not in {'queued', 'working'}:
            return current
        await asyncio.sleep(1)


async def run(args):
    runtime = Path('runtime/live-demo') / now().replace(':', '').replace('+', '_')
    config = live_settings(args.env_file, runtime.resolve())
    if args.model:
        config.model = args.model
    if args.fallback_models:
        config.fallback_models = tuple(m.strip() for m in args.fallback_models.split(',') if m.strip())
    engine = Engine(config)
    first = engine.submit(ResearchInput(query='为个人知识库比较pgvector、Qdrant、Milvus。采用本地自托管部署，'
        '优先考虑维护成本。已有技术栈、预算和数据规模尚未明确，先保留条件式结论。不计算总费用，不声称性能实测结果。', allow_unknown=True))
    tasks = [await wait(engine, first)]
    if tasks[0].get('report_version'):
        revised = engine.revise(first['report_id'], RevisionInput(base_version=1,
            query='补充条件：我已经使用PostgreSQL。重新判断适配性，复用仍有效的原文，不需要为展示变化而改变推荐。', allow_unknown=True))
        tasks.append(await wait(engine, revised))
    reports = [engine.report(t['report_id'], t['report_version']) for t in tasks if t.get('report_version')]
    evidence_ids = {eid for r in reports for c in r['claims'] for eid in c['evidence_ids']}
    sources = {s['id']: s for r in reports for s in r['sources']}
    result = {'generated_at': now(), 'mode': 'live', 'config': engine.config.public(), 'tasks': tasks,
              'reports': reports, 'evidence': [engine.db.get('evidence', e) for e in sorted(evidence_ids)],
              'source_snapshots': [{**s, 'text': (runtime / 'snapshots' / s['content_path']).read_text(encoding='utf-8')
                  if s['content_path'] else s['summary']} for s in sources.values()],
              'note': '真实运行原始结果；completed仅表示结构化流程完成，事实支持需独立审计。'}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    for r in reports:
        output.with_name(f'{output.stem}-v{r["version"]}.md').write_text(r['markdown'], encoding='utf-8')
    await engine.close()
    print(json.dumps({'saved': str(output), 'statuses': [t['status'] for t in tasks], 'reports': len(reports)}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-file')
    parser.add_argument('--model', help='Explicit Qwen-compatible model override, recorded in the report')
    parser.add_argument('--fallback-models', help='Trusted comma-separated alternatives on explicit quota exhaustion')
    parser.add_argument('--output', default='reports/live-demo.json')
    asyncio.run(run(parser.parse_args()))


if __name__ == '__main__':
    main()
