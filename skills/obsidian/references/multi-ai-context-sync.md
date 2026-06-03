# Multi-AI Context Sync → Obsidian

## Problem
User works with multiple AI assistants (Hermes, Gemini, future Feishu bot), each accumulating separate memories and context. Information becomes scattered — user can't remember which AI discussed what, and scrolling through chat histories is exhausting (especially on mobile).

## Solution: Unified Personal Profile in Obsidian
Consolidate all AI-relevant personal context into a single Obsidian wiki page that any AI can reference.

### Template: `wiki/个人/个人档案.md`

```yaml
---
title: 个人档案
category: 个人
tags: [personal/profile, digital-twin]
updated: YYYY-MM-DD
---
```

Sections to include:
1. **基本信息** — name, ID, location, workplace, profession
2. **教育背景** — schools, majors, status, advisors, thesis topic
3. **家庭** — family members, daily time constraints
4. **技术栈与工具** — core tools (what's used), deprecated tools (what's abandoned + why), hardware inventory, AI tool stack
5. **兴趣与项目** — active hobbies with current status/progress
6. **近期项目** — table with deadline + status
7. **沟通偏好** — explicit style rules (scannability, no fluff, professional but empathetic)
8. **AI Persona 配置** — which AI handles what (e.g., Hermes=orchestrator, Gemini=nutrition coach, Feishu=data tables)

### Workflow: Syncing from Other AIs

When user shares a "context sync" or "persona prompt" from another AI (e.g., Gemini system prompt):

1. **Parse** — extract structured facts (not prose)
2. **Cross-check** against existing memory and Obsidian notes — flag contradictions (e.g., Gemini said "纽约" but user is in 泰州)
3. **Merge** — update the unified profile, noting source
4. **Correct** — fix outdated/incorrect information
5. **Log** — append to `wiki/log.md`

### Key Principle
The Obsidian profile is the **single source of truth**. Each AI's memory/persona is a *projection* of this profile optimized for its domain. When conflicts arise, Obsidian wins.

### Integration with BuJo
- Daily notes reference the profile via wikilinks: `[[个人档案]]`
- Meeting notes, project notes can link to relevant profile sections
- The profile is NOT a daily-updated document — it changes when fundamental facts change (new tool, new project, abandoned habit)
