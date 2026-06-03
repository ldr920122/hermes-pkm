<div align="center">

# 🧠 药师的第二大脑

### 基于 Obsidian + Hermes Agent 的个人知识管理系统

**让AI成为你的药学知识助手，而不是替代你的思考**

[![GitHub stars](https://img.shields.io/github/stars/ldr920122/hermes-pkm?style=social)](https://github.com/ldr920122/hermes-pkm)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made for Pharmacists](https://img.shields.io/badge/Made%20for-Pharmacists-7C3AED.svg)](https://github.com/ldr920122/hermes-pkm)

</div>

---

## 💡 这是什么？

一个**药房药师**搭建的AI增强知识管理系统。核心思路：

> **Obsidian 管记忆，Hermes Agent 管行动，AI 管思考。**

不用写代码，不用懂技术。就像给你的大脑装了一个「搜索 + 整理 + 执行」的外挂。

```
┌─────────────────────────────────────────────────┐
│                  你的大脑 🧠                      │
│         想法 / 经验 / 灵感 / 问题                  │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │      Obsidian 📓        │
        │   双向链接 · 知识图谱    │
        │   存储 · 检索 · 关联     │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   Hermes Agent 🤖       │
        │   AI对话 · 自动化流程    │
        │   多平台 · 持久记忆      │
        └────────────┬────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐     ┌─────▼─────┐    ┌────▼────┐
│ 微信 💬│     │ Telegram 📱│    │ 飞书 📨 │
│随手问AI│     │ 深度对话   │    │ 团队协作│
└────────┘     └───────────┘    └─────────┘
```

---

## 🚀 5分钟上手

### 第一步：安装 Hermes Agent

```bash
# macOS / Linux
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 初始化
hermes setup
```

> 💡 详细安装文档：[hermes-agent.nousresearch.com/docs](https://hermes-agent.nousresearch.com/docs)

### 第二步：安装 Obsidian

从 [obsidian.md](https://obsidian.md) 下载，创建一个 Vault（知识库）。

### 第三步：添加本仓库的 Skills

```bash
# 克隆本仓库
git clone https://github.com/ldr920122/hermes-pkm.git

# 安装 skills（每个子目录就是一个 skill）
cd hermes-pkm/skills
for skill in */; do
  hermes skill install "$skill"
done
```

### 第四步：开始使用

```
你：帮我整理一下卡瑞利珠单抗的不良反应
Hermes：正在搜索文献... 已整理为结构化笔记，保存到 Obsidian
```

---

## 📚 Skills 分类

### 🎓 学术与科研

| Skill | 功能 | 药师场景 |
|-------|------|----------|
| **[academic-writing](skills/academic-writing/)** | 中文学术写作助手 | 论文撰写、课题申报、基金申请 |
| **[arxiv](skills/arxiv/)** | 学术论文搜索 | 追踪药物研发前沿 |
| **[llm-wiki](skills/llm-wiki/)** | AI知识库构建 | 自动整理文献为结构化wiki |
| **[obsidian](skills/obsidian/)** | Obsidian笔记管理 | 创建、搜索、管理知识库 |
| **[obsidian-dashboard-design](skills/obsidian-dashboard-design/)** | 工作台设计 | 个性化首页、项目看板 |

### 💊 药学专业

| Skill | 功能 | 药师场景 |
|-------|------|----------|
| **[carl-weread](skills/carl-weread/)** | 微信读书教练 | 阅读药学书籍→行动卡片 |
| **[learning-fable-writer](skills/learning-fable-writer/)** | 学习寓言创作 | 用故事理解复杂概念 |

### 🤖 AI 效率工具

| Skill | 功能 | 药师场景 |
|-------|------|----------|
| **[hermes-agent](skills/hermes-agent/)** | AI助手配置 | 多平台对话、自动化工作流 |
| **[ai-productivity-workflow](skills/ai-productivity-workflow/)** | AI增强工作流 | 研究→计划→执行 |
| **[fat-loss-coach](skills/fat-loss-coach/)** | 赛博健身搭子 | 值班夜班的健康管理 |
| **[huashu-md-html](skills/huashu-md-html/)** | 文档格式转换 | 论文/报告互相转换 |

### 🎯 职场技能

| Skill | 功能 | 药师场景 |
|-------|------|----------|
| **[powerpoint](skills/powerpoint/)** | PPT自动生成 | 教学查房、科室汇报 |
| **[humanize-ppt](skills/humanize-ppt/)** | 人性化PPT设计 | 让AI做的PPT不再像AI |
| **[x-article-publisher](skills/x-article-publisher/)** | X/Twitter发布 | 药学科普、个人品牌 |

---

## 🏗️ 系统架构

```
你的手机/电脑
    │
    ├── Obsidian（知识库）
    │   ├── 📂 wiki/          ← 结构化知识
    │   ├── 📂 raw/           ← 原始素材
    │   ├── 📂 子弹笔记/      ← 日记 + 待办
    │   └── 📊 一页纸工作台.md  ← 仪表盘
    │
    ├── Hermes Agent（AI层）
    │   ├── 💬 微信/Telegram/飞书  ← 多平台入口
    │   ├── 🧠 持久记忆           ← 跨会话记住你
    │   ├── ⚡ Skills             ← 可复用的工作流
    │   └── ⏰ Cron Jobs         ← 定时自动化
    │
    └── 云端 API
        ├── DeepSeek / Claude   ← AI推理引擎
        └── 各种工具API         ← 扩展能力
```

---

## 📖 真实使用场景

### 场景 1：文献整理

```
你（微信发消息）：这篇文献帮我整理一下，保存到知识库
    ↓
Hermes：抓取网页 → 提取核心信息 → 生成结构化笔记 → 保存到 Obsidian
    ↓
你的 Obsidian 里多了一篇带标签、双向链接的笔记
```

### 场景 2：值班夜班

```
你：今晚夜班，帮我列一下注意事项
    ↓
Hermes：基于你的历史笔记 → 整理值班清单 → 发到微信
```

### 场景 3：论文写作

```
你：帮我写一段卡瑞利珠单抗心脏毒性的文献综述
    ↓
Hermes：搜索 arXiv/文献库 → 整理关键发现 → 生成结构化综述 → 保存到 Obsidian
```

---

## 🎤 关于我

**刘冬瑞** — 泰州市人民医院药师 / 扬州大学药学硕士 / 东华理工大学CS在读

一个白天在药房发药、晚上在学代码的普通药师。用这个系统管理自己的知识、论文、项目和生活。

> *"药师不只是发药的，我们是药物信息的管理者。用好AI，才能更好地服务患者。"*

---

## 📄 License

MIT License — 随便用，改，分享。

---

<div align="center">

**觉得有用？给个 ⭐ Star 鼓励一下！**

*Built with ❤️ by a pharmacist who codes*

</div>
