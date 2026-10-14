> 历史报告导出 / Historical report export. 原运行的证据 ID 保留为文本；旧会话数据库不随源码发布，ID 不能在新实例直接恢复。Evidence IDs refer to the original run, whose session database is not distributed.

# 技术选型研究报告 · 第 2 版

**基于本次抓取资料；模型语义核验不等同于独立事实审计。**

## 用户条件

- 维护要求：优先考虑维护成本
- 部署方式：本地自托管部署
- 已有技术栈：已使用PostgreSQL
- 偏好：维护成本优先
- 尚未明确：预算
- 尚未明确：数据规模

## 来源事实对比

| 比较维度 | pgvector | Qdrant | Milvus |
|---|---|---|---|
| 部署方式 | 证据不足，不能确定 | 证据不足，不能确定 | Milvus支持三种部署选项：Milvus Lite、Milvus Standalone和Milvus Distributed [C-2afd280d88d14034]；Milvus Standalone是单机服务器部署，所有组件打包到单个Docker镜像中 [C-cc33ee8b8d2e4182] |
| 已有技术栈 | 证据不足，不能确定 | 证据不足，不能确定 | 证据不足，不能确定 |
| 检索与过滤 | 证据不足，不能确定 | 证据不足，不能确定 | Milvus支持向量搜索（ANN搜索）、元数据过滤、范围搜索、标量查询、按主键获取实体、混合搜索 [C-080f4304ab08495a] |
| 维护要求 | 证据不足，不能确定 | 证据不足，不能确定 | Milvus Standalone比维护K8s集群需要少得多的DevOps工作 [C-2db86d7ade514d74] |
| 扩展方式 | 证据不足，不能确定 | 证据不足，不能确定 | Milvus Distributed设计用于大规模部署，能够处理从1亿到数百亿向量的数据集 [C-9f18c8d4a04e423a] |

## 基于条件的判断（与来源事实分开）

- **Milvus**：用户要求本地自托管部署，Milvus支持Standalone单机Docker部署（claim_ids: C-cc33ee8b8d2e4182），符合部署方式条件。用户优先考虑维护成本，Milvus Standalone比维护K8s集群需要少得多的DevOps工作（claim_ids: C-2db86d7ade514d74），符合维护要求条件。用户已使用PostgreSQL，但Milvus本身不是PostgreSQL扩展，而是独立向量数据库，与已有技术栈条件不完全匹配。 [C-cc33ee8b8d2e4182] [C-2db86d7ade514d74]

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
- GitHub - pgvector/pgvector: Open-source vector similarity search for Postgres · GitHub · official · 已读取原文 · 抓取 2026-09-21T09:47:25.945967+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/pgvector/pgvector
- Overview of Milvus Deployment Options \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T09:46:19.201912+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/install-overview.md
- Syncing Qdrant with Postgres Using Airbyte to Build RAG Applications over SQL Data · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:30.483789+00:00 · 发布 未知 · 文档版本 未知 · https://rito.hashnode.dev/syncing-qdrant-with-postgres-using-airbyte
- pgvector vs Milvus: 5 key differences and how to choose · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.850256+00:00 · 发布 未知 · 文档版本 未知 · https://www.instaclustr.com/education/vector-database/pgvector-vs-milvus-5-key-differences-and-how-to-choose
- What is Milvus \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:30.234692+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/overview.md
- Optimize generative AI applications with pgvector indexing: A deep dive into IVFFlat and HNSW techniques \| AWS Database Blog · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:32.418996+00:00 · 发布 未知 · 文档版本 未知 · https://aws.amazon.com/blogs/database/optimize-generative-ai-applications-with-pgvector-indexing-a-deep-dive-into-ivfflat-and-hnsw-techniques
- PGVector: HNSW vs IVFFlat — A Comprehensive Study · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:32.428216+00:00 · 发布 未知 · 文档版本 未知 · https://medium.com/@bavalpreetsinghh/pgvector-hnsw-vs-ivfflat-a-comprehensive-study-21ce0aaab931
- Deploying pgvector with Docker and Building a Container for RAG Applications · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.700811+00:00 · 发布 未知 · 文档版本 未知 · https://www.instaclustr.com/education/vector-database/deploying-pgvector-with-docker-and-building-a-container-for-rag-applications
- Deployment Options - Greptile · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.708857+00:00 · 发布 未知 · 文档版本 未知 · https://www.greptile.com/docs/deployment-options
- Deploy &amp; Host PgVector \[Updated Sep '26\] · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:22.824531+00:00 · 发布 未知 · 文档版本 未知 · https://railway.com/deploy/pgvector-updated-sep-26--pgvector-latest
- Nearest Neighbor Indexes \| Tiger Data · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:32.437575+00:00 · 发布 未知 · 文档版本 未知 · https://www.tigerdata.com/blog/nearest-neighbor-indexes-what-are-ivfflat-indexes-in-pgvector-and-how-do-they-work
- Turning PostgreSQL Into a Vector Database With pgvector \| Tiger Data · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:22.830076+00:00 · 发布 未知 · 文档版本 未知 · https://www.tigerdata.com/learn/postgresql-extensions-pgvector
- Milvus 和PGVector，哪个更好？ - 腾讯云开发者社区- Tencent · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.855394+00:00 · 发布 未知 · 文档版本 未知 · https://developer.cloud.tencent.com/article/2658089
- How does Milvus work with PostgreSQL? · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.839750+00:00 · 发布 未知 · 文档版本 未知 · https://help.tessell.com/en/articles/8462637-how-does-milvus-work-with-postgresql
- Keeping Postgres and Qdrant in Sync - Qdrant · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:30.489358+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/data-synchronization/with-postgres
- Self-Hosting Qdrant the Easy Way in 2026 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:24.953926+00:00 · 发布 未知 · 文档版本 未知 · https://sliplane.io/blog/self-hosting-qdrant-the-easy-way
- What is pgvector? \| Google Cloud · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.704807+00:00 · 发布 未知 · 文档版本 未知 · https://cloud.google.com/discover/what-is-pgvector
- Integrate Milvus with MindsDB \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:30.231181+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/integration_with_mindsdb.md
- Distributed Deployment · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:24.961971+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/scaling/distributed_deployment
- Qdrant Self Hosted · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:24.948279+00:00 · 发布 未知 · 文档版本 未知 · https://medium.com/@fadil.parves/qdrant-self-hosted-28a30106e9dd
- Use a Python program to migrate data from a self-managed Qdrant cluster to an AnalyticDB for PostgreSQL instance - AnalyticDB - Alibaba Cloud Documentation Center · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:30.498571+00:00 · 发布 未知 · 文档版本 未知 · https://www.alibabacloud.com/help/en/analyticdb/analyticdb-for-postgresql/user-guide/migrate-data-from-a-self-managed-qdrant-collection-to-an-analyticdb-for-postgresql-instance
- Vector Similarity Search with PostgreSQL's pgvector · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:32.424371+00:00 · 发布 未知 · 文档版本 未知 · https://severalnines.com/blog/vector-similarity-search-with-postgresqls-pgvector-a-deep-dive
- Local Quickstart · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:24.967537+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/quickstart
- Database \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:30.239722+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/manage_databases.md
- pgvector vs Qdrant in 2026 - Encore.dev · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:30.502977+00:00 · 发布 未知 · 文档版本 未知 · https://encore.dev/articles/pgvector-vs-qdrant
- Milvus vs Postgres - Understanding Vector Data Storage · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.845113+00:00 · 发布 未知 · 文档版本 未知 · https://myscale.com/blog/milvus-vs-postgres-performance-vector-data-storage
- Quickstart \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:30.242745+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/quickstart.md
- pgvector vs Qdrant: 5 key differences and how to choose · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:30.495368+00:00 · 发布 未知 · 文档版本 未知 · https://www.instaclustr.com/education/vector-database/pgvector-vs-qdrant-5-key-differences-and-how-to-choose
- Build a Self-Hosted RAG with Postgres pgvector: 2026 Guide · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.695923+00:00 · 发布 未知 · 文档版本 未知 · https://www.digitalapplied.com/blog/build-self-hosted-rag-postgres-pgvector-tutorial-2026
- 高性能向量資料庫，為規模而構建 · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.859639+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/zh-hant
- Installing pgvector · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:22.839306+00:00 · 发布 未知 · 文档版本 未知 · https://www.enterprisedb.com/docs/pg_extensions/pgvector/installing
- Step-by-Step Guide to Installing “pgvector” and Loading ... · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:22.835008+00:00 · 发布 未知 · 文档版本 未知 · https://medium.com/@besttechreads/step-by-step-guide-to-installing-pgvector-and-loading-data-in-postgresql-f2cffb5dec43
- Hosting Postgres with pgvector: provider tradeoffs, migrations, indexes, and tuning · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:47:59.690854+00:00 · 发布 未知 · 文档版本 未知 · https://blog.railway.com/p/hosting-postgres-with-pgvector