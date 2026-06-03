# Obsidian Plugin Installation (Manual)

When a user wants to install an Obsidian plugin that's not yet in the community plugins marketplace (or they want a specific GitHub repo version):

## Standard Manual Installation

```bash
# 1. Clone/download the plugin repo
cd ~/Downloads && git clone https://github.com/<owner>/<plugin-name>.git

# 2. Create plugin directory in vault
PLUGIN_DIR="$VAULT/.obsidian/plugins/<plugin-id>"
mkdir -p "$PLUGIN_DIR"

# 3. Copy required files (usually main.js, manifest.json, styles.css)
cp <plugin-name>/main.js <plugin-name>/manifest.json <plugin-name>/styles.css "$PLUGIN_DIR/"
# Some plugins also need package.json
cp <plugin-name>/package.json "$PLUGIN_DIR/" 2>/dev/null || true

# 4. Add plugin ID to community-plugins.json
# Edit .obsidian/community-plugins.json — add the plugin ID to the array
# Plugin ID comes from manifest.json → "id" field

# 5. Restart Obsidian

# 6. Enable in Settings → Community Plugins
```

## Key Files Check

Always check `manifest.json` for the plugin ID:
```bash
cat "$PLUGIN_DIR/manifest.json" | grep '"id"'
```

## Pitfalls

- **Plugin ID mismatch**: The ID in `manifest.json` must exactly match what you add to `community-plugins.json`. Case-sensitive.
- **Missing files**: Some plugins need additional files (assets, fonts, etc.). Check the repo's README.
- **Dependency issues**: Some plugins require other plugins to be installed first. Check the README.
- **Version compatibility**: Check `minAppVersion` in `manifest.json` against user's Obsidian version.

## Recommended Plugins for This User

Based on user's workflow (P-person, minimalist, BuJo, research):

| Plugin | Purpose | Why needed |
|--------|---------|------------|
| **Apex Dashboard** | Beautiful one-page workspace | User prefers "人文味" design over plain Markdown |
| **Dataview** | Dynamic queries for tasks/stats | Essential for BuJo dashboard |
| **Tasks** | Enhanced task management | Dates, priorities, recurrence |
| **Calendar** | Daily note navigation | Click date → open daily note |
| **QuickAdd** | Quick capture | Add to inbox without opening file |

## Apex Dashboard (Specific Recommendation)

**GitHub**: https://github.com/PandoraReads/apex-dashboard
**Why**: 11 curated themes with warm, humanistic options (大地, 春日, 余烬)
**Install**: See `references/apex-dashboard-install.md` for step-by-step
**Theme recommendation**: 大地 (earthy parchment) or 春日 (rose warmth) for "人文味" preference