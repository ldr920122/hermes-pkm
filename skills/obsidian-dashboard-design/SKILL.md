---
name: obsidian-dashboard-design
description: Design patterns for Obsidian personal dashboards and workbenches. Use when building HTML-based productivity dashboards that integrate with Obsidian vaults.
version: 1.0.0
metadata:
  hermes:
    tags: [obsidian, dashboard, design, html, productivity, workbench]
    related_skills: [web-design-engineer, obsidian]
---

# Obsidian Dashboard Design

Patterns and lessons learned for building HTML-based personal dashboards that integrate with Obsidian.

## Core Philosophy

The dashboard is the user's "homepage" — the first thing they see when opening Obsidian. It should be:
- **Quiet**: Not overwhelming, lots of whitespace
- **Actionable**: Clear what to do today
- **Integrated**: Links directly to Obsidian notes

## Design Pattern: MUJI + Accent

A combination of MUJI/Kenya Hara minimalism with selective color accents for hierarchy.

### Why This Works for Obsidian Users

1. **Whitespace = Focus**: Users open dashboards to see what matters, not to be dazzled
2. **Hard edges = Honesty**: No rounded corners = no "app-like" feel = fits Obsidian's aesthetic
3. **Single accent = Clarity**: One color (e.g., orange) highlights what's important
4. **System fonts = Speed**: No external font loading, instant render

### Proven Color System

```css
:root {
  --ground: #F4F2EC;           /* warm paper */
  --ink: #2A2A28;              /* warm dark */
  --ink-secondary: #7C7B76;    /* muted */
  --hairline: #D9D6CD;         /* dividers */
  --accent: #D97706;           /* Claude Code orange */
  --accent-light: rgba(217, 119, 6, 0.08);
}
```

### Spacing (MUJI Scale)

```
8 / 16 / 32 / 48 / 96 / 160 / 240 px
```

Section breaks at 240px — extreme whitespace that creates breathing room.

## Dashboard Structure

Based on user testing, this structure works well:

```
01 — 今日焦点 (Hero date + top 3 priorities)
02 — 今日任务 (Actionable checklist)
03 — 项目追踪 (Active projects with progress)
04 — 数据看板 (Key metrics)
05 — 备忘 (Recent memos)
06 — 快速入口 (Quick links to notes)
```

### Hero Date Section

The date should be LARGE (96px) — it's the first thing users see.

```html
<div class="hero-date">5月25日</div>
<div class="hero-weekday">星期一</div>
<div class="hero-meta">
  <span>☀️ 晴 · 26°C</span>
  <span>打开即专注</span>
</div>
```

## Obsidian Integration

### Quick Links

Use `obsidian://` protocol for direct jumping:

```html
<a href="obsidian://open?vault=VAULT_NAME&file=PATH">Link Text</a>
```

**Fallback**: Add `data-path` attribute and JavaScript to copy path to clipboard if `obsidian://` fails (e.g., in browser).

```javascript
link.addEventListener('click', async function() {
  const path = this.dataset.path;
  setTimeout(async () => {
    await navigator.clipboard.writeText(path);
    // Show "✓ 已复制路径" feedback
  }, 100);
});
```

### File Organization

- **Dashboard HTML**: Root of vault (`工作台.html`)
- **Entry point**: `首页.md` with link to HTML
- **Daily notes**: `子弹笔记/日记/YYYY-MM-DD_Ddd.md`
- **Projects**: `子弹笔记/项目/`
- **Collections**: `子弹笔记/收集箱.md`

### Don't Create Separate Folders For

- Fitness/exercise logs → keep in daily notes
- Reading logs → keep in daily notes  
- Food logs → keep in daily notes

Daily context > separate organization.

## Timezone Handling

For users in UTC+8 (China):

```javascript
function getBeijingTime() {
  const now = new Date();
  const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
  return new Date(utc + (3600000 * 8)); // UTC+8
}
```

## Common Pitfalls

1. **Too many colors** → Stick to 1 accent + neutrals
2. **Rounded corners everywhere** → Use 0 radius (hard edges)
3. **Shadows** → Don't use them; elevation through whitespace
4. **External fonts** → Use system-ui for speed
5. **Complex animations** → Subtle fades only (600-900ms)
6. **Emoji as icons** → Use placeholders or text labels
7. **Forgetting timezone** → Always use user's timezone for dates

## Iteration Process

1. **v0**: Show structure + design system, get approval
2. **v1**: Add colors, refine hierarchy based on feedback
3. **v2**: Polish interactions, add dynamic data

Always show v0 early — let user course-correct direction before building full features.