---
name: academic-writing
description: >
  Academic writing workflows for Chinese pharmaceutical/academic contexts:
  reference verification, SCI submission preparation, and grant/competition
  applications. Use when the user mentions 论文, 参考文献, SCI, 期刊, 投稿,
  申报书, 课题申报, 基金申请, or academic writing tasks.
version: 1.0.0
author: hermes
tags: [academic, writing, references, SCI, grants, pharmaceutical]
---

# Academic Writing Workflows

Three interconnected workflows for academic publishing in Chinese pharmaceutical/academic contexts.

## Workflow 1: Reference Verification (reference-checker)

Check reference authenticity in papers. 8 inspection dimensions, 3-step process.

### Inspection Dimensions
1. **Cross-matching** — text citations vs reference list
2. **Format audit** — punctuation, italics, capitalization consistency
3. **Naming standardization** — author name variants, journal abbreviations
4. **DOI/URL validation** — format checking, no fabricated links
5. **Year logic** — publication year plausibility, volume/year conflicts
6. **Completeness** — required fields (author, title, journal, year, volume/pages)
7. **Accessibility** — can the reference be found in databases?
8. **Comprehensive report** —汇总所有检查结果

### Process
1. Extract text from .docx (python-docx) or PDF (pdftotext/pymupdf)
2. Identify document structure (body references vs review references)
3. Run automated checks (regex patterns for citations and entries)
4. Generate audit report with severity levels

### Common Pitfalls
- Citation errata vs original papers
- Author name abbreviation errors (>3 authors not abbreviated per GB/T 7714)
- Missing volume/pages for recent publications
- Body vs review reference numbering conflicts

---

## Workflow 2: SCI Submission Preparation (sci-submission-prep)

Convert Chinese thesis/dissertation to SCI journal submission format.

### Process
1. **Read thesis** — extract research design, outcomes, methods, performance metrics
2. **Journal matching** — 3-tier selection (primary/backup/safety) based on:
   - Topic match, research type friendliness, impact factor, APC, review timeline
3. **TRIPOD+AI compliance audit** — check against TRIPOD+AI checklist
4. **Generate submission materials** — data availability, conflicts, AI transparency statements

### Key Considerations
- Positive events <50 → high IF journals (>5) unlikely
- Position as "exploratory tool" not "clinical diagnostic tool"
- Information leakage control is a methodological highlight
- Dual-language publication requires both journals to allow it

### Reference Files
- `references/tripod-ai-checklist.md` — TRIPOD+AI compliance checklist
- `references/submission-supplements-template.md` — submission material templates

---

## Workflow 3: Grant/Competition Applications (project-application)

Write applications for Chinese pharmaceutical competitions, grants, and project submissions.

### Process
1. **Read notification PDF** — deadlines, tracks, form structure, word limits
2. **Extract data from materials** — QCC PPTs, .doc files, existing projects
3. **Project selection** — evaluate candidates against competition criteria
4. **Fill application form** — 7-9 section structure (~2300 words)
5. **Save & sync** — Obsidian vault updates

### Application Structure (typical)
| # | Section | Word Limit |
|---|---------|-----------|
| 1 | 项目基本信息 | — |
| 2 | 项目简介 | 300字 |
| 3 | 业务痛点与应用场景 | 500字 |
| 4 | AI技术路线与数据来源 | 500字 |
| 5 | 已取得成效与量化指标 | 300字 |
| 6 | 可推广性与复制条件 | 300字 |
| 7 | 风险控制与合规说明 | 200字 |
| 8 | 知识产权与数据合规 | 200字 |

### Critical Rules
- **Data-first**: Every claim needs a number
- **Thesis trap**: Don't default to thesis as project base (competitions want implemented projects)
- **Name the right leader**: QCC project leader ≠ form filler
- **Maturity accuracy**: Deployed = "规模化应用", not "试点应用"

### Reference Files
- `references/project-comparison.md` — candidate project comparison framework
- `references/application-template.md` — application form template

---

## Cross-Workflow Patterns

All three workflows share:
- **python-docx** for .docx extraction
- **pymupdf** for PDF extraction
- **Obsidian** for knowledge management
- **Data-first writing style** — numbers > descriptions
- **Chinese academic conventions** — GB/T 7714, 考试-oriented language
