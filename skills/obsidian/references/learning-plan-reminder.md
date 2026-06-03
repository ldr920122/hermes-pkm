# Learning Plan Daily Reminder — Cron Job Execution

When a cron job fires to remind the user about their learning plan, follow this workflow.

## 1. Find the learning plan file

The plan lives at `wiki/{Topic}学习计划.md` inside the Obsidian vault. The cron job runs on the server, not the user's Mac, so you must locate the vault path.

**Vault path discovery** (in order of reliability):
1. Check memory for saved vault path
2. Probe known locations:
   ```bash
   ls "$HOME/Documents/obsidian/wbaoc-wiki/wiki/"*学习计划* 2>/dev/null
   ```
3. Fallback search (slow):
   ```bash
   find "$HOME/Documents" -name "*学习计划*" -path "*/wiki/*" 2>/dev/null | head -5
   ```

**Pitfall**: The `obsidian` skill says vault path is `OBSIDIAN_VAULT_PATH` env var, but on cron servers this is often unset. The actual path is typically `/Users/wbaoc/Documents/obsidian/wbaoc-wiki/`.

## 2. Read and parse the plan

The plan file has these key sections:
- **阶段/Week sections**: Markdown checkboxes (`- [ ]` / `- [x]`) organized by week and day
- **学习进度追踪**: A table at the bottom logging what was learned each day
- **与现有任务的协调**: Priority ordering with other commitments

**Determine current position**:
1. Scan all `- [ ]` and `- [x]` checkboxes
2. Find the first unchecked item — that's the current task
3. Count checked items to estimate overall progress (e.g., "0/14 tasks in Week 1")
4. Note which Week/Day section the current task falls in

## 3. Check today's daily note for context

Read today's diary at `子弹笔记/日记/YYYY-MM-DD_ddd.md` (weekday suffix from `date +%a`).

**Why**: The daily note reveals what the user is already doing today. A reminder that acknowledges their existing workload feels supportive, not nagging.

**What to extract**:
- 今日三件事 (top 3 priorities) — is the learning plan task already there?
- Active tasks — is the user swamped today?
- Training/diet notes — general energy level signal

## 4. Compose the reminder

### Weekday vs Weekend variants

**Weekday** (周一–周五):
- Keep it short: 1 task suggestion, specific chapter/section name
- Acknowledge they're busy (thesis, courses, work)
- Suggest a small time window (20-30 min) rather than a full hour
- Tone: "if you have energy, try X" — not "you must do X"
- Link to the specific resource URL if available

**Weekend** (周六–周日):
- Suggest a bigger block (1-2 hours)
- Encourage hands-on project work over reading docs
- Can mention cumulative progress ("你已经完成了 Week 1 的一半")
- Tone: more enthusiastic, framing it as "you time"

### Reminder structure

```
🌙 Vibe Coding 每日提醒 · {星期}

{1 sentence acknowledging today's context from diary}

📖 今日建议：{specific task from plan}
{If URL available: link to the resource}
{If hands-on task: mention what to do in 1-2 sentences}

💡 你的节奏：{encouragement based on their constraints}
```

### Tone rules (user-specific)
- User is a 药学信息师 with only 3-4h personal time daily
- Vibe Coding is a 1-hour/day long-term project — never frame it as urgent
- Always acknowledge if today is a heavy day (thesis deadline, exam, etc.)
- Never add new tasks — only remind about the plan they already agreed to
- End with something warm, not a command

## 5. Update progress tracking

After the user confirms they did some learning (or after a few days if they report back), update the plan's progress tracking table:

```markdown
| 2026-05-26 | Day 1: 觉醒章节 | 跑通 3 分钟 AI 网页 | 30 min |
```

## Pitfalls
- **File not found on cron server**: The vault is on the user's Mac. If `find` times out, use session_search to look for recent sessions that read the plan file — they'll have the content.
- **Don't read the entire plan every time**: It's 168 lines. Just scan for the first unchecked checkbox and its surrounding section header.
- **Weekday suffix matters**: `date +%a` gives `Mon`, `Tue`, etc. The daily note filename must match. Getting the suffix wrong creates a file the Calendar plugin won't recognize.
- **Don't compete with thesis**: If today's diary shows thesis work as top priority, the reminder should say "论文忙完了再碰 Vibe Coding 也行" — not push learning over graduation.
- **Agent Skills course overlap**: If the user is mid-course on another learning commitment, acknowledge it: "Agent Skills 课程还在继续吧？Vibe Coding 不急，等那边告一段落再加量。"
