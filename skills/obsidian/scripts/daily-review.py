#!/usr/bin/env python3
"""
每日随机复习：从 Obsidian vault 中随机抽取一块内容，用于间隔重复。
输出 JSON 供 cron job prompt 使用。

用法: python3 daily-review.py
输出: {"status": "ok", "file": "...", "content": "...", "date": "..."}
"""
import json
import os
import random
from pathlib import Path
from datetime import datetime

VAULT = Path(os.environ.get("OBSIDIAN_VAULT_PATH", str(Path.home() / "Documents" / "Obsidian")))
HISTORY_FILE = Path.home() / ".hermes" / "scripts" / ".review_history.json"

# 可复习的目录（排除日记、模板、系统文件）
REVIEWABLE_DIRS = [
    "wiki",
    "raw/AI",
    "raw/效率工具",
    "raw/学术",
    "raw/编程",
    "raw/3D打印",
    "raw/摄影",
    "raw/通用",
    "微信读书",
    "子弹笔记/项目",
    "子弹笔记/会议",
]

# 排除的文件模式
EXCLUDE_PATTERNS = [
    "log.md", "index.md", "CLAUDE.md", "purpose.md",
    "年度.md", "收集箱.md", "一页纸工作台.md",
    "模板", "infographic", "attachments",
]

def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return {"reviewed": [], "last_date": None}

def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2))

def get_reviewable_files():
    files = []
    for rel_dir in REVIEWABLE_DIRS:
        abs_dir = VAULT / rel_dir
        if not abs_dir.exists():
            continue
        for md_file in abs_dir.rglob("*.md"):
            rel_path = md_file.relative_to(VAULT)
            if any(p in str(rel_path) for p in EXCLUDE_PATTERNS):
                continue
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            if len(content.strip()) < 50:
                continue
            files.append({
                "path": str(rel_path),
                "abs_path": str(md_file),
                "size": len(content),
            })
    return files

def extract_review_chunk(content, max_chars=800):
    """从文件中提取一段适合复习的内容"""
    lines = content.split("\n")
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    while start < len(lines) and not lines[start].strip():
        start += 1
    text = "\n".join(lines[start:]).strip()
    if len(text) <= max_chars:
        return text
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return text[:max_chars]
    idx = random.randint(0, len(paragraphs) - 1)
    chunk = ""
    for i in range(idx, len(paragraphs)):
        if len(chunk) + len(paragraphs[i]) > max_chars:
            break
        chunk += paragraphs[i] + "\n\n"
    if not chunk:
        chunk = paragraphs[idx][:max_chars]
    return chunk.strip()

def main():
    history = load_history()
    today = datetime.now().strftime("%Y-%m-%d")
    if history.get("last_date") == today:
        print(json.dumps({"status": "already_reviewed", "date": today}))
        return
    files = get_reviewable_files()
    if not files:
        print(json.dumps({"status": "no_files"}))
        return
    reviewed_set = set(history.get("reviewed", [])[-200:])
    unreviewed = [f for f in files if f["path"] not in reviewed_set]
    if not unreviewed:
        history["reviewed"] = []
        unreviewed = files
    chosen = random.choice(unreviewed)
    content = Path(chosen["abs_path"]).read_text(encoding="utf-8", errors="ignore")
    chunk = extract_review_chunk(content)
    history["reviewed"].append(chosen["path"])
    history["last_date"] = today
    save_history(history)
    print(json.dumps({
        "status": "ok",
        "file": chosen["path"],
        "content": chunk,
        "date": today,
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
