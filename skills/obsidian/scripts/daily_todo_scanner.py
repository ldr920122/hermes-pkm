#!/usr/bin/env python3
"""
Daily todo scanner for Obsidian bullet journal.
Scans project files and 收集箱 for pending items, outputs summary
for cron job injection.

Usage: python3 daily_todo_scanner.py

Output is structured for cron prompt consumption:
- Date and weekday
- Todo counts (project vs collection)
- Daily note path and existence check
- Todo section block for injection into daily note
- High-priority items flagged separately
"""
import os
import re
from datetime import datetime

# === CONFIGURE THESE PATHS ===
WIKI_ROOT = os.environ.get("OBSIDIAN_VAULT_PATH", os.path.expanduser("~/Documents/Obsidian"))
DAILY_DIR = os.path.join(WIKI_ROOT, "子弹笔记", "日记")
PROJECT_DIR = os.path.join(WIKI_ROOT, "子弹笔记", "项目")
COLLECTION_FILE = os.path.join(WIKI_ROOT, "子弹笔记", "收集箱.md")
# ==============================

today = datetime.now()
date_str = today.strftime("%Y-%m-%d")
weekday_en = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][today.weekday()]

# 1. Scan project files for pending items
project_todos = []
for fname in sorted(os.listdir(PROJECT_DIR)):
    if not fname.endswith(".md"):
        continue
    fpath = os.path.join(PROJECT_DIR, fname)
    with open(fpath, "r") as f:
        content = f.read()
    proj = fname.replace(".md", "")
    for m in re.finditer(r'^- \[ \] (.+)$', content, re.MULTILINE):
        item = m.group(1).strip()
        project_todos.append(f"[{proj}] {item}")

# 2. Scan 收集箱 for pending items (exclude archived section)
collection_todos = []
if os.path.exists(COLLECTION_FILE):
    with open(COLLECTION_FILE, "r") as f:
        content = f.read()
    main_content = content.split("## 已归档")[0] if "## 已归档" in content else content
    for m in re.finditer(r'^- \[ \] (.+)$', main_content, re.MULTILINE):
        item = m.group(1).strip()
        collection_todos.append(item)

# 3. Check if daily note exists
daily_file = os.path.join(DAILY_DIR, f"{date_str}_{weekday_en}.md")
existing_content = ""
if os.path.exists(daily_file):
    with open(daily_file, "r") as f:
        existing_content = f.read()

# 4. Generate todo section for daily note injection
todo_section = "## 📋 待办事项（自动同步）\n\n"
if project_todos:
    todo_section += "### 项目待办\n\n"
    for item in project_todos:
        todo_section += f"- [ ] {item}\n"
    todo_section += "\n"
if collection_todos:
    todo_section += "### 收集箱\n\n"
    for item in collection_todos:
        todo_section += f"- [ ] {item}\n"
    todo_section += "\n"
if not project_todos and not collection_todos:
    todo_section += "_暂无待办事项_\n\n"

# 5. Output for cron job
print(f"📅 {date_str} {weekday_en}")
print(f"\n待办总数：{len(project_todos) + len(collection_todos)} 项")
print(f"- 项目待办：{len(project_todos)} 项")
print(f"- 收集箱：{len(collection_todos)} 项")
print(f"\n日记文件：{daily_file}")
print(f"日记已存在：{'是' if existing_content else '否'}")
print(f"\n---TODO_SECTION---")
print(todo_section)

# 6. Auto-update workbench transclusion link
workbench_file = os.path.join(WIKI_ROOT, "子弹笔记", "一页纸工作台.md")
if os.path.exists(workbench_file):
    with open(workbench_file, "r") as f:
        wb = f.read()
    today_link = f"![[{date_str}_{weekday_en}#🎯 今日三件事]]"
    # Find existing transclusion and replace
    wb_new = re.sub(
        r'!\[\[\d{4}-\d{2}-\d{2}_\w+#🎯 今日三件事\]\]',
        today_link,
        wb
    )
    if wb_new != wb:
        with open(workbench_file, "w") as f:
            f.write(wb_new)
        print(f"\n✅ 工作台嵌入链接已更新为 {today_link}")

# 7. High-priority items
high_priority = [t for t in project_todos if "⏫" in t or "紧急" in t or "Deadline" in t]
if high_priority:
    print(f"\n🔴 高优先级：")
    for item in high_priority:
        print(f"  - {item}")
