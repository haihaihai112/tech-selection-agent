import argparse
import asyncio
import json
from pathlib import Path

from selection_agent.evaluation import run_scenario, reuse_ablation, evidence_ablation
from selection_agent.models import now


async def evaluate(args):
    cases = json.loads(Path(args.dataset).read_text(encoding='utf-8'))
    run_id = now().replace(':', '').replace('+', '_')
    root = Path('runtime/evaluations') / run_id
    results = []
    for case in cases:
        result = await run_scenario(case, root)
        results.append(result)
        print(case['id'], 'PASS' if result['passed'] else 'FAIL', flush=True)
    report = {'generated_at': now(), 'mode': 'fixture', 'dataset': args.dataset,
              'total': len(results), 'passed': sum(r['passed'] for r in results), 'results': results,
              'limits': '确定性开发/留出机制测试；不能作为真实模型成功率或真实产品事实支持率。'}
    if args.ablation:
        report['reuse_ablation'] = await reuse_ablation(root / 'ablation-reuse')
        report['evidence_ablation'] = await evidence_ablation(root / 'ablation-evidence')
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if report['passed'] != report['total']:
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='evaluation/development_30.json')
    parser.add_argument('--output', default='reports/development.json')
    parser.add_argument('--ablation', action='store_true')
    asyncio.run(evaluate(parser.parse_args()))


if __name__ == '__main__':
    main()
