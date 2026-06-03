# Chrome Headless 批量抓取回退方案

> 当 baoyu-url-to-markdown 因依赖缺失或 JS 渲染失败无法使用时，
> 用本方案作为 fallback 批量抓取网页并存入 Obsidian vault。

## 适用场景

- Next.js SSR 渲染的博客/文档站（如 Anthropic Engineering Blog）
- 页面内容在 `<div class="Body-module-...body">` 等 CSS 类中
- 需要批量抓取（10+ 页面）

## 前置依赖

```bash
pip3 install beautifulsoup4 html2text
```

### baoyu-url-to-markdown 失败原因

当 `npx -y bun scripts/main.ts` 报 `Cannot find package 'baoyu-chrome-cdp'` 时：
```bash
cd ~/.hermes/skills/llm-wiki/deps/baoyu-url-to-markdown
npm init -y && npm install baoyu-chrome-cdp
```
但即使依赖装好，Next.js SSR 页面的 JS 渲染时序问题仍可能导致抓取不稳定（同一页面有时成功有时失败），此时改用本方案的 Chrome headless + BeautifulSoup 管道。

Chrome 路径（macOS）：
```
/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

## 核心流程

### 1. 提取文章列表

用 `browser_console` 提取页面中所有文章链接：

```js
Array.from(document.querySelectorAll('article a[href^="/engineering/"]'))
  .map(a => ({title: ..., url: a.href}))
```

### 2. Chrome headless dump DOM

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox --dump-dom URL
```

**关键坑**：
- Next.js 页面可能 JS 未完成渲染就 dump，导致内容缺失
- 现象：HTML 很大（150K+），但找不到目标 div
- 解决：增大 timeout（90s）+ 重试 3 次 + `--virtual-time-budget=10000`
- 非确定性：同一页面可能这次成功、下次失败

### 3. BeautifulSoup 提取正文

**永远用 CSS 选择器，不要用 class_ lambda**：

```python
# ✅ 正确
body = soup.select_one('div[class*="Body-module"][class*="body"]')

# ❌ 错误（BeautifulSoup 多类元素传 list 而非 str，lambda 会漏）
body = soup.find('div', class_=lambda c: 'Body-module' in c)
```

**回退链**：
1. `div[class*="Body-module"][class*="body"]`
2. `article` 标签
3. `main article` 或 `main div[class*="Body-module"]`

### 4. 生成 Markdown

格式：YAML frontmatter + 标题 + 正文

```yaml
---
title: "文章标题"
source: "原始URL"
date: "发布日期"
tags: [anthropic, engineering, ai]
---
```

正文：遍历 `body.find_all(['h1','h2','h3','h4','p','ul','ol','pre','figure','blockquote'])`，按标签类型转 markdown。

**坑**：跳过 `<li>` 和 `<figcaption>` 内的子标签（已在父级处理）。

### 5. 批量脚本模板

见同目录 `scripts/batch-scraper.py`（如有）。核心循环：

```python
for url, slug in articles:
    html = fetch_page(url)  # Chrome headless + 重试
    md, title = html_to_md(html, url)  # CSS selector + 转换
    write_file(f"{OUT_DIR}/{slug}.md", md)
```

## 已知限制

- 页面内容必须在首屏 HTML 中（SSR），纯 CSR 渲染的页面无法抓
- 图片链接保留远程 URL（不下载到本地）
- 重定向页面（如原链接迁移到 docs 站）需手动处理
- 每页约 5-15 秒，24 页约 2-4 分钟
