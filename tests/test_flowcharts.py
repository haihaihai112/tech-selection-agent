import re

from selection_agent.flowcharts import build_flowchart, render_mermaid


def task(status='completed', trace=None):
    return {
        'id': 'task-1',
        'report_id': 'report-1',
        'status': status,
        'brief': {
            'products': ['pgvector', 'Qdrant', 'Milvus'],
            'dimensions': ['部署方式', '维护要求'],
        },
        'trace': trace or [],
        'claims': [],
    }


def node_ids(graph):
    return [node.id for node in graph.nodes]


def test_build_flowchart_has_stable_stages_and_parallel_products():
    first = build_flowchart(task())
    second = build_flowchart(task())

    assert first.model_dump() == second.model_dump()
    assert node_ids(first) == [
        'clarify', 'research', 'research-pgvector', 'research-Qdrant', 'research-Milvus',
        'verify', 'write',
    ]
    assert ('research', 'research-pgvector') in {(edge.source, edge.target) for edge in first.edges}
    assert ('research', 'research-Milvus') in {(edge.source, edge.target) for edge in first.edges}
    assert first.status == 'completed'


def test_flowchart_preserves_non_success_status_and_sanitizes_trace_errors():
    value = task(status='failed', trace=[
        {'operation': 'research_round', 'round': 1, 'targets': {'pgvector': ['部署方式']}},
        {'operation': 'task', 'status': 'error', 'error_type': 'ValueError',
         'error': 'secret=do-not-render'},
    ])

    graph = build_flowchart(value)
    assert graph.status == 'failed'
    assert graph.nodes[-1].status == 'failed'
    assert any(node.id == 'repair-1' for node in graph.nodes)
    assert 'secret=do-not-render' not in render_mermaid(graph)
    assert 'ValueError' not in render_mermaid(graph)


def test_mermaid_contains_only_safe_node_ids_and_status_classes():
    graph = build_flowchart(task(status='input_required'))
    mermaid = render_mermaid(graph)

    assert mermaid.startswith('flowchart TD')
    assert 'class clarify waiting' in mermaid
    assert re.search(r'\bclassDef (success|partial|failed|waiting|pending) ', mermaid)
    assert 'task-1' not in mermaid
