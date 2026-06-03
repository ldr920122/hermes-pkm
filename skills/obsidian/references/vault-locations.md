# Obsidian Vault Locations (macOS)

Common real-world Obsidian vault paths — the default `~/Documents/Obsidian Vault` is rarely accurate.

## Discovery Commands

Probe for all `.obsidian` config dirs on the system (up to 3 levels deep):

```bash
# Local Documents
find ~/Documents -name ".obsidian" -type d -maxdepth 3 2>/dev/null

# iCloud Obsidian sync
find "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents" -name ".obsidian" -type d -maxdepth 2 2>/dev/null

# Broad scan (Desktop + Documents + user Home)
find ~/Documents ~/Desktop ~ -maxdepth 4 -name ".obsidian" -type d 2>/dev/null | head -10
```

## Common Patterns

| Location | Typical Owner | Notes |
|----------|---------------|-------|
| `~/Documents/Obsidian Vault/` | New/auto-created | Rarely used in practice |
| `~/Documents/obsidian/<vault-name>/` | Enthusiast | Manually organized, nested |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<vault-name>/` | iCloud sync user | Apple ecosystem, also in Files app |
| `~/Desktop/<vault-name>/` | Quick start | Often temporary |

## Inferring the Vault Name

The vault directory name is what Obsidian calls it. If the dir has a `.obsidian/` subfolder inside, it's a vault. The `workspace.json` contains the last-opened workspace but **not** the vault ID — that's stored in `app.json`:

```bash
cat "$VAULT/.obsidian/app.json" 2>/dev/null | python3 -m json.tool | grep vault
```

## When Vault Path Changes (Migration)

Users may switch between iCloud and local storage. Steps to re-discover:

1. Check `memory` for saved vault path — if stale, update it
2. Probe common locations with the find commands above
3. Look for Chinese folder names (e.g. `学习笔记`, `个人`, `知识库`) — these are strong identifiers
4. Verify: confirm there's a `.obsidian/` config directory and at least one `.md` note

## Bilingual Tag Convention

When creating notes for Chinese-speaking users, frontmatter tags **should match their existing convention**. Common patterns:

```yaml
tags: [ obsidian, obsidian同步, 效率, mac, macos, shortcut ]
```

Mixing Chinese and English tags is normal. Do not force purely English tags.
