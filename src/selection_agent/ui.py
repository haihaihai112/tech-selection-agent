import json

import gradio as gr

from .catalog import CATALOG
from .engine import Conflict
from .flowcharts import build_flowchart, render_mermaid
from .models import AnswerInput, ResearchInput, RevisionInput
from .models import ConfirmationInput, ProjectInput
from .projects import ProjectService


def build_ui(engine):
    projects = ProjectService(engine)
    def display(task):
        brief = task.get('brief') or {}
        questions = '\n'.join('- ' + q for q in brief.get('questions', []))
        labels = {'queued': '等待处理', 'working': '正在研究', 'input_required': '请补充条件',
                  'completed': '报告已生成', 'partial': '部分完成，仍有待确认项',
                  'failed': '处理失败', 'canceled': '已取消', 'interrupted': '已中断'}
        status = labels.get(task['status'], task['status']) + '\n' + questions
        if task.get('error'):
            status += '\n' + task['error']
        report = engine.report(task['report_id'], task.get('report_version')) if task.get('report_version') else None
        claims = report['claims'] if report else task.get('claims', [])
        ids = list(dict.fromkeys(e for c in claims for e in c['evidence_ids'] if engine.db.get('evidence', e)))
        changes = report['changes'] if report else {}
        graph = build_flowchart(task, report)
        change_lines = [f"复用 {changes.get('reused_snapshots', 0)} 份原文快照。"]
        for key, value in changes.get('condition_changes', {}).items():
            change_lines.append(f"{key}：{value['before']} → {value['after']}")
        if report and report['previous_version']:
            change_lines.append('条件式判断已重新生成。' if changes.get('judgments_changed') else '判断未发生变化。')
        return (task['id'], status, report['markdown'] if report else '报告将在研究完成后显示。',
                report['report_id'] if report else '', report['version'] if report else 1,
                gr.update(choices=ids, value=ids[0] if ids else None), '\n'.join(change_lines),
                changes.get('markdown_diff', ''), {'trace': task.get('trace', []), 'usage': task.get('usage', {})},
                render_mermaid(graph), graph.model_dump())

    async def start(query, group, allow_unknown):
        task = engine.submit(ResearchInput(query=query, group=group, allow_unknown=allow_unknown))
        return display(task)

    async def answer(task_id, text, allow_unknown):
        try:
            task = engine.answer(task_id, AnswerInput(answer=text, allow_unknown=allow_unknown))
        except (Conflict, KeyError) as exc:
            raise gr.Error(str(exc)) from exc
        return display(task)

    async def revise(report_id, version, query, force, allow_unknown):
        try:
            task = engine.revise(report_id, RevisionInput(base_version=int(version), query=query,
                                force_refresh=force, allow_unknown=allow_unknown))
        except (Conflict, KeyError) as exc:
            raise gr.Error(str(exc)) from exc
        return display(task)

    def poll(task_id):
        task = engine.db.get('tasks', task_id) if task_id else None
        if not task or task['status'] not in {'queued', 'working', 'input_required'}:
            # Display the final state once, then stop the timer to preserve selected versions.
            return (*display(task), gr.Timer(active=False)) if task else (*[gr.skip() for _ in range(11)], gr.Timer(active=False))
        return (*display(task), gr.Timer(active=task['status'] in {'queued', 'working'}))

    async def cancel(task_id):
        if not task_id:
            return '当前没有任务。'
        task = await engine.cancel(task_id)
        return '任务状态：' + task['status']

    def restore(task_id):
        task = engine.db.get('tasks', task_id)
        if not task:
            raise gr.Error('任务不存在')
        return display(task)

    def evidence(evidence_id):
        item = engine.db.get('evidence', evidence_id or '')
        if not item:
            return '', ''
        source = engine.db.get('sources', item['snapshot_id'])
        metadata = {k: source[k] for k in ('title', 'url', 'source_type', 'retrieved_at', 'published_at',
                    'document_version', 'status', 'content_hash', 'original_url', 'duplicate_of', 'model_mode')}
        return item['text'], json.dumps(metadata, ensure_ascii=False, indent=2)

    def export(report_id, version):
        report = engine.report(report_id, int(version))
        if not report:
            raise gr.Error('指定版本不存在')
        path = engine.config.runtime / 'exports' / f'{report_id}-v{int(version)}.md'
        path.parent.mkdir(exist_ok=True)
        path.write_text(report['markdown'], encoding='utf-8')
        return str(path)

    async def create_project(goal, allow_unknown):
        project = await projects.create(ProjectInput(goal=goal, allow_unknown=allow_unknown))
        layers = project['options']['layers']
        return project['id'], project['options'], gr.update(choices=[layer['id'] for layer in layers],
                                                            value=layers[0]['id'] if layers else None), ''

    def research_project_layer(project_id, layer_id):
        try:
            task = projects.research(project_id, layer_id)
            return task['id'], '层研究已提交，等待轮询。'
        except (Conflict, KeyError, ValueError) as exc:
            raise gr.Error(str(exc)) from exc

    def poll_project_task(task_id):
        task = engine.db.get('tasks', task_id) if task_id else None
        if not task:
            return '', '没有层研究任务。'
        return task.get('report_id', ''), task.get('status', '') + (('：' + task['error']) if task.get('error') else '')

    def confirm_project(project_id, base_version, selections):
        try:
            parsed = json.loads(selections)
            request = ConfirmationInput(base_version=int(base_version) if base_version else None, selections=parsed)
            result = projects.confirm(project_id, request)
            return result['version'], result['mermaid'], result['svg'], json.dumps(result['choices'], ensure_ascii=False, indent=2)
        except (Conflict, KeyError, ValueError, json.JSONDecodeError) as exc:
            raise gr.Error(str(exc)) from exc

    with gr.Blocks(title='技术选型研究 Agent', theme=gr.themes.Soft(primary_hue='indigo'),
                   css='.gradio-container {max-width:1400px !important;}') as ui:
        timer = gr.Timer(1, active=False)
        gr.Markdown('# 技术选型研究 Agent\n先明确条件，再核对依据；条件改变后，可以继续修订。')
        gr.Markdown('**确定性测试替身：产品资料均为合成内容，不构成真实产品建议。**' if engine.config.mode == 'fixture' else
                    '**真实研究模式**：使用当前配置的模型与Tavily；未确定的信息会保留为缺口。')
        with gr.Row():
            with gr.Column(scale=4):
                group = gr.Dropdown([(v['title'], k) for k, v in CATALOG.items()], value='vector_databases', label='产品组')
                query = gr.Textbox(label='研究目标与条件', lines=4,
                    value='为个人知识库比较三款向量数据库，优先考虑维护成本。')
                allow = gr.Checkbox(label='允许缺少部分条件，先生成条件式分析', value=False)
                start_button = gr.Button('开始研究', variant='primary')
                task_id = gr.Textbox(label='任务编号（可用于恢复）')
                with gr.Row():
                    restore_button = gr.Button('恢复任务')
                    cancel_button = gr.Button('取消任务')
                status = gr.Textbox(label='研究进度与追问', lines=5, interactive=False)
                answer_text = gr.Textbox(label='补充条件', placeholder='本地部署；已有技术栈暂不确定。')
                answer_button = gr.Button('提交补充条件')
                gr.Examples([['vector_databases', '本地部署知识库，已经使用PostgreSQL，比较维护要求。'],
                    ['search_apis', '为研究报告选择搜索API，需要正文，预算与用量暂不确定。'],
                    ['rag_platforms', '本地部署知识库，主要处理PDF文档，比较三种平台。']], inputs=[group, query])
            with gr.Column(scale=7):
                with gr.Tab('比较报告'):
                    report_text = gr.Markdown('报告将在研究完成后显示。')
                    report_id = gr.Textbox(label='报告编号', interactive=False)
                    version = gr.Number(label='报告版本（导出时可选择旧版）', value=1, precision=0, minimum=1)
                    export_button = gr.Button('导出指定版本 Markdown')
                    export_file = gr.File(label='报告文件')
                with gr.Tab('证据原文'):
                    evidence_id = gr.Dropdown(choices=[], label='选择证据编号')
                    evidence_button = gr.Button('查看原文')
                    evidence_text = gr.Textbox(label='原文片段', lines=12, interactive=False)
                    evidence_meta = gr.Textbox(label='来源、版本与时间', lines=9, interactive=False)
                with gr.Tab('修改条件与版本变化'):
                    revision = gr.Textbox(label='新的条件', value='补充一下，我已经使用PostgreSQL。')
                    force = gr.Checkbox(label='强制重新读取资料', value=False)
                    revise_button = gr.Button('生成修订版')
                    changes = gr.Textbox(label='变化摘要', lines=5, interactive=False)
                    changes_diff = gr.Code(label='报告版本差异', language='markdown', interactive=False)
                with gr.Tab('运行记录'):
                    trace = gr.JSON(label='可观察调用、错误与用量，不包含内部思维链')
                with gr.Tab('流程图'):
                    flowchart_text = gr.Code(label='确定性 Mermaid 流程图', language='markdown', interactive=False)
                    flowchart_data = gr.JSON(label='结构化节点、边与状态')
                with gr.Tab('项目方案与架构'):
                    gr.Markdown('先提交项目目标，再逐层研究候选；只有引用已发布报告版本，才能确认架构。')
                    project_goal = gr.Textbox(label='项目目标', lines=3, value='为个人知识库设计可维护的技术方案')
                    project_allow = gr.Checkbox(label='允许未知条件，先生成条件式候选', value=True)
                    project_create = gr.Button('生成候选技术层', variant='primary')
                    project_id = gr.Textbox(label='项目编号', interactive=False)
                    project_options = gr.JSON(label='候选层、候选产品和研究维度')
                    project_layer = gr.Dropdown(label='选择要研究的技术层', choices=[])
                    project_research = gr.Button('研究此技术层')
                    project_task = gr.Textbox(label='层研究任务编号', interactive=False)
                    project_poll = gr.Button('查看层研究状态')
                    project_report = gr.Textbox(label='已发布报告编号（确认时使用）', interactive=False)
                    project_status = gr.Textbox(label='层研究状态', interactive=False)
                    project_base = gr.Number(label='架构基础版本（首次留空）', value=0, precision=0, minimum=0)
                    project_selections = gr.Textbox(label='选择 JSON（层 id → product/report_id/report_version）', lines=8,
                        placeholder='研究完成后按候选层填写，例如 {"vector_databases":{"product":"pgvector","report_id":"...","report_version":1}}')
                    project_confirm = gr.Button('确认并生成项目架构图')
                    project_version = gr.Number(label='架构版本', interactive=False)
                    project_mermaid = gr.Code(label='项目架构 Mermaid', language='markdown', interactive=False)
                    project_svg = gr.HTML(label='项目架构 SVG 预览')
                    project_choices = gr.Code(label='已确认选择与证据', language='json', interactive=False)
        outputs = [task_id, status, report_text, report_id, version, evidence_id, changes, changes_diff, trace,
                   flowchart_text, flowchart_data]
        start_button.click(start, [query, group, allow], outputs, api_name='start').then(
            lambda: gr.Timer(active=True), outputs=timer, api_name=False)
        answer_button.click(answer, [task_id, answer_text, allow], outputs, api_name='answer').then(
            lambda: gr.Timer(active=True), outputs=timer, api_name=False)
        revise_button.click(revise, [report_id, version, revision, force, allow], outputs, api_name='revise').then(
            lambda: gr.Timer(active=True), outputs=timer, api_name=False)
        timer.tick(poll, task_id, [*outputs, timer], queue=False, api_name='poll')
        restore_button.click(restore, task_id, outputs).then(
            lambda: gr.Timer(active=True), outputs=timer, api_name=False)
        cancel_button.click(cancel, task_id, status, queue=False)
        evidence_button.click(evidence, evidence_id, [evidence_text, evidence_meta])
        export_button.click(export, [report_id, version], export_file)
        project_create.click(create_project, [project_goal, project_allow],
                             [project_id, project_options, project_layer, project_status])
        project_research.click(research_project_layer, [project_id, project_layer], [project_task, project_status])
        project_poll.click(poll_project_task, project_task, [project_report, project_status])
        project_confirm.click(confirm_project, [project_id, project_base, project_selections],
                              [project_version, project_mermaid, project_svg, project_choices])
    return ui
