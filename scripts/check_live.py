"""Bounded real preflight. Never prints credentials or raw upstream exception messages."""
import argparse
import asyncio
import json
from pathlib import Path

from dotenv import dotenv_values

from selection_agent.config import Settings
from selection_agent.db import Store
from selection_agent.llm import Model
from selection_agent.models import StrictModel, now
from selection_agent.sources import Sources
from selection_agent.usage import Usage


class Probe(StrictModel):
    value: str


def live_settings(env_file=None, runtime=None):
    values = dotenv_values(env_file) if env_file else {}
    defaults = Settings()
    return Settings(mode='live', runtime=runtime or defaults.runtime,
        api_key=values.get('LLM_API_KEY') or defaults.api_key,
        tavily_key=values.get('TAVILY_API_KEY') or defaults.tavily_key,
        model=defaults.model,
        fallback_models=tuple(m.strip() for m in values.get('LLM_FALLBACK_MODELS', '').split(',') if m.strip()),
        base_url=values.get('LLM_BASE_URL') or defaults.base_url)


async def check(config):
    report = {'observed_at': now(), 'config': config.public(), 'model': {}, 'search': {}, 'page': {}}
    usage = Usage(config)
    model = Model(config, usage)
    try:
        result = await model.structured('preflight', '通过emit返回value为ok，不执行其他操作。', {}, Probe)
        report['model'] = {'ok': result.value == 'ok'}
    except Exception as exc:
        report['model'] = {'ok': False, 'error_type': type(exc).__name__}
    sources = Sources(config, Store(config.runtime / 'preflight.sqlite'), 'preflight', usage, [])
    result = await sources.search('pgvector', 'pgvector official PostgreSQL extension documentation')
    report['search'] = {'ok': result['ok'], 'result_count': len(result.get('results', []))}
    if result['ok'] and result['results']:
        page = await sources.read('pgvector', result['results'][0]['url'])
        report['page'] = {'ok': page['ok'], 'evidence_count': len(page.get('evidence', [])),
                          'source_url': result['results'][0]['url']}
    report['usage'] = usage.snapshot()
    report['ready_for_demo'] = all(report[k].get('ok') for k in ('model', 'search', 'page'))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-file')
    parser.add_argument('--model', help='Explicit model; legacy credential file does not override the current default')
    parser.add_argument('--output', default='reports/live-preflight.json')
    args = parser.parse_args()
    config = live_settings(args.env_file, Path('runtime/live-preflight').resolve())
    if args.model:
        config.model = args.model
    result = asyncio.run(check(config))
    output = Path(args.output)
    output.parent.mkdir(exist_ok=True, parents=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
