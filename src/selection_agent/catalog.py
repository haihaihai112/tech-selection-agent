CATALOG = {
    'vector_databases': {'title': '向量数据库', 'products': ['pgvector', 'Qdrant', 'Milvus'],
        'dimensions': ['部署方式', '已有技术栈', '检索与过滤', '维护要求', '扩展方式'],
        'questions': ['部署要求（本地、自托管或托管服务）', '已有技术栈（例如是否使用PostgreSQL）']},
    'search_apis': {'title': '搜索API', 'products': ['Tavily', 'Exa', 'Brave Search API'],
        'dimensions': ['查询控制', '内容返回', '来源信息', '接口限制', '计费方式'],
        'questions': ['使用场景（研究报告、问答或其他）', '内容要求（链接、摘要或正文）']},
    'rag_platforms': {'title': '知识库应用平台', 'products': ['Dify', 'FastGPT', 'RAGFlow'],
        'dimensions': ['文档处理', '检索配置', '工作流', '模型接入', '部署与许可'],
        'questions': ['部署要求（本地、自托管或托管服务）', '主要文档类型与需要的工作流']},
}


def validate_catalog(catalog):
    if not isinstance(catalog, dict):
        raise ValueError('自定义目录必须是对象')
    title, products, dimensions = catalog.get('title'), catalog.get('products'), catalog.get('dimensions')
    if not isinstance(title, str) or not title.strip() or not isinstance(products, list) or not 1 <= len(products) <= 3:
        raise ValueError('自定义目录需要1到3个候选产品')
    if not isinstance(dimensions, list) or not 1 <= len(dimensions) <= 8:
        raise ValueError('自定义目录需要1到8个比较维度')
    if any(not isinstance(v, str) or not v.strip() for v in [*products, *dimensions]):
        raise ValueError('自定义目录中的产品和维度必须是非空文本')
    if len(set(products)) != len(products) or len(set(dimensions)) != len(dimensions):
        raise ValueError('自定义目录中的产品和维度不能重复')
    return {'title': title.strip(), 'products': products, 'dimensions': dimensions,
            'questions': catalog.get('questions', []) if isinstance(catalog.get('questions', []), list) else []}


def catalog_for_request(request):
    if request['group'] == 'custom':
        return validate_catalog(request.get('custom_catalog'))
    return CATALOG[request['group']]

# Identification hints only: these are not cached feature or price claims.
OFFICIAL_ROOTS = {
    'pgvector': ['https://github.com/pgvector/pgvector'],
    'Qdrant': ['https://qdrant.tech/'], 'Milvus': ['https://milvus.io/'],
    'Tavily': ['https://tavily.com/', 'https://docs.tavily.com/'],
    'Exa': ['https://exa.ai/'], 'Brave Search API': ['https://brave.com/search/api/', 'https://api.search.brave.com/'],
    'Dify': ['https://docs.dify.ai/', 'https://dify.ai/', 'https://github.com/langgenius/dify'],
    'FastGPT': ['https://doc.fastgpt.io/', 'https://github.com/labring/FastGPT'],
    'RAGFlow': ['https://ragflow.io/', 'https://github.com/infiniflow/ragflow'],
}


def is_official(product, url):
    from urllib.parse import urlsplit
    target = urlsplit(url)
    for root in OFFICIAL_ROOTS.get(product, []):
        expected = urlsplit(root)
        if target.hostname == expected.hostname and (expected.path == '/' or
                target.path == expected.path.rstrip('/') or target.path.startswith(expected.path.rstrip('/') + '/')):
            return True
    return False


def infer_group(text):
    lowered = text.lower()
    for key, data in CATALOG.items():
        if data['title'] in text or any(p.lower() in lowered for p in data['products']):
            return key
    return 'vector_databases'
