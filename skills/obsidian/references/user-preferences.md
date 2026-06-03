# User Preferences for Obsidian

## Structure Philosophy

User follows **minimalist "奥卡姆剃刀" principle**: "如无必要勿增实体" (Occam's Razor - don't multiply entities unnecessarily).

### Key Preferences

1. **One entry point, not many directories**
   - User prefers a single wiki page as the entry point
   - Avoid creating new subdirectories under `attachments/` when content can go in existing `infographic/` or `raw/` directories
   
2. **Clear hierarchy, findable immediately**
   - User wants to "一眼找到" (find at a glance)
   - Structure should be obvious: entry page → file location

3. **No duplicate storage**
   - Don't copy files to multiple locations
   - Pick ONE canonical location and link/reference it

### Approved Structure Pattern

```
wiki/AI工具/[EntryPage].md     ← Single entry point
infographic/[topic]/           ← All related files here
  ├── source.md
  ├── structured-content.md
  └── output.html/.png
```

### Avoid

- Creating `attachments/macos-shortcuts/` when `infographic/` already has the files
- Multiple directories with overlapping content
- Deep nesting (>2 levels)

## Wiki Page Format

When creating wiki pages, follow this structure:
- YAML frontmatter: title, category, tags, sources, updated
- Clear section headers
- Direct links to files using relative paths
- Related pages section at bottom

## Design Preferences

### Dashboard Style
- **Not too plain**: User corrected agent for "太素了" (too plain) Markdown dashboard
- **Not bullet journal template style**: Don't make dashboards look like BuJo templates
- **HTML preferred**: For dashboards, use HTML with modern design (gradients, cards, animations)
- **Beautiful but minimalist**: Clean design that's visually appealing

### Visual Style
- Modern UI: gradient backgrounds, card layouts, rounded corners
- Responsive: works on phone, tablet, desktop
- Interactive: hover effects, smooth transitions
- Real-time elements: live clock display

### File Placement
- Put important files in **root directory** for easy access
- Don't bury dashboards in `attachments/` subdirectories
- "既然叫一页纸工作台的话" (if it's called a one-page workspace, it should be easily accessible)

## Index Updates

Always update `wiki/index.md` when adding new pages:
- Find the correct category section
- Add `| [[PageName]] | Brief description |`
- Keep alphabetical or logical ordering within section