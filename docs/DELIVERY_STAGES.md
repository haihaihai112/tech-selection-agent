# 分阶段交付与复核命令

所有命令在项目目录执行，Python 3.11。当前安装版本见 `reports/environment.json`，依赖锁见 `uv.lock` 和 `requirements.lock.txt`。

| 阶段 | 已实现 | 复核命令与证据 | 边界 |
|---|---|---|---|
| 基础层 | SQLite WAL、三组产品目录、HTML/文本/PDF读取、正文快照与测试模式 | `uv sync --frozen`；`pytest tests/test_sources.py -q` | PDF须有文本层；无登录绕过、OCR和浏览器渲染 |
| 首个闭环 | LangGraph澄清、并行Researcher、原文核验、有预算补查、报告生成 | `pytest tests/test_workflow.py tests/test_verification.py -q` | 缺口会保留为partial；不强制排名 |
| 修订与工作台 | Gradio、HTTP API、历史版本、证据复用、取消与重启记录 | `selection --fixture`；`python scripts/smoke.py`；`python scripts/ui_smoke.py` | 本地单用户、单进程；没有独立浏览器视觉检查 |
| 扩展与验证 | 三组目录、真实模型接入、配额切换、开发场景、消融、留出记录 | `python scripts/evaluate.py --ablation`；真实调用见 `scripts/run_live_demo.py` | 真实长流程当前只验证向量数据库组；另两组仅机制验证 |

## 真实运行

复制 `.env.example` 为 `.env`，配置同一供应商的实际地址与可用模型、LLM_API_KEY及TAVILY_API_KEY。

```powershell
uv run --no-sync python scripts/check_live.py --model deepseek-v3.2
uv run --no-sync python scripts/run_live_demo.py --model deepseek-v3.2 --output reports/my-live-demo.json
```

`--env-file` 可仅从已有文件读取凭据与地址；旧凭据文件里的模型名不再覆盖新项目默认模型。多供应商并非自动发现：备用模型必须属于所配置地址并支持原生工具调用，使用 `--fallback-models model-a,model-b` 显式配置。

## 安装和容器

锁文件已经按官方 PyPI 地址保存并通过离线一致性检查。当前主机安装时官方索引TLS不稳定，曾用本地转发下载且保留包哈希；该临时转发不是交付依赖。Docker Compose配置可解析，本机Docker daemon未运行，未声称实际容器启动通过。
