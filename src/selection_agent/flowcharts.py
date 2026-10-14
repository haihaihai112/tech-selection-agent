"""Deterministic flowchart projections for saved research tasks and reports."""

from collections import defaultdict
import re
from typing import Literal

from pydantic import Field

from .models import StrictModel


FlowStatus = Literal[
    'completed', 'partial', 'failed', 'input_required', 'queued', 'working',
    'canceled', 'interrupted', 'success', 'waiting', 'pending',
]


class FlowNode(StrictModel):
    id: str
    title: str
    kind: Literal['stage', 'product', 'repair']
    status: FlowStatus
    product: str | None = None
    evidence_ids: list[str] = Field(default_factory=list)


class FlowEdge(StrictModel):
    id: str
    source: str
    target: str
    label: str = ''


class FlowGraph(StrictModel):
    status: FlowStatus
    nodes: list[FlowNode]
    edges: list[FlowEdge]


_TERMINAL = {'completed', 'partial', 'failed', 'canceled', 'interrupted'}
_FAILED = {'failed', 'canceled', 'interrupted'}
_CHECKPOINT_ORDER = {'starting': 0, 'clarify': 1, 'research': 2, 'researched': 3,
                     'verified': 4, 'reported': 5}
_VALID_FLOW_STATUSES = {'completed', 'partial', 'failed', 'input_required', 'queued', 'working',
                        'canceled', 'interrupted', 'success', 'waiting', 'pending'}


def _safe_text(value, limit=80):
    value = re.sub(r'[\x00-\x1f\x7f]', ' ', str(value or ''))
    return ' '.join(value.split())[:limit]


def _node_id(prefix, value):
    safe = re.sub(r'[^A-Za-z0-9_-]+', '-', str(value)).strip('-') or 'item'
    return f'{prefix}-{safe}'


def _stage_status(task, stage):
    status = task.get('status', 'queued')
    checkpoint = task.get('checkpoint', '')
    if status == 'input_required' and stage == 'clarify':
        return 'waiting'
    if status in _FAILED and stage == 'write' and checkpoint in {'verified', 'reported', ''}:
        return 'failed'
    if status == 'partial' and stage == 'write':
        return 'partial'
    if status == 'completed':
        return 'success'
    if status in _FAILED:
        position = _CHECKPOINT_ORDER.get(checkpoint, 0)
        stage_position = {'clarify': 1, 'research': 2, 'verify': 4, 'write': 5}[stage]
        if position >= stage_position:
            return 'success'
        if position == stage_position - 1:
            return 'failed'
        return 'pending'
    if status == 'input_required':
        return 'pending'
    position = _CHECKPOINT_ORDER.get(checkpoint, 0)
    stage_position = {'clarify': 1, 'research': 2, 'verify': 4, 'write': 5}[stage]
    return 'success' if position >= stage_position else 'pending'


def build_flowchart(task: dict, report: dict | None = None) -> FlowGraph:
    """Build a stable graph from persisted task data without external calls."""
    status = task.get('status', 'queued')
    products = list((task.get('brief') or {}).get('products') or [])
    trace = task.get('trace') or []
    claims = (report or {}).get('claims') if report else task.get('claims')
    claims = claims or []
    evidence_by_product = defaultdict(list)
    for claim in claims:
        if claim.get('status') == 'supported':
            evidence_by_product[claim.get('product')].extend(claim.get('evidence_ids') or [])

    nodes = [
        FlowNode(id='clarify', title='条件澄清', kind='stage', status=_stage_status(task, 'clarify')),
        FlowNode(id='research', title='并行研究', kind='stage', status=_stage_status(task, 'research')),
    ]
    error_products = {entry.get('product') for entry in trace
                      if entry.get('operation') in {'researcher', 'read_page'} and entry.get('status') == 'error'}
    for product in products:
        product_status = _stage_status(task, 'research')
        if product in error_products:
            product_status = 'failed' if status in _FAILED else 'partial'
        nodes.append(FlowNode(id=_node_id('research', product), title=f'{_safe_text(product)} 研究', kind='product',
                              status=product_status, product=_safe_text(product),
                              evidence_ids=sorted(set(evidence_by_product.get(product, [])))))

    repair_rounds = sorted({int(entry.get('round', 0)) for entry in trace
                            if entry.get('operation') == 'research_round' and entry.get('round', 0) > 0})
    if repair_rounds:
        for round_number in repair_rounds:
            nodes.append(FlowNode(id=f'repair-{round_number}', title=f'定向补查第 {round_number} 轮', kind='repair',
                                  status='success' if status in {'completed', 'partial'} else 'failed'))

    nodes.extend([
        FlowNode(id='verify', title='证据核验', kind='stage', status=_stage_status(task, 'verify')),
        FlowNode(id='write', title='推荐与报告', kind='stage', status=_stage_status(task, 'write')),
    ])

    edges = [FlowEdge(id='e-clarify-research', source='clarify', target='research'),
             *[FlowEdge(id=f'e-research-{_node_id("product", product)}', source='research', target=_node_id('research', product))
               for product in products]]
    for product in products:
        edges.append(FlowEdge(id=f'e-{_node_id("product", product)}-verify', source=_node_id('research', product), target='verify'))
    if repair_rounds:
        edges.append(FlowEdge(id='e-verify-repair', source='verify', target=f'repair-{repair_rounds[0]}', label='存在缺口'))
        for before, after in zip(repair_rounds, repair_rounds[1:]):
            edges.append(FlowEdge(id=f'e-repair-{before}-{after}', source=f'repair-{before}', target=f'repair-{after}'))
        edges.append(FlowEdge(id=f'e-repair-{repair_rounds[-1]}-verify', source=f'repair-{repair_rounds[-1]}', target='verify', label='再次核验'))
    else:
        edges.append(FlowEdge(id='e-research-verify', source='research', target='verify'))
    edges.append(FlowEdge(id='e-verify-write', source='verify', target='write'))
    return FlowGraph(status=status if status in _VALID_FLOW_STATUSES else 'queued', nodes=nodes, edges=edges)


def _mermaid_label(value):
    return _safe_text(value, 100).replace('"', "'")


def render_mermaid(graph: FlowGraph) -> str:
    """Render a FlowGraph using fixed syntax and labels from trusted graph fields."""
    lines = ['flowchart TD']
    for node in graph.nodes:
        lines.append(f'    {node.id}["{_mermaid_label(node.title)}"]')
    for edge in graph.edges:
        label = f'|{_mermaid_label(edge.label)}|' if edge.label else ''
        lines.append(f'    {edge.source} -->{label} {edge.target}')
    lines.extend([
        '    classDef success fill:#dcfce7,stroke:#16a34a,color:#14532d',
        '    classDef partial fill:#fef3c7,stroke:#d97706,color:#78350f',
        '    classDef failed fill:#fee2e2,stroke:#dc2626,color:#7f1d1d',
        '    classDef waiting fill:#dbeafe,stroke:#2563eb,color:#1e3a8a',
        '    classDef pending fill:#f3f4f6,stroke:#6b7280,color:#374151',
    ])
    classes = {'completed': 'success', 'success': 'success', 'partial': 'partial',
               'failed': 'failed', 'canceled': 'failed', 'interrupted': 'failed',
               'input_required': 'waiting', 'waiting': 'waiting', 'queued': 'pending',
               'working': 'pending', 'pending': 'pending'}
    for node in graph.nodes:
        lines.append(f'    class {node.id} {classes.get(node.status, "pending")}')
    return '\n'.join(lines)
