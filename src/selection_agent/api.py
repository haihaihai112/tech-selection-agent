from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

from .catalog import CATALOG
from .engine import Conflict, Engine
from .flowcharts import build_flowchart, render_mermaid
from .models import AnswerInput, ConfirmationInput, ProjectInput, ResearchInput, RevisionInput
from .projects import ProjectService


def create_app(config, with_ui=True, engine=None):
    engine = engine or Engine(config)
    projects = ProjectService(engine)

    @asynccontextmanager
    async def lifespan(app):
        yield
        await engine.close()

    app = FastAPI(title='技术选型研究 Agent', version='0.1.0', lifespan=lifespan)
    app.state.engine = engine

    def found(value):
        if value is None:
            raise HTTPException(404, '记录不存在')
        return value

    def submit(call):
        try:
            task = call()
            return {k: task[k] for k in ('id', 'session_id', 'report_id', 'status')}
        except Conflict as exc:
            raise HTTPException(409, str(exc)) from exc
        except KeyError as exc:
            raise HTTPException(404, '记录不存在') from exc

    @app.get('/health')
    async def health():
        ready = config.mode == 'fixture' or bool(config.api_key and config.tavily_key)
        return {'status': 'ok' if ready else 'configuration_required', 'config': config.public(),
                'provider_connectivity': 'not_checked', 'local_single_user': True}

    @app.get('/v1/catalog')
    async def catalog():
        return CATALOG

    @app.post('/v1/projects', status_code=201)
    async def create_project(request: ProjectInput):
        try:
            return await projects.create(request)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.get('/v1/projects/{project_id}')
    async def project(project_id: str):
        try:
            return projects._get(project_id)
        except KeyError as exc:
            raise HTTPException(404, '记录不存在') from exc

    @app.post('/v1/projects/{project_id}/layers/{layer_id}/research', status_code=202)
    async def project_research(project_id: str, layer_id: str):
        try:
            task = projects.research(project_id, layer_id)
            return {k: task[k] for k in ('id', 'session_id', 'report_id', 'status')}
        except KeyError as exc:
            raise HTTPException(404, '记录不存在') from exc
        except (Conflict, ValueError) as exc:
            raise HTTPException(409, str(exc)) from exc

    @app.post('/v1/projects/{project_id}/confirm')
    async def confirm_project(project_id: str, request: ConfirmationInput):
        try:
            return projects.confirm(project_id, request)
        except KeyError as exc:
            raise HTTPException(404, '记录不存在') from exc
        except Conflict as exc:
            raise HTTPException(409, str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.get('/v1/projects/{project_id}/architecture')
    async def project_architecture(project_id: str, version: int | None = None):
        try:
            value = projects.architecture(project_id, version)
        except KeyError as exc:
            raise HTTPException(404, '记录不存在') from exc
        return found(value)

    @app.post('/v1/research', status_code=202)
    async def research(request: ResearchInput):
        return submit(lambda: engine.submit(request))

    @app.get('/v1/tasks/{task_id}')
    async def task(task_id: str):
        return found(engine.db.get('tasks', task_id))

    @app.get('/v1/tasks/{task_id}/flowchart')
    async def task_flowchart(task_id: str):
        value = found(engine.db.get('tasks', task_id))
        report = (engine.report(value['report_id'], value.get('report_version'))
                  if value.get('report_version') else None)
        graph = build_flowchart(value, report)
        return {'task_id': task_id, 'report_id': value['report_id'], 'status': value['status'],
                'graph': graph.model_dump(), 'mermaid': render_mermaid(graph)}

    @app.post('/v1/tasks/{task_id}/answers', status_code=202)
    async def answer(task_id: str, request: AnswerInput):
        return submit(lambda: engine.answer(task_id, request))

    @app.post('/v1/tasks/{task_id}/cancel')
    async def cancel(task_id: str):
        found(engine.db.get('tasks', task_id))
        return await engine.cancel(task_id)

    @app.get('/v1/reports/{report_id}')
    async def report(report_id: str, version: int | None = None):
        return found(engine.report(report_id, version))

    @app.get('/v1/reports/{report_id}/flowchart')
    async def report_flowchart(report_id: str, version: int | None = None):
        report = found(engine.report(report_id, version))
        task = found(engine.db.get('tasks', report['task_id']))
        graph = build_flowchart(task, report)
        return {'report_id': report_id, 'version': report['version'], 'status': graph.status,
                'graph': graph.model_dump(), 'mermaid': render_mermaid(graph)}

    @app.post('/v1/reports/{report_id}/revisions', status_code=202)
    async def revise(report_id: str, request: RevisionInput):
        return submit(lambda: engine.revise(report_id, request))

    @app.get('/v1/reports/{report_id}/export')
    async def export(report_id: str, version: int | None = None):
        value = found(engine.report(report_id, version))
        return Response(value['markdown'], media_type='text/markdown; charset=utf-8',
                        headers={'Content-Disposition': f'attachment; filename="selection-v{value["version"]}.md"'})

    @app.get('/v1/evidence/{evidence_id}')
    async def evidence(evidence_id: str):
        value = found(engine.db.get('evidence', evidence_id))
        source = found(engine.db.get('sources', value['snapshot_id']))
        path = config.runtime / 'snapshots' / source['content_path']
        return {'evidence': value, 'source': source, 'snapshot_text': path.read_text(encoding='utf-8') if path.exists() else None}

    if with_ui:
        import gradio as gr
        from .ui import build_ui
        app = gr.mount_gradio_app(app, build_ui(engine), path='/ui')
    return app
