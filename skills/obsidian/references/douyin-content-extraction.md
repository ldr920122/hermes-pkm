# Douyin (抖音) Content Extraction to Obsidian Vault

Pattern for extracting useful content from Douyin video links the user shares via chat.

## Why This Matters

The user frequently sends Douyin links (tutorials, news, learning tips). These are ephemeral — they scroll away. Extracting and archiving them to the knowledge base turns a 2-minute video into lasting reference material.

## Extraction Workflow

### Step 1: Navigate to the Douyin link

```python
browser_navigate("https://v.douyin.com/XXXXX/")
```

The short link auto-redirects to `douyin.com/video/XXXXX`.

### Step 2: Extract from "章节要点" (Section Summary)

Douyin's video player includes an AI-generated **章节要点** (chapter summary) that captures the video's key points. This is the primary extraction target — it's concise, accurate, and requires no video playback.

After navigation, check the snapshot for the "章节要点" section:

```
- StaticText "章节要点"
- StaticText "视频的核心内容摘要..."
```

### Step 3: Fall back to meta tags in `<head>` (reliable fallback)

If 章节要点 isn't present, extract metadata from the page `<head>` using `browser_console`. Douyin injects rich metadata into `<meta>` tags even when the video body requires login:

```javascript
const meta = {};
document.querySelectorAll('meta').forEach(m => {
  const name = m.getAttribute('name') || m.getAttribute('property') || '';
  const content = m.getAttribute('content') || '';
  if (name && content) meta[name] = content;
});
JSON.stringify(meta, null, 2);
```

Key fields to extract:
- `description` — full video description with hashtags and creator info
- `lark:url:video_title` — video title (may be longer than `description`)
- `lark:url:video_cover_image_url` — thumbnail URL
- `keywords` — topic tags

This technique works because Douyin uses server-side rendering for `<meta>` tags (for SEO/sharing), even though the video player itself requires JS + login. The description field typically contains the full creator-written text.

### Step 4: Fall back to page body extraction

If meta tags are also empty (rare), extract from the video description area using `browser_console`:

```javascript
document.querySelector('h1')?.textContent + '\n' + 
Array.from(document.querySelectorAll('[class*="desc"]')).map(e => e.textContent).filter(t => t.length > 30).join('\n')
```

### Step 4: For tutorial articles on ModelScope/Bilibili/etc.

When the Douyin video links to a detailed tutorial (common for techie videos), navigate to the tutorial page and extract the full article content:

```javascript
document.querySelector('.markdown-body')?.textContent?.substring(0, 5000)
```

### Step 5: Save to vault — TWO destinations, not one

Save **both** a raw clip AND a structured wiki page:

1. **Raw clip** → `raw/clippings/Douyin/{date}-{short-title}.md`
   - YAML frontmatter with `source_url`, `captured_at`, `platform`, `duration`
   - 章节要点 + 时间线 + 标签 + 热门评论摘要
   - Purpose: provenance traceability — links back to original video

2. **Wiki page** → `wiki/AI工具/{topic-name}.md` (or appropriate category)
   - Structured knowledge with concept definitions, examples, and cross-references
   - Must link to related existing wiki pages using `[[wikilinks]]`
   - Use concept mapping tables when the video introduces a framework/taxonomy
   - Purpose: reusable knowledge — the value-add over the raw clip

Then update `wiki/index.md` (add entry under the right category) and `wiki/log.md` (append ingest record).

**Why two files**: raw clip preserves the original structure (chapters, timestamps, comments) for reference; the wiki page extracts and restructures the knowledge for long-term use. Copying just one loses either provenance or structure.

## Platform-Specific Notes

### ModelScope (魔搭)

When a Douyin video references ModelScope content:
- The video description often mentions "教程" or "研习社"
- Search ModelScope for the topic: `browser_navigate("https://modelscope.cn")` → search → find tutorial
- Extract from `.markdown-body` or the article's page content
- Save as `wiki/AI工具/<topic>.md`

### Douyin Limitations

- No programmatic transcript API (unlike YouTube)
- 章节要点 is AI-generated, not verbatim — good enough for key points, not for exact quotes
- Browser must render the page; `browser_navigate` handles the redirect chain automatically
- Videos may require login for full content; if blocked, ask user to provide key info directly

## Pitfalls

- **Not logged in** — The browser session isn't authenticated to Douyin ("登录/注册" button visible). Some videos may restrict content to logged-in users. If 章节要点 is missing and description is truncated, ask user to provide the key info directly (see OCR failure below).
- **OCR on Douyin screenshots fails badly** — Tesseract (chi_sim+eng) cannot reliably read Douyin's stylized video overlays (dark backgrounds, colored text, emoji, hashtag decorations). Even with contrast enhancement, grayscale conversion, and adaptive thresholding, the output is gibberish. Do NOT attempt OCR on Douyin screenshots — it wastes time. Instead, ask the user to type out the key info (repo names, links, project names) directly. The user is usually happy to do this since they're already looking at the content.
- **章节要点 availability** — Not all Douyin videos have AI-generated chapter summaries. Tech/educational content (ModelScope, tutorials) almost always does. Entertainment content rarely does. Check the snapshot for `StaticText "章节要点"` before assuming it's there.
- **Video description ≠ 章节要点** — The description area (below the username) is often hashtag-heavy marketing text. Always target the "章节要点" label specifically in the snapshot tree, not the generic description field.
- **Wrong video loaded** — Douyin's infinite-scroll can load a different video than the one linked. The `document.title` or description may mismatch the expected content. Verify against the video the user described before extracting.

## Examples from This Vault

- `wiki/AI工具/MIT超前学习法.md` — extracted from 清华姜学长 video via 章节要点
- AMD ModelScope GPU offer — extracted from 魔搭ModelScope社区 video + linked tutorial

## Related Skills & References

- `youtube-content` — for YouTube videos (more reliable, has transcripts API)
- `references/bulk-web-scraping.md` — for batch scraping blog archives
- `references/web-scraping-to-vault.md` — general web scraping workflow
