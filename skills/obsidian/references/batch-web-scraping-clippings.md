# Batch Web Scraping → Obsidian Clippings

When the user asks to ingest an entire blog/site index into their vault:

## 1. Discover article list
- Navigate to the index page with `browser_navigate`
- Extract all article links with `browser_console`:
  ```js
  Array.from(document.querySelectorAll('article a[href^="/path/"]'))
    .map(a => ({title: ..., url: a.href}))
  ```

## 2. Write a batch scraper

For Next.js/React sites, Chrome `--dump-dom` works but has **non-deterministic timing** — 
~50% of pages will fail because JS hasn't finished rendering. Key mitigations:

- Use CSS selectors (`div[class*="Body-module"][class*="body"]`) instead of 
  BeautifulSoup `class_` lambdas — lambdas break on multi-class elements
- Add 3-attempt retry logic with 90s timeout per page
- Set `--no-sandbox` flag for Chrome headless
- HTML length check: reject if < 5000 chars (incomplete load)

**Script skeleton** (`/tmp/scraper.py`):
```python
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
def fetch_page(url):
    for attempt in range(3):
        result = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom", url],
            capture_output=True, text=True, timeout=90
        )
        if result.returncode == 0 and len(result.stdout) > 5000:
            return result.stdout
    return None
```

## 3. Extract and convert

Target the body div: `soup.select_one('div[class*="Body-module"][class*="body"]')`  
Iterate `body.find_all(['h1','h2','h3','h4','p','ul','ol','pre','figure','blockquote'])`  
Skip `li` and `figcaption` children (handled by parents).

Output each page as a YAML-frontmatter markdown file.

## 4. Save and index

- Save to `raw/clippings/<topic>/` (one .md per article)
- Create `index.md` with topic categorization + wikilinks
- Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <description>`
- Update memory with vault structure notes if paths changed

## Pitfalls

- **BS4 class_ lambda**: `lambda c: 'Body-module' in c` fails when `c` is a list. Use CSS selectors.
- **Chrome timeout**: increase to 90s, use retry loop — Next.js hydration is unpredictable
- **Page redirects**: some articles move to docs sites — verify the URL after navigation, note as "migrated" in index
- **Don't run Chrome headless in parallel from the same terminal** — it can cause timeouts
