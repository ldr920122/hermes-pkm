# Karpathy LLM Wiki Ingest Workflow

User's vault follows CLAUDE.md schema: Karpathy LLM Wiki pattern with `wiki/` as structured knowledge base.

**Vault location:** `<VAULT_PATH>/` (not default paths)

## Full Ingest Checklist

When ingesting content (image, article, video notes) into the wiki:

### 1. Copy attachments
```bash
# Images → attachments/
cp ~/Desktop/image.png <VAULT_PATH>/attachments/

# Articles → raw/articles/ or raw/clippings/
cp ~/Downloads/article.md <VAULT_PATH>/raw/articles/
```

### 2. Create wiki page with frontmatter
Location: `wiki/<category>/<title>.md`

```yaml
---
title: 页面标题
category: AI工具 | 生物信息学 | 网络药理学 | 临床数据库 | 信息药师 | 个人 | 杂项
tags: [tag1, tag2, tag3]
sources: [来源描述]
updated: YYYY-MM-DD
---

# Title

Content with `![[filename.png]]` wikilink references to attachments.
```

### 3. Update `wiki/index.md`
Add row to appropriate category table:
```markdown
| [[页面标题]] | 一句话摘要 |
```

### 4. Update `wiki/log.md`
Append ingest entry at the end:
```markdown
## [YYYY-MM-DD] ingest | <title>

- 来源：<url or description>
- 保存至 `wiki/<category>/<filename>.md`
- <1-3 key takeaways>
```

## Category Directory Map
- `wiki/AI工具/` — AI tools, programming agents, productivity
- `wiki/生物信息学/` — bioinformatics, genomics, R/Python
- `wiki/网络药理学/` — network pharmacology, molecular docking
- `wiki/临床数据库/` — NHANES, clinical data mining
- `wiki/信息药师/` — pharmacy informatics, research methods
- `wiki/个人/` — personal backups, memories
- `wiki/杂项/` — misc (Obsidian, Mac tips, fitness)

## Pitfalls
- **Always check if file exists before overwriting** — use `ls` or `search_files` first
- **Attachment wikilinks** use `![[filename.png]]` not `![](path)` — Obsidian wikilink format
- **Tags can be bilingual** — user mixes Chinese and English tags
- **Log is append-only** — never delete or rewrite history
- **Index table format** must match existing rows exactly (spacing, pipe alignment)