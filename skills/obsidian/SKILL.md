---
name: obsidian
description: Read, search, and create notes in the Obsidian vault.
---

# Obsidian Vault

**Location:** Set via `OBSIDIAN_VAULT_PATH` environment variable (e.g. in `~/.hermes/.env`).

If unset, defaults to `~/Documents/Obsidian Vault`.

Note: Vault paths may contain spaces - always quote them.

## Read a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
cat "$VAULT/Note Name.md"
```

## List notes

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# All notes
find "$VAULT" -name "*.md" -type f

# In a specific folder
ls "$VAULT/Subfolder/"
```

## Search

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"

# By filename
find "$VAULT" -name "*.md" -iname "*keyword*"

# By content
grep -rli "keyword" "$VAULT" --include="*.md"
```

## Create a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
cat > "$VAULT/New Note.md" << 'ENDNOTE'
# Title

Content here.
ENDNOTE
```

## Append to a note

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
echo "
New content here." >> "$VAULT/Existing Note.md"
```

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

## Vault Architecture Patterns

When a user asks to restructure, partition, or combine workflows in their vault, recommend the **single-vault multi-zone** pattern. Avoid splitting into multiple vaults unless there's a strong security or sync boundary — `[[wikilinks]]` cannot cross vaults, and graph view splits across vaults.

### The Three-Zone Pattern

A balanced vault layout that works for most knowledge workers:

```
vault/
├── 知识库/             ← Karpathy-style llm-wiki (compounding knowledge)
│   ├── index.md
│   ├── SCHEMA.md
│   ├── raw/            ← immutable source material
│   ├── concepts/       ← concept pages with [[wikilinks]]
│   └── entities/       ← entity pages
│
├── 个人/               ← personal info, backups (Gemini/Claude memories)
│
├── 学习笔记/           ← study notes, coursework, reading notes
│
└── 子弹笔记/           ← task management + journaling
    ├── 年度.md
    ├── 月度.md
    ├── 日记/           ← daily notes
    ├── 项目/           ← project tracking
    └── 收集箱.md       ← quick capture inbox
```

**Why one vault:**
- A single Graph View shows all connections across knowledge, study, and tasks
- `[[wikilinks]]` between zones: study notes can link to wiki concepts, tasks can reference knowledge base entries
- No vault switching needed — everything is one Cmd+O away

### When to recommend a new vault instead

- Separate sync boundaries (e.g., work vault on corporate iCloud vs personal vault on personal iCloud)
- Radically different tag taxonomies that would pollute search
- Security/compliance requirements where knowledge domains must not cross-reference

### Bullet Journal / Task Management Setup (Ryder Carroll Method)

Full BuJo implementation in Obsidian, adapted from Ryder Carroll's original method + elainooooo's tutorial. Designed for "P people" (spontaneous/flexible) — minimal ritual, maximal capture.

**Plugin stack** (check + install any missing):

| Plugin | Type | Role |
|--------|------|------|
| **Daily Notes** | core | Auto-generate daily journal files |
| **Templates** | core | Auto-fill daily notes from template |
| **Tasks** | community | Enhanced `- [ ]` with dates, priorities, recurrence |
| **Dataview** | community | SQL-like queries; auto-aggregate tasks across vault |
| **Calendar** | community | Calendar heatmap, click date → open daily note |
| **QuickAdd** | community (optional) | Quick-add to inbox without opening file |

**Dataview installation**: Dataview is not available via Obsidian's plugin browser in headless mode. Install manually from GitHub releases:
```bash
PLUGIN_DIR="$VAULT/.obsidian/plugins/dataview"
mkdir -p "$PLUGIN_DIR"
curl -sL 'https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download/main.js' -o "$PLUGIN_DIR/main.js"
curl -sL 'https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download/manifest.json' -o "$PLUGIN_DIR/manifest.json"
curl -sL 'https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download/styles.css' -o "$PLUGIN_DIR/styles.css"
# Then add "dataview" to community-plugins.json array
```

**Four-layer time framework** (the BuJo backbone):

```
📅 Future Log（年度）→ user sets annual goals + month-anchored items
    ↓ monthly migration
📆 Monthly Log（月度）→ calendar timeline + action plan + habit tracker
    ↓ daily reference
📝 Daily Log（每日）→ top 3 priorities + tasks + freeform notes
    ↓ end-of-month review
🔄 Migration Ritual → 4-step process to close the loop
```

**BuJo directory structure** (create inside existing vault):

```
子弹笔记/
├── 年度.md              ← Future Log: annual goals + month-anchored items
├── 月度/
│   └── YYYY-MM.md       ← Monthly Log: calendar timeline + action plan + habits
├── 仪表盘.md            ← Dataview dashboard: auto-aggregates all open tasks
├── 收集箱.md            ← Quick capture inbox: dump anything, triage later
├── 使用指南.md          ← User-facing how-to (link from dashboard)
└── 月度迁移仪式.md       ← Monthly migration ritual checklist
```

**Daily Notes config** — `.obsidian/daily-notes.json`:
```json
{
  "format": "YYYY-MM-DD_ddd",
  "folder": "子弹笔记/日记",
  "template": "00 templates/子弹笔记-日记模板"
}
```

**Naming convention**: files are `YYYY-MM-DD_ddd.md` (e.g. `2026-05-21_Thu.md`). The Calendar plugin generates them; Hermes should check if one already exists before creating. Never create `YYYY-MM-DD.md` (no weekday suffix) — that's a different file and causes duplicates.

### Updating Daily Notes

When adding content to existing daily notes (e.g., adding events, thoughts, or status updates):

1. **Locate the daily note**: Check if today's note exists using the naming convention `YYYY-MM-DD_ddd.md` in the `子弹笔记/日记/` folder
2. **Find insertion point**: Look for the `## 📝 笔记 · 事件 · 感想` section
3. **Append content**: Add new bullet points with appropriate markers:
   - `○` for events
   - `—` for thoughts/ideas
   - `- [ ]` for tasks
   - `- [x]` for completed tasks

**Example update pattern:**
```markdown
- ○ 今天完成了X任务
- ○ 参加了Y会议
- — 发现Z问题需要跟进
```

**Pitfalls:**
- **Duplicate daily notes**: Always check if Calendar plugin already created the note before creating a new one
- **Section targeting**: Use `search_files` to find the exact line number of the insertion point
- **Line number artifacts**: If patch fails with "Could not find a match", the file may have corrupted line-number prefixes. Use `references/fix-line-number-artifacts.md` for repair

**When to update vs. create:**
- If note exists: append to existing content
- If note doesn't exist: create from template first (see `templates/bujo-daily-template.md`)
- Always verify the `created` frontmatter field matches the expected format

**Important**: When Hermes writes to a daily note, always check if Calendar already created the file first. See `references/bujo-daily-reconcile.md` for the full reconciliation checklist.

**Daily template** (see `templates/bujo-daily-template.md` for the full content):
- Frontmatter with tags and created date
- 🎯 今日三件事 section (Ryder Carroll: "what would make today successful?")
- 📋 任务 section for standard `- [ ]` tasks
- 📝 笔记·事件·感想 section for freeform capture throughout the day
- 🔄 明日预览 section (30-second bedtime ritual)

**Monthly template** (see `templates/bujo-monthly-template.md`):
- Calendar timeline table (31 rows, one notable thing per day)
- Monthly action plan checklist
- Habit tracker table (max 3 habits, 4-week grid)
- End-of-month review prompts

**Migration ritual** (the critical monthly 4-step process):
1. Review last month's daily notes → find unfinished tasks → complete/migrate/cancel
2. Check Future Log → migrate this month's items to Monthly Log
3. Review last month's Monthly Log → migrate or cancel unfinished items
4. Create new Monthly Log from template → populate from steps 1-3

**Dashboard Dataview queries**:
```dataview
TASK FROM "子弹笔记/日记" WHERE !completed AND file.day = date(today) LIMIT 10
TASK FROM "子弹笔记/日记" OR "子弹笔记" WHERE !completed GROUP BY file.link LIMIT 30
LIST FROM "子弹笔记/日记" WHERE file.day.month = date(today).month SORT file.day DESC
```

**Brain dump → BuJo categorization workflow** (when a user dumps a stream of tasks, worries, and aspirations):

1. **Collect first** — dump everything verbatim into `收集箱.md`. Don't filter or sort yet. The act of emptying their head IS the therapeutic step.
2. **Categorize by urgency × importance** — use an Eisenhower-like grid:
   - 🚨 紧急且重要 → move to this month's action plan with deadlines
   - 🔴 重要不紧急 → move to Future Log with target month
   - 🟡 等待启动 → note blocking condition, don't create false urgency
   - 🔵 堆在心头的焦虑 → acknowledge "not now", leave in inbox with a note. Explicitly tell the user they don't need to act on these yet.
3. **Identify opportunities** — when the user mentions vague items like "课题申报 but no ideas", cross-reference their existing work (thesis, skills, data access) to spot matches. Grant calls, competitions, and funding opportunities from their field should trigger immediate alignment.
4. **Present the reorganized view** — show them the clarity they gained: what was chaos is now a prioritized plan with deadlines and next actions.
5. **Update all BuJo layers** — 收集箱, 月度记录, 年度 Future Log all get updated in one pass.
   - **Opportunity matching**: when funding calls or competition notices arrive in the user's domain, cross-reference their existing thesis/research against the call's funding directions. See `references/opportunity-matching.md` for the full pattern.

**Multi-source ingest log format**: When ingesting external content (articles, screenshots, PDFs) to `wiki/`, append to `wiki/log.md` in this exact format:

```markdown
## [YYYY-MM-DD] ingest | <title>

- 来源：<url or description>
- 保存至 `<relative path>`
- <1-3 key takeaways>
```

Each ingest entry should be 2-4 lines. Prepend new entries above older ones. For bulk ingests (multiple articles from one source), write a single log entry summarizing the batch. Keep the log append-only — never delete or rewrite history.

**Karpathy LLM Wiki ingest**: For vaults following the CLAUDE.md schema (wiki/ with YAML frontmatter, attachments/, raw/, index.md, log.md), see `references/karpathy-llm-wiki-ingest.md` for the full 4-step checklist: copy attachments → create page with frontmatter → update index.md → update log.md.

**Status-update sync pattern**: When the user announces a task status change ("提交了", "做完了", "搭好框架了"), update ALL relevant BuJo layers in one pass — don't make the user ask for each file separately. The standard sync set is:

1. **收集箱** — mark as [x] or update status description
2. **月度记录** — mark action-plan item as [x], append to today's calendar timeline
3. **今日日记** — if already created, add/update the task status
4. **Memory** — if the status change shifts a dependency or long-running assumption (e.g., "不再需要等 Claude 额度")

If the task was high-stress ("被催很久了"), add a small celebratory marker (✅ 🎉) — it matters for P-people.

**Long-term deferred items**: when user says "排期不确定", "等通知", "不知道什么时候", or "先不排进日常":
1. **日记** — record in 📝 笔记 section only, NOT in 今日三件事 or 任务
2. **月度计划** — add to `📌 长期待办（排期/审批未定，不进日常）` section
3. **Do NOT** create daily tasks or recurring reminders — the item has no anchor date

**Completed task archival**: when user says "做完了", "投稿了", "结束了", or marks a project as done:
1. **月度计划** — move from active section to `✅ 本月已完成` with checkmark and date
2. **月度日历时间线** — add entry on the completion date
3. **日记** — add celebratory note in 📝 笔记 section if significant (论文、投稿、大赛)
4. **收集箱** — mark as [x] if present there

### Timestamp Convention (All Created Notes)

Every note created by Hermes (via chat, web clipper ingest, or direct creation) MUST include a timestamp in YAML frontmatter:

```yaml
---
created: YYYY-MM-DD HH:mm
---
```

This enables:
- **Freshness tracking**: user can instantly see if content is outdated
- **Spaced repetition sorting**: daily review script uses creation date for prioritization
- **Chronological browsing**: notes have a clear time order

When creating notes, always add `created:` to the frontmatter. For existing notes without timestamps, do NOT add them retroactively (that would misrepresent when the content was actually captured).

**Daily Review System** — automated spaced repetition from Obsidian vault:

- Script: `scripts/daily-review.py` — randomly selects content from `wiki/`, `raw/AI/`, `raw/效率工具/`, `raw/学术/`, `raw/编程/`, `raw/通用/`, `微信读书/`, `子弹笔记/项目/`, `子弹笔记/会议/`
- Cron job: runs daily at 20:00, delivers a 200-word review card
- Tracks reviewed files in `~/.hermes/scripts/.review_history.json` to avoid repeats
- Excludes: daily notes, templates, system files, infographics
- Content is提炼d (not raw copy) — key points + memory hook + actionable insight

**P-person-friendly principles** (encode these into the usage guide):
- Zero-friction capture: Calendar click → template auto-fills → write, don't format
- Inbox first: any thought goes to 收集箱, triage weekly, never lose an idea
- No forced classification: dump first, sort later
- Minimal ritual: 3 min/day, 10 min/month, no drawing, no decoration
- Allow imperfection: missed a day? No penalty. Open tomorrow's page and continue.
- Ryder Carroll: limit 3 habits tracked simultaneously, first week is a test phase

### Long-term Waiting Items (📌 长期待办)

When user mentions tasks with **unknown/unfixed timelines** ("排期不知道什么时候", "等通知", "等那边排下来"), do NOT put them in:
- ❌ 今日三件事
- ❌ 任务清单
- ❌ 月度行动计划的时间槽

Instead, create a dedicated section in the **monthly plan**:

```markdown
### 📌 长期待办（排期/审批未定，不进日常）

- [ ] 讲课「主题」— 等排期通知，到时再排入日常
- [ ] 课题申报 — 等方向确定后再动
```

**Why**: P-people get anxious when "waiting" items sit alongside actionable tasks. Separating them into a dedicated "📌" section visually removes the pressure while keeping visibility. When the timeline becomes known, move the item into the appropriate time-slot section.

**Trigger keywords**: "排期", "等通知", "不知道什么时候", "等那边", "等审批", "等回复"

### Time-slot task organization (for users with very limited free time)**:

When the user has <4 hours/day of personal time, traditional priority labels
(紧急/重要/待启动) can be overwhelming. Replace or augment with time-slot grouping:

```
🌙 晚上黄金（e.g. 20:00-22:00）— highest-focus work (论文, deep work)
🏥 上班摸鱼（idle moments at work）— machine-monitored tasks (3D打印), quick writing
📅 周末大块（half-day on weekends）— video recording, content creation
☕ 碎片时间（commute/lunch/bedtime）— short courses, language, habit tracking
⏸️ 暂停线 — things the user still wants but has consciously deferred
🔄 后台挂机 — things that need no active push (waiting on others, long-term growth)
```

Key principles:
- Every task goes into exactly one slot — no "when I have time" ambiguity
- The user only looks at the current slot's list
- Slots don't compete: 3D打印 in 摸鱼 doesn't steal from 论文 in 晚上
- The ⏸️ line is NOT a failure — it's an honest inventory. The user can see everything
  they want to do without feeling they must do it all now

**Side-hustle/career planning in BuJo**: When user discusses career change or side income, add a `🚀 副业探索` section to the monthly plan with parallel numbered lines. See `references/bujo-side-hustle-framework.md` for the full pattern.

### Meeting Notes Ingestion

When the user shares meeting notes from external AI tools (Yuanbao 元宝, Tencent Meeting, etc.):

1. **Read the raw notes** — usually very long (300-600 lines) with AI commentary mixed in
2. **Strip AI meta-commentary** — remove "值得注意的是", "暗示了", "隐含了", and other AI analysis filler from tools like Yuanbao meeting assistant
3. **Structure by speaker/topic** — group content under each presenter with their key points, data, and conclusions
4. **Save to `子弹笔记/会议/`** — filename: `YYYY-MM-DD 会议名称.md`
5. **Frontmatter** — include `title`, `date`, `type: 会议记录`, `tags`, `platform`, `source`
6. **Add action items** — end with a `## 🔑 对我的启发` section with `- [ ]` items for follow-up
7. **Update daily note** — append to the `## 📝 笔记 · 事件 · 感想` section with a wikilink to the meeting record: `[[YYYY-MM-DD 会议名称|📄 会议纪要]]`

**Key pitfall:** Raw AI meeting notes (especially from Yuanbao) contain a LOT of filler analysis. The meeting assistant tends to add commentary like "这暗示了...", "从前后发言对比看...", "值得注意的是..." — strip all of these. Keep only the substantive content (data, conclusions, decisions).

## Trigger Keywords

"子弹笔记", "BuJo", "bullet journal", "年度计划", "月度计划", "daily planning", "任务管理", "习惯追踪", "P人", "ADHD 效率", "GTD alternative", "want to plan/organize/manage tasks with Obsidian", "副业", "职业规划", "career change", "side hustle"

### Minimalist Organization

When organizing files, follow minimalist principles: one entry page + one file directory, avoid duplicate directories, prefer flat structure. Don't create parallel folder trees for content that already has a canonical location.

**When the user wants diaries under `子弹笔记/`**: move them. The user's preference is for a single BuJo root with diaries as a subfolder (`子弹笔记/日记/`), not a separate `01 日记/` folder at vault root. When relocating: (1) `mv` all diary files into `子弹笔记/日记/`, (2) update `.obsidian/daily-notes.json` folder field, (3) update all Dataview queries in 仪表盘.md, (4) `rmdir` the old folder. Don't leave stale directories — they create confusion when Calendar generates to the old path.

### Vault Consolidation Workflow

When the user wants to reorganize their vault (merge folders, eliminate duplicates, rename directories), follow this checklist. The goal is a clean top-level with 3 visible zones + system dirs.

**Standard moves**:
1. **Move folders** — `mv` the source into the target. Always `mkdir -p` first.
2. **Merge duplicate directories** — e.g. root `Clippings/` and `raw/clippings/`. For each file in the source, check if it exists in the target before copying:
   ```bash
   for f in SourceDir/*.md; do
     base=$(basename "$f")
     [ ! -f "TargetDir/$base" ] && cp "$f" "TargetDir/$base" && echo "NEW: $base" || echo "SKIP: $base"
   done
   ```
3. **Update `.obsidian/daily-notes.json`** — if diary folder moved, change the `folder` field.
4. **Update Dataview queries** — `FROM "old_path"` → `FROM "new_path"` in 仪表盘.md (use `replace_all=true` if multiple occurrences).
5. **Update dashboard quick links** — add new entries (会议, 看板, 运动, 白板) to the shortcut section.
6. **Update CLAUDE.md** — mirror the new directory tree.
7. **Update memory** — sync the vault structure summary so future sessions use the right paths.
8. **Clean up** — `rm -rf` empty old directories. Check for `.DS_Store` remnants.

**Renaming user-visible folders**: if the user wants to see `微信读书/` instead of `carl-weread/` in the Obsidian sidebar, rename it. But check if any skill scripts hardcode the path first (grep the skill's SKILL.md and scripts/). If they do, either patch the skill or keep the old name. For `wiki/` → `维基库/`, note that llm-wiki scripts reference `wiki/` — don't rename this one.

**Obsidian plugin installation** (without opening the app):
1. Add the plugin ID to `.obsidian/community-plugins.json` array.
2. Obsidian will download the plugin files on next launch.
3. Common plugin IDs: `pdf-plus` (PDF++), `obsidian-book-search-plugin` (Book Search for covers).
4. Find IDs: `curl` the community-plugins.json from obsidian-releases and grep.

### Plugin Evaluation (\"Do I still need this plugin?\")

When the user asks whether an existing or potential Obsidian plugin is still worth using given Hermes capabilities:

1. **Research the plugin** — GitHub README, official docs, feature list (free vs pro tiers)
2. **Map features to Hermes equivalents** — what can Hermes already do via chat/Telegram?
3. **Identify irreplaceable features** — UI-only features (heatmaps, progress bars, visual dashboards) that Hermes cannot replicate
4. **Consider the user's actual workflow** — how do they interact with their vault? (This user: primarily Telegram, not opening Obsidian directly)
5. **Give a clear yes/no with rationale** — don't hedge. If Hermes covers 80%+ of the use case with less friction, recommend against the plugin.

Key insight for this user: they interact with their vault primarily through Telegram → Hermes, not by opening Obsidian. Any plugin whose core value is \"faster input inside Obsidian\" is superseded by the chat channel. Plugins that provide visualizations (graphs, calendars, heatmaps) still add value since Hermes is text-only.

**Thino-specific conclusion** (saved here as reference): Thino's core value is quick-capture inside Obsidian. The user's Telegram→Hermes pipeline is faster (native app, no vault-opening required). Pro features like heatmaps and progress bars are nice-to-have UI. Verdict: not needed, but keep Pro account for future optional use.

When user reports Obsidian sync issues (Fast Note Sync, Obsidian Sync, or other):

- Check plugin install status: `grep "plugin-id" "$VAULT/.obsidian/community-plugins.json"`
- Check config: plugin `data.json` + Obsidian's internal settings
- Verify server/container: Docker, VPS connectivity
- For Fast Note Sync specifically: `references/fast-note-sync-diagnostics.md`

### Obsidian Web Clipper Configuration

The user uses Obsidian Web Clipper browser extension to capture web content. Common pitfalls:

- **Vault misconfiguration**: Web Clipper's vault setting must be `<vault-name>` (the vault name), NOT `raw/AI` (that's a folder path, not a vault). If the vault is set to a path, Obsidian errors with "Unable to find a vault."
- **Folder path casing**: Default folder should be `raw/AI` (or other topic folder). raw/ is organized by topic, not by source.
- **YouTube limitation**: Web Clipper captures page metadata and structure, NOT video subtitles/transcripts. For YouTube transcripts, use Hermes's `youtube-content` skill instead, saving to `raw/AI/` or `raw/通用/`.

### Bulk Web Scraping to Vault

When asked to pull an entire blog index into the vault (e.g. "把这些拉下来放进知识库"):

1. Extract article URLs from the index page with `browser_console`
2. Use `scripts/chrome-headless-scraper.py` — edit the ARTICLES list, run in background
3. Output lands in `raw/<topic>/` (e.g. `raw/AI/`, `raw/编程/`)

Full workflow: `references/bulk-web-scraping.md`

Post-ingest: when the user archives content but hasn't read it and asks "when do I start?", see `references/post-ingest-digestion-scheduling.md` for the tiered scheduling pattern (light vs deep digestion, time-slot mapping, BuJo update steps).

Key insight: Next.js SSR blogs (like Anthropic's engineering blog) render content server-side. Chrome `--dump-dom` + BeautifulSoup is faster and more reliable than the Node.js CDP pipeline for bulk operations. Fall back to `baoyu-url-to-markdown` for CSR-only sites.

### Meeting Notes from AI Summaries

When user sends raw AI-generated meeting summaries (元宝/Yuanbao, Kimi, etc.) and asks to organize and save to Obsidian, follow `references/meeting-notes-processing.md`. Key: strip AI-flavor commentary aggressively, restructure by speaker/topic, preserve concrete data points, save to `子弹笔记/会议/`.

### Douyin (抖音) Content Extraction

When the user shares Douyin video links, extract and archive the content. Full workflow: `references/douyin-content-extraction.md`

### Bilibili (B站) Video Extraction

Bilibili videos have NO transcript API. Use browser automation, not youtube-content skill. Full workflow: `references/bilibili-content-extraction.md`

Save to: `raw/<topic>/YYYY-MM-DD-标题关键词.md` (e.g. `raw/AI/`, `raw/编程/`)

### Learning Plan Creation

When the user shares tutorial repos, course links, or learning resources and wants a structured plan: research the repos (GitHub API for structure, Brave search for context), create a week-by-week plan with checkboxes, save to `wiki/{Topic}学习计划.md`, and set up daily cron reminders. Full workflow and template: `references/learning-plan-creation.md`. For cron job execution (finding the file on the server, parsing progress, composing reminders): `references/learning-plan-reminder.md`.

Key principles for this user: 1 hour/day max (P-person with <4h personal time), map to lunch/evening/bedtime slots, cross-reference with existing deadlines (thesis, courses), use checkboxes not rigid schedules.

### 数字分身 (Digital Twin) Workflow

User wants Hermes to act as their "数字分身" — save content now, be reminded later. When user shares links (WeChat articles, Bilibili videos, course recommendations):

1. **Save immediately** to `raw/` (wechat/, Bilibili/, etc.)
2. **Create wiki pages** for important content
3. **Update wiki/index.md** and `wiki/log.md`
4. **Remind user later** when relevant context arises (e.g., "You saved a PPT Skill video when you start making 品管圈 PPT")

Key phrase: "作为我的数字分身，作为我的第二大脑，我希望能随时地你帮我想起我想不起来的事情"

**One-Page Workspace (一页纸工作台) Pattern**

⚠️ **TWO DASHboards exist** — user has both:
- `子弹笔记/一页纸工作台.md` — Obsidian markdown version (Dataview-driven, secondary)
- `工作台.html` — standalone HTML version in vault root (PRIMARY, opened in browser)

**When user says "工作台", they mean the HTML file.** All dashboard content updates target `工作台.html`, not the markdown file. The markdown version is a fallback for Obsidian-only context.

The HTML dashboard is fully static/hardcoded — sections must be manually added/updated via `skill_manage` or direct file edits. It uses `obsidian://` deep links for quick navigation.

When user wants an all-in-one dashboard that shows everything on open:

1. **Create `子弹笔记/一页纸工作台.md`** with these sections:
   - 今日三件事 (Today's top 3 — Ryder Carroll style, Dataview TASK query)
   - 所有未完成任务 (All open tasks)
   - 项目追踪 (Project status table with deadlines)
   - 每日读书 (Reading cards from `微信读书/reading-cards/` — Dataview TABLE)
   - 播客 & 演讲压缩 (Compressed summaries from `raw/AI/` — Dataview LIST filtered by "压缩")
   - 知识库最近消化 (Recent wiki ingestions — Dataview LIST from `wiki/` sorted by ctime DESC)
   - 习惯追踪 (Habit tracker)
   - 快速入口 (Quick links including knowledge graph HTML)
   - 数据看板 (Stats using Dataview inline queries)
   - 灵感收集箱 (From `子弹笔记/收集箱`)

2. **Set as default homepage**: modify `.obsidian/workspace.json`:
   ```json
   "state": {
     "type": "markdown",
     "state": {
       "file": "子弹笔记/一页纸工作台.md",
       "mode": "source"
     }
   }
   ```

3. **Key Dataview queries for dashboard**:
   ```dataview
   TASK FROM "子弹笔记/日记" WHERE !completed AND file.day = date(today) LIMIT 5
   TASK FROM "子弹笔记" WHERE !completed GROUP BY file.link LIMIT 15
   LIST FROM "子弹笔记/日记" WHERE file.day.month = date(today).month SORT file.day DESC
   ```
   
   **每日读书** (reading cards):
   ```dataview
   TABLE book AS "书/来源", date AS "日期"
   FROM "微信读书/reading-cards"
   SORT date DESC
   LIMIT 10
   ```
   
   **播客/演讲压缩** (compressed summaries):
   ```dataview
   LIST
   FROM "raw/AI"
   WHERE contains(file.name, "压缩")
   SORT file.ctime DESC
   LIMIT 5
   ```
   
   **知识库最近消化** (recent wiki ingestions):
   ```dataview
   TABLE file.ctime AS "入库时间"
   FROM "wiki"
   WHERE file.name != "index" AND file.name != "log" AND file.name != "overview"
   SORT file.ctime DESC
   LIMIT 10
   ```

3. **User preference**: This user prefers "极简" (minimalist) — one entry page + one file directory. Avoid creating duplicate directories (e.g., don't create `attachments/macos-shortcuts/` when `infographic/` already exists).

4. **HTML Dashboard Alternative**: When user wants a more visually appealing dashboard, create an HTML version with:
   - Modern UI: gradient backgrounds, card layouts, rounded corners, shadows
   - Responsive design: adapts to phone, tablet, desktop
   - Interactive: hover animations, click feedback, smooth transitions
   - Real-time clock display
   - Place HTML file in **root directory** (not attachments/) for easy access
   - Create `首页.md` as entry page with link/button to open HTML dashboard
   - Set `首页.md` as default homepage in workspace.json
   - **IMPORTANT**: Create `启动工作台.sh` launch script (local HTTP server) so `obsidian://` deep links work. `file://` protocol blocks custom protocols. Template at `templates/launch-dashboard.sh`. See `references/html-dashboard-obsidian-protocol-fix.md`.
   - **Content updates**: HTML dashboard is static — all sections (今日焦点, 读书, 播客, 知识库动态) must be manually updated in the HTML file. Dataview does NOT work in standalone HTML.

4. **Style**: don't use plain Markdown for dashboards — create HTML with modern aesthetics. Avoid generic AI-flavored design ("AI味"); aim for a humanistic, crafted feel. One ready-made option: the [Apex Dashboard](https://github.com/PandoraReads/apex-dashboard) plugin — 11 curated themes with warm options like 大地 (parchment) and 春日 (rose).

   **File placement**: put the dashboard in the vault root directory as the first page, not buried in subdirectories.

   See `references/html-dashboard-pattern.md` for full HTML template and setup instructions.

### Multi-AI Context Sync

When user works across multiple AIs (Hermes, Gemini, Feishu, etc.) and information becomes scattered, consolidate into a unified `wiki/个人/个人档案.md` as the single source of truth. Each AI's memory is a domain-specific projection of this profile. See `references/multi-ai-context-sync.md` for the full workflow: parsing external AI prompts, cross-checking against existing data, merging contradictions, and maintaining the profile.

Key pitfall: external AI memories may contain outdated/incorrect facts (e.g., Gemini had "纽约" when user is in "泰州"). Always cross-check before importing.

### Daily Learning Injection Pattern

When user wants to learn a subject through daily automated content (fables, stories, flashcards, etc.):

1. **Create organized folder structure** in `wiki/`:
   ```
   wiki/学习方法的寓言小故事/
   ├── README.md          ← prompt template + instructions
   ├── 统计学/
   │   ├── 概念名.md
   │   └── ...
   ├── 大语言模型/
   └── ...
   ```

2. **Create README.md** with:
   - Current field setting
   - Prompt template (adjustable with `{领域}` placeholder)
   - Directory structure explanation
   - Tag convention

3. **Set up cron job** for daily generation:
   - Schedule: `0 8 * * *

- **PDF generation with Chinese fonts on macOS** — when generating PDFs with Chinese text, use `fpdf2` with macOS system fonts: `/System/Library/Fonts/Supplemental/Songti.ttc`. Install: `pip3 install fpdf2`. Font path is critical — using wrong path causes garbled text or missing characters. For .doc/.docx conversion, use `textutil -convert txt` first to extract content, then generate PDF programmatically.

- **Daily note auto-sync via cron** — when the user wants todos automatically written to daily notes, use a Python script to scan `子弹笔记/项目/` and `子弹笔记/收集箱.md` for unchecked items, then write a `## 📋 待办事项（自动同步）` section into the daily note. See `references/bujo-cron-briefing.md` for the full script-based pattern and push filtering rules. Key preference: don't push daily habits (训练/饮食/日语) — too noisy.
- **Daily note filename weekday MUST be English** — the Calendar plugin uses Moment.js `ddd` token which produces English abbreviations (Mon, Tue, Wed...). Scripts like `daily_todo_scanner.py` must NOT use Chinese weekdays (周一, 周二). If a script creates daily notes, use `["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][weekday]` not `["周一","周二",...]`. Chinese weekday filenames cause Calendar to not recognize the file, breaking date navigation. Also: frontmatter tags should only contain `日记` — never embed the weekday or year/month in tags (e.g. avoid `周二`, `2026`, `5月`).
- **Dashboard must be Dataview-driven** — the 一页纸工作台 should NEVER have hardcoded task lists (like "今日三件事：1. xxx 2. xxx"). All dynamic content must use Dataview `TASK FROM "子弹笔记/日记" WHERE !completed AND file.day = date(today)` queries. Hardcoded content goes stale immediately and confuses the user.
- **Daily note duplication** — when Hermes writes a daily note and the user has the Calendar plugin, two files can emerge: `2026-05-21.md` (Hermes-created) and `2026-05-21_Thu.md` (Calendar-created). Always check the `daily-notes.json` config first for the **exact filename format** (`format` field, e.g. `YYYY-MM-DD_ddd`). Before writing any daily note, search the diary folder for files matching today's date. If Calendar already created one (even if empty/template-only), **fill that file, don't create a new one**. The `created` frontmatter field in Calendar-generated files uses the same format string (e.g. `\\\"2026-05-21_Thu\\\"`), which serves as a secondary signal.
- **Wrong day-of-week suffix** — the `ddd` token in Moment.js produces the **abbreviated English weekday** (Mon, Tue, Wed, Thu, Fri, Sat, Sun). Getting the weekday wrong (e.g. writing `2026-05-24_Sat.md` when it's actually Sunday) creates a file the Calendar plugin won't recognize, so clicking that date in Calendar will prompt "create new" instead of opening the existing note. **Always verify the actual day of week** before creating a daily note: `date +%a` returns the correct abbreviation for today. If a wrong-suffix file was created, delete it and write to the correct filename.
- **Cron script weekday format** — `scripts/daily_todo_scanner.py` must use English weekday abbreviations (`Mon`,`Tue`,`Wed`...) to match Calendar's `ddd` token. Chinese weekdays (`周一`,`周二`) in the filename break Calendar integration. If the script outputs Chinese weekdays, fix the `weekday_en` line. Also: daily note frontmatter tags should only contain `日记` — do NOT add weekday tags (`周二`), year (`2026`), or month (`5月`). These pollute tag search and are redundant with the filename date.
- **Wiki AI subdirectory structure** — `wiki/AI/` is the largest topic folder and needs internal sub-categories: `agent/` (智能体架构), `编程工具/` (Claude Code, Cursor), `prompt工程/`, `硬件/`, `知识库构建/`, `学术研究/`, `评测/`, `RAG/`, `行业观察/`. Each subdirectory gets an `index.md`. Other wiki topic folders stay flat unless they accumulate 10+ files. After creating subdirectories, update `wiki/AI/index.md`, `wiki/index.md`, and `CLAUDE.md`.

**Wiki → HTML export** — user wants wiki/ knowledge pages exported as beautiful HTML for reading. Use `huashu-md-html` skill's batch conversion. **Folder-per-note structure**: each note gets its own folder with md + html together, NOT `00-` prefix flat layout. Script: `scripts/restructure_wiki_folders.sh` in vault root. First batch: 93 files converted 2026-06-01. YAML frontmatter conflicts (mid-file `---` delimiters) fixed with `pandoc -f markdown-yaml_metadata_block`. Template path: `huashu-md-html/templates/article/template.html5`.

**HTML workbench ↔ Markdown workbench sync** — `工作台.html` and `子弹笔记/一页纸工作台.md` MUST have identical content. When updating one, update the other. The HTML version uses `obsidian://` deep links (requires local HTTP server via `启动工作台.sh`). Both share: 今日焦点(3 items) → 今日任务 → 项目追踪(4 projects) → 备忘 → 每日读书 → 播客压缩 → 寓言故事 → 知识库动态 → 快速入口. The HTML version has dynamic date via JS (auto-detects UTC+8).

**Raw→Wiki content promotion** — when raw/<topic>/ accumulates enough files, create wiki/<topic>/ subdirectories with提炼d content. Do NOT move files from raw/ to wiki/ — raw stays as-is, wiki pages are new summaries. Create index.md in each subdirectory listing files with 1-line descriptions.
- **Raw clips may have broken image references** — when a web clipper or export tool saves an article to `raw/AI/`, the images/ subdirectory often stays in the original output location (e.g. `~/output/`), NOT in the Obsidian vault. The raw .md references `![Image](images/img_001.png)` which only resolves if images/ is alongside the md file. **Always verify** that referenced images exist in `attachments/` or in a local images/ folder next to the raw .md. If missing, copy them to `attachments/` and update the image paths in the md to `![[filename.png]]` format. See `disk-hygiene` skill for the full cross-reference audit workflow.

**Renaming daily notes: filename AND content** — when fixing Chinese weekday daily notes (`2026-05-28_周四.md` → `2026-05-28_Thu.md`), you must update BOTH the filename AND all content inside: the heading (`# 2026-05-28 周四` → `# 2026-05-28 Thu`), frontmatter tags (remove weekday/year/month tags), and any other Chinese weekday references. Just renaming the file is insufficient — the user will see the old weekday in the heading.
- **Duplicate daily note files (Calendar vs cron)** — When Calendar creates an empty template file (`2026-05-27_Wed.md`) and the cron script creates one with content (`2026-05-27_周三.md`), two files exist for the same date. **Resolution**: merge the cron file's content into the Calendar file (correct filename), then delete the cron file. Never leave both — Calendar clicks will open the empty one.
- **Dashboard hardcoded content** — The `一页纸工作台.md` "今日三件事" section must be driven by Dataview queries, NOT hardcoded text. Hardcoded content goes stale immediately. If you find hardcoded task text in the dashboard, remove it and let the `TASK FROM "子弹笔记/日记" WHERE !completed AND file.day = date(today)` query handle it dynamically.
Dashboard missing knowledge/reading sections — User will complain if the dashboard only shows tasks and projects. It MUST also include: 每日读书 (reading cards), 播客/演讲压缩 (compressed summaries), 知识库最近消化 (recent wiki ingestions). These sections use Dataview queries against `微信读书/reading-cards/`, `raw/AI/` (filtered by "压缩"), and `wiki/` respectively.
- **Two dashboards — know which one** — User has `工作台.html` (browser, static HTML) AND `子弹笔记/一页纸工作台.md` (Obsidian, Dataview). When user says "工作台" they mean the HTML file. When they say "Obsidian里的工作台" they mean the markdown file. Editing the wrong one wastes time. See `references/html-dashboard-pattern.md` for the HTML dashboard pitfalls.
- **`obsidian://` links don't work from `file://`** — Browsers block custom protocol handlers from local files. Solution: serve via local HTTP server. See `references/html-dashboard-pattern.md` for the `启动工作台.sh` pattern.
- **Knowledge graph needs periodic rebuild** — `wiki/knowledge-graph.html` embeds stale data. After wiki ingestions, run `build-graph-data.sh` + `build-graph-html.sh`. Added auto-rebuild to `daily_todo_scanner.py` (8AM daily).
- **Knowledge graph HTML staleness** — The interactive knowledge graph HTML (`wiki/knowledge-graph.html`) embeds `graph-data.json` inline. If you update the JSON but don't rebuild the HTML, the graph shows stale data. Always run BOTH: `build-graph-data.sh` THEN `build-graph-html.sh`. See llm-wiki skill for the rebuild commands.
- **Blank daily notes — template directory missing** — when user reports new daily notes are empty/have no template content, the `00 templates/` directory (or its contents) may have been deleted. Diagnosis: (1) read `.obsidian/daily-notes.json` to confirm the `template` field still points to the right path, (2) check whether that directory and file actually exist on disk. If config is correct but the directory/file is gone, recreate from this skill's `templates/bujo-daily-template.md`. The `.json` config is rarely the culprit — it's almost always the filesystem that lost the folder.
- **Corrupted line-number artifacts in vault files** — Obsidian vault files edited via `patch` or other tooling can develop duplicated line-number prefixes on every line (`    48|    48|    48|...`). This happens when a previous merge operation injected its line-number markers into the file content. `patch` will fail with "Could not find a match" because it's trying to match clean text against prefix-contaminated lines. Don't keep retrying `patch` — the file is structurally corrupted and must be rewritten. Use `references/fix-line-number-artifacts.md` for the `cat` + regex-strip recipe.
- **Cache HIT but wiki pages missing** — when ingesting into llm-wiki, the cache may say HIT from a previous interrupted session, but actual wiki pages (`wiki/sources/`, `wiki/entities/`) were never written. Verify page existence even when cache says HIT. If index has entries but files are missing, force re-ingest.
- **Don't split vaults for organization** — folders within a single vault handle that. Only split for sync/sandboxing reasons.
- **Two dashboards exist — user means the HTML one** — `工作台.html` (vault root, browser) is the PRIMARY dashboard. `子弹笔记/一页纸工作台.md` is secondary (Obsidian-only). When user says "工作台" or complains about dashboard content, check/edit the HTML file first. The HTML is fully static — sections like 每日读书, 播客压缩, 知识库动态 must be hardcoded in HTML, not via Dataview.
- **`file://` blocks `obsidian://` protocol** — When HTML dashboard is opened via `file:///path/to/工作台.html`, browsers block the `obsidian://` custom protocol entirely. No JS workaround helps (setTimeout, window.location.href, window.open all fail). **Solution**: serve via local HTTP server (`python3 -m http.server 8088`). Create `启动工作台.sh` in vault root. See `references/html-dashboard-obsidian-protocol-fix.md`.
- **Knowledge graph HTML needs periodic rebuild** — `wiki/knowledge-graph.html` is self-contained (embeds `graph-data.json` inline). It does NOT auto-update when wiki pages change. Rebuild: run BOTH `build-graph-data.sh` THEN `build-graph-html.sh`. Already added to `daily_todo_scanner.py` so graph rebuilds every morning at 8am with the cron job. User doesn't need to manually trigger.
- **Don't create vaults inside vaults** — if the user has an Obsidian vault, recommend they use it rather than creating a new one for llm-wiki.
- **Daily Notes without a template is noise** — always set up a minimal daily note template with frontmatter and a section for tasks.
- **Tasks without Dataview = manual tracking** — always pair them. Dataview's `TASK FROM 子弹笔记/日记` query turns daily scribbles into a living agenda.
- **Don't over-structure upfront** — start with 3-4 folders, let the schema grow organically. Empty folders demotivate.
- **Default vault path is unreliable** — `OBSIDIAN_VAULT_PATH` env var is often unset. The skill's fallback (`~/Documents/Obsidian Vault`) is rarely the real path. **Always check memory first** for the user's actual vault path. If memory is absent or stale, probe with `find ~/Documents -name ".obsidian" -type d -maxdepth 3 2>/dev/null` and check iCloud paths (`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/`). See `references/vault-locations.md` for details.
- **Vault path can change** — users migrate between iCloud and local storage. If memory has an old path, probe the new one before assuming it's still valid.
- **Vault search returned nothing but user mentioned documents?** — the data may be Office files (`.docx`, `.xlsx`, `.rtf`, `.pptx`) elsewhere on the filesystem. See `references/macos-office-doc-extraction.md` for the macOS extraction workflow (textutil first, write-then-run for .xlsx).
- **PDF text extraction** — `pdftotext` is not on base macOS. Fallback chain: pdftotext → pymupdf (fitz). `textutil` and `python-docx` do NOT handle PDF. See `references/pdf-extraction-macos.md`.
- **Ultra-tall PDF screenshots** — when the user sends a screenshot-as-PDF of a long article (540×30,000px), the embedded JPEG needs chunked OCR. See `references/pdf-ocr-ultra-tall.md` for the 4000px slicing pipeline.
- **Batch web scraping to clippings** — when ingesting an entire blog index (20+ articles), use Chrome headless + CSS selectors + retry logic. See `references/batch-web-scraping-clippings.md` for the full scraper + ingest pattern.
- **Chinese grant call extraction** — recurring pattern for this user: fetch .cn URLs, strip HTML, extract deadline/funding/eligibility, cross-reference with thesis. See `references/grant-call-extraction.md`.
- **tesseract OCR CLI syntax** — the language flag is `-l chi_sim`, NOT `--lang=chi_sim`. The long-form flag doesn't exist and silently fails. Always use `tesseract <image> - -l chi_sim`. Also note: if vision_analyze returns 401 (invalid API key), fall back to tesseract immediately rather than retrying vision_analyze.
- **Academic materials intake** — when user shares teacher/administrative notices about thesis formatting, defense requirements, or submission deadlines: (1) copy attached images to BOTH `attachments/` (for Obsidian wikilinks) AND the external project directory (e.g. `/扬大硕士/通知文档/`), (2) create a project tracking note in `子弹笔记/项目/` with checklists for each requirement, (3) embed images with `![[filename.jpg]]` syntax, (4) include the external file path for reference. See `references/academic-materials-intake.md`.
- **Tags can be bilingual** — users may mix Chinese and English tags (e.g. `obsidian`, `Obsidian同步`, `效率`). Match their tagging convention rather than imposing purely English tags.
- **Web scraping into vault** — when baoyu-url-to-markdown fails (missing deps, JS render issues), fall back to Chrome headless + BeautifulSoup. See `references/headless-chrome-scraping.md` for the full pipeline: CSS selector pitfalls, retry logic, and batch script template.
- **Web scraping to vault** — when user asks to pull all articles from a blog/resource page into vault. Uses Chrome headless + BeautifulSoup with CSS selectors. See `references/web-scraping-to-vault.md`.
- **URL-to-markdown fallback for JS-rendered pages** — when baoyu-url-to-markdown fails (missing deps like `jsdom`, bun issues), fall back to browser automation: `browser_navigate` → `browser_console` with JS extraction. For article content, use `document.querySelector('article')` and walk the DOM tree extracting headings/paragraphs/lists/code blocks into structured text. Truncate to ~15K chars. Works well for Next.js SSR docs (Anthropic, OpenAI). Save to `raw/clippings/<topic>/` with YAML frontmatter (title, source, captured_at, category, tags).
- **Fast Note Sync self-hosted sync** — diagnosis, token/auth repair, and migration workflow. See `references/fast-note-sync-diagnostics.md`.
- **ModelScope/AMD 免费 GPU** — 激励计划细则、计时规则、领取路径。见 `references/modelscope-amd-gpu.md`。
- **Patching BuJo calendar tables** — monthly calendar rows like `|| 25 | |` are often identical to the 10+ other empty rows. `patch` will find many matches and refuse. Fix: include enough unique surrounding context (e.g. the filled-in row from the day before, like `|| 22 | Anthropic...`). Or use `replace_all=true` if genuinely replacing a pattern that appears only in the target range.
