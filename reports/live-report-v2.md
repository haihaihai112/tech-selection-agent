> 历史报告导出 / Historical report export. 原运行的证据 ID 保留为文本；旧会话数据库不随源码发布，ID 不能在新实例直接恢复。Evidence IDs refer to the original run, whose session database is not distributed.

# 技术选型研究报告 · 第 2 版

**基于本次抓取资料；模型语义核验不等同于独立事实审计。**

## 用户条件

- 部署方式：本地自托管部署
- 偏好：维护成本最低优先
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
- [C-1dbacb497ec844ae] pgvector：pgvector 扩展将开源向量相似性搜索添加到 PostgreSQL。；语义核验未完成：APITimeoutError
- [C-0dc55ad533ff432c] pgvector：PostgreSQL 11 （内核小版本 2.0.11.9.35.0 及以上）；语义核验未完成：APITimeoutError
- [C-da6d3a03d44243ad] pgvector：实例大版本为PostgreSQL 14或以上。；语义核验未完成：APITimeoutError
- [C-7d9e07792bf24f21] pgvector：PostgreSQL 17 （内核小版本 2.0.17.2.1.0 及以上）；语义核验未完成：APITimeoutError
- [C-ffc1ef2a23644179] pgvector：若要检索向量并计算相似性，请使用 SELECT 语句和内置向量运算符。 例如，查询会计算给定矢量与存储在 tblvector 表中的矢量之间的欧几里得距离（L2 距离）；语义核验未完成：APITimeoutError
- [C-3b5934caa0264ec9] pgvector：-- 余弦相似度搜索（最常用） SELECT id , content , 1 - ( embedding &lt;=&gt; query_vec ) AS similarity FROM documents ORDER BY embedding &lt;=&gt; query_vec LIMIT 10 ;；语义核验未完成：APITimeoutError
- [C-c3ec5fbeb6114672] pgvector：创建HNSW索引 CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);；语义核验未完成：APITimeoutError
- [C-b21dfcf8894944c4] pgvector：CREATE INDEX ON vecs USING ivfflat(embedding) WITH (lists=100);；语义核验未完成：APITimeoutError
- [C-6a1cff9ab8784c9f] pgvector：更新插件 ALTER EXTENSION vector UPDATE \[ TO new_version \]；语义核验未完成：APITimeoutError
- [C-482ca42e3a5343cb] pgvector：PGVector 插件的实现基于 PolarDB PostgreSQL 版 的扩展机制，利用 C 语言编写实现多种向量计算算法和数据类型。；语义核验未完成：APITimeoutError
- [C-34b13b4d45134d4e] pgvector：pgvector提供vector数据类型，使RDS PostgreSQL数据库具备了存储向量数据的能力。；语义核验未完成：APITimeoutError
- [C-cf7b0420a7d74c80] pgvector：CREATE TABLE docs_sparse ( id BIGSERIAL PRIMARY KEY , embedding sparsevec ( 30000 ) ) ;；语义核验未完成：APITimeoutError
- [C-2f7380f6771b4050] Qdrant：If you want to run Qdrant in your own infrastructure, without any cloud connection, we recommend to install Qdrant in a Kubernetes cluster with our Qdrant Private Cloud Enterprise Operator.；语义核验未完成：APITimeoutError
- [C-5308d8a0e33b4b7f] Qdrant：If you want to run Qdrant in your own infrastructure, without any cloud connection, we recommend to install Qdrant in a Kubernetes cluster with our Qdrant Private Cloud Enterprise Operator.；语义核验未完成：APITimeoutError
- [C-8b21e20f690d45e6] Qdrant：You can use a ready-made Helm Chart to run Qdrant in your Kubernetes cluster. While it is possible to deploy Qdrant in a distributed setup with the Helm chart, it does not come with the same level of features for zero-downtime upgrades, up；语义核验未完成：APITimeoutError
- [C-421696df08244edf] Qdrant：However, you can also use Docker and Docker Compose to run Qdrant in production, by following the setup instructions in the Docker and Docker Compose Development sections.；语义核验未完成：APITimeoutError
- [C-f20931183ab94dae] Qdrant：6333 - For the HTTP API, for the Monitoring health and metrics endpoints；语义核验未完成：APITimeoutError
- [C-20754b1cc5dc4ceb] Qdrant：6334 - For the gRPC API；语义核验未完成：APITimeoutError
- [C-909d12189f93432a] Qdrant：p2p : # Port for internal communication between peers port : 6335；语义核验未完成：APITimeoutError
- [C-43d00b8f1d614820] Qdrant：from qdrant_client.models import Filter , FieldCondition , MatchValue search_result = client . query_points ( collection_name = "test_collection" , query = \[ 0.2 , 0.1 , 0.9 , 0.7 \], query_filter = Filter ( must = \[ FieldCondition ( key = "city" , match = MatchValue ( value = "London" ))\] ), with_payload = True , limit = 3 , ) . points print ( search_result )；语义核验未完成：APITimeoutError
- [C-19700559e1e44fbd] Qdrant：It provides horizontal and vertical scaling, one click installation and upgrades, monitoring, logging, as well as backup and disaster recovery.；语义核验未完成：APITimeoutError
- [C-2934a6e25d344d67] Qdrant：To enable distributed deployment - enable the cluster mode in the configuration or using the ENV variable: QDRANT__CLUSTER__ENABLED=true .；语义核验未完成：APITimeoutError
- [C-40ac751b3b664bb9] Qdrant：client . create_collection ( collection_name = " {collection_name} " , vectors_config = models . VectorParams ( size = 300 , distance = models . Distance . COSINE ), shard_number = 6 , )；语义核验未完成：APITimeoutError
- [C-c812e613e0194792] Qdrant：client . create_collection ( collection_name = " {collection_name} " , vectors_config = models . VectorParams ( size = 300 , distance = models . Distance . COSINE ), shard_number = 6 , replication_factor = 2 , )；语义核验未完成：APITimeoutError
- [C-c17471c416b446f5] Qdrant：Qdrant allows moving shards between nodes in the cluster and removing nodes from the cluster. This functionality unlocks the ability to dynamically scale the cluster size without downtime.；语义核验未完成：APITimeoutError
- [C-b0787f5efc144054] Qdrant：If your cluster is running in Qdrant Cloud, shards are rebalanced across the cluster nodes automatically on an ongoing basis.；语义核验未完成：APITimeoutError
- [C-55454606d8434e53] Milvus：Milvus Standalone is a single-machine server deployment. All components of Milvus Standalone are packed into a single Docker image, making deployment convenient.；语义核验未完成：APITimeoutError
- [C-8f03a5bd25f84133] Milvus：Milvus Lite is a Python library that can be imported into your applications. As a lightweight version of Milvus, it is ideal for quick prototyping in Jupyter Notebooks or running on smart devices with limited resources.；语义核验未完成：APITimeoutError
- [C-06f041b1e7f64447] Milvus：Milvus Standalone is a single-machine server deployment. All components of Milvus Standalone are packed into a single Docker image, making deployment convenient.；语义核验未完成：APITimeoutError
- [C-1224d9c9d3844def] Milvus：If you want to use Backup in standalone deployment mode, it is recommended to use the Docker Compose deployment method.；语义核验未完成：APITimeoutError
- [C-854514d53a744d52] Milvus：Milvus Distributed can be deployed on Kubernetes clusters. This deployment features a cloud-native architecture, where ingestion load and search queries are separately handled by isolated nodes, allowing redundancy for critical components.；语义核验未完成：APITimeoutError
- [C-176de1b90ba64971] Milvus：Milvus supports several basic operators for filtering data: Comparison Operators: == , \!= , &gt; , &lt; , &gt;= , and &lt;= allow filtering based on numeric or text fields. Range Filters: IN and LIKE help match specific value ranges or sets.；语义核验未完成：APITimeoutError
- [C-c687cd726c6a4d4d] Milvus：Milvus allows referencing keys in JSON fields. For instance, if you have a JSON field product with keys price and model, and want to find products with a specific model and price lower than 1,850, use this filter expression: filter = 'product\["model"\] == "JSN-087" AND product\["price"\] &lt; 1850'；语义核验未完成：APITimeoutError
- [C-65b30509a32f4e3e] Milvus：The TEXT_MATCH operator allows precise document retrieval based on specific query terms. It is particularly useful for filtered searches that combine scalar filters with vector similarity searches.；语义核验未完成：APITimeoutError
- [C-a85a414bd6844597] Milvus：You can either download the compiled binary or build from the source.；语义核验未完成：APITimeoutError
- [C-42c4bb49730f4b83] Milvus：Prometheus is an open-source system monitoring and alerting toolkit for Kubernetes. Grafana is an open-source visualizing stack that can connect with all data sources. You can use Promethus &amp; Grafana as the monitoring service provider to visually monitor the performance of Milvus distributed.；语义核验未完成：APITimeoutError
- [C-2f50ff2339f34354] Milvus：Scaling out refers to increasing the number of nodes in a cluster. Unlike scaling up, scaling out does not require you to allocate more resources to one node in the cluster. Instead, scaling out expands the cluster horizontally by adding more nodes.；语义核验未完成：APITimeoutError
- [C-415fffc582a44548] Milvus：According to the Milvus architecture, stateless worker nodes include query node, data node, index node, and proxy. Therefore, you can scale out these type of nodes to suit your business needs and application scenarios.；语义核验未完成：APITimeoutError
- [C-890f182cc1a640b9] Milvus：Woodpecker Bundled with Milvus Default message queue (embedded); no separate service to install.；语义核验未完成：APITimeoutError
- [C-dbb5c1211c1d4513] Milvus：By default this deployment runs Woodpecker (local-filesystem WAL) as the message queue and an embedded etcd for metadata — nothing else to install.；语义核验未完成：APITimeoutError
- [C-b6caa5be0be24fa4] Milvus：Comparison Operators: == , \!= , &gt; , &lt; , &gt;= , and &lt;= allow filtering based on numeric or text fields. Range Filters: IN and LIKE help match specific value ranges or sets.；语义核验未完成：APITimeoutError
- [C-21ba1616af2e4494] Milvus：If you want to use Backup in standalone deployment mode, it is recommended to use the Docker Compose deployment method.；语义核验未完成：APITimeoutError
- [C-c958e7bf4c054868] Milvus：You can use Promethus &amp; Grafana as the monitoring service provider to visually monitor the performance of Milvus distributed.；语义核验未完成：APITimeoutError
- [C-a2edb04a46d04079] Milvus：Milvus Distributed can be deployed on Kubernetes clusters, featuring a cloud-native architecture designed for billion-scale or even larger scenarios.；语义核验未完成：APITimeoutError
- [C-5e1192704d3d4e62] Qdrant：from qdrant_client import QdrantClient , models client . create_collection ( collection_name = " {collection_name} " , vectors_config = models . VectorParams ( size = 300 , distance = models . Distance . COSINE ), shard_number = 6 , )；语义核验未完成：APITimeoutError
- [C-ad4f0ff5ab1c4dd3] Qdrant：import ( "context" "fmt" "github.com/qdrant/go-client/qdrant" ) searchResult , err := client . Query ( context . Background (), &amp; qdrant . QueryPoints { CollectionName : "test_collection" , Query : qdrant . NewQuery ( 0.2 , 0.1 , 0.9 , 0.7 ), Filter : &amp; qdrant . Filter { Must : \[\] \* qdrant . Condition { qdrant . NewMatch ( "city" , "London" ), }, }, WithPayload : qdrant . NewWithPayload ( true ), }) if err \!= nil { panic ( err ) } fmt . Println ( searchResult )；语义核验未完成：APITimeoutError
- [C-b45edfaa27634fd1] Qdrant：search_result = client . query_points ( collection_name = "test_collection" , query = \[ 0.2 , 0.1 , 0.9 , 0.7 \], with_payload = False , limit = 3 ) . points print ( search_result )；语义核验未完成：APITimeoutError
- [C-1c208415b8844932] Qdrant：It provides horizontal and vertical scaling, one click installation and upgrades, monitoring, logging, as well as backup and disaster recovery.；语义核验未完成：APITimeoutError
- [C-de381e74c3504f03] Qdrant：from qdrant_client import QdrantClient , models client . create_collection ( collection_name = " {collection_name} " , vectors_config = models . VectorParams ( size = 300 , distance = models . Distance . COSINE ), shard_number = 6 , )；语义核验未完成：APITimeoutError
- [C-a9f2a245d5624c7b] Qdrant：from qdrant_client import QdrantClient , models client . create_collection ( collection_name = " {collection_name} " , vectors_config = models . VectorParams ( size = 300 , distance = models . Distance . COSINE ), shard_number = 6 , replication_factor = 2 , )；语义核验未完成：APITimeoutError
- [C-c4341adda97648cd] pgvector：You can self-host PgVector by deploying a PostgreSQL instance on Railway and enabling the PgVector extension-no manual setup required.；语义核验未完成：APITimeoutError
- [C-02b43d687e8b48a7] pgvector：pgvector 扩展将开源向量相似性搜索添加到 PostgreSQL。；语义核验未完成：APITimeoutError
- [C-d569e57f255c4eff] pgvector：-- L2 距离搜索 SELECT id , content FROM documents ORDER BY embedding &lt; - &gt; query_vec LIMIT 10 ;；语义核验未完成：APITimeoutError
- [C-6cad85a42790460b] pgvector：CREATE INDEX ON documents USING hnsw ( embedding vector_cosine_ops ) WITH ( m = 16 , ef_construction = 200 ) ;；语义核验未完成：APITimeoutError
- [C-d113cb6ba7044852] pgvector：CREATE EXTENSION vector;；语义核验未完成：APITimeoutError
- [C-6458b540376a4ef6] pgvector：-- 需要先有数据才能创建 CREATE INDEX ON documents USING ivfflat ( embedding vector_cosine_ops ) WITH ( lists = 100 ) ; -- lists 建议 = sqrt(行数)；语义核验未完成：APITimeoutError
- [C-cf757e087b8248a6] Milvus：Milvus provides powerful filtering capabilities that enable precise querying of your data. Filter expressions allow you to target specific scalar fields and refine search results with different conditions.；
- [C-7cdc07dd16074ab1] Milvus：Milvus itself is fully stateless so it can be easily scaled with the help of Kubernetes or public clouds. In addition, Milvus components are well decoupled, with the three most critical tasks—search, data insertion, and indexing/compaction—designed as easily parallelized processes, with complex logic separated out.；

## 结论与原文证据

- [C-1dbacb497ec844ae] insufficient：E-8803ce8416a23a4342534df5-5 (`E-8803ce8416a23a4342534df5-5`)
- [C-0dc55ad533ff432c] insufficient：E-5bccb24843595d3f2079e052-10 (`E-5bccb24843595d3f2079e052-10`)
- [C-da6d3a03d44243ad] insufficient：E-fc980e29af3008d24a8748b4-31 (`E-fc980e29af3008d24a8748b4-31`)
- [C-7d9e07792bf24f21] insufficient：E-5bccb24843595d3f2079e052-6 (`E-5bccb24843595d3f2079e052-6`)
- [C-ffc1ef2a23644179] insufficient：E-8803ce8416a23a4342534df5-36 (`E-8803ce8416a23a4342534df5-36`)
- [C-3b5934caa0264ec9] insufficient：E-8bc1a6a388ed37432ba24012-45 (`E-8bc1a6a388ed37432ba24012-45`)
- [C-c3ec5fbeb6114672] insufficient：E-fc980e29af3008d24a8748b4-67 (`E-fc980e29af3008d24a8748b4-67`)
- [C-b21dfcf8894944c4] insufficient：E-5bccb24843595d3f2079e052-26 (`E-5bccb24843595d3f2079e052-26`)
- [C-6a1cff9ab8784c9f] insufficient：E-fc980e29af3008d24a8748b4-42 (`E-fc980e29af3008d24a8748b4-42`)
- [C-482ca42e3a5343cb] insufficient：E-5bccb24843595d3f2079e052-18 (`E-5bccb24843595d3f2079e052-18`)
- [C-34b13b4d45134d4e] insufficient：E-fc980e29af3008d24a8748b4-17 (`E-fc980e29af3008d24a8748b4-17`)
- [C-cf7b0420a7d74c80] insufficient：E-8bc1a6a388ed37432ba24012-38 (`E-8bc1a6a388ed37432ba24012-38`)
- [C-2f7380f6771b4050] insufficient：E-ab3b16efbc78de823592d2f3-36 (`E-ab3b16efbc78de823592d2f3-36`)
- [C-5308d8a0e33b4b7f] insufficient：E-ab3b16efbc78de823592d2f3-36 (`E-ab3b16efbc78de823592d2f3-36`)
- [C-8b21e20f690d45e6] insufficient：E-ab3b16efbc78de823592d2f3-45 (`E-ab3b16efbc78de823592d2f3-45`)
- [C-421696df08244edf] insufficient：E-ab3b16efbc78de823592d2f3-71 (`E-ab3b16efbc78de823592d2f3-71`)
- [C-f20931183ab94dae] insufficient：E-ab3b16efbc78de823592d2f3-25 (`E-ab3b16efbc78de823592d2f3-25`)
- [C-20754b1cc5dc4ceb] insufficient：E-ab3b16efbc78de823592d2f3-26 (`E-ab3b16efbc78de823592d2f3-26`)
- [C-909d12189f93432a] insufficient：E-843b7b896d15a8f4cbda875a-9 (`E-843b7b896d15a8f4cbda875a-9`)
- [C-43d00b8f1d614820] insufficient：E-b267b75ec4d3794f940d09e3-58 (`E-b267b75ec4d3794f940d09e3-58`)
- [C-19700559e1e44fbd] insufficient：E-ab3b16efbc78de823592d2f3-41 (`E-ab3b16efbc78de823592d2f3-41`)
- [C-2934a6e25d344d67] insufficient：E-843b7b896d15a8f4cbda875a-8 (`E-843b7b896d15a8f4cbda875a-8`)
- [C-40ac751b3b664bb9] insufficient：E-843b7b896d15a8f4cbda875a-41 (`E-843b7b896d15a8f4cbda875a-41`)
- [C-c812e613e0194792] insufficient：E-843b7b896d15a8f4cbda875a-181 (`E-843b7b896d15a8f4cbda875a-181`)
- [C-c17471c416b446f5] insufficient：E-843b7b896d15a8f4cbda875a-63 (`E-843b7b896d15a8f4cbda875a-63`)
- [C-b0787f5efc144054] insufficient：E-843b7b896d15a8f4cbda875a-64 (`E-843b7b896d15a8f4cbda875a-64`)
- [C-55454606d8434e53] insufficient：E-335072b8521330d1ace96332-27 (`E-335072b8521330d1ace96332-27`)
- [C-8f03a5bd25f84133] insufficient：E-335072b8521330d1ace96332-24 (`E-335072b8521330d1ace96332-24`)
- [C-06f041b1e7f64447] insufficient：E-335072b8521330d1ace96332-27 (`E-335072b8521330d1ace96332-27`)
- [C-1224d9c9d3844def] insufficient：E-4c0a76670299da1d62023759-35 (`E-4c0a76670299da1d62023759-35`)
- [C-854514d53a744d52] insufficient：E-335072b8521330d1ace96332-29 (`E-335072b8521330d1ace96332-29`)
- [C-176de1b90ba64971] insufficient：E-12ff100d35ab6b9f848cb9d5-26 (`E-12ff100d35ab6b9f848cb9d5-26`) E-12ff100d35ab6b9f848cb9d5-27 (`E-12ff100d35ab6b9f848cb9d5-27`)
- [C-c687cd726c6a4d4d] insufficient：E-12ff100d35ab6b9f848cb9d5-34 (`E-12ff100d35ab6b9f848cb9d5-34`) E-12ff100d35ab6b9f848cb9d5-35 (`E-12ff100d35ab6b9f848cb9d5-35`)
- [C-65b30509a32f4e3e] insufficient：E-12ff100d35ab6b9f848cb9d5-75 (`E-12ff100d35ab6b9f848cb9d5-75`)
- [C-a85a414bd6844597] insufficient：E-548cffa809b36d10ad17f977-24 (`E-548cffa809b36d10ad17f977-24`)
- [C-42c4bb49730f4b83] insufficient：E-f263dfe8d294d8f51ac22a40-92 (`E-f263dfe8d294d8f51ac22a40-92`)
- [C-2f50ff2339f34354] insufficient：E-aea21ef1d35dc105c11f1029-29 (`E-aea21ef1d35dc105c11f1029-29`)
- [C-415fffc582a44548] insufficient：E-aea21ef1d35dc105c11f1029-32 (`E-aea21ef1d35dc105c11f1029-32`)
- [C-890f182cc1a640b9] insufficient：E-d10798c474463d88f6fd4c1e-39 (`E-d10798c474463d88f6fd4c1e-39`)
- [C-dbb5c1211c1d4513] insufficient：E-4c0a76670299da1d62023759-64 (`E-4c0a76670299da1d62023759-64`)
- [C-b6caa5be0be24fa4] insufficient：E-12ff100d35ab6b9f848cb9d5-26 (`E-12ff100d35ab6b9f848cb9d5-26`) E-12ff100d35ab6b9f848cb9d5-27 (`E-12ff100d35ab6b9f848cb9d5-27`)
- [C-21ba1616af2e4494] insufficient：E-4c0a76670299da1d62023759-35 (`E-4c0a76670299da1d62023759-35`)
- [C-c958e7bf4c054868] insufficient：E-f263dfe8d294d8f51ac22a40-92 (`E-f263dfe8d294d8f51ac22a40-92`)
- [C-a2edb04a46d04079] insufficient：E-f263dfe8d294d8f51ac22a40-32 (`E-f263dfe8d294d8f51ac22a40-32`)
- [C-5e1192704d3d4e62] insufficient：E-843b7b896d15a8f4cbda875a-41 (`E-843b7b896d15a8f4cbda875a-41`)
- [C-ad4f0ff5ab1c4dd3] insufficient：E-b267b75ec4d3794f940d09e3-63 (`E-b267b75ec4d3794f940d09e3-63`)
- [C-b45edfaa27634fd1] insufficient：E-b267b75ec4d3794f940d09e3-46 (`E-b267b75ec4d3794f940d09e3-46`)
- [C-1c208415b8844932] insufficient：E-ab3b16efbc78de823592d2f3-41 (`E-ab3b16efbc78de823592d2f3-41`)
- [C-de381e74c3504f03] insufficient：E-843b7b896d15a8f4cbda875a-41 (`E-843b7b896d15a8f4cbda875a-41`)
- [C-a9f2a245d5624c7b] insufficient：E-843b7b896d15a8f4cbda875a-181 (`E-843b7b896d15a8f4cbda875a-181`)
- [C-c4341adda97648cd] insufficient：E-8803ce8416a23a4342534df5-4 (`E-8803ce8416a23a4342534df5-4`)
- [C-02b43d687e8b48a7] insufficient：E-8803ce8416a23a4342534df5-5 (`E-8803ce8416a23a4342534df5-5`)
- [C-d569e57f255c4eff] insufficient：E-8bc1a6a388ed37432ba24012-45 (`E-8bc1a6a388ed37432ba24012-45`)
- [C-6cad85a42790460b] insufficient：E-8bc1a6a388ed37432ba24012-48 (`E-8bc1a6a388ed37432ba24012-48`)
- [C-d113cb6ba7044852] insufficient：E-5bccb24843595d3f2079e052-29 (`E-5bccb24843595d3f2079e052-29`)
- [C-6458b540376a4ef6] insufficient：E-8bc1a6a388ed37432ba24012-54 (`E-8bc1a6a388ed37432ba24012-54`)
- [C-cf757e087b8248a6] insufficient：E-12ff100d35ab6b9f848cb9d5-23 (`E-12ff100d35ab6b9f848cb9d5-23`)
- [C-7cdc07dd16074ab1] insufficient：E-f263dfe8d294d8f51ac22a40-43 (`E-f263dfe8d294d8f51ac22a40-43`)

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
- Turning PostgreSQL Into a Vector Database With pgvector \| Tiger Data · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:02:39.613740+00:00 · 发布 未知 · 文档版本 未知 · https://www.tigerdata.com/learn/postgresql-extensions-pgvector
- Deploy &amp; Host PgVector \[Updated Sep '26\] · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:02:39.633646+00:00 · 发布 未知 · 文档版本 未知 · https://railway.com/deploy/pgvector-updated-sep-26--pgvector-latest
- Installing PostgreSQL + pgvector on Debian - DEV Community · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:02:39.653400+00:00 · 发布 未知 · 文档版本 未知 · https://dev.to/farez/installing-postgresql-pgvector-on-debian-fcf
- Deployment Options - Greptile · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:02:14.466466+00:00 · 发布 未知 · 文档版本 未知 · https://greptile.com/docs/deployment-options
- Deploy a PostgreSQL vector database on GKE · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:02:14.475562+00:00 · 发布 未知 · 文档版本 未知 · https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/deploy-pgvector
- Build a Self-Hosted RAG with Postgres pgvector: 2026 Guide · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:02:39.626043+00:00 · 发布 未知 · 文档版本 未知 · https://www.digitalapplied.com/blog/build-self-hosted-rag-postgres-pgvector-tutorial-2026
- pgvector/pgvector: Open-source vector similarity search for ... · official · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:02:39.642177+00:00 · 发布 未知 · 文档版本 未知 · https://github.com/pgvector/pgvector
- Deployment Options - Greptile · third_party · 仅搜索摘要，不能支持确定性事实 · 抓取 2026-09-21T09:02:14.457930+00:00 · 发布 未知 · 文档版本 未知 · https://www.greptile.com/docs/deployment-options