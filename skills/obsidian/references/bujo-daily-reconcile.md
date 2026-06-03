# Daily Note Reconciliation Checklist

> When Hermes needs to write to the user's daily note, follow this checklist to avoid creating duplicates.

## Obsidian Daily Notes Config

Location: `{vault}/.obsidian/daily-notes.json`

```json
{
  "format": "YYYY-MM-DD_ddd",
  "folder": "子弹笔记/日记",
  "template": "00 templates/子弹笔记-日记模板"
}
```

- `format` → determines the **exact filename** (e.g. `2026-05-21_Thu.md`)
- `folder` → where Calendar creates daily notes (now under 子弹笔记/ root)
- `template` → which template auto-fills new notes

## Step-by-Step Reconciliation

1. **Read `.obsidian/daily-notes.json`** to get the format, folder, and template
2. **Construct today's filename** from the format (e.g. `2026-05-21_Thu.md` for `YYYY-MM-DD_ddd`)
3. **Search `{folder}/` for files matching today's date** — Calendar may have already created an empty template
4. **If file exists** → read it, preserve the Calendar-generated frontmatter structure, and **fill the content sections** (do NOT overwrite with a new file). The file will have empty template sections — content goes into them.
5. **If no file exists** → create it using the exact template format from `00 templates/子弹笔记-日记模板`
6. **After writing**, also update in one pass:
   - `子弹笔记/月度/YYYY-MM.md` → add calendar line entry for today
   - `子弹笔记/月度/YYYY-MM.md` → refresh 行动计划 section with new/in-progress items
   - `子弹笔记/收集箱.md` → add/archive new floating items, update status of existing ones

## Template Sections (from 子弹笔记-日记模板)

```
🎯 今日三件事（按重要性排序）
📋 任务
📝 笔记 · 事件 · 感想
🔄 明日预览
```

Task symbols: `•` task, `✕` complete, `→` migrate to tomorrow, `←` migrate to monthly, `—` cancel.
Note symbols: `○` event, `—` thought/idea.

## Common Pitfalls

- **Filename mismatch** — Hermes creates `2026-05-21.md` while Calendar created `2026-05-21_Thu.md`. Root cause: ignoring the `format` field in `daily-notes.json`. Fix: delete the wrong one, use Calendar's filename.
- **Frontmatter mismatch** — Calendar uses `created: "2026-05-21_Thu"` (format string, not ISO date). Match this exactly.
- **Empty template file** — Calendar may create a file with only template boilerplate. This is the expected starting point — fill the sections, don't replace the file.
- **Overwriting filled content** — if the file already has user-written content, append new events to 📝 笔记 and new tasks to 📋 任务. Never regenerate the entire file from scratch.
- **Forgetting side updates** — writing the diary is step 1. 月度 and 收集箱 must be updated in the same pass or the user loses context.
- **Cron script creating wrong weekday format** — `daily_todo_scanner.py` previously used Chinese weekdays (周二, 周三) in filenames, causing Calendar to not recognize them. The `ddd` token in Moment.js produces English abbreviations (Mon, Tue, Wed...). Always verify cron scripts use English weekday names matching the `daily-notes.json` format field. After fixing the script, rename any wrongly-named files and merge duplicates (cron file has content, Calendar file is empty template).
- **Dashboard hardcoded content goes stale** — if a Dataview-driven dashboard (一页纸工作台.md) has hardcoded "今日三件事" content, it becomes stale within a day. The Dataview query `TASK FROM "子弹笔记/日记" WHERE file.day = date(today)` should be the sole source. Never hardcode todo items in the dashboard.
