from dataclasses import dataclass, field
from pathlib import Path
import os

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / '.env')


def optional_price(key):
    raw = os.getenv(key, '')
    return float(raw) if raw else None


@dataclass
class Settings:
    runtime: Path = field(default_factory=lambda: Path(os.getenv('SELECTION_RUNTIME', str(ROOT / 'runtime'))))
    mode: str = field(default_factory=lambda: os.getenv('AGENT_MODE', 'fixture'))
    model: str = field(default_factory=lambda: os.getenv('LLM_MODEL', 'deepseek-v3.2'))
    fallback_models: tuple[str, ...] = field(default_factory=lambda: tuple(
        name.strip() for name in os.getenv('LLM_FALLBACK_MODELS', '').split(',') if name.strip()))
    base_url: str = field(default_factory=lambda: os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1'))
    api_key: str = field(default_factory=lambda: os.getenv('LLM_API_KEY') or os.getenv('DASHSCOPE_API_KEY', ''), repr=False)
    tavily_key: str = field(default_factory=lambda: os.getenv('TAVILY_API_KEY', ''), repr=False)
    search_limit: int = field(default_factory=lambda: int(os.getenv('SEARCH_LIMIT', '18')))
    read_limit: int = field(default_factory=lambda: int(os.getenv('READ_LIMIT', '24')))
    research_steps: int = field(default_factory=lambda: int(os.getenv('RESEARCH_STEPS', '8')))
    repair_rounds: int = field(default_factory=lambda: int(os.getenv('REPAIR_ROUNDS', '2')))
    task_timeout: float = field(default_factory=lambda: float(os.getenv('TASK_TIMEOUT', '300')))
    input_price: float | None = field(default_factory=lambda: optional_price('LLM_INPUT_CNY_PER_MILLION'))
    output_price: float | None = field(default_factory=lambda: optional_price('LLM_OUTPUT_CNY_PER_MILLION'))
    search_price: float | None = field(default_factory=lambda: optional_price('SEARCH_USD_PER_REQUEST'))

    def __post_init__(self):
        if self.mode not in {'fixture', 'live'}:
            raise ValueError('AGENT_MODE must be fixture or live')
        if min(self.search_limit, self.read_limit, self.research_steps, self.task_timeout) <= 0:
            raise ValueError('budgets must be positive')
        if not 0 <= self.repair_rounds <= 2:
            raise ValueError('repair rounds must be between 0 and 2')
        self.runtime.mkdir(parents=True, exist_ok=True)

    def public(self):
        return {'mode': self.mode, 'model': self.model, 'fallback_models': list(self.fallback_models),
                'llm_configured': bool(self.api_key),
                'search_configured': bool(self.tavily_key), 'search_limit': self.search_limit,
                'read_limit': self.read_limit, 'research_steps': self.research_steps,
                'repair_rounds': self.repair_rounds, 'task_timeout': self.task_timeout}
