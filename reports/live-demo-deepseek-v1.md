> 历史报告导出 / Historical report export. 原运行的证据 ID 保留为文本；旧会话数据库不随源码发布，ID 不能在新实例直接恢复。Evidence IDs refer to the original run, whose session database is not distributed.

# 技术选型研究报告 · 第 1 版

**基于本次抓取资料；模型语义核验不等同于独立事实审计。**

## 用户条件

- 部署方式：本地自托管部署
- 维护要求：优先考虑维护成本
- 偏好：维护成本优先
- 尚未明确：预算
- 尚未明确：数据规模
- 尚未明确：已有技术栈
- 尚未明确：部署方式的具体要求

## 来源事实对比

| 比较维度 | pgvector | Qdrant | Milvus |
|---|---|---|---|
| 部署方式 | 证据不足，不能确定 | Qdrant支持通过Docker和Docker Compose在生产环境中运行，也提供Kubernetes Helm Chart和二进制安装方式 [C-4a230983b3b94082]；对于在自有基础设施中运行Qdrant且无需云连接的情况，推荐使用Qdrant Private Cloud Enterprise Operator在Kubernetes集群中安装 [C-9e0bde68deba443c] | 证据不足，不能确定 |
| 已有技术栈 | 证据不足，不能确定 | 证据不足，不能确定 | 证据不足，不能确定 |
| 检索与过滤 | 证据不足，不能确定 | 证据不足，不能确定 | 证据不足，不能确定 |
| 维护要求 | 证据不足，不能确定 | Helm chart的支持仅限于社区支持，企业级功能需要自行管理 [C-81a3912525904be5] | 证据不足，不能确定 |
| 扩展方式 | 证据不足，不能确定 | 可以通过Helm chart在分布式设置中部署Qdrant，支持水平扩展 [C-21daedef9a6e45ca]；Qdrant Private Cloud Enterprise Operator提供垂直扩展能力 [C-867454c533574605] | 证据不足，不能确定 |

## 基于条件的判断（与来源事实分开）

- **Qdrant**：用户要求本地自托管部署，Qdrant支持Docker/Docker Compose、Kubernetes Helm Chart、二进制安装等多种本地部署方式，符合部署条件。用户优先考虑维护成本，但Qdrant的Helm chart仅提供社区支持，企业级功能需要自行管理，这可能增加维护负担。 [C-4a230983b3b94082] [C-81a3912525904be5]

## 冲突与待确认项

- pgvector / 部署方式：没有足够的无冲突原文证据；不据此判定不支持。
- pgvector / 已有技术栈：没有足够的无冲突原文证据；不据此判定不支持。
- pgvector / 检索与过滤：没有足够的无冲突原文证据；不据此判定不支持。
- pgvector / 维护要求：没有足够的无冲突原文证据；不据此判定不支持。
- pgvector / 扩展方式：没有足够的无冲突原文证据；不据此判定不支持。
- Qdrant / 已有技术栈：没有足够的无冲突原文证据；不据此判定不支持。
- Qdrant / 检索与过滤：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 部署方式：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 已有技术栈：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 检索与过滤：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 维护要求：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 扩展方式：没有足够的无冲突原文证据；不据此判定不支持。
- [C-e284f96ab6b14137] Milvus：Milvus提供三种部署选项：Milvus Lite、Milvus Standalone和Milvus Distributed；适用条件没有原文支持
- [C-be850d46cbee43a6] Milvus：Milvus Standalone是单机服务器部署，所有组件打包到单个Docker镜像中，适合生产工作负载但不想使用Kubernetes的情况；适用条件没有原文支持
- [C-644635e0d8d848b9] Milvus：Milvus Standalone可以在给定足够机器资源的情况下扩展到1亿向量，同时比维护K8s集群需要更少的DevOps；适用条件没有原文支持
- [C-10a6c34e329347ad] Milvus：Milvus支持向量搜索（ANN搜索）、元数据过滤、范围搜索、标量查询、按主键获取实体和混合搜索；适用条件没有原文支持
- [C-a83cc1e0ec6b4517] Milvus：Milvus Distributed专为大规模部署设计，能够处理从1亿到数百亿向量的数据集；适用条件没有原文支持

## 结论与原文证据

- [C-e284f96ab6b14137] insufficient：E-8818cfb2321ddd07d3235399-22 (`E-8818cfb2321ddd07d3235399-22`)
- [C-be850d46cbee43a6] insufficient：E-8818cfb2321ddd07d3235399-27 (`E-8818cfb2321ddd07d3235399-27`)
- [C-644635e0d8d848b9] insufficient：E-8818cfb2321ddd07d3235399-33 (`E-8818cfb2321ddd07d3235399-33`)
- [C-10a6c34e329347ad] insufficient：E-8818cfb2321ddd07d3235399-45 (`E-8818cfb2321ddd07d3235399-45`)
- [C-a83cc1e0ec6b4517] insufficient：E-8818cfb2321ddd07d3235399-39 (`E-8818cfb2321ddd07d3235399-39`)
- [C-4a230983b3b94082] supported：E-cc31d7c44ff2284444ce189c-69 (`E-cc31d7c44ff2284444ce189c-69`) E-cc31d7c44ff2284444ce189c-71 (`E-cc31d7c44ff2284444ce189c-71`) E-cc31d7c44ff2284444ce189c-45 (`E-cc31d7c44ff2284444ce189c-45`) E-cc31d7c44ff2284444ce189c-103 (`E-cc31d7c44ff2284444ce189c-103`)
- [C-9e0bde68deba443c] supported：E-cc31d7c44ff2284444ce189c-36 (`E-cc31d7c44ff2284444ce189c-36`)
- [C-21daedef9a6e45ca] supported：E-cc31d7c44ff2284444ce189c-45 (`E-cc31d7c44ff2284444ce189c-45`)
- [C-867454c533574605] supported：E-cc31d7c44ff2284444ce189c-41 (`E-cc31d7c44ff2284444ce189c-41`)
- [C-81a3912525904be5] supported：E-cc31d7c44ff2284444ce189c-45 (`E-cc31d7c44ff2284444ce189c-45`)

## 来源与时间

- Overview of Milvus Deployment Options Milvus v2.5.x documentation · official · 已读取原文 · 抓取 2026-09-21T09:14:24.025272+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/v2.5.x/install-overview.md
- Installation - Qdrant · official · 已读取原文 · 抓取 2026-09-21T09:14:21.775613+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/installation
- GitHub - timescale/pgvectorscale: Postgres extension for vector search (DiskANN), complements pgvector for performance and scale. Postgres OSS licensed. · GitHub · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:22.940113+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/timescale/pgvectorscale
- 智譜上線AutoClaw 實現一鍵部署本地版「龍蝦」 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:18.636747+00:00 · 发布 未知 · 文档版本 未知 · https://hk.finance.yahoo.com/news/%E6%99%BA%E8%AD%9C%E4%B8%8A%E7%B7%9Aautoclaw-%E5%AF%A6%E7%8F%BE-%E9%8D%B5%E9%83%A8%E7%BD%B2%E6%9C%AC%E5%9C%B0%E7%89%88-%E9%BE%8D%E8%9D%A6-024443115.html
- Install SDKs \| Cloud \| Zilliz Cloud Developer Hub · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:28.691238+00:00 · 发布 未知 · 文档版本 未知 · https://docs.zilliz.com/docs/install-sdks
- PostgreSQL with pgvector 部署教學 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:15:00.868527+00:00 · 发布 未知 · 文档版本 未知 · https://zeabur.com/zh-TW/templates/773OAW
- API 与 SDK - Qdrant - Qdrant 向量数据库 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:26.767057+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.org.cn/documentation/interfaces
- 概述- Qdrant - Qdrant 向量数据库 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:18.702734+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.org.cn/documentation/overview
- 什么是Milvus \| Milvus 文档 · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:28.719975+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/overview.md
- 在VPS上自托管Loomfeed：Docker部署指南 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:15:00.851726+00:00 · 发布 未知 · 文档版本 未知 · https://www.ssdnodes.com/learn/lang/zh-hans/self-host-loomfeed-reddit-alternative
- GitHub - pgvector/pgvector-python: pgvector support for Python · GitHub · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:22.970199+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/pgvector/pgvector-python
- 部署Qdrant社区版服务实例-计算巢服务-阿里云-计算巢服务(Compute Nest)-阿里云帮助中心 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:18.693609+00:00 · 发布 未知 · 文档版本 未知 · https://help.aliyun.com/zh/compute-nest/use-cases/qdrant-community-edition-service-instance-deployment-document
- 華為ModelEngine支持DeepSeek全系列本地部署 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:18.646820+00:00 · 发布 未知 · 文档版本 未知 · https://hk.finance.yahoo.com/news/%E8%8F%AF%E7%82%BAmodelengine%E6%94%AF%E6%8C%81deepseek%E5%85%A8%E7%B3%BB%E5%88%97%E6%9C%AC%E5%9C%B0%E9%83%A8%E7%BD%B2-231813233.html
- 自托管指南 - Flashcards · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:15:00.878306+00:00 · 发布 未知 · 文档版本 未知 · https://flashcards-open-source-app.com/zh/docs/self-hosting
- Qdrant Python 客户端文档 — Qdrant 客户端文档 - Qdrant Python 客户端 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:26.776718+00:00 · 发布 未知 · 文档版本 未知 · https://python-client.qdrant.org.cn/
- 在GKE 上部署Qdrant 向量数据库\| Kubernetes Engine · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:18.720363+00:00 · 发布 未知 · 文档版本 未知 · https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/deploy-qdrant?hl=zh-cn
- 快速入门\| Milvus 文档 · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:28.708846+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/quickstart.md
- About - Milvus java sdk v3.0.x · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:28.699293+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/api-reference/java/v3.0.x/About.md
- Mem0 实战(一):Docker Compose 自托管部署,接 OpenAI-compatible 网关、pgvector 与 502/405 排错 - Hello_worlds - 博客园 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:15:00.842570+00:00 · 发布 未知 · 文档版本 未知 · https://www.cnblogs.com/suyj/p/21220796
- API &amp; SDKs · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:26.788165+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/interfaces
- 在GKE 上部署PostgreSQL 矢量数据库\| Kubernetes Engine · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:15:00.859481+00:00 · 发布 未知 · 文档版本 未知 · https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/deploy-pgvector?hl=zh-cn
- Milvus 向量数据库进阶系列丨部署形态选型 - Zilliz 向量数据库 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:18.905358+00:00 · 发布 未知 · 文档版本 未知 · https://zilliz.com.cn/blog/everaging-vector-databases-enhanced-competitive-intelligence
- Qdrant官方快速入门和教程简化版 - shizidushu - 博客园 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:26.797405+00:00 · 发布 未知 · 文档版本 未知 · https://www.cnblogs.com/shizidushu/p/18385637
- 本地运行Milvus Lite · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:18.914417+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/milvus_lite.md
- Milvus 部署选项概述 · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:18.897751+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/install-overview.md
- Milvus SDK Code Helper Guide \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:28.680124+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/milvus-sdk-helper-mcp.md
- The pgvector extension - Neon Docs · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:22.950779+00:00 · 发布 未知 · 文档版本 未知 · https://neon.com/docs/extensions/pgvector
- 金山云(KC)公司简介,联系方式,官网,高管档案_英为财情Investing.com · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:26.806979+00:00 · 发布 未知 · 文档版本 未知 · https://cn.investing.com/equities/kingsoft-cloud-holdings-ltd-company-profile
- pgvector 0.7.0 Released\! · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:22.980314+00:00 · 发布 未知 · 文档版本 未知 · https://www.postgresql.org/about/news/pgvector-070-released-2852
- pgvector Tutorial: Integrate Vector Search into PostgreSQL \| DataCamp · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:22.960095+00:00 · 发布 未知 · 文档版本 未知 · https://www.datacamp.com/tutorial/pgvector-tutorial
- Local Quickstart · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:14:18.730993+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/quickstart