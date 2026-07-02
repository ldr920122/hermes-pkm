#!/usr/bin/env python3
"""Chrome headless批量抓取博客文章到Obsidian。

用法：编辑下方的 ARTICLES 列表，然后 `python3 chrome-headless-scraper.py`

依赖：pip3 install beautifulsoup4
Chrome：macOS自带 /Applications/Google Chrome.app
"""

import subprocess, sys, os
from pathlib import Path

# ====== 配置区 ======
VAULT = os.environ.get("OBSIDIAN_VAULT_PATH", os.path.expanduser("~/Documents/Obsidian"))
OUT_DIR = f"{VAULT}/raw/clippings/your-site-name"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TIMEOUT = 90  # 秒
MAX_RETRIES = 3

ARTICLES = [
    # 格式: ("完整URL", "文件名slug")
    # ("https://example.com/blog/post-1", "post-1"),
]
# =====================

os.makedirs(OUT_DIR, exist_ok=True)

from bs4 import BeautifulSoup


def fetch_page(url: str) -> str | None:
    """Chrome headless dump DOM，带重试"""
    for attempt in range(MAX_RETRIES):
        try:
            result = subprocess.run(
                [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom", url],
                capture_output=True, text=True, timeout=TIMEOUT,
                env={**os.environ, "DISPLAY": ""},
            )
            if result.returncode != 0:
                print(f"  (attempt {attempt+1}: exit {result.returncode})", end=" ", flush=True)
                continue
            html = result.stdout
            if len(html) < 5000:
                print(f"  (attempt {attempt+1}: {len(html)} chars too short)", end=" ", flush=True)
                continue
            return html
        except subprocess.TimeoutExpired:
            print(f"  (attempt {attempt+1}: timeout)", end=" ", flush=True)
    return None


def html_to_md(html: str, url: str) -> tuple[str | None, str]:
    """提取文章正文 → Markdown"""
    soup = BeautifulSoup(html, "html.parser")

    # 标题
    title_tag = soup.find("h1", class_="headline-1")
    title = title_tag.text.strip() if title_tag else "Untitled"

    # 日期
    date_tag = soup.find("p", class_=lambda c: c and "date" in str(c))
    date_str = ""
    if date_tag:
        date_str = date_tag.get_text(strip=True).replace("Published", "").strip()

    # 摘要
    summary_tag = soup.select_one('p[class*="summary"]')
    summary = summary_tag.text.strip() if summary_tag else ""

    # 正文容器 — 优先 CSS 选择器，回退 article
    body = soup.select_one('div[class*="Body-module"][class*="body"]')
    if not body:
        body = soup.select_one("article")
    if not body:
        main = soup.find("main")
        if main:
            body = main.select_one('article, div[class*="Body-module"]')
    if not body:
        return None, title

    # 构建 Markdown
    lines = []
    lines.append("---")
    lines.append(f'title: "{title.replace(chr(34), chr(92)+chr(34))}"')
    lines.append(f'source: "{url}"')
    lines.append(f'date: "{date_str}"')
    lines.append("tags: []")
    lines.append("---\n")
    lines.append(f"# {title}\n")
    if summary:
        lines.append(f"> {summary}\n")

    for tag in body.find_all(
        ["h1", "h2", "h3", "h4", "p", "ul", "ol", "pre", "figure", "blockquote"],
        recursive=True,
    ):
        if tag.parent.name in ("li", "figcaption"):
            continue
        tag_text = tag.get_text(" ", strip=True)
        if not tag_text and tag.name != "figure":
            continue

        match tag.name:
            case "h1": lines.append(f"# {tag_text}\n")
            case "h2": lines.append(f"## {tag_text}\n")
            case "h3": lines.append(f"### {tag_text}\n")
            case "h4": lines.append(f"#### {tag_text}\n")
            case "p":  lines.append(f"{tag_text}\n")
            case "ul" | "ol":
                for li in tag.find_all("li", recursive=False):
                    text = li.get_text(" ", strip=True)
                    if text:
                        lines.append(f"- {text}")
                lines.append("")
            case "pre":
                lines.append("```")
                lines.append(tag_text)
                lines.append("```\n")
            case "figure":
                img = tag.find("img")
                if img and img.get("src"):
                    lines.append(f"![{img.get('alt', '')}]({img['src']})")
                    fc = tag.find("figcaption")
                    if fc:
                        lines.append(f"*{fc.get_text(strip=True)}*")
                    lines.append("")
            case "blockquote":
                lines.append(f"> {tag_text}\n")

    return "\n".join(lines), title


def main():
    success = 0
    failed = 0
    for i, (url, slug) in enumerate(ARTICLES):
        print(f"[{i+1}/{len(ARTICLES)}] {slug}", end=" ", flush=True)

        html = fetch_page(url)
        if not html:
            print("- FAILED (Chrome)")
            failed += 1
            continue

        md, title = html_to_md(html, url)
        if not md:
            print("- FAILED (parse)")
            failed += 1
            continue

        out_path = f"{OUT_DIR}/{slug}.md"
        Path(out_path).write_text(md, encoding="utf-8")
        print(f"- OK ({len(md)} chars) — {title[:60]}")
        success += 1

    print(f"\nDone. Success: {success}, Failed: {failed}")
    print(f"Output: {OUT_DIR}")


if __name__ == "__main__":
    main()
