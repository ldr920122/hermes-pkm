# Daily Learning Injection Pattern

## Overview

Automated daily content generation system that teaches academic concepts through stories/fables. Combines cron jobs, Obsidian storage, and Dataview dashboard integration.

## Components

### 1. Folder Structure
```
wiki/学习方法的寓言小故事/
├── README.md          ← prompt template + instructions
├── 统计学/
│   ├── 贝叶斯推断.md
│   ├── 第一类错误与第二类错误.md
│   └── ...
├── 大语言模型/
├── 计算机科学/
└── 金融/
```

### 2. README.md Template
```markdown
---
title: 学习方法的寓言小故事
category: 杂项
tags: [学习方法, 寓言, 知识卡片]
created: YYYY-MM-DD
---

# 学习方法的寓言小故事

> 用寓言故事学习研究生水平的概念。每天一个，潜移默化。

## 📐 当前领域：统计学

## 🎯 使用方法

### 换领域
对我说：「换领域：大语言模型」或「换领域：金融」

### 手动生成
对我说：「讲一个统计学寓言」

## 📝 Prompt 模板

我希望你从「{领域}」领域里选一个大概研究生水平的概念。然后通过写一个寓言的方式，间接地把这个概念完整讲出来。最好一直到快结尾时，人才会慢慢意识到这个概念究竟是什么。然后在故事之后，再补一段解释，把你刚才真正要讲的概念说清楚。

## 📂 目录结构
（同上）

## 🏷️ 标签规范
- `寓言故事` — 固定标签
- `学习方法` — 固定标签
- `{领域名}` — 如 `统计学`
- `概念名` — 如 `贝叶斯推断`
```

### 3. Cron Job Configuration
```json
{
  "name": "寓言故事-每日推送",
  "schedule": "0 8 * * *",
  "deliver": "origin",
  "prompt": "你是一个寓言故事作者。请完成以下任务：\n\n1. 从「{领域}」领域里选一个研究生水平的概念（不要重复已有的故事）\n2. 检查 {folder_path} 目录下已有的文件，避免重复\n3. 写一个寓言故事，间接地把这个概念讲出来，直到快结尾时读者才会意识到是什么概念\n4. **保持风格多样性**——每篇故事的叙事风格、角色、场景都要不同\n5. 故事后附上概念解析\n6. 保存为 Obsidian markdown 文件到：{folder_path}/{概念名}.md\n7. 文件格式要求：YAML frontmatter 包含 title, category(杂项), tags([寓言故事, 学习方法, {领域}, {概念名}]), created(今天日期)"
}
```

### 4. Dashboard Dataview Integration

Add to `子弹笔记/一页纸工作台.md`:
```markdown
## 07 — 寓言故事 · 每日一概念

> [!quote] 今日寓言
> ```dataview
> TABLE created as "日期", file.link as "故事"
> FROM "wiki/学习方法的寓言小故事/统计学"
> SORT created DESC
> LIMIT 1
> ```

📚 [[wiki/学习方法的寓言小故事/README|查看全部寓言故事]]
```

**Important**: When changing fields, update the `FROM` clause in the Dataview query to match the new folder path.

## Field Switching

To change the learning field:
1. Update the cron job prompt with new field name
2. Create new subfolder if it doesn't exist
3. Update README.md with new current field
4. Update Dataview query in dashboard

User says: 「换领域：大语言模型」
Agent does:
```bash
mkdir -p "wiki/学习方法的寓言小故事/大语言模型"
# Update cron job
# Update README.md
# Update dashboard Dataview query
```

## Story Style Diversity

User preference: **保持多样性** — each story should have different:
- Narrative style (寓言/神话/武侠/都市/科幻/民间故事)
- Characters and settings
- Tone and pacing

This prevents the learning system from feeling repetitive.

## Example Story Structure

```markdown
---
title: "寓言：{故事标题}"
category: 杂项
tags: [寓言故事, 学习方法, {领域}, {概念名}]
created: YYYY-MM-DD
---

# {故事标题}

## 📖 寓言
（故事内容，间接讲概念）

---

## 🔍 概念解析
（概念的正式解释，公式，应用）
```
