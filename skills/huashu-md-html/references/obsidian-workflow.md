# Obsidian 知识库 → HTML 消费层

> 用 huashu-md-html 把 Obsidian wiki 笔记转为精美 HTML，实现「md 生产，html 消费」。

## 用户背景

用户使用 Obsidian (`wbaoc-wiki`) 作为个人知识库，结构：
- `raw/` — 原始剪藏素材（网页、PDF、视频字幕等）
- `wiki/` — LLM 提炼的结构化知识页（带 YAML frontmatter）
- `子弹笔记/` — BuJo 系统（日记、项目、工作台）

核心理念引用自 Karpathy：HTML 是人类最自然的知识消费格式。浏览器渲染引擎 30 年优化的就是人眼阅读体验。PDF 给打印机，Markdown 给机器，HTML 给人脑。

## 工作流

### 源文件位置
```
/Users/wbaoc/Documents/Obsidian/wbaoc-wiki/wiki/
```

### 转换命令
```bash
# article 模板（默认推荐，Tufte 风）
python3 ~/.hermes/skills/huashu-md-html/scripts/md_to_html.py \
  /path/to/wiki/笔记.md --theme article \
  -o /path/to/wiki/笔记.html

# interactive 模板（长文档，带折叠目录侧边栏）
python3 ~/.hermes/skills/huashu-md-html/scripts/md_to_html.py \
  /path/to/wiki/笔记.md --theme interactive
```

### 输出位置约定
- HTML 文件放在 **与 md 同目录**（wiki/ 下）
- 不放在 `raw/`（raw 是素材入口，不是消费端）
- 文件名与 md 一致，扩展名改为 `.html`

## 模板选择建议

| 内容类型 | 推荐模板 | 理由 |
|---------|---------|------|
| 知识笔记（CS Day1 等） | `article` | Tufte 风，表格+代码块表现好 |
| 长篇教程/手册 | `interactive` | 侧边栏 TOC，方便跳转 |
| 读书笔记/思考 | `reading` | 极简沉浸，适合纯文字 |
| 调研报告/数据密集 | `report` | 多表格，KPI grid |

## 已验证的 demo

2026-06-01: `wiki/计算机基础/CS从零开始/Day1-计算机基础与网络入门.md`
→ `Day1-计算机基础与网络入门.html`（article 模板）
效果：表格清晰、代码块深色背景、§ 编号橙色醒目、留白舒适。

## 批量转换思路

如果用户需要批量转换 wiki/ 下所有 md → HTML：
```bash
# 在 wiki/ 目录下执行
for f in $(find . -name "*.md" -not -name "index.md" -not -name "log.md"); do
  python3 ~/.hermes/skills/huashu-md-html/scripts/md_to_html.py "$f" --theme article
done
```
注意：`index.md` 和 `log.md` 是 Obsidian 导航文件，不转。
