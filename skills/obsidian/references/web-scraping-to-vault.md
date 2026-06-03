# 网页批量抓取 → Obsidian Vault

## 适用场景

用户发来一个博客/文档索引页 URL，要求把所有文章抓取下来放入 vault 的 `raw/clippings/`。

## 工具链

| 工具 | 用途 |
|------|------|
| Chrome headless | 渲染 JS 页面，dump DOM（curl 拿不到 Next.js/React 内容） |
| BeautifulSoup | 解析 HTML，提取正文 |
| Python 批处理脚本 | 循环抓取 + 转换 + 写入 |

## 标准流程

### 1. 提取文章 URL 列表

使用 `browser_navigate` 打开索引页，`browser_console` 提取链接：

```js
Array.from(document.querySelectorAll('article a[href^="/engineering/"]'))
  .map(a => ({title: a.querySelector('h2,h3')?.textContent?.trim(), url: a.href}))
```

### 2. 编写批量抓取脚本

核心函数：

```python
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def fetch_page(url):
    result = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom", url],
        capture_output=True, text=True, timeout=90,
        env={**os.environ, "DISPLAY": ""}
    )
    return result.stdout if result.returncode == 0 and len(result.stdout) > 5000 else None
```

### 3. 提取正文 — 关键坑点

**不要用 BeautifulSoup 的 `class_` lambda 匹配多类元素！** 当元素有多个 class，bs4 传的是 list 而非 string，`'Body-module' in ['Body-module-scss-module__body']` 返回 `False`。

❌ 错误：
```python
body = soup.find('div', class_=lambda c: c and 'Body-module' in c)
```

✅ 正确：使用 CSS selector
```python
body = soup.select_one('div[class*="Body-module"][class*="body"]')
```

### 4. 降级策略

Next.js 页面 JS 渲染时序不确定，Chrome `--dump-dom` 可能拿到不完整 DOM：
- 在脚本中加 **3 次重试 + HTML 长度检查**（`len(html) > 5000`）
- 极端情况用 `browser_navigate` + `browser_console` 手动提取单篇
- `--virtual-time-budget=10000` 可增加渲染等待时间（不总是有效）

### 5. 写入 Vault

```python
OUT_DIR = f"{VAULT}/raw/clippings/{topic}/"
os.makedirs(OUT_DIR, exist_ok=True)

# YAML frontmatter + markdown body
lines = ["---", f'title: "{title}"', f'source: "{url}"', f'date: "{date}"', "---", "", f"# {title}"]
# ... append body content ...
with open(f"{OUT_DIR}/{slug}.md", 'w') as f:
    f.write("\n".join(lines))
```

### 6. 收尾

- 创建 `index.md`（文章列表 + 主题分类）
- 追加 `wiki/log.md` 的 ingest 记录（格式：`## [YYYY-MM-DD] ingest | 描述`）

## 依赖安装

```bash
pip3 install beautifulsoup4 html2text
```

Chrome 需预装在 `/Applications/Google Chrome.app/`。

## 失败处理

| 症状 | 原因 | 解决 |
|------|------|------|
| HTML < 5000 chars | JS 未渲染 | 重试 / browser 工具 |
| "No body found" | CSS selector 不匹配 | 检查页面 DOM 结构 |
| 超时（60s+） | 页面太重 | 增加 timeout / 降级用 browser 工具 |
| 重定向到其他域名 | 原文章已迁移 | 标记跳过，写进 index 说明 |
