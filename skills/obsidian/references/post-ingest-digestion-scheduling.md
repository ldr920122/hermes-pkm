# Post-Ingest Digestion Scheduling

Pattern: user bulk-ingests content (articles, blog posts, PDFs) into `raw/clippings/` or `wiki/`, then realizes they haven't actually read it, and asks "when should I start digesting these?"

This is normal. Ingest is cheap, digestion is expensive.

## Two tiers of digestion

### ① Light digestion (recommended first pass)
- Read 1 article/day in碎片时间 (commute/lunch)
- 10-15 min per article, no output required
- Mental model: browse with intent, mark anything striking
- Total time: N days for N articles

### ② Deep digestion
- Read + write a wiki page per article
- 30-45 min per article
- Only worth it for truly high-signal content (architecture decisions, novel patterns)
- Schedule during周末半天 or defer until current crunch period ends

## Scheduling rules

1. **Map current time-slot occupancy** — what's already in the user's slots?
2. **Find the slot that matches** — digesting text =碎片时间 (commute, lunch, bedtime)
3. **Sequence after current occupant finishes** — if碎片时间 has a course ending on 5/25, start digestion 5/26
4. **Present the concrete calendar range** — "5/26 to 6/18, 1 article/day"
5. **Update BuJo** — add to月度计划 (monthly action plan) and today's diary

## Signal detection

User phrases that trigger this:
- "这些我还没消化" / "我只是放进去了"
- "帮我定一下计划什么时候开始看"
- "先存着，之后再说" followed later by "现在有空了"
- Bulk ingest of 10+ articles without immediate discussion

## Default recommendation

Light digestion first. If an article is truly high-signal, the user will say "这篇写个笔记" and you can do a quick wiki entry on the spot. Don't pre-commit to deep digestion — it creates backlog guilt for no benefit.
