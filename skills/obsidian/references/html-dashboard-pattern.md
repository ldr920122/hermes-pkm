# HTML Dashboard Pattern for Obsidian

When user wants a visually appealing "一页纸工作台" (one-page workspace), create an HTML dashboard instead of plain Markdown.

## User Style Preferences

- **Not too plain**: User corrected agent for "太素了" (too plain) Markdown dashboard
- **Not bullet journal style**: Don't make it look like a template, make it look like a modern app
- **Beautiful design**: Modern UI with gradients, cards, animations
- **Minimalist but pretty**: Clean but visually appealing

## File Structure

```
vault/
├── 首页.md           ← Entry page (set as default in workspace.json)
├── 工作台.html       ← Full HTML dashboard (in ROOT, not attachments/)
└── attachments/
    └── dashboard.html  ← Backup copy
```

**Important**: Place `工作台.html` in root directory, not `attachments/`. User wants easy access.

## Setting Default Homepage

Edit `.obsidian/workspace.json` — find the main leaf's file path and change it:

```json
{
  "main": {
    "children": [
      {
        "type": "tabs",
        "children": [
          {
            "type": "leaf",
            "state": {
              "type": "markdown",
              "state": {
                "file": "首页.md",  ← Change this
                "mode": "source"
              }
            }
          }
        ]
      }
    ]
  }
}
```

## HTML Dashboard Template Structure

### Required Sections
1. **Header**: Logo + real-time date/time display
2. **Today's Focus**: TOP 3 priorities with icons (Ryder Carroll style)
3. **Task List**: Checkable tasks with status badges
4. **Project Tracker**: Progress bars with deadlines
5. **Daily Reading** (📚 每日读书): Reading cards from `微信读书/reading-cards/` — shows book name, date, key takeaway
6. **Podcast/Speech Compressions** (🎧 播客 & 演讲压缩): Links to compressed summaries in `raw/clippings/Bilibili/` — user listens during commute/exercise, needs quick access
7. **Recent Wiki Ingestions** (🧠 知识库最近消化): Latest entries from `wiki/` sorted by creation time — keeps knowledge fresh
8. **Habit Tracker**: Weekly grid with completion stats
9. **Quick Links**: Obsidian deep links (`obsidian://open?vault=...&file=...`) including knowledge graph HTML
10. **Stats Dashboard**: Key metrics (diary count, open tasks, wiki pages, reading cards)
11. **Inspiration Capture**: Recent ideas/insights from `子弹笔记/收集箱`

### Design Guidelines

**⚠️ Current accepted design: MUJI + Claude Code Orange (v3)**

The user rejected gradient backgrounds ("AI味太重") and pure white ("看不清重点"). The accepted design is:

**Colors** (MUJI + Orange accent):
```css
:root {
    --ground: #F4F2EC;        /* Warm off-white */
    --ink: #2A2A28;           /* Dark text */
    --ink-secondary: #7C7B76; /* Muted text */
    --hairline: #D9D6CD;      /* Borders */
    --accent: #D97706;        /* Claude Code orange - section labels, focus numbers */
    --color-green: #059669;   /* Success/progress */
    --color-red: #DC2626;     /* Danger/low progress */
}
```

**Background**: Solid warm off-white, NO gradients
```css
background-color: #F4F2EC;
```

**Cards**: White with hard edges (radius: 0), no shadows, no glassmorphism
```css
.card {
    background: white;
    border: 1px solid var(--hairline);
    border-radius: 0;  /* Hard edges - MUJI style */
}
```

**Progress Bars**: 2px height, color by status
```css
.progress-fill { height: 2px; }
.progress-fill.high { background: var(--accent); }
.progress-fill.low { background: var(--color-red); }
```

**Typography**: system-ui, hero date 96px, section labels 10px uppercase with 0.12em letter-spacing

### Obsidian Deep Links

For quick links that open files directly in Obsidian:
```html
<a href="obsidian://open?vault=VAULT_NAME&file=PATH_TO_FILE">
  Link Text
</a>
```

Example:
```html
<a href="obsidian://open?vault=wbaoc-wiki&file=子弹笔记/日记/2026-05-23_Sat.md">
  📝 今日日记
</a>
```

### Interactive Features (JavaScript)

1. **Real-time clock**:
```javascript
function updateDateTime() {
  const now = new Date();
  const dateStr = now.toLocaleDateString('zh-CN', { 
    year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' 
  });
  const timeStr = now.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', minute: '2-digit' 
  });
  document.getElementById('currentDate').textContent = dateStr;
  document.getElementById('currentTime').textContent = timeStr;
}
setInterval(updateDateTime, 1000);
```

2. **Task checkbox toggle**:
```javascript
document.querySelectorAll('.task-checkbox').forEach(checkbox => {
  checkbox.addEventListener('click', function() {
    this.classList.toggle('checked');
  });
});
```

3. **Card animations on load**:
```javascript
document.querySelectorAll('.card').forEach((card, index) => {
  card.style.opacity = '0';
  card.style.transform = 'translateY(20px)';
  setTimeout(() => {
    card.style.transition = 'all 0.5s ease';
    card.style.opacity = '1';
    card.style.transform = 'translateY(0)';
  }, index * 100);
});
```

## Entry Page (首页.md)

Create a Markdown entry page that links to the HTML dashboard:

```markdown
---
tags: [首页, 工作台, 仪表盘]
---

# 🏠 一页纸工作台

<a href="工作台.html" class="btn btn-primary">
    🚀 打开完整工作台
</a>

## 📊 今日速览

[Include key stats and quick links here for those who prefer Markdown view]
```

## Responsive Design

```css
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
  header {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
}
```

## Pitfalls

- **Don't put HTML in attachments/**: User wants it in root for easy access
- **Don't use plain Markdown**: User explicitly said "太素了" — create HTML
- **Don't forget to set homepage**: Edit workspace.json to show 首页.md on open
- **Test deep links**: `obsidian://` links only work if Obsidian is installed and vault name matches
- **Keep data updated**: HTML dashboard shows static data — update periodically or use JavaScript to fetch dynamic data
- **This IS the primary dashboard**: When user says "工作台", they mean this HTML file, not `子弹笔记/一页纸工作台.md`. All content updates go here.
- **Content is hardcoded**: Unlike the markdown version with Dataview, this HTML is fully static. New wiki entries, reading cards, or podcast compressions must be manually added as HTML sections.
- **`obsidian://` links broken from `file://`** — Browsers block custom protocol handlers from local files opened via `file://` protocol. Even `window.location.href = 'obsidian://...'` fails silently with no error. **Solution**: serve the HTML via local HTTP server (`python3 -m http.server 8088`), then `obsidian://` links work from `http://` context. Created `启动工作台.sh` in vault root for one-click launch: starts server + opens browser.
- **Stale content in HTML dashboard** — Date, tasks, and sections are hardcoded. When user reports "今日任务不对" or "已经做完了", update the HTML immediately. Check with user what today's actual tasks are before writing. Unlike the markdown version which auto-updates via Dataview, HTML needs manual edits.
- **Knowledge graph HTML goes stale** — `wiki/knowledge-graph.html` embeds `graph-data.json` at build time. After adding wiki pages, the graph is outdated. **Fix**: add graph rebuild to daily cron script (`daily_todo_scanner.py`) running `build-graph-data.sh` + `build-graph-html.sh`. Auto-rebuild at 8AM daily.
- **Markdown dashboard Dataview queries may show nothing** — If daily notes lack proper task syntax (`- [ ]`) or the Calendar plugin created files with wrong weekday suffix, Dataview returns empty. Check `daily-notes.json` config and verify filenames match the `ddd` format.

## Example File Locations

- Full HTML dashboard: `~/Documents/Obsidian/wbaoc-wiki/工作台.html`
- Entry page: `~/Documents/Obsidian/wbaoc-wiki/首页.md`
- Backup: `~/Documents/Obsidian/wbaoc-wiki/attachments/dashboard.html`
- Usage guide: `~/Documents/Obsidian/wbaoc-wiki/attachments/README-dashboard.md`
