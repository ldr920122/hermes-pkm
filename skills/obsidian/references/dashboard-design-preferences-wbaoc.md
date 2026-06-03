# Dashboard Design Preferences (wbaoc)

## User Corrections from Session 2026-05-25

### What They Said
1. "光是白色，没有其他颜色，就是你看不清重点" — too plain, need accent colors
2. "你也可以整一些其他的配色，比如那个 Claude Code 的橘黄色" — wants Claude Code orange
3. "不要光是这个这个白色，就米白色的背景" — needs more than just off-white
4. "AI味太重" — too generic AI-looking
5. "更具人文味的这种感觉" — wants humanistic, crafted feel
6. "根目录下第一页" — dashboard should be in root, not buried

### Design Evolution
1. **v0 (纯白)**: Pure MUJI off-white, no accent → "看不清重点"
2. **v1 (Apple)**: Apple HIG with blue accent → "AI味太重"
3. **v2 (Apex Dashboard)**: Third-party plugin → "不好看，不如你做的"
4. **v3 (MUJI + Orange)**: MUJI structure + Claude Code orange accent → ✅ Accepted

### Final Design System
- **Base**: MUJI/Kenya Hara (warm off-white #F4F2EC, hard edges, 60-80% whitespace)
- **Accent**: Claude Code orange #D97706 (section labels, focus numbers, progress bars)
- **Typography**: system-ui, 96px hero date, 24px weekday
- **Interaction**: clipboard fallback for obsidian:// links

### Key Components
1. **Hero Date Block**: 96px date + weekday + weather + quote
2. **Focus Items**: 32px accent numbers + left border hover effect
3. **Task List**: accent checkboxes + priority tags
4. **Progress Bars**: 2px, accent/green/red by status
5. **Stat Cards**: white bg with left accent border
6. **Quick Links**: obsidian:// with clipboard fallback

### Technical Notes
- **Timezone**: Always use UTC+8 for Beijing time
- **File naming**: Daily notes must be `YYYY-MM-DD_Day.md` (e.g., `2026-05-25_Mon.md`)
- **Dashboard updates**: Content must be manually updated daily from daily notes
- **Protocol fallback**: obsidian:// links need clipboard copy fallback for browser context

## What NOT to Do
- ❌ Pure white/off-white only — needs accent colors
- ❌ Generic gradient backgrounds — "AI味太重"
- ❌ Complex shadows and rounded corners — user prefers hard edges
- ❌ Bury dashboard in subdirectories — user wants root-level access
- ❌ Assume obsidian:// links work in all contexts — need fallback