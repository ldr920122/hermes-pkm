# Academic Materials Intake Workflow

When the user shares teacher/administrative notices about thesis formatting, defense requirements, or submission deadlines (typically via WeChat screenshots or forwarded messages).

## Trigger Signals

- "老师发了个通知"
- "论文格式要求"
- "答辩材料"
- "学位论文" + "模板" / "格式" / "提交"
- Screenshots of university notices with deadlines

## Workflow

### 1. Parse the notice
Extract from the message/images:
- What needs to be done (format changes, signatures, submissions)
- Deadlines
- Specific format requirements (degree titles, page layout, etc.)
- Submission method (email, portal, in-person)

### 2. Save images to dual locations
```bash
# Location A: Obsidian attachments (for wikilink embedding)
cp /path/to/image.jpg "$VAULT/attachments/扬大论文XXX模板.jpg"

# Location B: External project directory (for standalone reference)
cp /path/to/image.jpg "<MATERIALS_DIR>/论文格式模板/01_XXX模板.jpg"
```

### 3. Create project tracking note
Path: `子弹笔记/项目/扬大硕士论文.md` (or update if exists)

```yaml
---
tags: [项目, 扬大, 硕士, 论文, 毕业]
created: YYYY-MM-DD
status: 盲审等待中 ⏳
deadline: YYYY-MM-DD
---
```

Sections to include:
- **当前状态** — checklist of completed/pending milestones
- **老师通知** — verbatim key points from the notice
- **论文格式要求** — embed images with `![[filename.jpg]]`
- **提交清单** — actionable checklist with [ ] items
- **相关文件** — paths to external files and templates

### 4. If deadline involves a waiting condition
If the user says "等XX过了之后再做" (e.g., "等盲审过了之后"):
- Note the dependency in the project file
- Don't set a calendar reminder for an unknown date
- Tell the user: "你过了告诉我一声，我提醒你"
- The tracking note serves as the persistent reminder

## Key Distinctions

This is NOT the same as grant call extraction (which is about funding opportunities). This pattern is for:
- University administrative requirements
- Thesis formatting rules
- Defense preparation materials
- Degree application paperwork

## Pitfalls

- **Don't create separate subdirectories per notice** — keep everything in one project note with dated sections (minimalist principle)
- **Images go to attachments/** — not embedded as base64 or remote URLs. Obsidian wikilinks (`![[file.jpg]]`) require the file in `attachments/`
- **Teacher notices often have OCR-unfriendly formatting** — use tesseract (`-l chi_sim`) as fallback when vision_analyze fails
