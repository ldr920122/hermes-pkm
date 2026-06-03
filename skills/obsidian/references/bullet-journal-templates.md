# Bullet Journal Templates for Obsidian

Concrete templates and files built for a real BuJo deployment inside an existing
llm-wiki vault. Based on Ryder Carroll's original methodology + elainooooo's tutorial.

## Vault Layout After Setup

```
vault/
├── 子弹笔记/                    ← BuJo framework (separate from wiki/)
│   ├── 使用指南.md              ← First-time user guide
│   ├── 仪表盘.md                ← Dataview dashboard (auto-aggregates tasks)
│   ├── 年度.md                  ← Future Log (annual overview)
│   ├── 月度迁移仪式.md          ← Monthly migration ritual (4-step checklist)
│   ├── 收集箱.md                ← Brain dump inbox
│   ├── 月度/                    ← Monthly logs
│   │   └── 2026-05.md
│   └── 项目/                    ← Project-specific notes
├── 01 日记/                     ← Daily notes (existing, template updated)
└── 00 templates/
    ├── 子弹笔记-日记模板.md
    └── 子弹笔记-月度模板.md
```

## Required Plugins

| Plugin | Role | Type |
|--------|------|------|
| Daily Notes (core) | Auto-generate daily journal | Core |
| Templates (core) | Template auto-fill | Core |
| Calendar | Date picker sidebar | Community |
| Tasks | Enhanced task management | Community |
| Dataview | Dashboard queries (TASK FROM, LIST FROM) | Community |
| QuickAdd | Quick capture to inbox | Community |

## Daily Notes Config

```json
{
  "format": "YYYY-MM-DD_ddd",
  "folder": "01 日记",
  "template": "00 templates/子弹笔记-日记模板"
}
```

## Daily Template Structure

Frontmatter with `tags: [日记, 子弹笔记]`, then:
1. 🎯 今日三件事 (top 3 priorities, Ryder Carroll: "what makes today successful")
2. 📋 任务 (checklist with Tasks plugin markers)
3. 📝 笔记·事件·感想 (free-form daily log — built-in emotional context)
4. 🔄 明日预览 (30s before bed, reduces morning decision cost)

## Monthly Template Structure

Left page: calendar timeline (31 rows, one noteworthy event per day)
Right page: monthly action plan + habit tracker (max 3 habits, 30-day commitment)

## Migration Ritual (4 Steps)

1. Review last month's daily notes → find unfinished tasks → decide: complete/migrate/cancel
2. Check Future Log → migrate current month items to monthly log
3. Review last month's monthly log → migration decisions
4. Create new monthly log from template, fill in migrated items

## Brain Dump → Priority Workflow

When user dumps everything on their mind:
1. Dump everything into `收集箱.md` verbatim
2. Classify: 🚨urgent+important / 🔴important / 🟡waiting / 🔵aspirational / ✅daily habits
3. Move actionable items to monthly log and annual Future Log
4. Present the user with a clear single "do today" item
5. Everything else stays in 收集箱, reducing mental load

## P-Person Friendly Design Principles

- Zero-friction capture: Calendar click → template ready
- No forced categorization: inbox first, sort later
- Minimal ritual: 3 min daily, 10 min monthly
- Auto-aggregation: Dataview collects tasks across vault
- Forgiveness: missed days aren't failure, just resume
