# Minimalist Organization Principles (wbaoc)

## User Preference

User follows 奥卡姆剃刀原则（如无必要勿增实体）— Occam's razor, "don't multiply entities beyond necessity."

**Core principle**: When organizing files in Obsidian, prefer:
- **One entry page** + **one file directory** (not multiple scattered locations)
- **Flat structure** over deeply nested hierarchies
- **Avoid duplicate directories** — if files exist in `infographic/`, don't also copy them to `attachments/subfolder/`
- **一眼能找到** — findable at a glance, no hunting through nested folders

## Anti-patterns (User Corrected These)

1. **Creating `attachments/macos-shortcuts/` when `infographic/` already had the files** — duplicate locations create confusion
2. **Multiple entry points to the same content** — pick ONE canonical location
3. **Over-organizing small projects** — don't create a subdirectory for every 3-file project

## Recommended Pattern

```
# Good: one entry + one directory
wiki/AI工具/macOS常用快捷键速查图.md  ← single entry page with links
infographic/macos-shortcuts-command/    ← all files here
infographic/macos-shortcuts-option/
infographic/macos-shortcuts-control/

# Bad: duplicate locations
attachments/macos-shortcuts/            ← duplicate of infographic/
wiki/AI工具/macOS常用快捷键速查图.md   ← links to both locations = confusion
```

## When Organizing User's Vault

1. Check if content already exists somewhere before creating new directories
2. Prefer updating existing pages over creating new ones
3. If a small project (1-3 files), keep it in the parent directory rather than creating a subdirectory
4. Always have ONE clear entry point — the user should know "go to X to find Y"

## Trigger Keywords

"整理", "太乱了", "重复", "能不能整理一下", "一眼找到", "极简", "如无必要勿增实体"