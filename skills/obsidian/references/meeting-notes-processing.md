# Meeting Notes Processing Workflow

## Trigger
User sends raw AI-generated meeting summary (from 元宝/Yuanbao, Kimi, or other tools) and asks to "整理" (organize) and save to Obsidian.

## Input Sources
- **元宝会议助手** (Tencent Meeting AI): generates timestamped speaker-by-speaker commentary with heavy AI-flavor analysis ("值得注意的是", "暗示了", "隐含了", "侧面反映")
- **Kimi** / **通义听悟** / other transcription AI: similar pattern — raw transcript + AI commentary mixed together

## Processing Steps

1. **Read the full raw file** — it's usually very long (500+ lines). Don't skim.

2. **Identify structure from timestamps** — each `元宝会议助手(HH:MM:SS):` block is a speaker segment. Group by actual speaker/topic, not by AI commentary unit.

3. **Strip AI-flavor commentary aggressively**:
   - Remove: "值得注意的是", "暗示了", "隐含了", "侧面反映", "可能表明", "透露出"
   - Remove: meta-analysis of speaker's emotional state or delivery quality
   - Remove: speculation about motivations, hidden agendas, or interpersonal dynamics
   - Keep: concrete data points, policy details, technical specifications, named tools/systems

4. **Restructure by speaker/topic**:
   ```
   ### 一、主题名称（演讲者）
   - 核心数据/结论
   - 具体案例
   - 关键技术/工具
   ```

5. **Extract actionable insights** for a `🔑 对我的启发` section with `- [ ]` checkboxes

6. **Add YAML frontmatter**:
   ```yaml
   ---
   title: 会议名称
   date: YYYY-MM-DD
   type: 会议记录
   tags: [相关标签]
   platform: 腾讯会议/线下
   source: 元宝会议纪要
   ---
   ```

7. **Save to** `子弹笔记/会议/YYYY-MM-DD 会议名称.md`

8. **Offer to update daily note** — append a bullet to `## 📝 笔记 · 事件 · 感想`:
   ```
   - ○ 参加了[会议名称]（腾讯会议）
   ```

## Quality Standards

- **Compression ratio**: raw 600 lines → structured 100-150 lines (80%+ reduction)
- **Zero AI-flavor in output**: the final note should read as if a human pharmacist wrote it
- **Data preservation**: all concrete numbers (wait times, drug counts, pricing thresholds, system specs) must survive compression
- **Speaker attribution**: every key point must be traceable to a specific speaker
- **Actionable items**: if the meeting has implications for the user's work (thesis, hospital job, research), extract them as checkboxes

## Pitfalls

- **Don't merge speakers**: even if two speakers cover similar topics, keep them separate — different speakers may have different data or perspectives
- **元宝's commentary is unreliable**: it often misinterprets or over-interprets. Trust the speaker's words, not the AI's analysis of those words
- **Policy documents cited in meetings**: extract the exact document number (e.g., "国务院办公厅9号文") — these are useful references for the user's work
- **Drug pricing thresholds**: preserve exact multipliers (1.8倍, 3倍) — these are regulatory facts, not opinions
- **File naming**: use the official meeting name, not a casual description. Check the raw file's title or first few lines for the official name
