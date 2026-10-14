from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .catalog import validate_catalog


def now():
    return datetime.now(timezone.utc).isoformat()


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class ResearchInput(StrictModel):
    query: str = Field(min_length=1, max_length=6000)
    group: Literal['vector_databases', 'search_apis', 'rag_platforms', 'custom'] = 'vector_databases'
    custom_catalog: dict | None = None
    session_id: str | None = None
    allow_unknown: bool = False
    force_refresh: bool = False
    requested_versions: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode='after')
    def validate_custom(self):
        if self.group == 'custom':
            validate_catalog(self.custom_catalog)
        return self


class AnswerInput(StrictModel):
    answer: str = Field(min_length=1, max_length=6000)
    allow_unknown: bool = False


class RevisionInput(StrictModel):
    base_version: int = Field(ge=1)
    query: str = Field(min_length=1, max_length=6000)
    allow_unknown: bool = False
    force_refresh: bool = False
    requested_versions: dict[str, str] = Field(default_factory=dict)


class ResearchBrief(StrictModel):
    group: str
    products: list[str] = Field(min_length=1, max_length=3)
    dimensions: list[str] = Field(min_length=1, max_length=8)
    constraints: dict[str, str] = Field(default_factory=dict)
    preferences: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    requested_versions: dict[str, str] = Field(default_factory=dict)


class SourceSnapshot(StrictModel):
    id: str
    session_id: str
    product: str
    url: str
    title: str
    source_type: Literal['official', 'third_party', 'fixture']
    retrieved_at: str = Field(default_factory=now)
    published_at: str | None = None
    document_version: str | None = None
    requested_version: str | None = None
    content_hash: str = ''
    content_path: str = ''
    status: Literal['fulltext', 'summary_only'] = 'fulltext'
    summary: str = ''
    original_url: str | None = None
    duplicate_of: str | None = None
    sensitive: bool = False
    model_mode: str


class EvidenceSpan(StrictModel):
    id: str
    snapshot_id: str
    session_id: str
    product: str
    paragraph: int
    text: str
    status: str = 'fulltext'


class ClaimDraft(StrictModel):
    product: str
    dimension: str
    attribute: str
    value: str
    text: str
    evidence_ids: list[str] = Field(min_length=1, max_length=4)
    scope: dict[str, str] = Field(default_factory=dict)


class Findings(StrictModel):
    claims: list[ClaimDraft] = Field(default_factory=list, max_length=16)
    gaps: list[str] = Field(default_factory=list)


class VerifiedClaim(ClaimDraft):
    id: str
    status: Literal['supported', 'contradicted', 'insufficient'] = 'insufficient'
    reason: str = ''
    conflicting_ids: list[str] = Field(default_factory=list)


class Verdict(StrictModel):
    claim_id: str
    status: Literal['supported', 'contradicted', 'insufficient']
    reason: str
    conflicting_ids: list[str] = Field(default_factory=list)


class Verdicts(StrictModel):
    verdicts: list[Verdict]


class Judgment(StrictModel):
    product: str
    reasoning: str
    condition_keys: list[str] = Field(default_factory=list)
    claim_ids: list[str] = Field(min_length=1)


class WriterDraft(StrictModel):
    judgments: list[Judgment] = Field(default_factory=list, max_length=6)


class ReportVersion(StrictModel):
    report_id: str
    version: int
    task_id: str
    session_id: str
    model_mode: str
    created_at: str = Field(default_factory=now)
    brief: ResearchBrief
    claims: list[VerifiedClaim]
    judgments: list[Judgment]
    unresolved: list[dict]
    sources: list[SourceSnapshot]
    previous_version: int | None = None
    changes: dict = Field(default_factory=dict)
    usage: dict
    markdown: str


class ProjectInput(StrictModel):
    goal: str = Field(min_length=1, max_length=6000)
    constraints: dict[str, str] = Field(default_factory=dict)
    allow_unknown: bool = False
    custom_catalog: dict | None = None


class ConfirmationChoice(StrictModel):
    product: str = Field(min_length=1)
    report_id: str = Field(min_length=1)
    report_version: int = Field(ge=1)


class ConfirmationInput(StrictModel):
    base_version: int | None = Field(default=None, ge=1)
    selections: dict[str, ConfirmationChoice]
    edges: list[dict[str, str]] = Field(default_factory=list)
