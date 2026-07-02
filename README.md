<div align="center">

# 药师的第二大脑

**智能体 + Obsidian 的个人知识管理方法**

「知识库不是资料仓库，而是智能体的长期工作记忆。」

[这是什么](#这是什么) · [我怎么用的](#我怎么用的) · [安装](#安装) · [Skills](#skills) · [关于我](#关于我)

</div>

---

让 AI 不是"替你想"，而是能持续读写你的笔记、记住你的上下文、帮你把日常学习和工作沉淀下来。

你今天丢进去的东西，明天智能体还能继续用——这就是长期记忆和普通聊天的区别。

## 这是什么

一套在真实学习、科研、写作和日常管理中跑通的 AI 增强知识管理方法。

**Obsidian 管长期记忆，AI 智能体管收集、整理、提醒和调用。**

```
你（提问 / 丢资料 / 写想法）
  → 智能体（Claude Code / Hermes / Codex）  ← → LLM API（DeepSeek / Claude / GPT）
    → Obsidian Vault（raw/ 原始资料 · wiki/ 结构化知识 · 子弹笔记/）
      → 下一次写作、讲课、科研时被智能体再次检索和调用
```

不是一个新的笔记软件，也不是提示词集合。核心是把本地 Obsidian Vault 变成智能体可以长期读写的工作记忆。

---

## 我怎么用的

### 资料怎么存进来

文章、论文、网页、视频笔记、会议纪要、自己的想法——先放进 Obsidian。不是所有资料都会变成知识，判断标准很简单：**这条内容下个月我还能不能复用？**

临时信息留在 `raw/` 或收集箱。能反复用于论文、讲课、工作、项目判断的，让智能体整理成结构化 wiki：

> 一篇文章 → 智能体判断是否值得沉淀 → 拆成原则、方法、案例、工具、洞察 → 写入 wiki/

### 子弹笔记日常

我用 Obsidian 做日常任务和复盘，智能体负责提醒和整理：

| 时间 | 智能体做什么 |
|------|------------|
| **早 8:00** | 读取项目、收集箱和日记，推送今天最应该推进的事 |
| **白天不定时** | 从知识库里抽取旧笔记，生成复习卡片，避免知识只被收藏不被使用 |
| **晚 9:00** | 提醒安排 30 分钟学习，把学到的内容归档到 Obsidian |

重点不是把计划写得漂亮，而是让它和智能体形成闭环：**收集箱 → 今日任务 → 日记记录 → 每周复盘 → 重新沉淀成知识**。

### 知识库（LLM Wiki）

可复用内容整理成本地 wiki。它和普通资料库的区别：

| | 资料库 | 知识库 |
|---|------|------|
| 存什么 | 什么都存 | 只沉淀可复用内容 |
| 谁来用 | 主要给人翻 | 主要给智能体调用 |
| 时间久了 | 越堆越乱 | 定期复盘和更新 |
| 怎么存 | 原文照搬 | 拆成原则、方法、案例、反模式 |

写论文时让智能体从知识库找综述材料；做 PPT 时基于已有笔记生成大纲；每周复盘时让智能体告诉我哪些资料值得升级成知识。

**收集 → 整理 → 调用 → 复盘 → 再沉淀。** 这是整个系统的核心循环。

---

## 安装

你需要两个东西：**Obsidian**（本地知识库）+ **一个能读写本地文件的 AI 智能体**。

### 1. 安装 Obsidian

从 [obsidian.md](https://obsidian.md) 下载，创建一个 Vault。建议先从最简单的目录开始：

```
你的 Vault/
├── raw/          ← 原始资料
├── wiki/         ← 结构化知识
└── 子弹笔记/      ← 日记、待办、复盘
```

### 2. 安装一个智能体（三选一）

| 工具 | 一句话 | 安装 |
|------|-------|------|
| **Claude Code** | 最省心，读写本地文件、写文档、改代码 | [claude.ai/download](https://claude.ai/download) |
| **Hermes Agent** | 多平台入口、定时任务、长期自动化 | `curl -fsSL https://hermes-agent.nousresearch.com/install.sh \| bash` |
| **OpenAI Codex** | 在代码仓库和本地文件里协作 | [openai.com/codex](https://openai.com/codex) |

刚开始？装 **Obsidian + Claude Code** 就够了。

### 3. 使用本仓库的 Skills

```bash
git clone https://github.com/ldr920122/hermes-pkm.git
```

- **Claude Code / Codex 用户**：把 `skills/` 目录里的 `SKILL.md` 当作工作流说明，复制到你的项目中使用。
- **Hermes 用户**：`hermes skills install` 安装需要的 skill。
- **建议**：先把「Obsidian + 智能体能读写笔记」这个最小闭环跑通，不要一次装完所有 skill。

---

## Skills

先看这几个就够了：

| Skill | 做什么 |
|-------|-------|
| [obsidian](skills/obsidian/) | 读写 Obsidian 笔记——搜索、创建、追加、管理 Vault 结构 |
| [llm-wiki](skills/llm-wiki/) | 把资料整理成结构化知识库，生成可被智能体调用的 wiki 页面 |
| [hermes-agent](skills/hermes-agent/) | Hermes 配置、多平台入口、定时任务、自动化工作流 |
| [academic-writing](skills/academic-writing/) | 中文学术写作——论文、课题申报、基金申请 |
| [ai-productivity-workflow](skills/ai-productivity-workflow/) | 研究 → 计划 → 执行 → 复盘的完整工作流 |
| [hermes-tweet](skills/hermes-tweet/) | X/Twitter 读取、监控、用户查询和需确认的社交动作流程 |

更多 skills（PPT 大纲、arXiv 搜索、微信读书、Markdown/HTML 转换等）见 [`skills/`](skills/) 目录。

### 来源说明

`skills/` 里既有我自己写的，也有社区作者的优秀作品（均保留原作者署名和许可，方便你顺藤摸瓜找到原版）：

| 分类 | Skill | 作者 / 来源 |
|------|-------|------------|
| 原创 | academic-writing、learning-fable-writer、obsidian-dashboard-design、ai-productivity-workflow、x-article-publisher | 刘冬瑞（本仓库） |
| 原创（基于 Hermes 原版扩展） | obsidian | 本仓库 + Hermes Agent |
| 第三方 | llm-wiki | sdyckjq-lab · MIT |
| 第三方 | huashu-md-html | 花叔 |
| 第三方 | carl-weread、humanize-ppt | Carl / LearnPrompt · MIT |
| 第三方 | arxiv、hermes-agent | Hermes Agent / Nous Research · MIT |

需要 PowerPoint 文件生成能力，推荐 Anthropic 官方 [skills 仓库](https://github.com/anthropics/skills)的 pptx skill（专有许可，故不收录在本仓库）。

---

## 装好以后可以这样问

不要只问「帮我总结」。让智能体参与你的知识循环：

```
把这篇文章放进我的 Obsidian，判断它下个月还能不能复用。
帮我从最近一周的日记里整理出可以沉淀进 wiki 的知识。
基于我的知识库，帮我生成一个 10 分钟讲课大纲。
每天早上 8 点提醒我今天最重要的 3 件事。
```

---

## 适合谁

想把 Obsidian 从「笔记仓库」变成「AI 工作记忆」的人。药师、研究生、老师、学生、内容创作者都可以参考。如果你还没用过 Obsidian，也可以先把它当成「本地知识库 + AI 助手」的入门示例。

---

## 关于我

**刘冬瑞** · 泰州市人民医院药师 / 扬州大学药学硕士 / 东华理工大学 CS 在读

白天在药房发药，晚上学代码。这套系统不是坐在书桌前设计出来的，是在值班、写论文、备课、做项目、每天被琐事打断的生活里一点点长出来的。

> 药师不只是发药的，我们也是药物信息的管理者。用好 AI，才能更好地服务患者。

---

MIT License — 随便用、改、分享。

<div align="center">

如果这个方法对你有启发，欢迎 Star。

</div>
