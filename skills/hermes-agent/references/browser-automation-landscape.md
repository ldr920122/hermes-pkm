# Browser Automation Landscape (2026-06)

## Hermes Browser Architecture

**底层**: `agent-browser` CLI + CDP (Chrome DevTools Protocol)

**模式**:
- **本地模式** (默认): 无头 Chromium, 零成本, 服务器也能跑. 一键安装: `agent-browser install`
- **云端模式**: Browserbase / Browser Use cloud, 有代理和反检测

**交互方式**:
- Agent 看到的是 accessibility tree (纯文本快照), 每个元素标记为 `@e1`, `@e2`
- 用 `browser_click("@e5")` 点击, `browser_type("@e3", "文字")` 输入
- 不需要视觉能力, 纯文本就能操作

**工具集**:
- `browser_navigate` — 导航到 URL
- `browser_snapshot` — 获取页面 accessibility tree 快照
- `browser_click` — 点击元素 (ref selector)
- `browser_type` — 输入文字
- `browser_select` — 选择下拉选项
- `browser_screenshot` — 截图 (视觉分析)

**Provider 支持** (browser_providers/):
- `browserbase` — 云端, 需要 API key
- `browser_use` — 云端, Nous 订阅用户默认
- `camofox` — 本地反检测浏览器
- `firecrawl` — 网页内容提取 (非交互式)

**Session 隔离**: 每个 task_id 独立 session, 自动清理

## Browser Harness (browser-use, ⭐14k)

**底层**: 直接 CDP websocket 连**真实浏览器** (非无头模式)
**仓库**: https://github.com/browser-use/browser-harness

**核心理念**: "Self-healing harness" — agent 执行过程中发现自己缺什么能力, 就自己写 helper 代码补上

**跟 Hermes 的关键区别**:
| 维度 | Hermes | Browser Harness |
|------|--------|-----------------|
| 浏览器 | 无头 Chromium (本地) 或云端 | **真实 Chrome** (带登录状态、cookies) |
| 交互 | 预定义工具 (navigate/click/type/snapshot) | agent 直接写 Python 操作 CDP |
| 自愈 | 不支持 | agent 缺 helper 时自己写代码补 |
| 学习 | 每次重来 | 生成 domain-skills (站点专属技能) 下次复用 |
| 适合 | 简单网页操作、信息提取 | 复杂流程 (登录、表单、多步操作) |

**杀手锏**: 连接已登录的浏览器 → 可操作需要登录的网站 (GitHub, LinkedIn, 银行等), 不需要处理登录流程

**架构** (~1k lines, 4 core files):
- `install.md` — 首次安装和浏览器引导
- `SKILL.md` — 日常使用
- `src/browser_harness/` — 核心包
- `agent-workspace/agent_helpers.py` — agent 可编辑的 helper 代码
- `agent-workspace/domain-skills/` — 可复用的站点技能

**免费云浏览器**: Browser Use Cloud free tier (3 concurrent browsers, proxies, captcha solving)

## playwright-cli (⭐1, 小项目)

**底层**: Playwright MCP 的 CLI 封装
**仓库**: https://github.com/Baldwin509/playwright-cli

**定位**: 给 Claude Code / Codex 用的浏览器自动化工具
**功能**: 录制操作 → 生成 Playwright 代码, 截图, selector 检查

**评价**: 项目太小 (1 star), 功能不成熟, 不推荐当前使用

## 选择建议

- **Hermes 浏览器** 够用的场景: 简单网页操作、信息提取、截图分析
- **Browser Harness** 值得关注的场景: 需要操作已登录网站、需要跨多次任务记住站点操作方式、复杂多步流程
- **playwright-cli**: 不推荐, 等项目成熟
