# Vault Consolidation: wbaoc-wiki

## Round 1: Folder Merge (2026-05-21)

Moved scattered root-level folders into organized structure.

| Old Location | New Location | Action |
|---|---|---|
| `01 日记/` | `子弹笔记/日记/` | Moved all 19 diary files |
| `02 每周任务清单/` | `子弹笔记/每周/` | Moved 5 weekly files |
| `03 会议记录/` | `子弹笔记/会议/` | Moved 1 meeting note |
| `04 白板/` | `子弹笔记/白板/` | Moved 1 canvas file |
| `05 看板/` | `子弹笔记/看板/` | Moved 1 kanban file |
| `运动健身/` | `子弹笔记/运动/` | Moved (was mostly empty) |
| `carl-weread/` | `微信读书/` | Renamed (no skill hardcodes path) |
| `Clippings/` (root) | `raw/clippings/` | Merged unique files, deleted root dir |

## Round 2: Topic-Based Reorganization (2026-05-29)

Reorganized `wiki/` and `raw/` from **source-based** to **topic-based** folders.

### Wiki topic structure

```
wiki/
├── AI/                  ← AI工具、Agent、Prompt、大模型
├── 学术/                ← 论文写作、投稿、统计方法
│   └── 论文写作/
├── 临床药学/            ← 药学、处方、ADR、预测模型
│   ├── 临床数据库/      (含NHANES)
│   ├── 信息药师/
│   ├── 网络药理学/
│   └── 生物信息学/
├── 计算机基础/          ← OS、Linux、网络、数据库
│   └── Mac学习手册/
├── 编程/                ← Python、R、Git、开发工具
├── 3D打印/              ← 拓竹、eufyMaker、耗材、建模
├── 效率工具/            ← Obsidian、BuJo、Hermes
├── 摄影/                ← 焦段、构图、DJI
├── 健身/                ← 训练、饮食、碳水循环
├── 统计/                ← 贝叶斯、假设检验、回归
├── 金融/                ← 理财、投资（待填充）
├── 个人/                ← 档案、数字分身
├── 学习方法/            ← 学习方法论
├── 学习方法的寓言小故事/ ← 寓言故事（按领域子文件夹）
│   └── 统计学/
├── 杂项/                ← 兜底
├── entities/            ← 知识图谱实体（不动）
├── sources/             ← 知识图谱来源（不动）
└── topics/              ← 知识图谱主题（不动）
```

### Raw topic structure

```
raw/
├── AI/                  ← B站/抖音/微信的AI内容
├── 学术/                ← 论文写作剪藏
├── 临床药学/            ← 药学相关
├── 编程/                ← 编程相关
├── 3D打印/              ← 打印相关
├── 效率工具/            ← Obsidian等
├── 摄影/                ← 拍照技巧
├── 健身/                ← 健身相关
├── 通用/                ← 不好分类的
├── pdfs/                ← PDF文件
├── inbox/               ← 待分类入口
├── notes/               ← 个人笔记
└── chats/               ← 聊天记录
```

### Migration moves (Round 2)

| Old Location | New Location |
|---|---|
| `raw/clippings/Bilibili/` (AI内容) | `raw/AI/` |
| `raw/clippings/anthropic-engineering/` | `raw/AI/` |
| `wiki/信息药师/` | `wiki/临床药学/信息药师/` |
| `wiki/临床数据库/` | `wiki/临床药学/临床数据库/` |
| `wiki/网络药理学/` | `wiki/临床药学/网络药理学/` |
| `wiki/生物信息学/` | `wiki/临床药学/生物信息学/` |
| `wiki/AI工具/` | `wiki/AI/` |
| `raw/clippings/` (各子文件夹) | 按主题拆分到 `raw/<topic>/` |

## Config files updated (both rounds)

- `.obsidian/daily-notes.json` — folder: `01 日记` → `子弹笔记/日记`
- `子弹笔记/仪表盘.md` — Dataview FROM paths + quick links updated
- `CLAUDE.md` — full directory tree rewritten
- `.obsidian/community-plugins.json` — added `pdf-plus`, `obsidian-book-search-plugin`
- `scripts/daily-review.py` — scan paths updated to new raw/ structure
- `obsidian` skill — old path references patched

## Final top-level state

```
wbaoc-wiki/
├── 子弹笔记/      ← diaries, weekly, monthly, projects, meetings, kanban, whiteboard, fitness
├── 微信读书/      ← weread reading cards
├── wiki/          ← knowledge base by topic (don't rename — llm-wiki scripts hardcode)
├── raw/           ← source material by topic
├── 00 templates/
├── attachments/
└── media-lib/
```

## Categorization workflow (for saved content screenshots)

When user sends screenshots of Douyin "Watch Later" / Bilibili favorites / WeChat saved articles:

1. **Read each item** from the screenshot — extract title, source, topic
2. **Categorize by topic** using the wiki/raw folder structure above
3. **Present the plan** — show which folder each item goes to
4. **Wait for confirmation** before migrating
5. **Migrate** — move files to target folders, update index.md if wiki content

### Topic classification rules

| Content type | Target folder |
|---|---|
| AI工具/Agent/Prompt/大模型 | `raw/AI/` or `wiki/AI/` |
| 论文写作/投稿/统计方法 | `raw/学术/` or `wiki/学术/` |
| 药学/处方/ADR/预测模型 | `raw/临床药学/` or `wiki/临床药学/` |
| Python/R/Git/开发工具 | `raw/编程/` or `wiki/编程/` |
| 拓竹/eufyMaker/建模 | `raw/3D打印/` or `wiki/3D打印/` |
| Obsidian/BuJo/Hermes | `raw/效率工具/` or `wiki/效率工具/` |
| 摄影/构图/DJI | `raw/摄影/` or `wiki/摄影/` |
| 训练/饮食/碳水循环 | `raw/健身/` or `wiki/健身/` |
| 贝叶斯/假设检验/回归 | `wiki/统计/` |
| OS/Linux/网络/数据库 | `wiki/计算机基础/` |
| 不好分类 | `raw/通用/` |

### Wiki AI subdirectory structure (2026-05-29)

`wiki/AI/` is the largest topic folder — split into sub-categories:

```
wiki/AI/
├── agent/           ← 智能体架构、Harness、工具使用、多Agent系统（12 files）
├── 编程工具/        ← Claude Code、Cursor、Windsurf、GitHub Copilot（10 files）
├── prompt工程/      ← 提示词工程、思维链、结构化输出（4 files）
├── 硬件/            ← 芯片、GPU、算力基础设施（3 files）
├── 知识库构建/      ← RAG、LLM-Wiki、个人知识管理（3 files）
├── 学术研究/        ← AI辅助论文写作、文献综述（3 files）
├── 评测/            ← 模型评测、基准测试（2 files）
├── RAG/             ← 检索增强生成专题（2 files）
├── 行业观察/        ← 产业分析、公司动态（1 file）
└── index.md         ← 索引页（子文件夹+文件列表）
```

Other wiki topic folders (学术, 编程, 效率工具, etc.) stay flat unless they accumulate 10+ files.

### Raw→Wiki content promotion workflow

When raw/\<topic\>/ accumulates enough files on one sub-theme:

1. **Scan raw/\<topic\>/** — list all files, identify themes
2. **Create wiki/\<topic\>/ subdirectories** — group by sub-theme
3. **Create index.md** in each subdirectory — list files with 1-line descriptions
4. **Create root index.md** — list subdirectories + standalone files
5. **Update CLAUDE.md** — mirror new directory tree
6. **Update wiki/index.md** — add new entries

Do NOT move files from raw/ to wiki/ — raw stays as-is. Wiki pages are new提炼d content.

## Key lessons

- `wiki/` cannot be renamed to `维基库/` — llm-wiki scripts hardcode `wiki/` in paths
- `carl-weread/` safe to rename — skill uses `~/.config/carl-weread/` for config
- Duplicate `Clippings/` at root was from plugin capturing to wrong path — merged into `raw/clippings/`
- Calendar plugin uses `YYYY-MM-DD_ddd` format → daily notes have weekday suffix
- When `patch` fails on corrupted files (line-number artifacts), just `write_file` the whole thing clean
- **Topic-based > source-based** — user wants to find content by what it's ABOUT, not where it came from
- **Knowledge graph dirs are read-only** — `entities/`, `sources/`, `topics/` are managed by llm-wiki scripts, don't move files in/out
- **Clinical pharmacy subfolders** — keep `临床数据库/`, `信息药师/`, `网络药理学/`, `生物信息学/` as subfolders under `临床药学/` (too many files to flatten)
