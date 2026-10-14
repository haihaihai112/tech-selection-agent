# 接口、数据与恢复语义

## API

|接口|输入与结果|
|---|---|
|POST /v1/research|query、group、可选session_id、allow_unknown、force_refresh、requested_versions；202返回id/session_id/report_id/status|
|GET /v1/tasks/{id}|状态、条件、追问、调用记录、用量、报告版本、错误与检查点|
|POST /v1/tasks/{id}/answers|answer、allow_unknown；沿用原任务，只有input_required可继续|
|POST /v1/tasks/{id}/cancel|取消排队、执行中或等待输入任务；保留已有记录|
|GET /v1/reports/{id}?version=N|省略version取最新版；明确版本读取历史不可变报告|
|POST /v1/reports/{id}/revisions|base_version、query及刷新/未知/版本选项；基础版本过期返回409|
|GET /v1/evidence/{id}|证据片段、快照元信息及已保存全文；不接受任意文件路径|
|GET /v1/reports/{id}/export?version=N|下载指定版本Markdown|
|GET /v1/catalog|三个产品组、维度与默认澄清条件|
|POST /v1/projects|根据目标生成候选技术层；候选仍需研究核验|
|GET /v1/projects/{id}|读取项目目标、候选层及项目状态|
|POST /v1/projects/{id}/layers/{layer}/research|显式启动一个候选层研究，返回任务编号|
|POST /v1/projects/{id}/confirm|引用已发布报告版本，确认选择并生成不可变项目架构版本|
|GET /v1/projects/{id}/architecture?version=N|读取指定项目架构版本的结构化图、Mermaid 和 SVG|
|GET /v1/tasks/{id}/flowchart|返回任务研究流程图的结构化节点、边和 Mermaid 文本；不启动任务|
|GET /health|配置是否齐备；不将配置存在声称为上游连通|

`GET /v1/reports/{id}/flowchart?version=N` 返回指定不可变报告版本对应的研究流程图。流程图状态保留任务的 `completed`、`partial`、`failed`、`input_required` 等语义；Mermaid 颜色只是一层展示映射。首版不调用 ComfyUI/API，也不把推荐产品当作用户已确认的架构组件。

状态为 queued、working、input_required、completed、partial、failed、canceled、interrupted。completed只表示本次报告已生成且比较维度没有结构化缺口，不保证现实事实正确。partial可能生成带缺口报告；failed保留任务证据与轨迹但不发布本次报告。

同一会话不允许两个运行中任务，返回409；不同会话可以并行。等待补充问题可重启继续；执行中任务重启标为interrupted，不能静默重跑付费调用。检查点保存每阶段可观察业务状态，不包含模型思维链，也不承诺恢复未完成的模型请求。

## 证据与判断

ResearchBrief保存条件、偏好、未知项与显式版本要求。SourceSnapshot保存来源、抓取时间、发布时间（不可识别时为null）、文档版本、内容哈希、快照文件名、资料类型和重复关系。EvidenceSpan以稳定ID定位该快照的段落。数据仅在当前会话和当前模式中复用。

只有当前任务实际暴露的原文证据可以用于核验；程序校验证据归属、快照哈希、片段存在、产品与适用范围。模型核验返回supported、contradicted、insufficient。scope中版本、套餐、地区或日期文字必须在引用原文出现。不同scope不自动视为矛盾；相同属性和scope存在不同规范值时保守标为冲突。

Writer只提交条件式判断及已支持claim_ids，事实对比表由服务端直接从核验结果渲染。未知、冲突及未通过核验项单独展示，不进入确定性事实表。链接存在检查与语义支持判断分开。判断文字本身仍由模型生成，需要独立人工复核，不宣称程序能够证明其所有语义都正确。

普通快照24小时、价格/额度/套餐限制快照1小时；敏感文档全篇采用短TTL。请求特定版本、主动刷新或超时会重新读取；旧版报告引用的原文快照保持不变。跨会话不复用研究缓存。相同正文哈希共用快照文件以减少磁盘重复，但仍按会话重新获取与记录来源，不据此虚增独立证据数量。

## 持久化与费用

`research.sqlite`使用WAL：sessions、tasks、sources、evidence、reports、report_heads；报告版本和head在单一事务内提交。快照为`runtime/snapshots/<sha256>.txt`。任务记录保存每产品决策次数、补查轮数、累计主动耗时及调用预算。

真实模型Token来自各响应usage，不估算为实测Token；fixture以0记录并标注不适用。成本只在配置单价后估算，模型人民币与搜索美元分开，不自行混算。失败请求是否计费以供应商账单为准；认证、额度和限流错误保留脱敏代码。

当前采用单进程本地调度，没有分布式锁或持久化任务队列，不支持多worker写同一任务库。公网部署需要额外身份鉴别、会话归属验证和访问控制。
