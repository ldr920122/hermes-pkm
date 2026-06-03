---
name: ai-productivity-workflow
description: AI增强的个人生产力工作流。基于Matt Van Horn的"Research→Plan→Build"方法论，适配Hermes+Obsidian+Claude Code/Codex环境。当用户讨论工作流优化、效率提升、AI工具协同、多agent编排、或问"怎么更快/更高效"时加载。
version: 1.0.0
author: hermes
tags: [productivity, workflow, claude-code, codex, hermes, obsidian, plan-driven, matt-van-horn]
triggers:
  - 工作流|效率|优化工作|生产力|怎么更快|更高效
  - plan\.md|Research.*Plan.*Build|多agent|并行执行
  - Claude.*Codex.*配合|费用优化|额度有限|token预算
  - 语音输入|voice|通勤|碎片时间|双手占用
  - AI.*协同|agent.*协作|工具链|自动化流程
---

# AI-Enhanced Personal Productivity Workflow

基于 Matt Van Horn 的 "No IDE, Just plan.md and Voice" 方法论，适配用户现有环境（Hermes + Obsidian + Claude Code/Codex + Telegram）的个人生产力工作流。

## Core Methodology: Research → Plan → Build

Matt Van Horn 的核心工作流（原文：gu-log.vercel.app/en/posts/en-sp-126-20260322-mvanhorn-claude-code-hacks）：

### 1. Research（调研）
- **工具**：Hermes web_search / browser / Claude Code 的 /last30days 插件
- **原则**：任何任务开始前，先调研当前社区/领域已知的最佳实践
- **用户适配**：Hermes 已有 web_search 和 browser 能力，可直接用于调研

### 2. Plan（计划）
- **工具**：Obsidian 中的 plan.md 文件（或子弹笔记模板）
- **原则**：**除非是一行修改，否则永远先有 plan.md**
- **关键洞见**：聊天气泡是金鱼记忆，文件才是白板。plan.md 是"能存活跨会话的检查点"
- **用户适配**：子弹笔记的"脑内倾倒→收集箱→月度迁移"已有计划雏形，可升级为结构化 plan.md

### 3. Build（执行）
- **工具**：Claude Code（Opus）做深度推理，Codex 做批量执行，Hermes 做协调
- **原则**：80% 时间花在 planning，20% 花在 execution
- **用户适配**：额度有限时，Claude Code 用于高价值推理任务，Codex 用于重复性执行

## User-Specific Adaptations

### 时间约束
用户每天仅 3-4 小时自由时间（上班8h + 睡觉7h + 带娃2-3h + 通勤吃饭2h）。**做减法而非加法**——最多同时推进3件事。

### 通勤场景（骑车，无法看屏幕）
- 纯听场景：播客/音频/语音笔记
- M5Stack Cardputer 到货后：按一下键→语音→Hermes 转文字→自动存入 Obsidian
- 碎片时间（午休/睡前）：屏幕内容（视频/阅读/课程）

### 成本优化（额度有限）
- **Claude Code（Opus）**：高价值推理——论文改写策略、SCI 期刊匹配、复杂架构设计
- **Codex**：批量执行——数据处理脚本、格式转换、重复性代码
- **Hermes（DeepSeek）**：日常对话、文件管理、任务协调
- **规则**：先用有限额度跑通流程，验证 ROI 后再加预算

### 远程控制
- Mac Mini + Telegram → Hermes 已实现（比 Matt 更早走通）
- 睡前给 Hermes 排 cron 任务 → 第二天早上看结果（最接近"晚安模式"的实现）

## Plan.md Template for Obsidian

```markdown
# Plan: [任务名称]
created: YYYY-MM-DD HH:mm
status: [pending|in-progress|done]

## Goal
一句话描述目标

## Context
- 当前状态：
- 约束条件：
- 参考文件：

## Steps
- [ ] Step 1: ...
- [ ] Step 2: ...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
（执行过程中记录）
```

## Pitfalls

1. **不要照搬 Matt 的 4-6 个并行窗口**：他是全职开发者，你只有 3-4 小时自由时间。你的版本是 1 个 Hermes + 1 个 Claude Code + 睡前 cron
2. **额度有限时先验证 ROI**：不要一上来就买 $200+200 的订阅，先用有限额度跑通一个完整任务，确认工作流有效再加
3. **plan.md 不是待办清单**：它是执行蓝图，包含目标、方法、验收标准、参考文件路径。与子弹笔记的"今日三件事"互补而非替代
4. **语音输入的价值在于消除延迟**：不是"语音比打字快"，而是"有想法的瞬间就能捕捉，不用等到坐下打字"
5. **并行执行的核心不是同时想 6 件事**：是同一个 plan.md 驱动的 6 个执行步骤，本质上是流水线而非并行思考

## References

- 原文：Matt Van Horn's Full Claude Code Workflow (2026-03-23)
  - URL: gu-log.vercel.app/en/posts/en-sp-126-20260322-mvanhorn-claude-code-hacks
  - 核心概念：plan.md as checkpoint, voice as primary input, 4-6 parallel sessions, Claude thinking + Codex execution
