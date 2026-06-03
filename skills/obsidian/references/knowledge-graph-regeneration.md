# Knowledge Graph Regeneration

## Overview
The knowledge graph (`wiki/knowledge-graph.html`) displays relationships between wiki pages based on `[[wikilinks]]`. The graph data is static and needs manual regeneration when content changes.

## Regeneration Command
```bash
bash ~/.hermes/skills/llm-wiki/scripts/build-graph-data.sh ~/Documents/Obsidian/wbaoc-wiki
```

## Output
The script generates `wiki/graph-data.json` with:
- **Nodes**: All wiki pages (entities, topics, sources, etc.)
- **Edges**: Wikilink connections between pages
- **Meta**: Build date, node count, edge count

## When to Regenerate
- After adding multiple new wiki pages
- After significant content updates with new wikilinks
- When the graph looks outdated (check `meta.build_date` in graph-data.json)

## Pitfalls
- **Graph shows old data**: The HTML file reads from `graph-data.json` - if JSON is outdated, graph won't update automatically
- **Script location**: The build script is in the llm-wiki skill directory, not in the vault
- **Node count discrepancy**: If you added many pages but node count didn't increase much, check that pages have proper YAML frontmatter and are in the correct subdirectories (entities/, topics/, sources/, etc.)

## Verification
After regeneration, check:
```bash
# View graph metadata
cat ~/Documents/Obsidian/wbaoc-wiki/wiki/graph-data.json | jq '.meta'

# Should show:
# - build_date: recent timestamp
# - total_nodes: expected count
# - total_edges: expected connections
```

## Related
- Graph HTML: `wiki/knowledge-graph.html`
- Graph data: `wiki/graph-data.json`
- Build script: `~/.hermes/skills/llm-wiki/scripts/build-graph-data.sh`
- Analysis helper: `~/.hermes/skills/llm-wiki/scripts/graph-analysis.js`