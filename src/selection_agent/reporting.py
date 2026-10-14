import difflib
import re

from .models import WriterDraft, Verdicts


def plain(text):
    """Treat source strings as text, never HTML or generated Markdown links."""
    value = str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', ' ')
    return re.sub(r'([\\`*\[\]!|])', r'\\\1', value)


async def judgments(model, brief, claims):
    supported = {c.id: c for c in claims if c.status == 'supported'}
    if not supported:
        return []
    result = await model.structured('write',
        '根据用户条件与已核验事实给出条件式选型理由；不生成新的产品事实，不强制排名、不打综合分。'
        'reasoning只能解释条件与证据之间的关系，不补写费用、性能、能力或许可结论。'
        '每条判断关联同一product的已核验claim_ids，并用condition_keys指出关联的用户条件。'
        '缺少用量不能计算总费用，未知能力不等于不支持；可以不推荐任何产品。',
        {'brief': brief.model_dump(), 'claims': [c.model_dump() for c in supported.values()]}, WriterDraft)
    for judgment in result.judgments:
        if judgment.product not in brief.products or set(judgment.condition_keys) - set(brief.constraints):
            raise ValueError('报告判断引用了未知条件')
        if any(cid not in supported or supported[cid].product != judgment.product for cid in judgment.claim_ids):
            raise ValueError('报告判断引用未通过核验的事实')
        if re.search(r'https?://|\[E-|\[C-', judgment.reasoning):
            raise ValueError('判断文本不得自行构造引用，引用由服务端渲染')
    if result.judgments:
        audit = await model.structured('verify_judgments',
            '核验选型理由是否只使用关联的已核验事实和用户条件。每个判断返回一个verdict，claim_id使用其id。'
            '理由出现未在关联事实中支持的产品能力、架构、价格、性能或许可说法时必须为insufficient。'
            '减少运维工作不能直接等同于总体费用较低；来源特定场景的建议不能泛化。'
            '不使用外部知识填补依据。单纯表达条件式权衡可以supported。',
            {'brief': brief.model_dump(), 'judgments': [{'id': f'J-{i}', **j.model_dump(),
                'facts': [supported[cid].model_dump() for cid in j.claim_ids]}
                for i, j in enumerate(result.judgments)]}, Verdicts)
        mapping = {v.claim_id: v for v in audit.verdicts}
        if (len(mapping) != len(audit.verdicts) or set(mapping) != {f'J-{i}' for i in range(len(result.judgments))}
                or any(v.status != 'supported' for v in mapping.values())):
            raise ValueError('推荐理由未通过依据核验，保留任务证据但不发布报告')
    return result.judgments


def render(brief, claims, decisions, unresolved, sources, version, mode):
    lines = [f'# 技术选型研究报告 · 第 {version} 版', '',
        '**确定性测试替身：以下资料为合成内容，不构成真实产品建议。**' if mode == 'fixture' else
        '**基于本次抓取资料；模型语义核验不等同于独立事实审计。**', '', '## 用户条件', '']
    lines.extend(f'- {plain(k)}：{plain(v)}' for k, v in brief.constraints.items())
    lines.extend(f'- 偏好：{plain(p)}' for p in brief.preferences)
    lines.extend(f'- 尚未明确：{plain(q)}' for q in brief.unknowns)
    lines += ['', '## 来源事实对比', '', '| 比较维度 | ' + ' | '.join(plain(p) for p in brief.products) + ' |',
              '|---|' + '---|' * len(brief.products)]
    for dimension in brief.dimensions:
        cells = []
        for product in brief.products:
            facts = [c for c in claims if c.product == product and c.dimension == dimension and c.status == 'supported']
            cell = '；'.join(f'{plain(c.text)} [{c.id}]' for c in facts) or '证据不足，不能确定'
            if any(c.product == product and c.dimension == dimension and c.status == 'contradicted' for c in claims):
                cell += '；另有冲突资料待确认'
            cells.append(cell)
        lines.append('| ' + plain(dimension) + ' | ' + ' | '.join(cells) + ' |')
    lines += ['', '## 基于条件的判断（与来源事实分开）', '']
    if not decisions:
        lines.append('现有证据不足以形成可靠推荐；不强制排序。')
    for decision in decisions:
        lines.append(f'- **{plain(decision.product)}**：{plain(decision.reasoning)} ' +
                     ' '.join(f'[{cid}]' for cid in decision.claim_ids))
    lines += ['', '## 冲突与待确认项', '']
    lines.extend(f'- {plain(g["product"])} / {plain(g["dimension"])}：{plain(g["reason"])}' for g in unresolved)
    lines.extend(f'- [{c.id}] {plain(c.product)}：{plain(c.text)}；{plain(c.reason)}' for c in claims if c.status != 'supported')
    if not unresolved and all(c.status == 'supported' for c in claims):
        lines.append('本轮结构化核验未发现未解决项；这不代表已完成独立事实审计。')
    lines += ['', '## 结论与原文证据', '']
    source_ids = {s.id for s in sources}
    for claim in claims:
        ids = [eid for eid in claim.evidence_ids if any(eid.startswith('E-' + sid + '-') for sid in source_ids)]
        lines.append(f'- [{claim.id}] {plain(claim.status)}：' +
            (' '.join(f'[{eid}](/v1/evidence/{eid})' for eid in ids) or '没有可定位的有效证据'))
    lines += ['', '## 来源与时间', '']
    for source in sources:
        label = '合成测试资料' if source.model_mode == 'fixture' else source.source_type
        # URLs are validated by acquisition; source titles do not become executable markup.
        availability = '已读取原文' if source.status == 'fulltext' else '仅搜索摘要，不能支持确定性事实'
        lines.append(f'- {plain(source.title)} · {label} · {availability} · 抓取 {source.retrieved_at} · '
                     f'发布 {plain(source.published_at or "未知")} · 文档版本 {plain(source.document_version or "未知")} · '
                     f'{plain(source.url)}')
    return '\n'.join(lines)


def diff(previous, brief, claims, decisions, markdown, reused):
    if not previous:
        return {'reused_snapshots': reused, 'condition_changes': {}, 'added_facts': [], 'removed_facts': [], 'markdown_diff': ''}
    before = previous['brief']['constraints']
    changes = {k: {'before': before.get(k), 'after': brief.constraints.get(k)}
               for k in sorted(set(before) | set(brief.constraints)) if before.get(k) != brief.constraints.get(k)}
    def key(c):
        return c['product'], c['dimension'], c['text'], c['status']
    old = {key(c) for c in previous['claims']}
    new = {key(c.model_dump()) for c in claims}
    return {'reused_snapshots': reused, 'condition_changes': changes,
            'added_facts': [list(v) for v in sorted(new - old)], 'removed_facts': [list(v) for v in sorted(old - new)],
            'judgments_changed': previous['judgments'] != [j.model_dump() for j in decisions],
            'markdown_diff': '\n'.join(difflib.unified_diff(previous['markdown'].splitlines(), markdown.splitlines(),
                fromfile=f'version-{previous["version"]}', tofile=f'version-{previous["version"] + 1}', lineterm=''))}
