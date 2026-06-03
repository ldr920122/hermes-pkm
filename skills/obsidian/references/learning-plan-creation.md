# Learning Plan Creation Pattern

When the user sees a tutorial, course, or set of GitHub repos and wants to systematically learn from them, create a structured learning plan in Obsidian.

## Workflow

### 1. Research the resources
- Fetch README.md from each GitHub repo (via raw.githubusercontent.com)
- Use GitHub API tree endpoint for repo structure: `api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1`
- For Chinese searches: use Brave search (Google/Bing often CAPTCHA-blocked)
- Identify: table of contents, learning paths, prerequisites, estimated time

### 2. Structure the plan
Follow this template structure:
```markdown
# {Topic} 系统学习计划

> 创建日期：YYYY-MM-DD

## 学习路径总览
- Table with repos/resources, positioning, estimated time

## 阶段 N: {Resource Name}
- Week-by-week breakdown with checkboxes
- Each day: specific chapters/tasks to complete
- Concrete deliverables per week

## 阶段完成标准
- Checkable milestones

## 每日学习时间规划
- Map to user's actual available time slots

## 与现有任务的协调
- Priority ordering with other commitments

## 学习进度追踪
- Empty table for daily logging
```

### 3. Save to Obsidian
- Path: `wiki/{Topic}学习计划.md`
- Use frontmatter if vault schema requires it
- Link from `wiki/index.md` if appropriate

### 4. Set up daily reminders
- Use cronjob: create daily reminder at an appropriate evening time (e.g. 21:00)
- Prompt should reference the plan file and vary by weekday vs weekend
- Account for user's time constraints in the reminder tone
- **Execution details**: see `references/learning-plan-reminder.md` for vault path discovery on cron servers, progress parsing, diary context extraction, and weekday/weekend reminder templates

## Pitfalls
- **Don't over-plan** — users with <4h/day personal time need realistic targets. 1 hour/day is sustainable; 3 hours/day is not.
- **Map to actual time slots** — lunch break (screen), evening (deep work), bedtime (review). Don't assume contiguous blocks.
- **Link to existing commitments** — always cross-reference with other deadlines (thesis, courses, work) to prevent the learning plan from becoming another source of anxiety.
- **P-people need flexibility** — checkboxes are good, rigid daily schedules are not. Use "this week" not "Monday do X, Tuesday do Y".
