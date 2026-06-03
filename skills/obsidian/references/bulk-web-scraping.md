# Bulk Web Scraping → Obsidian Vault

Pattern for ingesting an entire blog index (10+ pages) in one pass.

## Quick Start

1. Extract URLs from index page with `browser_console`
2. Edit `scripts/chrome-headless-scraper.py` (ARTICLES list)
3. Run in background: `python3 scripts/chrome-headless-scraper.py`
4. Create `index.md` with topic tags + [[wikilinks]]
5. Append to `wiki/log.md` per ingest workflow

## Pitfall: BeautifulSoup `class_` lambdas

```python
# ❌ FAILS when bs4 passes class as list:
body = soup.find('div', class_=lambda c: 'Body-module' in c and 'body' in c)

# ✅ CSS selectors always work:
body = soup.select_one('div[class*="Body-module"][class*="body"]')
```

## Pitfall: Chrome --dump-dom + Next.js

Next.js SSR pages serve content server-side but hydration may not complete before `--dump-dom` snapshots. Result: HTML is present but article body div isn't populated.

**Fix**: retry 3x with 90s timeout, check `len(html) > 5000`. For stubborn pages, fall back to `browser_navigate()` + `browser_console()`.

## Pitfall: baoyu-chrome-cdp missing

```
error: Cannot find package 'baoyu-chrome-cdp'
```

Fix: install locally in the skill dir:
```bash
cd ~/.hermes/skills/llm-wiki/deps/baoyu-url-to-markdown
npm init -y && npm install baoyu-chrome-cdp
```

## Page type → tool selection

| Page type | Tool |
|-----------|------|
| Static HTML (server-rendered) | Chrome --dump-dom + BeautifulSoup |
| SPA / CSR-only | baoyu-url-to-markdown (CDP) |
| Login-required | browser_navigate() + browser_console() |
| Single page, ad-hoc | browser_navigate() → extract |
| Batch (10+) | scripts/chrome-headless-scraper.py |
