"""Adapted from enterprise-intelligence-agent's per-workflow locked usage accounting."""
import asyncio
import copy


class BudgetExceeded(Exception):
    pass


class Usage:
    def __init__(self, config, initial=None):
        self.config = config
        self.lock = asyncio.Lock()
        self.values = {'search_calls': 0, 'read_calls': 0, 'model_calls': 0,
                       'prompt_tokens': 0, 'completion_tokens': 0, 'reused_snapshots': 0,
                       'failed_calls': 0, 'model_attempts': [], 'model_fallbacks': [],
                       'models': {}, 'exhausted_models': [], **copy.deepcopy(initial or {})}

    async def reserve(self, kind):
        key = kind + '_calls'
        async with self.lock:
            limit = self.config.search_limit if kind == 'search' else self.config.read_limit
            if self.values[key] >= limit:
                raise BudgetExceeded(f'{kind}预算已耗尽')
            self.values[key] += 1

    async def model(self, value, requested_model=None, actual_model=None, stage=None, elapsed=None):
        async with self.lock:
            self.values['model_calls'] += 1
            for key in ('prompt_tokens', 'completion_tokens'):
                self.values[key] += int(value.get(key, 0) or 0)
            if requested_model:
                name = actual_model or requested_model
                counts = self.values['models'].setdefault(name, {'calls': 0, 'prompt_tokens': 0, 'completion_tokens': 0})
                counts['calls'] += 1
                for key in ('prompt_tokens', 'completion_tokens'):
                    counts[key] += int(value.get(key, 0) or 0)
                self.values['model_attempts'].append({'requested_model': requested_model, 'actual_model': name,
                    'stage': stage, 'status': 'ok', 'elapsed_seconds': elapsed, **value})

    async def model_failure(self, model, stage, code, status, elapsed):
        async with self.lock:
            self.values['failed_calls'] += 1
            self.values['model_attempts'].append({'requested_model': model, 'stage': stage, 'status': 'error',
                'provider_code': code, 'http_status': status, 'elapsed_seconds': elapsed})

    async def fallback(self, previous, next_model, code):
        async with self.lock:
            self.values['model_fallbacks'].append({'from': previous, 'to': next_model, 'provider_code': code})

    def snapshot(self):
        data = copy.deepcopy(self.values)
        data['token_measurement'] = 'provider_reported' if self.config.mode == 'live' else 'not_applicable_fixture'
        data['llm_cost_cny'] = None
        data['search_cost_usd'] = None
        if self.config.mode == 'live':
            if (self.config.input_price is not None and self.config.output_price is not None
                    and set(data['models']) == {self.config.model}):
                data['llm_cost_cny'] = (data['prompt_tokens'] * self.config.input_price +
                                        data['completion_tokens'] * self.config.output_price) / 1_000_000
            if self.config.search_price is not None:
                data['search_cost_usd'] = data['search_calls'] * self.config.search_price
        data['cost_note'] = '单价只适用于配置的主模型；切换或供应商返回不同模型名时费用未知。失败调用是否计费以账单为准；币种不混加。'
        return data
