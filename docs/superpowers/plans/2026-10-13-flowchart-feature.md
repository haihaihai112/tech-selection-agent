# 选型结果流程图 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 根据已保存的研究任务和报告结果生成可追溯的结构化流程图与 Mermaid 文本，供用户审查和学习。

**Architecture:** 新增纯函数式 FlowGraph 构建器和 Mermaid 渲染器。Engine 不执行额外调用；API 读取任务/报告后调用构建器，UI 通过已有轮询结果展示流程图。ComfyUI/API 图像适配器暂缓到独立计划。

**Tech Stack:** Python 3.11、Pydantic 2、FastAPI、Gradio、pytest；不增加运行时依赖。

**Spec:** `docs/superpowers/specs/2026-10-13-flowchart-design.md`

## Global Constraints

- 只消费已有任务 trace、brief、claims 和报告版本，不触发模型、搜索或读取调用。
- 不把失败、部分完成或等待输入渲染为成功。
- 不输出模型思维链、密钥、完整请求或不受控异常文本。
- Mermaid 和 JSON 是首版权威产物；图像 API 不属于首版验收范围。

---

### Task 1: 定义流程图模型与确定性构建器

**Files:**
- Create: `src/selection_agent/flowcharts.py`
- Test: `tests/test_flowcharts.py`

**Interfaces:**
- Produces `FlowNode`, `FlowEdge`, `FlowGraph` Pydantic 模型。
- Produces `build_flowchart(task: dict, report: dict | None = None) -> FlowGraph`。
- Produces `render_mermaid(graph: FlowGraph) -> str`。

- [ ] 写测试：默认任务包含 clarify、research、verify、write 四个主阶段，三个产品作为研究分支；断言节点顺序和边顺序稳定。
- [ ] 写测试：`failed`、`partial`、`input_required` 状态映射为对应状态，不出现成功状态。
- [ ] 写测试：trace 中存在 `research_round` 且 round 大于 0 时，图包含 repair 节点或边；异常文本不进入节点标签。
- [ ] 运行 `pytest tests/test_flowcharts.py -q`，确认在模块尚不存在时按预期失败。
- [ ] 实现严格模型、状态映射、产品分支构建和有限字符清洗。
- [ ] 实现 Mermaid 节点 id 转义、稳定顺序和状态 classDef；不嵌入原始 URL 或异常详情。
- [ ] 运行 `pytest tests/test_flowcharts.py -q`，确认通过。

### Task 2: 接入 FastAPI 查询接口

**Files:**
- Modify: `src/selection_agent/api.py`
- Test: `tests/test_api.py`

**Interfaces:**
- `GET /v1/tasks/{task_id}/flowchart` 返回 `{task_id, report_id, status, graph, mermaid}`。
- `GET /v1/reports/{report_id}/flowchart?version=N` 返回 `{report_id, version, graph, mermaid}`。

- [ ] 为完成任务和指定旧报告版本写 API 测试，断言图可解析且版本正确。
- [ ] 为未知任务、未知报告和不存在版本写 404 测试。
- [ ] 运行对应 API 测试，确认新接口先失败。
- [ ] 在 API 中读取记录并调用 `build_flowchart`、`render_mermaid`；不启动新任务。
- [ ] 运行 API 测试和现有 API 测试，确认通过。

### Task 3: 接入 Gradio 展示

**Files:**
- Modify: `src/selection_agent/ui.py`
- Test: `tests/test_api.py` 或新增 `tests/test_flowcharts.py`

**Interfaces:**
- `display(task)` 返回值增加 Mermaid 文本和结构化 JSON 两个展示字段。
- UI 增加“流程图”页签，展示 Mermaid 源码及节点 JSON。

- [ ] 写一个无浏览器的回调测试，确认报告完成后 display 返回流程图内容，失败任务也能显示状态图。
- [ ] 运行测试确认新增输出尚不存在。
- [ ] 调整 `display` 和 outputs 接线，保持已有报告、证据、修订和运行记录顺序兼容。
- [ ] 运行 UI smoke 所覆盖的回调测试和完整 pytest。

### Task 4: 文档与回归验证

**Files:**
- Modify: `README.md`
- Modify: `docs/INTERFACES.md`
- Modify: `reports/VALIDATION.md`（只记录本轮实际运行结果）

**Interfaces:**
- 文档说明流程图来源、接口、fixture 限制和后续 ComfyUI 边界。

- [ ] 增加 API 示例、Mermaid 产物说明和失败状态语义。
- [ ] 跑 `pytest -q`、`ruff check src tests scripts` 和 `python -m compileall -q src scripts`。
- [ ] 运行 fixture HTTP smoke；不调用 `scripts/check_live.py`。
- [ ] 只在命令实际通过后更新验证记录并汇报结果。

### 后续独立计划：ComfyUI/API 视觉适配器

首版确定性流程图完成并验证后，再单独设计 `ImageRenderer` 接口、ComfyUI workflow 模板、预算与脱敏日志、mock 测试和真实调用授权流程。它不应阻塞结构化流程图交付。

### Task 5: 用户目标与可核验的自定义技术目录

- [x] 新增 `ProjectInput`、候选层和候选产品边界，校验去重和引用。
- [x] 新增 `ResearchInput.custom_catalog` 和 `group=custom`，保留所有固定目录逻辑，禁止未给目录的自定义研究。
- [x] 测试动态目录的 fixture 完整报告、修订复用和跨项目绑定。
- [x] 实现 `ProjectService.create/research/architecture`；create 只提出未验证候选，research 显式启动单层任务。
- [x] 候选条件保留在 options；已确认架构以不可变版本保存。

### Task 6: 确认选择、不可变项目架构和 SVG

- [x] 测试报告必须归属项目和层、版本存在、选择在候选范围内、未确认不生成架构。
- [x] 测试旧架构在后续报告及架构修订后不改变；过期基础版本返回 409。
- [x] 新增 `ProjectService.confirm/architecture`，保存不可变架构版本和 head。
- [x] 实现确定性 `render_svg`；使用转义文本、固定几何布局和服务端节点 id，不加载远程资源。
- [x] 测试 SVG 输出、安全文本、明确显示合成标识。

### Task 7: 项目工作台、API 和完整验收

- [x] 新增 `/v1/projects`、指定层研究、架构确认、指定版本读取与 Mermaid/SVG 输出接口。
- [x] Gradio 增加目标、候选、层研究、选择 JSON、图形审查与导出展示。
- [x] fixture HTTP 与既有 Gradio 回调完成研究流程和项目创建边界验证。
- [x] 新测试和完整 pytest/Ruff/compileall 后更新验证和使用说明。
