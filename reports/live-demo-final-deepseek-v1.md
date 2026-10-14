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

## 来源事实对比

| 比较维度 | pgvector | Qdrant | Milvus |
|---|---|---|---|
| 部署方式 | 证据不足，不能确定 | 证据不足，不能确定 | Milvus支持三种部署选项：Milvus Lite、Milvus Standalone和Milvus Distributed [C-2afd280d88d14034]；Milvus Standalone是单机服务器部署，所有组件打包到单个Docker镜像中 [C-cc33ee8b8d2e4182] |
| 已有技术栈 | 证据不足，不能确定 | 证据不足，不能确定 | 证据不足，不能确定 |
| 检索与过滤 | 证据不足，不能确定 | 证据不足，不能确定 | Milvus支持向量搜索（ANN搜索）、元数据过滤、范围搜索、标量查询、按主键获取实体、混合搜索 [C-080f4304ab08495a] |
| 维护要求 | 证据不足，不能确定 | 证据不足，不能确定 | Milvus Standalone比维护K8s集群需要少得多的DevOps工作 [C-2db86d7ade514d74] |
| 扩展方式 | 证据不足，不能确定 | 证据不足，不能确定 | Milvus Distributed设计用于大规模部署，能够处理从1亿到数百亿向量的数据集 [C-9f18c8d4a04e423a] |

## 基于条件的判断（与来源事实分开）

- **Milvus**：用户要求本地自托管部署，Milvus支持三种部署选项包括Standalone单机Docker部署，符合本地自托管条件。用户优先考虑维护成本，Milvus Standalone比维护K8s集群需要少得多的DevOps工作，维护成本较低。 [C-2afd280d88d14034] [C-cc33ee8b8d2e4182] [C-2db86d7ade514d74]

## 冲突与待确认项

- pgvector / 部署方式：没有足够的无冲突原文证据；不据此判定不支持。
- pgvector / 已有技术栈：没有足够的无冲突原文证据；不据此判定不支持。
- pgvector / 检索与过滤：没有足够的无冲突原文证据；不据此判定不支持。
- pgvector / 维护要求：没有足够的无冲突原文证据；不据此判定不支持。
- pgvector / 扩展方式：没有足够的无冲突原文证据；不据此判定不支持。
- Qdrant / 部署方式：没有足够的无冲突原文证据；不据此判定不支持。
- Qdrant / 已有技术栈：没有足够的无冲突原文证据；不据此判定不支持。
- Qdrant / 检索与过滤：没有足够的无冲突原文证据；不据此判定不支持。
- Qdrant / 维护要求：没有足够的无冲突原文证据；不据此判定不支持。
- Qdrant / 扩展方式：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 已有技术栈：没有足够的无冲突原文证据；不据此判定不支持。

## 结论与原文证据

- [C-2afd280d88d14034] supported：E-edb209f32f4109ddadb255a9-22 (`E-edb209f32f4109ddadb255a9-22`)
- [C-cc33ee8b8d2e4182] supported：E-edb209f32f4109ddadb255a9-27 (`E-edb209f32f4109ddadb255a9-27`)
- [C-2db86d7ade514d74] supported：E-edb209f32f4109ddadb255a9-33 (`E-edb209f32f4109ddadb255a9-33`)
- [C-080f4304ab08495a] supported：E-edb209f32f4109ddadb255a9-46 (`E-edb209f32f4109ddadb255a9-46`)
- [C-9f18c8d4a04e423a] supported：E-edb209f32f4109ddadb255a9-39 (`E-edb209f32f4109ddadb255a9-39`)

## 来源与时间

- Installation - Qdrant · official · 已读取原文 · 抓取 2026-09-21T09:46:17.439471+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/installation
- Overview of Milvus Deployment Options \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T09:46:19.201912+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/install-overview.md
- Configuration - Qdrant · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.396071+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/ops-configuration/configuration
- 运行向量相似度搜索  \|  AlloyDB for PostgreSQL  \|  Google Cloud Documentation · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:18.518686+00:00 · 发布 未知 · 文档版本 未知 · https://docs.cloud.google.com/alloydb/docs/ai/run-vector-similarity-search?hl=zh-cn
- pgvector使用指南 - 阿里云文档 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:18.557310+00:00 · 发布 未知 · 文档版本 未知 · https://help.aliyun.com/zh/rds/apsaradb-rds-for-postgresql/pgvector-use-guide
- pgvector/pgvector: Open-source vector similarity search for ... · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.966024+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/pgvector/pgvector
- 十倍成本优化，Milvus 2.5到2.6升级官方手把手教程 - 向量数据库 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:23.516015+00:00 · 发布 未知 · 文档版本 未知 · https://zilliz.com.cn/blog/Milvus-2.5-to-2.6-tenfold-cost-optimization-guide
- 如何在 VPS 上自托管 RAG 流水线：从分块到向量检索 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.466053+00:00 · 发布 未知 · 文档版本 未知 · https://www.ssdnodes.com/learn/lang/zh-hans/self-host-rag-pipeline-on-a-vps
- Main Components \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:23.532421+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/main_components.md
- \[向量数据库/AI\] Milvus 安装部署篇- 千千寰宇 - 博客园 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.920906+00:00 · 发布 未知 · 文档版本 未知 · https://www.cnblogs.com/johnnyzen/p/19749790
- pgvector 向量扩展使用指南 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.956468+00:00 · 发布 未知 · 文档版本 未知 · https://intl.cloud.tencent.com/zh/document/product/409/80360
- pgvector实现高维向量检索- 云数据库RDS - 阿里云 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.947508+00:00 · 发布 未知 · 文档版本 未知 · https://www.alibabacloud.com/help/zh/rds/apsaradb-rds-for-postgresql/pgvector-use-guide
- 在Docker 中运行Milvus（Linux） · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.946258+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/install_standalone-docker.md
- Qdrant Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.376104+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation
- 快速入门\| Milvus 文档 · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.931624+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/quickstart.md
- PostgreSQL pgvector: Getting Started and Scaling · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.495532+00:00 · 发布 未知 · 文档版本 未知 · https://www.yugabyte.com/blog/postgresql-pgvector-getting-started
- 用pgvector 做RAG：别急着上Pinecone，你的PostgreSQL 就 ... · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.477192+00:00 · 发布 未知 · 文档版本 未知 · https://www.fanyamin.com/2026-03-10-pgvector-rag.html
- 在VPS上自托管Loomfeed：Docker部署指南 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:45.920283+00:00 · 发布 未知 · 文档版本 未知 · https://www.ssdnodes.com/learn/lang/zh-hans/self-host-loomfeed-reddit-alternative
- 轻量应用服务器 部署 Qdrant 向量数据库应用模板_腾讯云 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.320018+00:00 · 发布 未知 · 文档版本 未知 · https://cloud.tencent.com/document/product/1207/122669
- Azure Database for PostgreSQL 灵活服务器中的向量搜索 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:18.529370+00:00 · 发布 未知 · 文档版本 未知 · https://learn.microsoft.com/zh-cn/azure/postgresql/extensions/how-to-use-pgvector
- 本地向量数据库PGVector部署 - 钧泽 - 博客园 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:45.911169+00:00 · 发布 未知 · 文档版本 未知 · https://www.cnblogs.com/anpeiyong/p/19916831
- PostgreSQL with pgvector 部署教學 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:45.937092+00:00 · 发布 未知 · 文档版本 未知 · https://zeabur.com/zh-TW/templates/773OAW
- 在GKE 上部署PostgreSQL 矢量数据库\| Kubernetes Engine · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:45.927384+00:00 · 发布 未知 · 文档版本 未知 · https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/deploy-pgvector?hl=zh-cn
- PGVector（向量检索） - 阿里云文档 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.938405+00:00 · 发布 未知 · 文档版本 未知 · https://help.aliyun.com/zh/polardb/polardb-for-postgresql/pgvector
- 本地运行Milvus Lite · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.955449+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/milvus_lite.md
- Collections - Qdrant · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.413313+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/manage-data/collections
- 什么是Milvus \| Milvus 文档 · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:23.524151+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/overview.md
- Milvus 向量数据库文档 · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:23.542675+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh
- milvus/README_CN.md at master · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:23.504400+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/milvus-io/milvus/blob/master/README_CN.md
- Qdrant Overview · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.404278+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/overview
- 如何使用 Pgvector 將效能最佳化 - Azure Cosmos DB for PostgreSQL \| Microsoft Learn · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.976203+00:00 · 发布 未知 · 文档版本 未知 · https://learn.microsoft.com/zh-tw/azure/cosmos-db/postgresql/howto-optimize-performance-pgvector
- 概述- Qdrant - Qdrant 向量数据库 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.338642+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.org.cn/documentation/overview
- Qdrant社区版服务实例部署文档 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.327461+00:00 · 发布 未知 · 文档版本 未知 · https://help.aliyun.com/zh/compute-nest/use-cases/qdrant-community-edition-service-instance-deployment-document
- 在GKE 上部署Qdrant 向量数据库\| Kubernetes Engine · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:13.354995+00:00 · 发布 未知 · 文档版本 未知 · https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/deploy-qdrant?hl=zh-cn
- 3分钟搞定pgvector Docker部署：版本兼容性避坑指南 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:45.946219+00:00 · 发布 未知 · 文档版本 未知 · https://blog.csdn.net/gitblog_00039/article/details/155879937
- Pricing for Cloud and Vector Database Solutions Qdrant · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:46:22.385704+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/pricing