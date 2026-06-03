# Bilibili (B站) Content Extraction

## Overview

Bilibili videos do NOT have a transcript API like YouTube. The `youtube-content` skill's transcript extraction will fail on `bilibili.com` URLs.

## Extraction Methods

### Method 1: Browser Automation (Recommended)

Use browser tools to navigate to the video page and extract information:

```python
# 1. Navigate to video page
browser_navigate(url="https://www.bilibili.com/video/BV1XXXXXX/")

# 2. Extract title from page heading
# Title appears in: heading "视频标题" [level=1, ref=eXX]

# 3. Extract description from page snapshot
# Description appears in StaticText blocks after the video player

# 4. Extract metadata (views, likes, date) from snapshot
```

**Key elements to extract:**
- Title: `heading` element with level=1
- Description: `StaticText` blocks in the description area
- Date: Look for pattern like `2026-05-11 16:11:19`
- Author: Link element near the video title
- Tags: Links in the tag area

### Method 2: Browser Console (for description)

```javascript
// Get full description text
document.querySelector('.desc-info-text').innerText
// OR
document.querySelector('#v-desc').innerText
```

Note: Selectors may vary; check the actual DOM structure.

### Method 3: Manual Extraction

If browser automation fails:
1. Ask user to open video in browser
2. Copy-paste title, description, and key points
3. Format into markdown

## Save Path

Save to Obsidian vault:
```
/Users/wbaoc/Documents/Obsidian/wbaoc-wiki/raw/clippings/Bilibili/
```

## Filename Convention

```
YYYY-MM-DD-视频标题关键词.md
```

Example: `2026-05-11-开源一个PPT-压进了我10年的设计经验.md`

## Template

```markdown
# 视频标题

**来源：** B站
**作者：** 作者名称
**日期：** YYYY-MM-DD
**链接：** https://www.bilibili.com/video/BV1XXXXXX/

---

## 视频简介

[Description from video page]

## 主要内容

[Key points, features, takeaways]

## 相关链接

- GitHub: [if applicable]
- 作者主页: [if applicable]

## 标签

#标签1 #标签2 #标签3
```

## Pitfalls

- **No transcript available** — unlike YouTube, Bilibili doesn't expose video subtitles via API
- **Anti-scraping** — Bilibili may block direct curl requests; browser automation is more reliable
- **Video ID format** — Bilibili uses `BV` prefix (e.g., `BV1K2546oEkg`), not YouTube's 11-char ID
- **Description selectors vary** — the DOM structure may change; verify selectors before batch extraction
- **Browser console selectors may fail** — `.desc-info-text` and `#v-desc` selectors often return null. Use `browser_snapshot` to find the actual DOM structure and extract from `StaticText` blocks instead.
- **Page loading** — Bilibili pages may need scrolling to load full content. Use `browser_scroll(direction="down")` before extraction.

## Batch Extraction Pattern

When extracting multiple Bilibili videos (e.g., user shares 3-4 links):

1. **Process sequentially** — navigate to each video, extract, save
2. **Check for duplicates** — search `raw/clippings/Bilibili/` for existing BV IDs before saving
3. **Consistent naming** — use `YYYY-MM-DD-标题关键词.md` format
4. **Create wiki pages** — for important content, create pages in `wiki/AI工具/` or appropriate category
5. **Update index and log** — batch update `wiki/index.md` and `wiki/log.md` after all extractions

## User Context

This user saves Bilibili videos for later learning (courses, tutorials, skill demos). They want:
1. Quick extraction of title + description + key links
2. Saved to `raw/clippings/Bilibili/` for later digestion
3. Wiki pages created for important content