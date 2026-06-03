# Daily Bullet Journal Briefing via Cron

When a user has a BuJo system and wants a morning briefing delivered to their phone:

## Setup

Use the `cronjob` tool with `action=create`:

```
schedule: 0 8 * * *      (8 AM daily)
deliver: telegram:NAME    (must be Telegram — see WeChat pitfall below)
repeat: forever
```

## Prompt template for the cron job

```
早安简报任务。请完成以下步骤：

1. 读取 /path/to/vault/子弹笔记/仪表盘.md 了解整体概况
2. 读取 /path/to/vault/子弹笔记/月度/ 下当月的月度记录
3. 读取 /path/to/vault/子弹笔记/收集箱.md 中最新的待办
4. 查看 01 日记/ 下昨天的日记是否有未完成的任务

然后组织一条简洁的 Telegram 消息发送到 telegram:TARGET (dm)，格式如下：

☀️ 早安！今天 {日期}

📋 今日待办
• （最重要的 3 件事）

🔥 紧急提醒
• （有 deadline 即将到来的事项）

📊 进行中
• （正在推进的项目状态）

💪 每日习惯
• 训练打卡 · 饮食打卡 · 日语学习

⏰ 即将截止
• （接下来 7 天内截止的事项）

保持简洁，每条不超过一行。用中文。
```

## Delivery channel

**Telegram or WeChat.** Both work for automated delivery. Use `deliver: origin` to reply in the channel the cron was created from. If the user is primarily on WeChat (Weixin), deliver there.

## What the cron job reads

The BuJo system provides:
- `仪表盘.md` — Dataview queries auto-aggregate all open tasks
- `月度/YYYY-MM.md` — calendar timeline shows daily notable events, action plan has prioritized tasks
- `收集箱.md` — brain dump items organized by urgency quadrant
- `子弹笔记/日记/` — yesterday's unfinished tasks (Tasks plugin `- [ ]` items)
- `子弹笔记/项目/` — project-specific checklists and deadlines

## Script-based daily todo scanner (recommended)

Use a Python script (`scripts/daily_todo_scanner.py`) to scan all project files and 收集箱 for unchecked items. The script's stdout is injected into the cron prompt as context.

**What the scanner does:**
1. Scans all `.md` files in `子弹笔记/项目/` for `- [ ]` items
2. Scans `子弹笔记/收集箱.md` for `- [ ]` items (excluding archived section)
3. Checks if today's daily note exists
4. Outputs structured data: date, todo counts, todo section for injection

**Cron prompt should do TWO things:**
1. **Write todos into the daily note** — create from template if needed, insert `## 📋 待办事项（自动同步）` section before `## 📝 笔记`
2. **Push a concise summary** — only urgent/high-priority items, max 8-10 items

**Push filtering rules (user preference):**
- 每日习惯（训练/饮食/日语）→ DON'T push (too noisy)
- 收集箱中"想做的事" and "不紧急" → DON'T push
- Deadline within 7 days or marked ⏫ → DO push
- Project items with approaching deadlines → DO push
- Keep message compact, use emoji sections
- **Context-aware deadline filtering**: if a deadline doesn't apply to the user (e.g. "6月5日提交" but user's blind review is in the second half of the year), DO NOT mention it. The user explicitly said: "6月5号发到邮箱就不要告诉我了，因为我是下半年才盲审." Before pushing any deadline, check whether it actually applies to this user's timeline.
