# Apple Silicon Model Recommendations for Hermes Agent

Last updated: 2026-05-03. Tested on MacBook Air M5 24GB.

## Sizing Rule of Thumb

GGUF Q4_K_M quantization: **~0.6 GB per 1B parameters**

| Model size | Memory (Q4_K_M) | Fits 24GB? | Speed (M5) |
|-----------|-----------------|------------|------------|
| 3B | ~2 GB | ✓✓✓ | 80+ tok/s |
| 7-8B | ~5 GB | ✓✓✓ | 60+ tok/s |
| 12-14B | ~8-9 GB | ✓✓ | 30-40 tok/s |
| 27B | ~17 GB | ✓ (tight) | 15-20 tok/s |
| 32B | ~19 GB | ✓ (limit) | 12-15 tok/s |
| 70B | ~40 GB | ✗ | — |

Leave 4 GB for macOS + Hermes + other apps.

## Recommended Models for Agent Tasks

### qwen3:14b  ← Best all-around for Chinese/English agent work

- Memory: ~9 GB (Q4_K_M)
- Context: 128K
- Tool calling: Excellent. Qwen3 family has strong function-calling fine-tuning.
- Coding: Top-tier for 14B class.
- Chinese: Native-level.
- Non-thinking: no wasted reasoning tokens.
- `ollama pull qwen3:14b`

### llama4:8b  ← Best for English-centric agent work

- Memory: ~5 GB
- Context: 128K+
- Tool calling: Architecture-level support (not bolted on via fine-tune).
- Coding: Strong.
- Chinese: Functional but not great.
- Very fast on M5 (60+ tok/s).
- `ollama pull llama4:8b`

### phi4:14b  ← Small model, big brain

- Memory: ~9 GB
- Context: 128K
- Tool calling: Surprising strong for size. Microsoft's post-training is exceptional.
- Coding + reasoning: Punches at 30B level.
- English-first, Chinese okay.
- `ollama pull phi4:14b`

### deepseek-r1:14b  ← Reasoning specialist (thinking model)

- Memory: ~9 GB
- Context: 128K
- Use when: complex logic, math, multi-step planning.
- Thinking model — will reason before answering. Use `/reasoning show` to see it.
- NOT for fast agent turns. NOT for simple commands.
- `ollama pull deepseek-r1:14b`

### gemma3:12b  ← Multilingual generalist

- Memory: ~7-8 GB
- Context: 128K
- 35+ languages, Chinese strong.
- Tool calling: mid-tier, adequate for most tasks.
- Google safety: rarely goes off-rails.
- `ollama pull gemma3:12b`

### qwq:32b  ← Hard-reasoning specialist (limit case)

- Memory: ~19 GB — pushes 24GB to the absolute limit
- Use only when nothing else can solve the problem.
- Close other apps before loading.
- `ollama pull qwq:32b`

## Dual-Model Strategy

Two models can coexist in 24GB:

```
qwen3:14b (9 GB) + deepseek-r1:14b (9 GB) = 18 GB
→ System has ~6 GB breathing room
→ Switch with /model <name> in Hermes, then /reset
```

## Models to AVOID for Agent Work on 24GB

- **qwen3.6:27b** — Thinking variant, wastes 200-300+ tokens reasoning even for trivial prompts. Content field stays empty during thinking → Hermes appears frozen. Use `qwen3:27b` (non-thinking) if you really want 27B, or drop to `qwen3:14b`.
- **Any 70B model** — Won't fit.
- **deepseek-r1:32b** — Might fit (19 GB) but extremely tight; system will swap.
