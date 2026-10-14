import json
from types import SimpleNamespace

import httpx
import pytest
from openai import PermissionDeniedError

from selection_agent.config import Settings
from selection_agent.llm import Model, ModelUnavailable, bounded_context, tool, decode_tool_arguments
from selection_agent.usage import Usage


async def test_live_response_length_is_rejected_and_usage_kept(tmp_path, monkeypatch):
    class Client:
        def __init__(self, **kwargs):
            self.http = kwargs['http_client']
            self.chat = SimpleNamespace(completions=self)
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            await self.http.aclose()
        async def create(self, **kwargs):
            assert kwargs['tools'][0]['type'] == 'function'
            return SimpleNamespace(usage=SimpleNamespace(prompt_tokens=10, completion_tokens=4),
                                   choices=[SimpleNamespace(finish_reason='length')])
    monkeypatch.setattr('selection_agent.llm.AsyncOpenAI', Client)
    config = Settings(runtime=tmp_path, mode='live', api_key='test-only')
    usage = Usage(config)
    with pytest.raises(ValueError, match='截断'):
        await Model(config, usage).respond('probe', [], [tool('emit', '', {'type': 'object'})])
    assert usage.values['prompt_tokens'] == 10 and usage.values['completion_tokens'] == 4


async def test_quota_error_is_typed_without_secret_message(tmp_path, monkeypatch):
    class Client:
        def __init__(self, **kwargs):
            self.http = kwargs['http_client']
            self.chat = SimpleNamespace(completions=self)
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            await self.http.aclose()
        async def create(self, **kwargs):
            response = httpx.Response(403, request=httpx.Request('POST', 'https://example.com/'))
            raise PermissionDeniedError('secret-in-upstream', response=response,
                                         body={'code': 'AllocationQuota.FreeTierOnly'})
    monkeypatch.setattr('selection_agent.llm.AsyncOpenAI', Client)
    config = Settings(runtime=tmp_path, mode='live', api_key='test-only')
    with pytest.raises(ModelUnavailable) as error:
        await Model(config, Usage(config)).respond('probe', [], [])
    assert error.value.code == 'AllocationQuota.FreeTierOnly' and 'secret' not in str(error.value)


def test_context_compaction_preserves_tool_message_pairs():
    messages = []
    for i in range(4):
        messages.extend([{'role': 'assistant', 'tool_calls': [{'id': str(i)}]},
            {'role': 'tool', 'tool_call_id': str(i), 'content': json.dumps({'evidence': [{'id': str(i), 'text': 'x' * 1000}]})}])
    bounded = bounded_context(messages)
    assert [m.get('tool_call_id') for m in bounded if m['role'] == 'tool'] == ['0', '1', '2', '3']
    assert len(json.loads(bounded[1]['content'])['evidence'][0]['text']) == 240
    assert len(json.loads(bounded[-1]['content'])['evidence'][0]['text']) == 1000


@pytest.mark.parametrize('code,should_switch', [('AllocationQuota.FreeTierOnly', True),
    ('insufficient_quota', True), ('AccessDenied', False), ('rate_limit_exceeded', False)])
async def test_only_quota_exhaustion_switches_and_attributes_usage(tmp_path, monkeypatch, code, should_switch):
    calls = []
    class Client:
        def __init__(self, **kwargs):
            self.http = kwargs['http_client']
            self.chat = SimpleNamespace(completions=self)
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            await self.http.aclose()
        async def create(self, **kwargs):
            calls.append(kwargs)
            if kwargs['model'] == 'qwen-plus':
                response = httpx.Response(403, request=httpx.Request('POST', 'https://example.com/'))
                raise PermissionDeniedError('private-upstream-text', response=response, body={'code': code})
            assert kwargs['extra_body'] is None
            return SimpleNamespace(model='deepseek-v3.2', usage=SimpleNamespace(prompt_tokens=12, completion_tokens=3),
                choices=[SimpleNamespace(finish_reason='stop', message=SimpleNamespace(content='done', tool_calls=[]))])
    monkeypatch.setattr('selection_agent.llm.AsyncOpenAI', Client)
    config = Settings(runtime=tmp_path, mode='live', model='qwen-plus', fallback_models=('deepseek-v3.2',),
                      api_key='test-only', input_price=1, output_price=2)
    usage = Usage(config)
    model = Model(config, usage)
    messages = [{'role': 'user', 'content': 'test'}]
    offered = [tool('emit', '', {'type': 'object'})]
    if not should_switch:
        with pytest.raises(ModelUnavailable):
            await model.respond('probe', messages, offered)
        assert len(calls) == 1 and not usage.values['model_fallbacks']
        return
    assert (await model.respond('probe', messages, offered))['content'] == 'done'
    await model.respond('probe', messages, offered)
    assert [c['model'] for c in calls] == ['qwen-plus', 'deepseek-v3.2', 'deepseek-v3.2']
    assert calls[0]['messages'] == calls[1]['messages'] and calls[0]['tools'] == calls[1]['tools']
    snapshot = usage.snapshot()
    assert snapshot['models']['deepseek-v3.2'] == {'calls': 2, 'prompt_tokens': 24, 'completion_tokens': 6}
    assert snapshot['llm_cost_cny'] is None and len(snapshot['model_fallbacks']) == 1
    assert 'private-upstream-text' not in json.dumps(snapshot)


async def test_exhausted_models_are_bounded_and_not_retried(tmp_path, monkeypatch):
    calls = []
    class Client:
        def __init__(self, **kwargs):
            self.http = kwargs['http_client']
            self.chat = SimpleNamespace(completions=self)
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            await self.http.aclose()
        async def create(self, **kwargs):
            calls.append(kwargs['model'])
            response = httpx.Response(403, request=httpx.Request('POST', 'https://example.com/'))
            raise PermissionDeniedError('private', response=response, body={'code': 'AllocationQuota.FreeTierOnly'})
    monkeypatch.setattr('selection_agent.llm.AsyncOpenAI', Client)
    config = Settings(runtime=tmp_path, mode='live', api_key='test-only', model='primary', fallback_models=('backup',))
    usage = Usage(config)
    model = Model(config, usage)
    for instance in (model, model, Model(config, usage)):
        with pytest.raises(ModelUnavailable):
            await instance.respond('probe', [], [])
    assert calls == ['primary', 'backup']


@pytest.mark.parametrize('repairable', [True, False])
async def test_structured_format_repair_is_bounded_and_keeps_native_pair(tmp_path, repairable):
    from selection_agent.models import StrictModel
    from pydantic import ValidationError
    class Output(StrictModel):
        value: str
    class FormatModel(Model):
        seen = []
        async def respond(self, stage, messages, tools, context=None):
            self.seen.append(list(messages))
            args = {'value': 'valid'} if len(self.seen) == 2 and repairable else {'wrong': 'bad'}
            return {'role': 'assistant', 'content': '', 'tool_calls': [{'id': 'call-1', 'type': 'function',
                'function': {'name': 'emit', 'arguments': json.dumps(args)}}]}
    config = Settings(runtime=tmp_path)
    model = FormatModel(config, Usage(config))
    if repairable:
        assert (await model.structured('test', 'test', {}, Output)).value == 'valid'
    else:
        with pytest.raises(ValidationError):
            await model.structured('test', 'test', {}, Output)
    assert len(model.seen) == 2
    assert model.seen[1][-1]['tool_call_id'] == model.seen[1][-2]['tool_calls'][0]['id']


def test_gateway_string_envelope_preserves_schema_validation():
    from selection_agent.models import Findings
    from pydantic import ValidationError
    raw = json.dumps({'string': json.dumps({'claims': [], 'gaps': ['unknown']})})
    assert Findings.model_validate(decode_tool_arguments(raw)).gaps == ['unknown']
    with pytest.raises(ValidationError):
        Findings.model_validate(decode_tool_arguments(json.dumps({'string': json.dumps({'forged': True})})))
    with pytest.raises(ValidationError):
        Findings.model_validate(decode_tool_arguments(json.dumps({'string': '{}', 'extra': 'reject'})))
