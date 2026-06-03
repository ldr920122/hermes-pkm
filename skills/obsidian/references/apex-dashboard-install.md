# Apex Dashboard Plugin Installation Log

**Date**: 2026-05-23
**Plugin**: Apex Dashboard v1.0.7
**GitHub**: https://github.com/PandoraReads/apex-dashboard

## Installation Steps Performed

```bash
# 1. Cloned repo
cd ~/Downloads && git clone https://github.com/PandoraReads/apex-dashboard.git

# 2. Created plugin directory
mkdir -p ~/Documents/Obsidian/wbaoc-wiki/.obsidian/plugins/apex-dashboard

# 3. Copied files
cp ~/Downloads/apex-dashboard/main.js \
    ~/Downloads/apex-dashboard/manifest.json \
    ~/Downloads/apex-dashboard/styles.css \
    ~/Downloads/apex-dashboard/package.json \
    ~/Documents/Obsidian/wbaoc-wiki/.obsidian/plugins/apex-dashboard/

# 4. Added to community-plugins.json
# Added "apex-dashboard" to the array

# 5. User needs to restart Obsidian and enable plugin
```

## Plugin Features (v1.0.7)

- **Memo cards** with `[[双链]]` support
- **Todo** with drag-and-drop, progress bar, reminders
- **Projects** supporting multiple file types
- **Notes** compact list view
- **Quick actions** sidebar with file/command shortcuts
- **Banner** with rotating quotes and background images
- **11 themes**: 大地, 北欧, 极光, 春日, 岛屿, 苔原, 花漾, 薄雾, 余烬, 暮霞, 翡翠

## User Context

User wanted a dashboard that feels "人文味" (humanistic) rather than "AI味" (AI-flavored). The plain Markdown dashboard I created was "太素了" (too plain). Apex Dashboard with its curated themes (especially 大地 - earthy parchment) matches this preference.

## Usage

1. Open via left sidebar icon or command: `Apex Dashboard: Open dashboard`
2. First use creates `dashboard.md` in vault root
3. Change theme in Settings → Apex Dashboard → Style
4. All data saved to `dashboard.md` (plain text, portable)