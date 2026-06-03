# 批量网页抓取 → Obsidian 入库流水线

> 用于一次性拉取整个博客/文档站的全部文章到 Obsidian vault 的 `raw/clippings/`。

## 适用场景

- 博客索引页列出多篇文章链接（如 Anthropic Engineering Blog）
- 页面是 SSR/Next.js，内容在初始 HTML 中（不需要 JS 渲染）
- 目标：全部抓取 → 提取正文 → 存为 .md → 创建索引 + wiki log

## 流水线

### Step 1: 提取文章列表

```python
# 用 browser_console 从索引页提取所有链接
Array.from(document.querySelectorAll('article a[href^="/engineering/"]'))
  .map(a => ({title: ..., url: a.href}))
```

### Step 2: Chrome headless 逐篇抓取

```python
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def fetch_page(url):
    result = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom", url],
        capture_output=True, text=True, timeout=90
    )
    return result.stdout if result.returncode == 0 and len(result.stdout) > 5000 else None
```

### Step 3: BeautifulSoup 提取正文 → Markdown

**关键坑：不要用 `class_` lambda**，在 bs4 中多类元素可能以 list 传递，`'foo' in ['foo-bar-baz']` 返回 False。

✅ **始终用 CSS 选择器：**

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# 标题
title = soup.find('h1', class_='headline-1').text.strip()

# 日期
date_tag = soup.find('p', class_=lambda c: c and 'date' in str(c))

# 正文容器
body = soup.select_one('div[class*="Body-module"][class*="body"]')
if not body:
    body = soup.select_one('article')  # 回退

# 遍历内容标签
for tag in body.find_all(['h1','h2','h3','h4','p','ul','ol','pre','figure']):
    # 用 tag.get_text(' ', strip=True) 保留空格
    # 跳过嵌套在 li/figcaption 内的标签
```

### Step 4: 输出格式

```markdown
---
title: "文章标题"
source: "原始URL"
date: "2024-12-19"
tags: [anthropic, engineering, ai]
---

# 文章标题

> 摘要

正文内容...
```

### Step 5: 创建索引 + 写 log

- 索引文件：`raw/clippings/<source>/index.md`，用 `[[wikilink]]` 链接所有文章
- Ingest log：在 `wiki/log.md` 追加 `## [YYYY-MM-DD] ingest | 描述`

## 常见坑

| 问题 | 原因 | 解决 |
|------|------|------|
| Chrome 超时 | Next.js hydration 未完成 | 增加 timeout 90s + 重试 3 次 |
| bs4 `class_` lambda 不匹配 | 多类元素传 list 而非 str | 用 `select_one('div[class*="X"][class*="Y"]')` |
| 部分页面 DOM 结构不同 | 不同页面模板 | 加 fallback：`article` → `main > article` |
| 抓取非确定性失败 | Chrome 渲染时序 | 循环重试，检查 HTML 长度 > 5000 |

## 工具链

- Chrome headless（macOS 自带）
- beautifulsoup4 + html2text（`pip3 install`）
- Python subprocess 调用 Chrome

## 后续：ingest 到 wiki

抓取完成后按 `CLAUDE.md` 的 ingest 流程：
1. 读取 raw/clippings/ 新文件
2. 与用户讨论关键要点
3. 在 wiki/ 下写摘要/知识页
4. 更新 wiki/index.md
5. 更新 wiki/log.md
