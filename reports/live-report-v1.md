> 历史报告导出 / Historical report export. 原运行的证据 ID 保留为文本；旧会话数据库不随源码发布，ID 不能在新实例直接恢复。Evidence IDs refer to the original run, whose session database is not distributed.

# 技术选型研究报告 · 第 1 版

**基于本次抓取资料；模型语义核验不等同于独立事实审计。**

## 用户条件

- 部署方式：本地自托管部署
- 偏好：维护成本最低优先
- 尚未明确：已有技术栈
- 尚未明确：数据规模
- 尚未明确：预算

## 来源事实对比

| 比较维度 | pgvector | Qdrant | Milvus |
|---|---|---|---|
| 部署方式 | 证据不足，不能确定 | 证据不足，不能确定 | 证据不足，不能确定 |
| 已有技术栈 | 证据不足，不能确定 | 证据不足，不能确定 | 证据不足，不能确定 |
| 检索与过滤 | 证据不足，不能确定 | 证据不足，不能确定 | 证据不足，不能确定 |
| 维护要求 | 证据不足，不能确定 | 证据不足，不能确定 | 证据不足，不能确定 |
| 扩展方式 | 证据不足，不能确定 | 证据不足，不能确定 | 证据不足，不能确定 |

## 基于条件的判断（与来源事实分开）

现有证据不足以形成可靠推荐；不强制排序。

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
- Milvus / 部署方式：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 已有技术栈：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 检索与过滤：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 维护要求：没有足够的无冲突原文证据；不据此判定不支持。
- Milvus / 扩展方式：没有足够的无冲突原文证据；不据此判定不支持。
- [C-ae58369ac63a4f5f] Qdrant：If you want to run Qdrant in your own infrastructure, without any cloud connection, we recommend to install Qdrant in a Kubernetes cluster with our Qdrant Private Cloud Enterprise Operator.；语义核验未完成：APITimeoutError
- [C-3db5a5862261461c] Qdrant：6333 - For the HTTP API, for the Monitoring health and metrics endpoints；语义核验未完成：APITimeoutError
- [C-eea3e31053f844f6] Qdrant：6334 - For the gRPC API；语义核验未完成：APITimeoutError
- [C-439c5c84aa3f46d8] Qdrant：docker run -p 6333:6333 -p 6334:6334 \\ -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \\ qdrant/qdrant；语义核验未完成：APITimeoutError
- [C-98b45be19ec946fc] Qdrant：from qdrant_client.models import Filter , FieldCondition , MatchValue search_result = client . query_points ( collection_name = "test_collection" , query = \[ 0.2 , 0.1 , 0.9 , 0.7 \], query_filter = Filter ( must = \[ FieldCondition ( key = "city" , match = MatchValue ( value = "London" ))\] ), with_payload = True , limit = 3 , ) . points print ( search_result )；语义核验未完成：APITimeoutError
- [C-9f416ad176c941ae] Qdrant：To enable distributed deployment - enable the cluster mode in the configuration or using the ENV variable: QDRANT__CLUSTER__ENABLED=true .；语义核验未完成：APITimeoutError
- [C-91a47e1a02ea405d] Qdrant：client . create_collection ( collection_name = " {collection_name} " , vectors_config = models . VectorParams ( size = 300 , distance = models . Distance . COSINE ), shard_number = 6 , )；语义核验未完成：APITimeoutError
- [C-a67d26b015ec48f1] Qdrant：client . create_collection ( collection_name = " {collection_name} " , vectors_config = models . VectorParams ( size = 300 , distance = models . Distance . COSINE ), shard_number = 6 , replication_factor = 2 , )；语义核验未完成：APITimeoutError
- [C-9633f88cea8f4bc9] Qdrant：Qdrant allows moving shards between nodes in the cluster and removing nodes from the cluster. This functionality unlocks the ability to dynamically scale the cluster size without downtime.；语义核验未完成：APITimeoutError
- [C-bb458e01d19342b2] Qdrant：It provides horizontal and vertical scaling, one click installation and upgrades, monitoring, logging, as well as backup and disaster recovery.；语义核验未完成：APITimeoutError
- [C-ff8259bce03e4990] Qdrant：It provides horizontal and vertical scaling, one click installation and upgrades, monitoring, logging, as well as backup and disaster recovery.；语义核验未完成：APITimeoutError
- [C-5a6d882803aa48fc] Qdrant：It provides horizontal and vertical scaling, one click installation and upgrades, monitoring, logging, as well as backup and disaster recovery.；语义核验未完成：APITimeoutError
- [C-47f3fd9083b04c77] pgvector：pgvector 是 PostgreSQL 的一个扩展，它做了三件事：1. 新增 \`vector\` 数据类型；2. 提供距离运算符；3. 支持 ANN 索引：IVFFlat 和 HNSW 两种近似最近邻索引。；语义核验未完成：APITimeoutError
- [C-8a5ffd0630f24657] pgvector：pgvector 是 PostgreSQL 的一个扩展；语义核验未完成：APITimeoutError
- [C-451b1079adf24387] pgvector：查询使用“&lt;-&gt;”运算符，这是用于计算多维空间中两个向量之间距离的“距离运算符”。 查询会返回所有与向量 \[3,1,2\] 的距离小于 6 的行。 SELECT  FROM tblvector WHERE embedding &lt;-&gt; '\[3,1,2\]' &lt; 6;；语义核验未完成：APITimeoutError
- [C-c6239fec3b734cc4] pgvector：pgvector部署（一行SQL）：CREATE EXTENSION vector;；语义核验未完成：APITimeoutError
- [C-b6a6446828774706] pgvector：最直接的方法是垂直扩展，通过增加更多 CPU、内存或存储来增强单个机器的资源，以容纳不断增长的数据量。；引用不属于本任务可用证据
- [C-5fa8b3d2f93f42a3] pgvector：Pgvector、Qdrant、Weaviate大多会采用手动来处理分片问题。但手动分片通常会导致：一开始看似低门槛的解决方案，发展到后期，随着数据量的增长，全都会变成惰性带来的技术负债：一个短择的技术决策，可能导致长期的遗患无穷。；引用不属于本任务可用证据
- [C-0ccb8245a5374c8e] Milvus：Milvus Standalone is a single-machine server deployment. All components of Milvus Standalone are packed into a single Docker image, making deployment convenient.；语义核验未完成：APITimeoutError
- [C-675e10b0e80849bb] Milvus：Milvus Lite is a Python library that can be imported into your applications. As a lightweight version of Milvus, it is ideal for quick prototyping in Jupyter Notebooks or running on smart devices with limited resources.；语义核验未完成：APITimeoutError
- [C-c0dc4d8673f947cb] Milvus：Vector similarity search and index building within Milvus require CPU’s support of single instruction, multiple data (SIMD) extension sets. Ensure that the CPU supports at least one of SSE4.2, AVX, AVX2, or AVX-512.；语义核验未完成：APITimeoutError
- [C-e55cfa5adb2b4313] Milvus：macOS 10.14 or later Docker Desktop Set the Docker virtual machine (VM) to use a minimum of 2 virtual CPUs (vCPUs) and 8 GB of initial memory. Otherwise, installation might fail. See Install Docker Desktop on Mac for more information. Linux platforms Docker 19.03 or later Docker Compose 1.25.1 or later See Install Docker Engine and Install Docker Compose for more information. Windows with WSL 2 enabled Docker Desktop We recommend that you store source code and other data bind-mounted into Linux containers in the Linux file system instead of the Windows file system. See Install Docker Desktop on Windows with WSL ；语义核验未完成：APITimeoutError
- [C-e78811f76d594f58] Milvus：By default this deployment runs Woodpecker (local-filesystem WAL) as the message queue and an embedded etcd for metadata — nothing else to install.；语义核验未完成：APITimeoutError
- [C-787898ff99cc479a] Milvus：Milvus supports sophisticated filtering capabilities including: \`==\` \`\!=\` \`&gt;\` \`&lt;\` \`&gt;=\` \`&lt;=\` \`and\` \`or\` \`not\` \`like\` \`array_contains\` \`array_length\`；语义核验未完成：APITimeoutError
- [C-8aa12bcc523c4edc] Milvus：Milvus provides powerful filtering capabilities that enable precise querying of your data. Filter expressions allow you to target specific scalar fields and refine search results with different conditions.；语义核验未完成：APITimeoutError
- [C-8ba4caba8cb9453e] Milvus：Milvus Backup is a tool that allows users to back up and restore Milvus data. It provides both CLI and API to fit itself into different application scenarios.；引用不属于本任务可用证据
- [C-f1ae976886b84090] Milvus：Prometheus is an open-source system monitoring and alerting toolkit for Kubernetes. Grafana is an open-source visualizing stack that can connect with all data sources. You can use Promethus &amp; Grafana as the monitoring service provider to visually monitor the performance of Milvus distributed.；语义核验未完成：APITimeoutError
- [C-4c44be5867f24cdc] Milvus：Milvus supports horizontal scaling of its components. This means you can either increase or decrease the number of worker nodes of each type according to your own need.；语义核验未完成：APITimeoutError
- [C-78ba027152e64af5] Milvus：Milvus itself is fully stateless so it can be easily scaled with the help of Kubernetes or public clouds. In addition, Milvus components are well decoupled, with the three most critical tasks—search, data insertion, and indexing/compaction—designed as easily parallelized processes, with complex logic separated out. This ensures that the corresponding query node, data node, and index node can scale both up and out independently, optimizing performance and cost efficiency.；语义核验未完成：APITimeoutError
- [C-72ab90fb04ea41ee] Milvus：In core, Milvus organizes data into 'Segments' — the smallest unit of data management: + Growing Segment located on StreamNodes, optimizing data freshness for real-time queries + Sealed Segment managed by QueryNodes, leveraging powerful indexes to accelerate search + These Segments are evenly distributed across nodes to optimize parallel processing；引用不属于本任务可用证据
- [C-ac9ff3a4fdb5484b] Qdrant：You can use a ready-made Helm Chart to run Qdrant in your Kubernetes cluster. While it is possible to deploy Qdrant in a distributed setup with the Helm chart, it does not come with the same level of features for zero-downtime upgrades, up and down-scaling, monitoring, logging, and backup and disaster recovery as the Qdrant Cloud offering or the Qdrant Private Cloud Enterprise Operator. Instead you must manage and set this up yourself . Support for the Helm chart is limited to community support.；语义核验未完成：APITimeoutError
- [C-7ab2c921923d44b7] Qdrant：You can use a ready-made Helm Chart to run Qdrant in your Kubernetes cluster. While it is possible to deploy Qdrant in a distributed setup with the Helm chart, it does not come with the same level of features for zero-downtime upgrades, up and down-scaling, monitoring, logging, and backup and disaster recovery as the Qdrant Cloud offering or the Qdrant Private Cloud Enterprise Operator. Instead you must manage and set this up yourself . Support for the Helm chart is limited to community support.；语义核验未完成：APITimeoutError
- [C-bbd83d3267af4d07] Qdrant：If you want to run Qdrant in your own infrastructure, without any cloud connection, we recommend to install Qdrant in a Kubernetes cluster with our Qdrant Private Cloud Enterprise Operator.；语义核验未完成：APITimeoutError
- [C-163bf618e96847b1] Qdrant：To enable distributed deployment - enable the cluster mode in the configuration or using the ENV variable: QDRANT__CLUSTER__ENABLED=true .；语义核验未完成：APITimeoutError
- [C-f01ab55c485a4476] Qdrant：If your cluster is running in Qdrant Cloud, shards are rebalanced across the cluster nodes automatically on an ongoing basis.；语义核验未完成：APITimeoutError
- [C-7e9738b4ab534801] Milvus：Milvus Standalone is a single-machine server deployment. All components of Milvus Standalone are packed into a single Docker image , making deployment convenient.；语义核验未完成：APITimeoutError
- [C-58cb6fd1fecf4140] Milvus：Milvus Distributed can be deployed on Kubernetes clusters. This deployment features a cloud-native architecture, where ingestion load and search queries are separately handled by isolated nodes, allowing redundancy for critical components.；语义核验未完成：APITimeoutError
- [C-16102b6e5abc42ab] Milvus：Milvus Standalone is a single-machine server deployment, with all components bundled into a single Docker image for convenient deployment.；语义核验未完成：APITimeoutError
- [C-e379dc580bfe4c47] Milvus：Milvus Distributed can be deployed on Kubernetes clusters, featuring a cloud-native architecture designed for billion-scale or even larger scenarios.；语义核验未完成：APITimeoutError
- [C-ef92bbb6b9fb4ac4] Milvus：If you want to use Backup in standalone deployment mode, it is recommended to use the Docker Compose deployment method.；语义核验未完成：APITimeoutError
- [C-b50276bb0681433b] Milvus：Linux platforms Docker 19.03 or later Docker Compose 1.25.1 or later；语义核验未完成：APITimeoutError
- [C-e236c3b7ea1d48c4] Milvus：macOS 10.14 or later Docker Desktop Set the Docker virtual machine (VM) to use a minimum of 2 virtual CPUs (vCPUs) and 8 GB of initial memory.；语义核验未完成：APITimeoutError
- [C-80f831d718ec4f46] Milvus：Windows with WSL 2 enabled Docker Desktop；语义核验未完成：APITimeoutError
- [C-4fc377a559bb453e] Milvus：Yes, Milvus supports both x86 and ARM architectures. ARM64 support is available through multiple deployment options including Docker images, RPM/DEB packages, and Milvus Lite.；语义核验未完成：APITimeoutError
- [C-bbe3fd59fed94152] Milvus：Yes, Milvus supports both x86 and ARM architectures. ARM64 support is available through multiple deployment options including Docker images, RPM/DEB packages, and Milvus Lite.；语义核验未完成：APITimeoutError
- [C-5ab6fc918eb84081] Milvus：Vector similarity search and index building within Milvus require CPU’s support of single instruction, multiple data (SIMD) extension sets. Ensure that the CPU supports at least one of SSE4.2, AVX, AVX2, or AVX-512.；语义核验未完成：APITimeoutError
- [C-004b8a21a9a047f5] Milvus：RAM Standalone: 8G Cluster: 32G；语义核验未完成：APITimeoutError
- [C-83feac7fd08e4693] Milvus：RAM Standalone: 16G Cluster: 128G The size of RAM depends on the data volume.；语义核验未完成：APITimeoutError
- [C-75be8772e3eb4091] Milvus：Disk performance is critical to etcd. It is highly recommended that you use local NVMe SSDs.；语义核验未完成：APITimeoutError

## 结论与原文证据

- [C-ae58369ac63a4f5f] insufficient：E-ab3b16efbc78de823592d2f3-36 (`E-ab3b16efbc78de823592d2f3-36`)
- [C-3db5a5862261461c] insufficient：E-ab3b16efbc78de823592d2f3-25 (`E-ab3b16efbc78de823592d2f3-25`)
- [C-eea3e31053f844f6] insufficient：E-ab3b16efbc78de823592d2f3-26 (`E-ab3b16efbc78de823592d2f3-26`)
- [C-439c5c84aa3f46d8] insufficient：E-b267b75ec4d3794f940d09e3-8 (`E-b267b75ec4d3794f940d09e3-8`)
- [C-98b45be19ec946fc] insufficient：E-b267b75ec4d3794f940d09e3-58 (`E-b267b75ec4d3794f940d09e3-58`)
- [C-9f416ad176c941ae] insufficient：E-843b7b896d15a8f4cbda875a-8 (`E-843b7b896d15a8f4cbda875a-8`)
- [C-91a47e1a02ea405d] insufficient：E-843b7b896d15a8f4cbda875a-41 (`E-843b7b896d15a8f4cbda875a-41`)
- [C-a67d26b015ec48f1] insufficient：E-843b7b896d15a8f4cbda875a-181 (`E-843b7b896d15a8f4cbda875a-181`)
- [C-9633f88cea8f4bc9] insufficient：E-843b7b896d15a8f4cbda875a-63 (`E-843b7b896d15a8f4cbda875a-63`)
- [C-bb458e01d19342b2] insufficient：E-ab3b16efbc78de823592d2f3-41 (`E-ab3b16efbc78de823592d2f3-41`)
- [C-ff8259bce03e4990] insufficient：E-ab3b16efbc78de823592d2f3-41 (`E-ab3b16efbc78de823592d2f3-41`)
- [C-5a6d882803aa48fc] insufficient：E-ab3b16efbc78de823592d2f3-41 (`E-ab3b16efbc78de823592d2f3-41`)
- [C-47f3fd9083b04c77] insufficient：E-8803ce8416a23a4342534df5-5 (`E-8803ce8416a23a4342534df5-5`)
- [C-8a5ffd0630f24657] insufficient：E-8803ce8416a23a4342534df5-5 (`E-8803ce8416a23a4342534df5-5`)
- [C-451b1079adf24387] insufficient：E-8803ce8416a23a4342534df5-39 (`E-8803ce8416a23a4342534df5-39`)
- [C-c6239fec3b734cc4] insufficient：E-fc980e29af3008d24a8748b4-37 (`E-fc980e29af3008d24a8748b4-37`)
- [C-b6a6446828774706] insufficient：没有可定位的有效证据
- [C-5fa8b3d2f93f42a3] insufficient：没有可定位的有效证据
- [C-0ccb8245a5374c8e] insufficient：E-335072b8521330d1ace96332-27 (`E-335072b8521330d1ace96332-27`)
- [C-675e10b0e80849bb] insufficient：E-335072b8521330d1ace96332-24 (`E-335072b8521330d1ace96332-24`)
- [C-c0dc4d8673f947cb] insufficient：E-d10798c474463d88f6fd4c1e-27 (`E-d10798c474463d88f6fd4c1e-27`)
- [C-e55cfa5adb2b4313] insufficient：E-d10798c474463d88f6fd4c1e-32 (`E-d10798c474463d88f6fd4c1e-32`) E-d10798c474463d88f6fd4c1e-33 (`E-d10798c474463d88f6fd4c1e-33`) E-d10798c474463d88f6fd4c1e-34 (`E-d10798c474463d88f6fd4c1e-34`)
- [C-e78811f76d594f58] insufficient：E-4c0a76670299da1d62023759-64 (`E-4c0a76670299da1d62023759-64`)
- [C-787898ff99cc479a] insufficient：E-22a0a13707908966fd68a23e-21 (`E-22a0a13707908966fd68a23e-21`)
- [C-8aa12bcc523c4edc] insufficient：E-12ff100d35ab6b9f848cb9d5-23 (`E-12ff100d35ab6b9f848cb9d5-23`)
- [C-8ba4caba8cb9453e] insufficient：E-f263dfe8d294d8f51ac22a40-37 (`E-f263dfe8d294d8f51ac22a40-37`)
- [C-f1ae976886b84090] insufficient：E-f263dfe8d294d8f51ac22a40-92 (`E-f263dfe8d294d8f51ac22a40-92`)
- [C-4c44be5867f24cdc] insufficient：E-aea21ef1d35dc105c11f1029-21 (`E-aea21ef1d35dc105c11f1029-21`)
- [C-78ba027152e64af5] insufficient：E-4187c264f9628ee144647da9-40 (`E-4187c264f9628ee144647da9-40`)
- [C-72ab90fb04ea41ee] insufficient：没有可定位的有效证据
- [C-ac9ff3a4fdb5484b] insufficient：E-ab3b16efbc78de823592d2f3-45 (`E-ab3b16efbc78de823592d2f3-45`)
- [C-7ab2c921923d44b7] insufficient：E-ab3b16efbc78de823592d2f3-45 (`E-ab3b16efbc78de823592d2f3-45`)
- [C-bbd83d3267af4d07] insufficient：E-ab3b16efbc78de823592d2f3-36 (`E-ab3b16efbc78de823592d2f3-36`)
- [C-163bf618e96847b1] insufficient：E-843b7b896d15a8f4cbda875a-8 (`E-843b7b896d15a8f4cbda875a-8`)
- [C-f01ab55c485a4476] insufficient：E-843b7b896d15a8f4cbda875a-64 (`E-843b7b896d15a8f4cbda875a-64`)
- [C-7e9738b4ab534801] insufficient：E-335072b8521330d1ace96332-27 (`E-335072b8521330d1ace96332-27`)
- [C-58cb6fd1fecf4140] insufficient：E-335072b8521330d1ace96332-29 (`E-335072b8521330d1ace96332-29`)
- [C-16102b6e5abc42ab] insufficient：E-f263dfe8d294d8f51ac22a40-31 (`E-f263dfe8d294d8f51ac22a40-31`)
- [C-e379dc580bfe4c47] insufficient：E-f263dfe8d294d8f51ac22a40-32 (`E-f263dfe8d294d8f51ac22a40-32`)
- [C-ef92bbb6b9fb4ac4] insufficient：E-4c0a76670299da1d62023759-35 (`E-4c0a76670299da1d62023759-35`)
- [C-b50276bb0681433b] insufficient：E-d10798c474463d88f6fd4c1e-33 (`E-d10798c474463d88f6fd4c1e-33`)
- [C-e236c3b7ea1d48c4] insufficient：E-d10798c474463d88f6fd4c1e-32 (`E-d10798c474463d88f6fd4c1e-32`)
- [C-80f831d718ec4f46] insufficient：E-d10798c474463d88f6fd4c1e-34 (`E-d10798c474463d88f6fd4c1e-34`)
- [C-4fc377a559bb453e] insufficient：E-87efa24ff3fbc99443566ee3-26 (`E-87efa24ff3fbc99443566ee3-26`)
- [C-bbe3fd59fed94152] insufficient：E-87efa24ff3fbc99443566ee3-26 (`E-87efa24ff3fbc99443566ee3-26`)
- [C-5ab6fc918eb84081] insufficient：E-d10798c474463d88f6fd4c1e-27 (`E-d10798c474463d88f6fd4c1e-27`)
- [C-004b8a21a9a047f5] insufficient：E-d10798c474463d88f6fd4c1e-28 (`E-d10798c474463d88f6fd4c1e-28`)
- [C-83feac7fd08e4693] insufficient：E-d10798c474463d88f6fd4c1e-28 (`E-d10798c474463d88f6fd4c1e-28`)
- [C-75be8772e3eb4091] insufficient：E-d10798c474463d88f6fd4c1e-42 (`E-d10798c474463d88f6fd4c1e-42`)

## 来源与时间

- Filtering Explained Milvus v2.5.x documentation · official · 已读取原文 · 抓取 2026-09-21T08:56:40.523100+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/v2.5.x/boolean.md
- Generating Milvus Query Filter Expressions with Large Language Models \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T08:56:36.806596+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/generating_milvus_query_filter_expressions.md
- Overview of Milvus Deployment Options \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T08:56:29.346701+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/install-overview.md
- What is Milvus Milvus v2.4.x documentation · official · 已读取原文 · 抓取 2026-09-21T08:56:58.631713+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/v2.4.x/overview.md
- Run Milvus in Docker (Linux) \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T08:56:34.195245+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/install_standalone-docker.md
- Back up and Restore Data Using Commands \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T08:56:52.397954+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/milvus_backup_cli.md
- AI Embedding存储检索-PGVector-云原生数据库 PolarDB-阿里云 · third_party · 已读取原文 · 抓取 2026-09-21T08:56:55.164987+00:00 · 发布 2023-06-29T11:05:32+08:00 · 文档版本 未知 · https://help.aliyun.com/zh/polardb/polardb-for-postgresql/pgvector
- Distributed Deployment - Qdrant · official · 已读取原文 · 抓取 2026-09-21T08:56:16.342844+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/scaling/distributed_deployment
- Product FAQ \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T08:57:02.212868+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/product_faq.md
- Azure Database for PostgreSQL 灵活服务器中的向量搜索 - Azure Database for PostgreSQL \| Microsoft Learn · third_party · 已读取原文 · 抓取 2026-09-21T08:56:48.378638+00:00 · 发布 未知 · 文档版本 未知 · https://learn.microsoft.com/zh-cn/azure/postgresql/extensions/how-to-use-pgvector
- pgvector 向量扩展使用指南 · third_party · 已读取原文 · 抓取 2026-09-21T08:57:01.544048+00:00 · 发布 未知 · 文档版本 未知 · https://intl.cloud.tencent.com/zh/document/product/409/80360
- Installation - Qdrant · official · 已读取原文 · 抓取 2026-09-21T08:56:11.939662+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/installation
- Scale a Milvus Cluster \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T08:56:49.612510+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/scaleout.md
- Local Quickstart - Qdrant · official · 已读取原文 · 抓取 2026-09-21T08:56:21.627608+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.tech/documentation/quickstart
- Requirements for Installing Milvus Standalone \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T08:56:31.799201+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/prerequisite-docker.md
- What is Milvus \| Milvus Documentation · official · 已读取原文 · 抓取 2026-09-21T08:56:55.867726+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/overview.md
- pgvector实现高维向量检索 - 云数据库 RDS - 阿里云 · third_party · 已读取原文 · 抓取 2026-09-21T08:56:53.900228+00:00 · 发布 未知 · 文档版本 未知 · https://www.alibabacloud.com/help/zh/rds/apsaradb-rds-for-postgresql/pgvector-use-guide
- Turning PostgreSQL Into a Vector Database With pgvector \| Tiger Data · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:58:38.911966+00:00 · 发布 未知 · 文档版本 未知 · https://www.tigerdata.com/learn/postgresql-extensions-pgvector
- 在 GKE 上部署 Qdrant 向量数据库  \|  Kubernetes Engine  \|  Google Cloud Documentation · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:09.489045+00:00 · 发布 未知 · 文档版本 未知 · https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/deploy-qdrant?hl=zh-cn
- Nuwellis获得儿科血液过滤安全技术专利 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:18.508206+00:00 · 发布 未知 · 文档版本 未知 · https://cn.investing.com/news/company-news/article-93CH-3074056
- 在GKE 上部署PostgreSQL 矢量数据库\| Kubernetes Engine · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:20.373755+00:00 · 发布 未知 · 文档版本 未知 · https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/deploy-pgvector?hl=zh-cn
- Filter Templating \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:18.580131+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/filtering-templating.md
- 概述 - Qdrant - Qdrant 向量数据库 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:09.467737+00:00 · 发布 未知 · 文档版本 未知 · https://qdrant.org.cn/documentation/overview
- Milvus 和PGVector，哪个更好？ - 腾讯云开发者社区- Tencent · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:20.337365+00:00 · 发布 未知 · 文档版本 未知 · https://developer.cloud.tencent.com/article/2658089
- MongoDB性能系列最佳实践-分片 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:22.439274+00:00 · 发布 未知 · 文档版本 未知 · https://www.mongodb.com/blog/post/performance-best-practices-series-sharding-cn
- 放弃pgvector，Milvus 才是海量非结构化数据自动分片最优解 - Zilliz 向量数据库 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:22.330370+00:00 · 发布 未知 · 文档版本 未知 · https://zilliz.com.cn/blog/Milvus-Best-Sharding-for-Unstructured
- Walter Fan's Blog – 用 pgvector 做 RAG：别急着上 Pinecone，你的 PostgreSQL 就够了 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:13.035363+00:00 · 发布 未知 · 文档版本 未知 · https://www.fanyamin.com/2026-03-10-pgvector-rag.html
- PostgreSQL pgvector: Getting Started and Scaling · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:13.044425+00:00 · 发布 未知 · 文档版本 未知 · https://www.yugabyte.com/blog/postgresql-pgvector-getting-started
- pgvector (PostgreSQL Vector Extension) \| Genkit · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:14.583427+00:00 · 发布 未知 · 文档版本 未知 · https://genkit.dev/docs/go/integrations/pgvector
- LiqTech 2025年商用泳池过滤系统销售创历史新高 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:18.516782+00:00 · 发布 未知 · 文档版本 未知 · https://cn.investing.com/news/company-news/article-93CH-3163504
- PGvector :: Spring AI Reference · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:58:36.127639+00:00 · 发布 未知 · 文档版本 未知 · https://docs.spring.io/spring-ai/reference/api/vectordbs/pgvector.html
- Storing Vector Easily with pgvector Extension by PostgreSQL · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:58:38.904054+00:00 · 发布 未知 · 文档版本 未知 · https://medium.com/edts/storing-vector-easily-with-pgvector-extension-by-postgresql-63418acc9802
- The pgvector extension - Neon Docs · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:58:38.896492+00:00 · 发布 未知 · 文档版本 未知 · https://neon.com/docs/extensions/pgvector
- pgvector/README.md at master - GitHub · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:14.543372+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/pgvector/pgvector/blob/master/README.md
- GitHub - aws-samples/aurora-postgresql-pgvector: Agentic AI Use Cases with pgvector, Aurora PostgreSQL and Amazon Bedrock · GitHub · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:14.566203+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/aws-samples/aurora-postgresql-pgvector
- Pgvector Extension – CedarDB Documentation · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:58:38.885258+00:00 · 发布 未知 · 文档版本 未知 · https://cedardb.com/docs/references/advanced/pgvector
- Milvus与自建Milvus对比-向量检索服务 Milvus 版(Milvus)-阿里云帮助中心 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:20.161458+00:00 · 发布 未知 · 文档版本 未知 · https://help.aliyun.com/zh/milvus/product-overview/comparison-between-alibaba-cloud-milvus-and-ecs-self-built-milvus
- 快速入门\| Milvus 文档 · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:15.090184+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/quickstart.md
- MongoDB性能系列最佳实践-分片 \| MongoDB Blog · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:22.365577+00:00 · 发布 未知 · 文档版本 未知 · https://www.mongodb.com/blog/post/performance-best-practices-series-sharding-cn
- All You Need to Know about PGVector \| Part 3 — Metadata Filtering · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:18.478164+00:00 · 发布 未知 · 文档版本 未知 · https://medium.com/@aysebilgegunduz/all-you-need-to-know-about-pgvector-part-3-metadata-filtering-531725da83db
- 数据分片 :: ShardingSphere · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:22.348044+00:00 · 发布 未知 · 文档版本 未知 · https://shardingsphere.apache.org/document/5.1.1/cn/features/sharding
- pgvector-python/README.md at master · pgvector/pgvector-python · GitHub · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:14.558675+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/pgvector/pgvector-python/blob/master/README.md
- Understanding pgvector: Optimizing Your Vector Database · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:58:38.919749+00:00 · 发布 未知 · 文档版本 未知 · https://www.enterprisedb.com/blog/what-is-pgvector
- Everything you need to know about pgvector \| Blog · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:58:36.150126+00:00 · 发布 未知 · 文档版本 未知 · https://northflank.com/blog/postgresql-vector-search-guide-with-pgvector
- How does the IVF-FLAT index search work when "where" clause is provided in SQL query? · Issue #301 · pgvector/pgvector · GitHub · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:18.496768+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/pgvector/pgvector/issues/301
- 放弃pgvector，Milvus 才是海量非结构化数据自动分片最优解 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:22.412427+00:00 · 发布 未知 · 文档版本 未知 · https://zilliz.com.cn/blog/Milvus-Best-Sharding-for-Unstructured
- Scalar Filtering Rules \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:18.597524+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/boolean.md
- Gate for AI 再升级：一键安装、对话即可授权，CEX MCP 工具扩展至 161 项 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:22.448377+00:00 · 发布 未知 · 文档版本 未知 · https://cryptorank.io/zh/news/feed/39581-2251170
- Query \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:18.589417+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/get-and-scalar-query.md
- Milvus, a highly performant distributed vector database for AI apps · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:15.097800+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/zh/intro
- pgvector/pgvector: Open-source vector similarity search for ... · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:58:36.135129+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/pgvector/pgvector
- Rubrik为Okta用户推出身份恢复解决方案 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:20.193474+00:00 · 发布 未知 · 文档版本 未知 · https://cn.investing.com/news/company-news/article-93CH-2999186
- milvus/README_CN.md at master · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:15.072972+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/milvus-io/milvus/blob/master/README_CN.md
- Run Milvus Lite Locally \| Milvus Documentation · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:12.980050+00:00 · 发布 未知 · 文档版本 未知 · https://milvus.io/docs/zh/milvus_lite.md
- 十倍成本优化，Milvus 2.5到2.6升级官方手把手教程 - Zilliz 向量数据库 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:15.081548+00:00 · 发布 未知 · 文档版本 未知 · https://zilliz.com.cn/blog/Milvus-2.5-to-2.6-tenfold-cost-optimization-guide
- GitHub - pgvector/pgvector-r: pgvector examples for R · GitHub · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:14.574865+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/pgvector/pgvector-r
- Milvus 深度解析：开源向量数据库的技术架构、实践指南与生态生态-腾讯云开发者社区-腾讯云 · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T08:56:15.063873+00:00 · 发布 未知 · 文档版本 未知 · https://developer.cloud.tencent.com/article/2617781