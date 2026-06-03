# Obsidian Knowledge Base Organization Patterns

## User's Vault Structure
```
wbaoc-wiki/
├── 00 templates/       # Templates
├── attachments/        # Images and attachments
├── raw/                # Raw materials (read-only)
│   ├── clippings/      # Web/video clippings
│   ├── articles/       # Articles
│   ├── chats/          # AI conversations
│   └── inbox/          # Pending items
├── wiki/               # Structured knowledge base
│   ├── AI工具/         # AI tools and techniques
│   ├── 生物信息学/     # Bioinformatics
│   ├── 网络药理学/     # Network pharmacology
│   └── ...
├── 子弹笔记/           # Bullet journal system
│   ├── 日记/           # Daily notes
│   ├── 每周/           # Weekly reviews
│   ├── 项目/           # Projects
│   └── ...
└── 微信读书/           # WeChat reading notes
```

## Organization Principles

### 1. Single Entry Point
- Create one Markdown page as the main reference for each topic
- Place in appropriate `wiki/` subdirectory
- Include all relevant links and references in this single page

### 2. Clear File Hierarchy
- **Source files**: `infographic/{topic-slug}/` or similar logical grouping
- **Attachments**: `attachments/` for images, PDFs, etc.
- **Templates**: `00 templates/` for reusable templates

### 3. Avoid Duplication
- Don't create multiple copies of the same file
- Use relative links to reference files from their actual location
- If creating temporary files, clean up after organization

### 4. Index Maintenance
Always update `wiki/index.md` when adding new content:
```markdown
| [[Page Title]] | Brief description of content |
```

### 5. Change Logging
Add entry to `wiki/log.md` for traceability:
```markdown
## [YYYY-MM-DD] action | description
- Details of what was done
- Files created/modified
- Key decisions made
```

## Workflow for Adding New Content

### Step 1: Create Content
- Generate files in appropriate location
- Follow naming conventions (kebab-case, descriptive)

### Step 2: Create Reference Page
- Create Markdown page in `wiki/{category}/`
- Include YAML frontmatter with metadata
- Add clear description and usage instructions

### Step 3: Update Index
- Add entry to `wiki/index.md`
- Use consistent format with existing entries

### Step 4: Log Changes
- Add entry to `wiki/log.md`
- Include date, action, and details

### Step 5: Clean Up
- Remove any temporary or duplicate files
- Ensure all links are working

## Common Patterns

### For Infographics/Visual Content
```
infographic/{topic-slug}/
├── source-{slug}.md          # Source content
├── analysis.md               # Content analysis
├── structured-content.md     # Structured content
├── prompts/infographic.md    # Generation prompt
└── {topic-slug}.html         # HTML version (fallback)
```

### For Reference Materials
```
wiki/{category}/{topic}.md    # Main reference page
attachments/{topic}/          # Supporting files
```

### For Daily Notes
```
子弹笔记/日记/YYYY-MM-DD_ddd.md
```

## User Preferences

1. **Minimalism**: Keep structure simple and clean
2. **Discoverability**: Easy to find what you need
3. **Consistency**: Follow established patterns
4. **Traceability**: Log changes for future reference

## Pitfalls to Avoid

1. **Creating duplicate directories**: Don't create `attachments/macos-shortcuts/` when `infographic/` already exists
2. **Missing index updates**: Always update `wiki/index.md`
3. **Inconsistent naming**: Use kebab-case for directories and files
4. **Forgetting cleanup**: Remove temporary files after organization
5. **Over-complicating**: Don't create unnecessary subdirectories or files