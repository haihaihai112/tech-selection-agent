# 验证记录

更新时间：2026-09-21（Asia/Shanghai）。本文件只记录实际运行结果；fixture 数字代表机制测试，不代表真实模型准确率或真实产品结论。

## 自动检查

- `pytest -q --junitxml=reports/tests.xml`：52 passed。
- `ruff check src tests scripts`：通过。
- `python -m compileall -q src scripts`：通过。
- `scripts/smoke.py`：真实 ASGI/HTTP 闭环通过，结果保存在 `reports/http-smoke.json`。
- Gradio 回调 smoke：通过追问、轮询、修订、证据查看、旧版导出、恢复和取消；没有浏览器视觉检查，结果保存在 `reports/ui-smoke.json`。
- Docker Compose：配置语法已检查；本环境未把容器启动结果写成通过项。

## 确定性评测

`reports/development.json` 是 30 个开发场景及两项消融的原始结果。场景覆盖三个产品组的条件追问、原文不可读、证据不足、版本限制、预算、修订复用、重启恢复等机制。评测使用合成资料与确定性测试替身，不作为真实模型成功率。

`evaluation/holdout_15.json` 是实现后新增的 15 个机制留出场景；首次结果 **12/15 通过**，原始失败结果保存在 `reports/holdout.json`，未通过修改输入或代码把此次留出结果改成全通过。运行命令：

```powershell
.venv/Scripts/python.exe scripts/evaluate.py --dataset evaluation/holdout_15.json --output reports/holdout.json
```

三项失败原因：vector-03 初始输入已包含 PostgreSQL，修订未改变条件而测试要求有变化；search-02、rag-02 的测试替身使用简单词项识别，把“不确定是否需要正文”“文档类型尚未确定”误识别为已知条件，导致没有追问。真实模型不使用该词项规则。这暴露了测试替身的语义限制，也说明这些场景不能作为真实模型能力评测。

留出场景同样只验证程序机制，不能替代人工事实审阅。`reports/freeze.json` 保存此次运行关键源码哈希；记录时间以 actual_recorded_at 为准，原 created_at 是记录脚本的手填值，不能作为精确冻结时间证据。场景生成与源码摘要记录不构成独立盲评。

## 真实模型运行

`reports/live-demo-final-deepseek.json` 使用原配置文件中的真实 LLM/Tavily 凭据，以 `deepseek-v3.2` 完成了首版研究和一次条件修订。两个任务均生成 `partial` 报告，各自保留 5 条 `supported` 事实和未解决缺口；调用量、Token、页面读取、原始轨迹和来源快照均已保存。此结果只代表这次运行，不是准确率或推荐成功率。

此前的失败记录也保留：`live-demo.json`、`live-demo-final.json`、`live-demo-repaired.json` 和 `live-quota-block.json`。其中包括 Qwen 配额耗尽、页面读取超时和供应商结构化参数包装问题。修复后当前适配层支持严格的单字段 JSON 包装，并对结构化输出最多做一次纠错。

模型配置支持 `LLM_FALLBACK_MODELS`。只有供应商明确返回 `AllocationQuota.FreeTierOnly`、`insufficient_quota` 等配额耗尽代码才切换；认证失败、普通限流和格式错误不触发切换。每次尝试记录请求模型、实际响应模型、Token和切换原因；混用模型时费用保持未知，除非分别提供单价。

未完成的外部核验：没有对九款产品做性能基准，没有人工独立审阅全部真实结论，没有验证所有供应商套餐价格，也没有声明公网多租户安全。

新增推荐理由核验后的真实运行见 `reports/live-demo-audited.json`：任务在 Writer 阶段以 ValueError 停止，没有发布报告。当前轨迹只保存异常类型，不能据此准确区分具体哪条推荐校验失败；该运行不计为完成。较早的两版 partial 报告仅是审计样本，不代表新增门禁后已通过完整真实闭环。助手复核与后续人工审阅模板见 `ASSISTANT_REVIEW.md` 和 `human-review-template.csv`。

最终检查：52 项 pytest 通过、30/30 开发机制场景通过，15 项留出首次结果为 12/15。源码在留出运行后增加了推荐理由语义门禁，因此该留出结果对应原始记录的实现版本，并非最终版本独立盲评。完整 HTTP 和 Gradio 回调已在最终代码上重跑通过。Docker daemon 不可用，仅验证 Compose 语法。
## 2026-10-13 增量功能验证

本节只记录本轮为“目标→候选技术层→逐层研究→确认选择→项目架构图”新增的验证，不覆盖历史真实模型结论。

- `uv run --no-sync pytest -q --junitxml=reports/tests-flowchart-projects.xml`：61 passed，0 failed。
- `uv run --no-sync ruff check src tests scripts`：通过。
- `uv run --no-sync python -m compileall -q src scripts`：通过。
- `scripts/smoke.py --base http://127.0.0.1:8151 --output reports/http-smoke-flowchart.json`：ASGI/HTTP fixture 闭环通过；健康检查、研究、修订、旧版导出和项目创建均完成。项目未确认架构时读取接口返回 404，符合未发布版本语义。
- `scripts/ui_smoke.py`：在约定的 `http://127.0.0.1:8050/ui/` 上通过 Gradio 回调；覆盖既有澄清、轮询、修订、证据、导出、恢复和取消。`visual_inspection=false`，没有浏览器视觉检查。
- 新增确定性流程图测试覆盖稳定节点与边、并行候选、补查、失败和等待输入状态、Mermaid 状态映射、任务/报告流程图 API。
- 新增项目测试覆盖固定目录候选层、自定义目录边界、逐层 fixture 研究、报告版本绑定、选择校验、不可变架构版本和 SVG 输出。

本轮仍未调用真实模型、Tavily、ComfyUI 或其他付费图像 API。候选适配理由和项目架构连线在 fixture 中是教学用合成内容；真实资料支持和产品兼容性仍需单独核验。
