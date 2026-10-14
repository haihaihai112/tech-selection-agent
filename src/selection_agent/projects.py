"""Project-level candidate selection and immutable architecture projections."""

from html import escape
import re
import uuid

from .catalog import CATALOG, validate_catalog
from .engine import Conflict, Engine
from .models import ConfirmationInput, ProjectInput, ResearchInput


def _slug(value):
    value = re.sub(r'[^A-Za-z0-9\u4e00-\u9fff]+', '-', value).strip('-')
    return value.lower()[:40] or 'layer'


class ProjectService:
    def __init__(self, engine: Engine):
        self.engine = engine

    def _options(self, request: ProjectInput):
        if request.custom_catalog:
            catalog = validate_catalog(request.custom_catalog)
            return [{'id': 'core', 'title': catalog['title'], 'group': 'custom', 'dimensions': catalog['dimensions'],
                     'candidates': [{'product': product, 'rationale': '候选待公开资料核验；当前仅是目标适配假设。'}
                                    for product in catalog['products']], 'catalog': catalog}]
        layers = []
        titles = {'vector_databases': '数据与检索存储', 'search_apis': '外部搜索', 'rag_platforms': '知识库应用'}
        for group, catalog in CATALOG.items():
            layers.append({'id': group, 'title': titles[group], 'group': group,
                           'dimensions': catalog['dimensions'],
                           'candidates': [{'product': product,
                                          'rationale': '根据目标提出的候选，需通过公开原文研究确认。'}
                                         for product in catalog['products']],
                           'catalog': catalog})
        return layers

    async def create(self, request: ProjectInput):
        layers = self._options(request)
        project_id = uuid.uuid4().hex
        session_id = uuid.uuid4().hex
        project = {'id': project_id, 'session_id': session_id, 'goal': request.goal,
                   'constraints': request.constraints, 'allow_unknown': request.allow_unknown,
                   'mode': self.engine.config.mode, 'status': 'options_ready',
                   'options': {'layers': layers}, 'architecture_version': 0,
                   'created_at': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()}
        self.engine.db.put('projects', project_id, project)
        self.engine.db.put('sessions', session_id, {'id': session_id, 'created_at': project['created_at'],
                                                    'project_id': project_id})
        return project

    def _get(self, project_id):
        project = self.engine.db.get('projects', project_id)
        if not project:
            raise KeyError('project not found')
        return project

    def _layer(self, project, layer_id):
        layer = next((layer for layer in project['options']['layers'] if layer['id'] == layer_id), None)
        if not layer:
            raise KeyError('layer not found')
        return layer

    def research(self, project_id, layer_id):
        project = self._get(project_id)
        layer = self._layer(project, layer_id)
        request = ResearchInput(query=project['goal'], group=layer['group'], session_id=project['session_id'],
                                allow_unknown=project['allow_unknown'], custom_catalog=layer.get('catalog')
                                if layer['group'] == 'custom' else None)
        task = self.engine.submit(request)
        project['options']['layers'] = [dict(item, task_id=task['id']) if item['id'] == layer_id else item
                                        for item in project['options']['layers']]
        project['status'] = 'researching'
        self.engine.db.put('projects', project_id, project)
        return task

    def _graph(self, project, choices, requested_edges=None):
        nodes = [{'id': 'goal', 'title': '项目目标与约束', 'kind': 'goal'}]
        for index, choice in enumerate(choices):
            nodes.append({'id': f'choice-{index}', 'title': choice['product'], 'kind': 'selected_component',
                          'layer_id': choice['layer_id'], 'evidence_ids': choice['evidence_ids']})
        edges = []
        if requested_edges:
            ids = {'goal': 'goal', **{choice['layer_id']: f'choice-{i}' for i, choice in enumerate(choices)}}
            for edge in requested_edges:
                source, target = ids.get(edge.get('source')), ids.get(edge.get('target'))
                if not source or not target or source == target:
                    raise ValueError('架构连线必须引用已确认的技术层，且不能连接自身')
                edges.append({'source': source, 'target': target, 'label': str(edge.get('label', '设计关系'))[:80]})
        else:
            edges = ([{'source': 'goal', 'target': 'choice-0', 'label': '约束'}] if choices else [])
            edges.extend({'source': f'choice-{i}', 'target': f'choice-{i + 1}', 'label': '数据或调用流'}
                          for i in range(len(choices) - 1))
        return {'kind': 'project', 'nodes': nodes, 'edges': edges}

    @staticmethod
    def _mermaid(graph, notice):
        lines = ['flowchart LR']
        for node in graph['nodes']:
            node_id = node['id']
            title = str(node['title']).replace('"', "'")[:100]
            lines.append(f'    {node_id}["{title}"]')
        for edge in graph['edges']:
            label = f'|{str(edge["label"]).replace("|", " ")[:60]}|' if edge.get('label') else ''
            lines.append(f'    {edge["source"]} -->{label} {edge["target"]}')
        lines.append('    classDef component fill:#dbeafe,stroke:#2563eb,color:#1e3a8a')
        lines.append('    class goal component')
        for node in graph['nodes']:
            if node['id'] != 'goal':
                lines.append(f'    class {node["id"]} component')
        lines.append(f'    %% {notice}')
        return '\n'.join(lines)

    @staticmethod
    def _svg(graph, notice):
        width, height, gap = 880, 150, 260
        pieces = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
                  '<style>rect{fill:#dbeafe;stroke:#2563eb}text{font:14px sans-serif;fill:#1e3a8a}</style>']
        for index, node in enumerate(graph['nodes']):
            x = 30 + index * gap
            pieces.append(f'<rect x="{x}" y="45" width="190" height="50" rx="8"/>')
            pieces.append(f'<text x="{x + 95}" y="75" text-anchor="middle">{escape(str(node["title"])[:40])}</text>')
            if index:
                pieces.append(f'<path d="M {x - 40} 70 L {x} 70" stroke="#64748b" marker-end="url(#arrow)"/>')
        pieces.insert(1, '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#64748b"/></marker></defs>')
        pieces.append(f'<text x="30" y="130">{escape(notice)}</text></svg>')
        return ''.join(pieces)

    def confirm(self, project_id, request: ConfirmationInput):
        project = self._get(project_id)
        current = project['architecture_version']
        if current and request.base_version != current:
            raise Conflict('项目架构基础版本已变化，请读取最新版本。')
        layers = project['options']['layers']
        if set(request.selections) != {layer['id'] for layer in layers}:
            raise ValueError('必须为每个技术层确认一个候选')
        choices = []
        for layer in layers:
            selected = request.selections[layer['id']]
            if selected.product not in {candidate['product'] for candidate in layer['candidates']}:
                raise ValueError('选择的产品不在该技术层候选中')
            report = self.engine.report(selected.report_id, selected.report_version)
            if not report or report['session_id'] != project['session_id'] or report['version'] != selected.report_version:
                raise ValueError('报告不存在、版本不匹配或不属于该项目')
            if selected.product not in report['brief']['products']:
                raise ValueError('报告不覆盖该候选产品')
            supported = [claim for claim in report['claims']
                         if claim['product'] == selected.product and claim['status'] == 'supported']
            if not supported:
                raise ValueError('没有可用于确认的已核验事实')
            choices.append({'layer_id': layer['id'], 'layer_title': layer['title'], 'product': selected.product,
                            'report_id': selected.report_id, 'report_version': selected.report_version,
                            'evidence_ids': sorted({eid for claim in supported for eid in claim['evidence_ids']})})
        graph = self._graph(project, choices, request.edges)
        notice = '合成测试资料：候选与证据用于演示，不构成真实产品建议。' if self.engine.config.mode == 'fixture' else '架构关系是用户确认的设计关系，未证明产品兼容性。'
        version = current + 1
        result = {'project_id': project_id, 'version': version, 'goal': project['goal'], 'choices': choices,
                  'graph': graph, 'mermaid': self._mermaid(graph, notice), 'svg': self._svg(graph, notice),
                  'notice': notice, 'base_version': current or None}
        self.engine.db.put('project_architectures', f'{project_id}:{version}', result)
        project['architecture_version'] = version
        project['status'] = 'architecture_ready'
        self.engine.db.put('projects', project_id, project)
        return result

    def architecture(self, project_id, version=None):
        project = self._get(project_id)
        version = version or project['architecture_version']
        if not version:
            return None
        return self.engine.db.get('project_architectures', f'{project_id}:{version}')
