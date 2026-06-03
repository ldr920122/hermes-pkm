---
name: hermes-agent
description: "Configure, extend, or contribute to Hermes Agent."
version: 2.0.0
author: Hermes Agent + Teknium
license: MIT
metadata:
  hermes:
    tags: [hermes, setup, configuration, multi-agent, spawning, cli, gateway, development]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [claude-code, codex, opencode]
---

# Hermes Agent

Hermes Agent is an open-source AI agent framework by Nous Research that runs in your terminal, messaging platforms, and IDEs. It belongs to the same category as Claude Code (Anthropic), Codex (OpenAI), and OpenClaw — autonomous coding and task-execution agents that use tool calling to interact with your system. Hermes works with any LLM provider (OpenRouter, Anthropic, OpenAI, DeepSeek, local models, and 15+ others) and runs on Linux, macOS, and WSL.

What makes Hermes different:

- **Self-improving through skills** — Hermes learns from experience by saving reusable procedures as skills. When it solves a complex problem, discovers a workflow, or gets corrected, it can persist that knowledge as a skill document that loads into future sessions. Skills accumulate over time, making the agent better at your specific tasks and environment.
- **Persistent memory across sessions** — remembers who you are, your preferences, environment details, and lessons learned. Pluggable memory backends (built-in, Honcho, Mem0, and more) let you choose how memory works.
- **Multi-platform gateway** — the same agent runs on Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, and 10+ other platforms with full tool access, not just chat.
- **Provider-agnostic** — swap models and providers mid-workflow without changing anything else. Credential pools rotate across multiple API keys automatically.
- **Profiles** — run multiple independent Hermes instances with isolated configs, sessions, skills, and memory.
- **Extensible** — plugins, MCP servers, custom tools, webhook triggers, cron scheduling, and the full Python ecosystem.

People use Hermes for software development, research, system administration, data analysis, content creation, home automation, and anything else that benefits from an AI agent with persistent context and full system access.

**This skill helps you work with Hermes Agent effectively** — setting it up, configuring features, spawning additional agent instances, troubleshooting issues, finding the right commands and settings, and understanding how the system works when you need to extend or contribute to it.

**Docs:** https://hermes-agent.nousresearch.com/docs/

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Interactive chat (default)
hermes

# Single query
hermes chat -q "What is the capital of France?"

# Setup wizard
hermes setup

# Change model/provider
hermes model

# Check health
hermes doctor
```

---

## CLI Reference

### Global Flags

```
hermes [flags] [command]

  --version, -V             Show version
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --pass-session-id         Include session ID in system prompt
```

No subcommand defaults to `chat`.

### Chat

```
hermes chat [flags]
  -q, --query TEXT          Single query, non-interactive
  -m, --model MODEL         Model (e.g. anthropic/claude-sonnet-4)
  -t, --toolsets LIST       Comma-separated toolsets
  --provider PROVIDER       Force provider (openrouter, anthropic, nous, etc.)
  -v, --verbose             Verbose output
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --source TAG              Session source tag (default: cli)
```

### Configuration

```
hermes setup [section]      Interactive wizard (model|terminal|gateway|tools|agent)
hermes model                Interactive model/provider picker
hermes config               View current config
hermes config edit          Open config.yaml in $EDITOR
hermes config set KEY VAL   Set a config value
hermes config path          Print config.yaml path
hermes config env-path      Print .env path
hermes config check         Check for missing/outdated config
hermes config migrate       Update config with new options
hermes login [--provider P] OAuth login (nous, openai-codex)
hermes logout               Clear stored auth
hermes doctor [--fix]       Check dependencies and config
hermes status [--all]       Show component status
```

### Tools & Skills

```
hermes tools                Interactive tool enable/disable (curses UI)
hermes tools list           Show all tools and status
hermes tools enable NAME    Enable a toolset
hermes tools disable NAME   Disable a toolset

hermes skills list          List installed skills
hermes skills search QUERY  Search the skills hub
hermes skills install ID    Install a skill (ID can be a hub identifier OR a direct https://…/SKILL.md URL; pass --name to override when frontmatter has no name)
hermes skills inspect ID    Preview without installing
hermes skills config        Enable/disable skills per platform
hermes skills check         Check for updates
hermes skills update        Update outdated skills
hermes skills uninstall N   Remove a hub skill
hermes skills publish PATH  Publish to registry
hermes skills browse        Browse all available skills
hermes skills tap add REPO  Add a GitHub repo as skill source
```

### MCP Servers

```
hermes mcp serve            Run Hermes as an MCP server
hermes mcp add NAME         Add an MCP server (--url or --command)
hermes mcp remove NAME      Remove an MCP server
hermes mcp list             List configured servers
hermes mcp test NAME        Test connection
hermes mcp configure NAME   Toggle tool selection
```

### Gateway (Messaging Platforms)

```bash
hermes gateway run          Start gateway foreground
hermes gateway install      Install as background service
hermes gateway start/stop   Control the service
hermes gateway restart      Restart the service
hermes gateway status       Check status
hermes gateway setup        Configure platforms
```

Supported platforms: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Home Assistant, DingTalk, Feishu, WeCom, BlueBubbles (iMessage), Weixin (WeChat), API Server, Webhooks. Open WebUI connects via the API Server adapter.

Platform docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

**Platform comparison quick ref:** `references/platform-comparison.md` — feature matrix (Telegram/微信/飞书/QQ/Discord), per-platform strengths/weaknesses, recommended use cases, and talking points for presentations.

A config template with common platform blocks (WeChat, Telegram, Feishu, Discord, Slack, Email) is at `templates/gateway-platforms.yaml` in the skill directory — copy the relevant block rather than guessing field names.

### Platform Config in config.yaml

Platform credentials live under the **top-level** `platforms:` key in `config.yaml` — NOT under `gateway:` or any other section. Each platform gets a nested dict:

```yaml
platforms:
  telegram:
    enabled: true
    token: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
  weixin:
    enabled: true
    token: e81004a40e7e@im.bot:06000085c34f20ad9c8deb0dd2ca04bfc32837
    extra:
      account_id: e81004a40e7e@im.bot
      base_url: https://ilinkai.weixin.qq.com
```

Key fields:
- `enabled` (bool) — whether to connect this platform on gateway startup
- `token` (str) — platform-specific auth token (bot token for Telegram, iLink token for WeChat)
- `extra` (dict) — adapter-specific config keys (account_id, base_url, dm_policy, etc.)

The gateway reads `platforms:` from config.yaml at line 696 of `gateway/config.py`. Env vars (`WEIXIN_TOKEN`, `TELEGRAM_TOKEN`, etc.) can also supply token values when the config key is absent. See `references/gateway-troubleshooting.md` for per-platform field tables and diagnostic patterns.

After changing `platforms:` in config.yaml, restart the gateway:
```bash
hermes gateway restart
```

### Sessions

```
hermes sessions list        List recent sessions
hermes sessions browse      Interactive picker
hermes sessions export OUT  Export to JSONL
hermes sessions rename ID T Rename a session
hermes sessions delete ID   Delete a session
hermes sessions prune       Clean up old sessions (--older-than N days)
hermes sessions stats       Session store statistics
```

### Cron Jobs

```
hermes cron list            List jobs (--all for disabled)
hermes cron create SCHED    Create: '30m', 'every 2h', '0 9 * * *'
hermes cron edit ID         Edit schedule, prompt, delivery
hermes cron pause/resume ID Control job state
hermes cron run ID          Trigger on next tick
hermes cron remove ID       Delete a job
hermes cron status          Scheduler status
```

**Pitfalls:**

- **`deliver` is single-target.** A cron job can only deliver to ONE platform/chat at a time. To send the same scheduled message to multiple platforms (e.g. both Telegram and WeChat), you must create **separate cron jobs** with the same prompt but different `deliver` targets. There is no multi-target syntax.
- **`prompt_preview` is truncated.** The `cronjob` tool's `list` action returns only a truncated `prompt_preview`. To get the **full prompt** of an existing job (e.g. when cloning it for another platform), read the raw jobs file directly:
  ```bash
  cat ~/.hermes/cron/jobs.json
  ```
  The `prompt` field contains the complete, untruncated text.
- **Deliver target formats:** `telegram:USERNAME (dm)`, `weixin:<chat_id>@im.wechat`, `discord:<channel_id>`, `slack:<channel>`. WeChat chat IDs use the format `o9cq...@im.wechat` (from `weixin` platform adapter).

### Webhooks

```
hermes webhook subscribe N  Create route at /webhooks/<name>
hermes webhook list         List subscriptions
hermes webhook remove NAME  Remove a subscription
hermes webhook test NAME    Send a test POST
```

### Profiles

```
hermes profile list         List all profiles
hermes profile create NAME  Create (--clone, --clone-all, --clone-from)
hermes profile use NAME     Set sticky default
hermes profile delete NAME  Delete a profile
hermes profile show NAME    Show details
hermes profile alias NAME   Manage wrapper scripts
hermes profile rename A B   Rename a profile
hermes profile export NAME  Export to tar.gz
hermes profile import FILE  Import from archive
```

### Credential Pools

```
hermes auth add             Interactive credential wizard
hermes auth list [PROVIDER] List pooled credentials
hermes auth remove P INDEX  Remove by provider + index
hermes auth reset PROVIDER  Clear exhaustion status
```

### Other

```
hermes insights [--days N]  Usage analytics
hermes update               Update to latest version
hermes pairing list/approve/revoke  DM authorization
hermes plugins list/install/remove  Plugin management
hermes honcho setup/status  Honcho memory integration (requires honcho plugin)
hermes memory setup/status/off  Memory provider config
hermes completion bash|zsh  Shell completions
hermes acp                  ACP server (IDE integration)
hermes claw migrate         Migrate from OpenClaw
hermes uninstall            Uninstall Hermes
```

---

## Slash Commands (In-Session)

Type these during an interactive chat session.

### Session Control
```
/new (/reset)        Fresh session
/clear               Clear screen + new session (CLI)
/retry               Resend last message
/undo                Remove last exchange
/title [name]        Name the session
/compress            Manually compress context
/stop                Kill background processes
/rollback [N]        Restore filesystem checkpoint
/background <prompt> Run prompt in background
/queue <prompt>      Queue for next turn
/resume [name]       Resume a named session
```

### Configuration
```
/config              Show config (CLI)
/model [name]        Show or change model
/personality [name]  Set personality
/reasoning [level]   Set reasoning (none|minimal|low|medium|high|xhigh|show|hide)
/verbose             Cycle: off → new → all → verbose
/voice [on|off|tts]  Voice mode
/yolo                Toggle approval bypass
/skin [name]         Change theme (CLI)
/statusbar           Toggle status bar (CLI)
```

### Tools & Skills
```
/tools               Manage tools (CLI)
/toolsets            List toolsets (CLI)
/skills              Search/install skills (CLI)
/skill <name>        Load a skill into session
/cron                Manage cron jobs (CLI)
/reload-mcp          Reload MCP servers
/plugins             List plugins (CLI)
```

### Gateway
```
/approve             Approve a pending command (gateway)
/deny                Deny a pending command (gateway)
/restart             Restart gateway (gateway)
/sethome             Set current chat as home channel (gateway)
/update              Update Hermes to latest (gateway)
/platforms (/gateway) Show platform connection status (gateway)
```

### Utility
```
/branch (/fork)      Branch the current session
/fast                Toggle priority/fast processing
/browser             Open CDP browser connection
/history             Show conversation history (CLI)
/save                Save conversation to file (CLI)
/paste               Attach clipboard image (CLI)
/image               Attach local image file (CLI)
```

### Info
```
/help                Show commands
/commands [page]     Browse all commands (gateway)
/usage               Token usage
/insights [days]     Usage analytics
/status              Session info (gateway)
/profile             Active profile info
```

### Exit
```
/quit (/exit, /q)    Exit CLI
```

---

## Key Paths & Config

```
~/.hermes/config.yaml       Main configuration
~/.hermes/.env              API keys and secrets
$HERMES_HOME/skills/        Installed skills
~/.hermes/sessions/         Session transcripts
~/.hermes/logs/             Gateway and error logs
~/.hermes/auth.json         OAuth tokens and credential pools
~/.hermes/hermes-agent/     Source code (if git-installed)
```

Profiles use `~/.hermes/profiles/<name>/` with the same layout.

### Config Sections

Edit with `hermes config edit` or `hermes config set section.key value`.

| Section | Key options |
|---------|-------------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement` |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral) |
| `tts` | `provider` (edge/elevenlabs/openai/minimax/mistral/neutts) |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` |
| `security` | `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort` |
| `checkpoints` | `enabled`, `max_snapshots` (50) |

Full config reference: https://hermes-agent.nousresearch.com/docs/user-guide/configuration

### Providers

20+ providers supported. Set via `hermes model` or `hermes setup`.

| Provider | Auth | Key env var |
|----------|------|-------------|
| OpenRouter | API key | `OPENROUTER_API_KEY` |
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes auth` |
| OpenAI Codex | OAuth | `hermes auth` |
| GitHub Copilot | Token | `COPILOT_GITHUB_TOKEN` |
| Google Gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| xAI / Grok | API key | `XAI_API_KEY` |
| Hugging Face | Token | `HF_TOKEN` |
| Z.AI / GLM | API key | `GLM_API_KEY` |
| MiniMax | API key | `MINIMAX_API_KEY` |
| MiniMax CN | API key | `MINIMAX_CN_API_KEY` |
| Kimi / Moonshot | API key | `KIMI_API_KEY` |
| Alibaba / DashScope | API key | `DASHSCOPE_API_KEY` |
| Xiaomi MiMo | API key | `XIAOMI_API_KEY` |
| Kilo Code | API key | `KILOCODE_API_KEY` |
| AI Gateway (Vercel) | API key | `AI_GATEWAY_API_KEY` |
| OpenCode Zen | API key | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | API key | `OPENCODE_GO_API_KEY` |
| Qwen OAuth | OAuth | `hermes login --provider qwen-oauth` |
| Custom endpoint | Config | `model.base_url` + `model.api_key` in config.yaml |
| Ollama (local) | None | Runs on `http://localhost:11434/v1` by default |

Full provider docs: https://hermes-agent.nousresearch.com/docs/integrations/providers

### Xiaomi MiMo: Token Plan vs Standard API

Xiaomi MiMo has **two API endpoint types** and the correct one depends on your key prefix:

| Key prefix | Endpoint type | Base URL |
|------------|--------------|----------|
| `tp-` (Token Plan) | Regional Token Plan | `https://token-plan-{region}.xiaomimimo.com/v1` |
| Other | Standard API | `https://api.xiaomimimo.com/v1` |

Token Plan regions: `cn` (China), `sgp` (Singapore), `ams` (Amsterdam). The key prefix itself encodes the region — `tp-ck` → China, `tp-sk` → Singapore, `tp-ak` → Amsterdam.

**Pitfall:** Using a Token Plan key (`tp-*`) with the standard `api.xiaomimimo.com` endpoint returns `HTTP 401 Invalid API Key` despite the key being valid. The error is misleading — the key is correct, the endpoint is wrong. Also: after changing `model.base_url`, Hermes still uses the `.env` value for the key — if both are stale, the error persists even after a URL fix.

**Diagnostic flow (isolate key vs endpoint issues):**

```bash
# Step 1: Test with curl to rule out Hermes config issues
KEY=$(grep XIAOMI_API_KEY ~/.hermes/.env | cut -d= -f2)

# Test standard endpoint
curl -s -o /dev/null -w "std: %{http_code}\n" \
  -H "Authorization: Bearer $KEY" \
  "https://api.xiaomimimo.com/v1/models"

# Test Token Plan CN endpoint
curl -s -o /dev/null -w "tp-cn: %{http_code}\n" \
  -H "Authorization: Bearer $KEY" \
  "https://token-plan-cn.xiaomimimo.com/v1/models"

# Step 2: If tp-cn returns 200, fix the base_url
hermes config set model.base_url "https://token-plan-cn.xiaomimimo.com/v1"

# Step 3: If both return 401, the key itself is expired — get a new one
# from Xiaomi console and update ~/.hermes/.env (NOT via config set!)
```

**mimo-v2-pro reasoning caveat:** Like Qwen thinking models, `mimo-v2-pro` can spend nearly all output tokens on internal reasoning — tests show 49/50 tokens consumed by reasoning on a trivial 你好 prompt, leaving `content: ""`. Mitigations: (a) use `/reasoning show` to see the thinking output; (b) increase `max_tokens` significantly (≥500 for tool-calling workloads); (c) switch to `mimo-v2-flash` or `mimo-v2.5` for faster turnarounds when deep reasoning isn't needed.

Hermes source confirmation: `tests/hermes_cli/test_xiaomi_provider.py` line 287-291 documents the three Token Plan regional endpoints.

### Xiaomi MiMo Model Switching

When switching between Xiaomi MiMo models (e.g., from `mimo-v2-pro` to `mimo-v2.5-pro`), three locations in `config.yaml` must be updated:

1. **Default model**: `model.default`
2. **Provider model list**: `custom_providers[].models` (add new model if not present)
3. **Provider default model**: `custom_providers[].model`

**Step-by-step switching process:**

```bash
# 1. Query available models from API
curl -s https://token-plan-cn.xiaomimimo.com/v1/models \
  -H "Authorization: Bearer $(grep XIAOMI_API_KEY ~/.hermes/.env | cut -d= -f2)"

# 2. Update config.yaml (three changes)
hermes config set model.default mimo-v2.5-pro

# 3. Edit config.yaml manually to add model to provider list
# Under custom_providers → xiaomi → models, add:
#   mimo-v2.5-pro:
#     name: MiMo v2.5 Pro
# And update the provider's model field to: mimo-v2.5-pro

# 4. Restart gateway
hermes gateway restart

# 5. Verify
hermes status | grep "Model:"
```

**Pitfalls:**
- **Missing model in provider list**: If `mimo-v2.5-pro` is not in `custom_providers[].models`, Hermes may fall back to default or error
- **Gateway vs CLI independence**: Changing `model.default` affects the gateway only after restart. CLI sessions use their own model selection
- **Image recognition**: `mimo-v2.5` works as a vision model when configured as `auxiliary.vision.provider: xiaomi` with model `mimo-v2.5` in config.yaml. The default `vision.provider: auto` may fail if no other vision-capable provider is configured. Fix:

```bash
hermes config set auxiliary.vision.provider xiaomi
hermes config set auxiliary.vision.model mimo-v2.5
hermes gateway restart
```

Pitfall: earlier testing used the main model endpoint directly (model_messages API), which returned URL download errors. The `auxiliary.vision` tool uses a different code path that works correctly with `mimo-v2.5`.

See `references/xiaomi-mimo-model-switching.md` for step-by-step switching guide and full model list.

See `references/xiaomi-mimo-provider.md` for full model list and detailed testing results.

### Local Model Setup (Ollama)

Run models locally via [Ollama](https://ollama.com). No API key needed — Hermes auto-fills `no-key-required` for local endpoints that lack credentials.

```bash
# 1. Pull a model
ollama pull qwen3:27b

# 2. Configure Hermes (three keys)
hermes config set model.provider ollama
hermes config set model.default qwen3.6:27b
hermes config set model.base_url http://localhost:11434/v1

# 3. New session — /reset in chat or restart hermes
```

Pitfalls:

- **`/v1` suffix is mandatory.** Omitting it from `base_url` produces 404 / connection errors because Ollama's OpenAI-compatible endpoint lives at `/v1`, not the root.
- **Provider is `ollama`, not `custom` or `openai`.** The `ollama` provider string triggers Ollama-specific logic: automatic `num_ctx` detection from GGUF metadata, `/api/show` probing for context length, and model-name resolution that preserves `:tag` syntax. `custom` works superficially but misses these paths.
- **Model name must match `ollama list` exactly**, including the colon tag — e.g. `qwen3.6:27b`, not `qwen3.6-27b` or `qwen3.6`.
- **No API key required.** For local custom providers, Hermes sets `api_key = "no-key-required"` automatically. Setting one explicitly is harmless but unnecessary.
- **Qwen thinking models (qwen3.6, qwq, qwen3.6:27b, etc.) produce extensive reasoning tokens before any visible content.** The `content` field in the API response stays empty while the model thinks — for trivial prompts this can be 200-300+ tokens of reasoning before a two-word answer. Hermes may appear stuck, unresponsive, or "not running." The model IS loaded and working; it's just thinking out loud invisibly. Symptoms: memory doesn't appear to grow (Ollama loads on-demand and unloads after idle timeout), requests seem to hang, response appears blank. Fixes: (a) use the non-thinking variant — `qwen3:27b` instead of `qwen3.6:27b`; (b) enable `/reasoning show` in Hermes to see thinking output rather than a blank screen; (c) ensure `max_tokens` is high enough for the thinking phase to complete (300+ for simple queries, much more for tool-calling). Ollama's `enable_thinking: false` param is ignored by these models — they think regardless.

Same pattern works for LM Studio (`http://localhost:1234/v1`), llama.cpp server, and vLLM — change `base_url` and use provider `custom` for those.

See `references/apple-silicon-models.md` for tested model recommendations on Apple Silicon Macs with memory sizing and dual-model strategies.

### Toolsets

Enable/disable via `hermes tools` (interactive) or `hermes tools enable/disable NAME`.

| Toolset | What it provides |
|---------|-----------------|
| `web` | Web search and content extraction |
| `browser` | Browser automation — see `references/browser-automation-landscape.md` for architecture details and comparison with Browser Harness / playwright-cli |
| `terminal` | Shell commands and process management |
| `file` | File read/write/search/patch |
| `code_execution` | Sandboxed Python execution |
| `vision` | Image analysis |
| `image_gen` | AI image generation |
| `tts` | Text-to-speech |
| `skills` | Skill browsing and management |
| `memory` | Persistent cross-session memory |
| `session_search` | Search past conversations |
| `delegation` | Subagent task delegation |
| `cronjob` | Scheduled task management |
| `clarify` | Ask user clarifying questions |
| `messaging` | Cross-platform message sending |
| `search` | Web search only (subset of `web`) |
| `todo` | In-session task planning and tracking |
| `rl` | Reinforcement learning tools (off by default) |
| `moa` | Mixture of Agents (off by default) |
| `homeassistant` | Smart home control (off by default) |

Tool changes take effect on `/reset` (new session). They do NOT apply mid-conversation to preserve prompt caching.

---

## Security & Privacy Toggles

Common "why is Hermes doing X to my output / tool calls / commands?" toggles — and the exact commands to change them. Most of these need a fresh session (`/reset` in chat, or start a new `hermes` invocation) because they're read once at startup.

### Secret redaction in tool output

Secret redaction is **off by default** — tool output (terminal stdout, `read_file`, web content, subagent summaries, etc.) passes through unmodified. If the user wants Hermes to auto-mask strings that look like API keys, tokens, and secrets before they enter the conversation context and logs:

```bash
hermes config set security.redact_secrets true       # enable globally
```

**Restart required.** `security.redact_secrets` is snapshotted at import time — toggling it mid-session (e.g. via `export HERMES_REDACT_SECRETS=true` from a tool call) will NOT take effect for the running process. Tell the user to run `hermes config set security.redact_secrets true` in a terminal, then start a new session. This is deliberate — it prevents an LLM from flipping the toggle on itself mid-task.

Disable again with:
```bash
hermes config set security.redact_secrets false
```

### PII redaction in gateway messages

Separate from secret redaction. When enabled, the gateway hashes user IDs and strips phone numbers from the session context before it reaches the model:

```bash
hermes config set privacy.redact_pii true    # enable
hermes config set privacy.redact_pii false   # disable (default)
```

### Command approval prompts

By default (`approvals.mode: manual`), Hermes prompts the user before running shell commands flagged as destructive (`rm -rf`, `git reset --hard`, etc.). The modes are:

- `manual` — always prompt (default)
- `smart` — use an auxiliary LLM to auto-approve low-risk commands, prompt on high-risk
- `off` — skip all approval prompts (equivalent to `--yolo`)

```bash
hermes config set approvals.mode smart       # recommended middle ground
hermes config set approvals.mode off         # bypass everything (not recommended)
```

Per-invocation bypass without changing config:
- `hermes --yolo …`
- `export HERMES_YOLO_MODE=1`

Note: YOLO / `approvals.mode: off` does NOT turn off secret redaction. They are independent.

### Shell hooks allowlist

Some shell-hook integrations require explicit allowlisting before they fire. Managed via `~/.hermes/shell-hooks-allowlist.json` — prompted interactively the first time a hook wants to run.

### Disabling the web/browser/image-gen tools

To keep the model away from network or media tools entirely, open `hermes tools` and toggle per-platform. Takes effect on next session (`/reset`). See the Tools & Skills section above.

---

## Reasoning Configuration

Hermes separates reasoning into **two independent dimensions** that control different things:

### Reasoning Effort (`agent.reasoning_effort`)

Controls how deeply the model *thinks* before responding. Only works with providers/models that support reasoning (OpenRouter thinking models, OpenAI o-series, Anthropic extended thinking, Codex). **Local Ollama models ignore this — they either think or they don't, based on the GGUF variant.**

| Level | Meaning | Token cost | Use case |
|-------|---------|------------|----------|
| `none` | Disable thinking entirely | Lowest | Simple Q&A, fast agent turns |
| `minimal` | Bare minimum reasoning | Low | Routine tasks |
| `low` | Light reasoning | Low-med | Standard agent work |
| `medium` | Balanced (OpenRouter default) | Medium | Everyday coding, debugging |
| `high` | Deep reasoning | High | Complex architecture, math |
| `xhigh` | Maximum reasoning | Highest | Multi-step analysis, research |

```bash
# Set globally
hermes config set agent.reasoning_effort high
hermes config set agent.reasoning_effort none

# Query current
hermes config | grep -i reason
# Or in-session:
/reasoning
```

Default: `""` (empty) = inherit provider default. OpenRouter defaults to `medium`.

### Reasoning Display (`display.show_reasoning`)

Controls whether the model's thinking process is *shown to you* in the output. Does NOT affect whether the model thinks — that's `reasoning_effort`'s job. Does NOT affect token cost.

| Value | Default | Effect |
|-------|---------|--------|
| `false` | ✓ | Thinking filtered out; only final response shown |
| `true` | | Thinking shown in `<think>…</think>` blocks |

```bash
hermes config set display.show_reasoning false   # default
hermes config set display.show_reasoning true
```

### How They Interact

```
reasoning_effort=none  →  model doesn't think, show_reasoning has nothing to show
reasoning_effort=high  +  show_reasoning=false →  model thinks, you don't see it (cost still applies)
reasoning_effort=high  +  show_reasoning=true  →  model thinks, you see the thinking
```

### In-Session: `/reasoning` Command

```
/reasoning              →  Show current effort + display state
/reasoning medium       →  Set effort level (saved to config)
/reasoning none         →  Disable thinking (saved to config)
/reasoning show         →  Show thinking in output (saves display.show_reasoning=true)
/reasoning hide         →  Hide thinking from output (saves display.show_reasoning=false)
```

Local model caveat: Ollama models like `qwen3.6:27b` always think regardless of `reasoning_effort` — they embed thinking behavior in the GGUF file itself. Use `/reasoning show` to at least see what they're doing, or switch to the non-thinking variant (e.g. `qwen3:27b` instead of `qwen3.6:27b`). See "Local Model Setup (Ollama) → Pitfalls" above for Qwen thinking-model specifics.

---

## Context Compression

Hermes automatically compresses conversation history when it approaches the model's context window limit. This is transparent — the conversation continues without interruption.

### How Automatic Compression Works

1. **Trigger check**: After each API call, Hermes compares `prompt_tokens` against `threshold_tokens` (= `context_length × compression.threshold`, default 50%)
2. **Tool output pruning** (cheap pre-pass, no LLM call): Old tool results (file reads, terminal output, web content) are replaced with `[Old tool output cleared to save context space]`
3. **LLM summarization**: The middle portion of the conversation is summarized by an auxiliary model (cheap/fast, auto-detected from available providers). The summary includes: Resolved questions, Pending questions, Active Task, Remaining Work.
4. **Message protection**: First 3 messages and last 20 messages (`protect_last_n`) are never compressed. The compressed region is everything between them.
5. **Result**: Shorter message list with a `[CONTEXT COMPACTION — REFERENCE ONLY]` summary at the top + recent messages preserved verbatim.

### Config

```yaml
compression:
  enabled: true              # master switch
  threshold: 0.50            # compress when context usage exceeds 50%
  target_ratio: 0.20         # fraction of threshold to preserve as recent tail
  protect_last_n: 20         # minimum recent messages kept uncompressed
  hygiene_hard_message_limit: 400  # gateway: force-compress at message count
```

Adjust for small-context models:
```bash
hermes config set compression.threshold 0.40   # compress earlier
hermes config set compression.enabled false     # disable (not recommended)
```

The auxiliary model used for summarization is configured separately:
```yaml
auxiliary:
  compression:
    provider: auto   # auto-detects from available API keys
    model: ""        # empty = provider's default
    timeout: 120
```

### Manual Compression

`/compress` — compress on demand, useful at logical breakpoints between task phases.

`/compress <topic>` — guided compression: the summarizer prioritizes preserving information about the specified topic.

### Anti-Thrashing

If the last 2 compressions each saved less than 10% of context, auto-compression is skipped to avoid infinite loops where each pass removes only 1-2 messages. The agent logs a warning suggesting `/new` or `/compress <topic>`.

### Long Tasks / Cron Jobs / Subagents

**No special configuration needed.** Each conversation (interactive session, cron job, delegate_task subagent) has its own context window with independent compression. The agent loop checks `should_compress()` after every turn — no instructions in the task prompt are required. Cron jobs and subagents auto-compress just like interactive sessions.

---

## Voice & Transcription

### STT (Voice → Text)

Voice messages from messaging platforms are auto-transcribed.

Provider priority (auto-detected):
1. **Local faster-whisper** — free, no API key: `pip install faster-whisper`
2. **Groq Whisper** — free tier: set `GROQ_API_KEY`
3. **OpenAI Whisper** — paid: set `VOICE_TOOLS_OPENAI_KEY`
4. **Mistral Voxtral** — set `MISTRAL_API_KEY`

Config:
```yaml
stt:
  enabled: true
  provider: local        # local, groq, openai, mistral
  local:
    model: base          # tiny, base, small, medium, large-v3
```

### TTS (Text → Voice)

| Provider | Env var | Free? |
|----------|---------|-------|
| Edge TTS | None | Yes (default) |
| ElevenLabs | `ELEVENLABS_API_KEY` | Free tier |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | Paid |
| MiniMax | `MINIMAX_API_KEY` | Paid |
| Mistral (Voxtral) | `MISTRAL_API_KEY` | Paid |
| NeuTTS (local) | None (`pip install neutts[all]` + `espeak-ng`) | Free |

Voice commands: `/voice on` (voice-to-voice), `/voice tts` (always voice), `/voice off`.

---

## Spawning Additional Hermes Instances

Run additional Hermes processes as fully independent subprocesses — separate sessions, tools, and environments.

### When to Use This vs delegate_task

| | `delegate_task` | Spawning `hermes` process |
|-|-----------------|--------------------------|
| Isolation | Separate conversation, shared process | Fully independent process |
| Duration | Minutes (bounded by parent loop) | Hours/days |
| Tool access | Subset of parent's tools | Full tool access |
| Interactive | No | Yes (PTY mode) |
| Use case | Quick parallel subtasks | Long autonomous missions |

### One-Shot Mode

```
terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)

# Background for long tasks:
terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)
```

### Interactive PTY Mode (via tmux)

Hermes uses prompt_toolkit, which requires a real terminal. Use tmux for interactive spawning:

```
# Start
terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)

# Wait for startup, then send a message
terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)

# Read output
terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)

# Send follow-up
terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)

# Exit
terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)
```

### Multi-Agent Coordination

```
# Agent A: backend
terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)

# Agent B: frontend
terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)

# Check progress, relay context between them
terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)
terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)
```

### Session Resume

```
# Resume most recent session
terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)

# Resume specific session
terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)
```

### Tips

- **Prefer `delegate_task` for quick subtasks** — less overhead than spawning a full process
- **delegate_task API key pitfall**: Subagents use `delegation.model` and `delegation.provider` config, NOT the parent session's active model/API key. If `delegation.model` points to a provider without a valid key in `.env`, subagents fail with `401 Invalid API Key`. Symptoms: parent session works fine, but all delegated tasks fail silently. Fix: ensure the delegation provider's env var is set, or set `delegation.model` to a provider that has a working key.
- **Use `-w` (worktree mode)** when spawning agents that edit code — prevents git conflicts
- **Set timeouts** for one-shot mode — complex tasks can take 5-10 minutes
- **Use `hermes chat -q` for fire-and-forget** — no PTY needed
- **Use tmux for interactive sessions** — raw PTY mode has `\r` vs `\n` issues with prompt_toolkit
- **For scheduled tasks**, use the `cronjob` tool instead of spawning — handles delivery and retry

---

## User Preferences & Workflow Patterns

### Minimalism Principle
User follows Occam's razor principle: "Entities should not be multiplied without necessity." This applies to:
- **Tool selection**: Prefer fewer, more versatile tools over many specialized ones
- **File organization**: Single entry point + clear directory structure, avoid duplicates
- **Information presentation**: Concise, direct answers without unnecessary explanation

### Obsidian Knowledge Base Organization
When adding new content to user's Obsidian vault:
1. **Single entry point**: Create/update one Markdown page in `wiki/AI工具/` as the main reference
2. **Clear file location**: Store files in logical subdirectories (e.g., `infographic/`, `attachments/`)
3. **Avoid duplication**: Don't create multiple copies in different locations
4. **Update index**: Always update `wiki/index.md` with new entries
5. **Log changes**: Add entry to `wiki/log.md` for traceability

### Skills Confusion Clarification
User may confuse `/skill` command (shows current session loaded skills) with `skills_list` tool (shows all available skills). Clarify this distinction when relevant.

## Troubleshooting

### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify provider: `pip install faster-whisper` or set API key
3. In gateway: `/restart`. In CLI: exit and relaunch.

### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

### Model/provider issues
1. `hermes doctor` — check config and dependencies
2. `hermes login` — re-authenticate OAuth providers
3. Check `.env` has the right API key
4. **Copilot 403**: `gh auth login` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.
5. **`hermes model` is interactive-only**: It requires a real TTY and fails with `Error: 'hermes model' requires an interactive terminal.` when called from a tool/script. To change models non-interactively, use `hermes config set model.default <model-name>` directly. Verify available models by querying the provider's API (e.g. `curl -s https://api.deepseek.com/v1/models -H "Authorization: Bearer $DEEPSEEK_API_KEY"`) or by checking `hermes config | grep model` to see current settings.

### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
- **Code changes:** Restart the CLI or gateway process

### `hermes config set` does NOT update API keys

This is a common pitfall that produces 401 errors even after the user "changed the key" via `hermes config set`:

- `hermes config set model.base_url …` → writes `config.yaml` ✅
- `hermes config set model.default …` → writes `config.yaml` ✅
- **API keys** (`XIAOMI_API_KEY`, `DEEPSEEK_API_KEY`, etc.) → live in **`~/.hermes/.env`**, NOT `config.yaml`

`hermes config set` only touches `config.yaml`. To update an API key, edit `.env` directly:
```bash
# View current key
grep XIAOMI_API_KEY ~/.hermes/.env

# Update (macOS sed)
sed -i '' 's/^XIAOMI_API_KEY=.*/XIAOMI_API_KEY=新key/' ~/.hermes/.env
```
Then `/reset` or restart Hermes for the new key to take effect.

**Symptom:** User says "I changed the key with config set but still get 401" — check whether they updated `config.yaml` or `.env`.

### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `/skill name` or `hermes -s name`

### Skills Count Confusion

Users may see only 3-4 skills with `/skill` command but 136+ with `skills_list`. This is expected:

- **`/skill` command**: Shows skills currently loaded or available for loading in the session
- **`skills_list` tool**: Shows ALL installed skills in `~/.hermes/skills/` directory
- **Skills are loaded on-demand**: Most skills load automatically when triggered by keywords

The `/skill` view is like "what's in my toolbox right now" while `skills_list` is "what's in the entire warehouse".

### `hermes skills install` times out / can't reach raw.githubusercontent.com

`hermes skills install` does NOT inherit the system proxy (ClashX, V2Ray, Surge, etc.) — even if `curl` works fine through the proxy. Symptoms: command hangs at "Fetching:" then times out after 30-120s.

**Workaround — manual file placement** (the skill gets picked up on next session):
```bash
# 1. Download SKILL.md with curl (which respects system proxy)
curl -sL -o /tmp/SKILL.md "https://raw.githubusercontent.com/<owner>/<repo>/main/SKILL.md"

# 2. Place it in the skills directory
SKILL_NAME="my-skill"
mkdir -p ~/.hermes/skills/"$SKILL_NAME"
cp /tmp/SKILL.md ~/.hermes/skills/"$SKILL_NAME"/SKILL.md
```
Skills installed this way appear in `hermes skills list` and load normally — the directory structure is identical to what `hermes skills install` creates. No restart needed for new sessions to pick it up.

### Gateway issues
Check logs first — two logs to consult depending on the error type:

```bash
# Platform adapter errors (connection drops, DNS failures, API 4xx/5xx from the messaging service)
grep -i "poll error\|failed to send\|connect.*failed\|error" ~/.hermes/logs/gateway.log | tail -20

# LLM model API errors (the model provider returned an error, NOT the messaging platform)
grep "Non-retryable client error" ~/.hermes/logs/errors.log | tail -10
```

**Crucial diagnostic distinction:** an `HTTP 400` or `Error code: 400` shown during gateway message processing is almost always an **LLM model API error** (from `run_agent.py`), NOT a messaging-platform error. The platform adapter already delivered the message to Hermes; the failure is in the LLM call. Check `~/.hermes/logs/errors.log` for the exact error, not `gateway.log`.

Common gateway problems:
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`
- **Cron job delivers with DNS errors** (macOS sleep): Machine asleep at cron time → network down → delivery transport can't connect. See `references/cron-sleep-delivery-failure.md` for diagnosis and all fix options.

### Gateway model config independence

The gateway runs as a **separate long-lived process** that reads `config.yaml` at startup. CLI model switches (`hermes model`, or passing `-m` at invocation) affect only that CLI session, NOT the gateway. To change the model used by the gateway:

1. Update `config.yaml`:
   ```bash
   hermes config set model.default <new-model>
   hermes config set model.provider <provider>
   hermes config set model.base_url <endpoint>
   ```
2. Restart the gateway:
   ```bash
   hermes gateway restart
   ```

If a user reports HTTP 400/500 errors from a messaging platform (Telegram, WeChat, etc.), first check whether `config.yaml` still points to an unavailable model (e.g. Ollama model that isn't running, or a local model that was swapped out). The gateway inherits whatever is in `config.yaml` — it does not inherit the CLI session's active model.

### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows HTTP 400 "No models provided"**: Config file encoding issue (BOM). Ensure `config.yaml` is saved as UTF-8 without BOM.
- **WeChat (Weixin) DNS / connection failures**: The adapter connects to `ilinkai.weixin.qq.com` via Tencent's iLink Bot API. If DNS resolves to `198.18.x.x` (RFC 2544 benchmark range), a local proxy/VPN (Clash, Surge, V2Ray) is intercepting the connection. Symptoms: repeated `Cannot connect to host ilinkai.weixin.qq.com:443` errors in `gateway.log`. Fix: ensure your proxy is running and properly routing traffic to `*.weixin.qq.com`. The gateway will log `Proxy detected; passing explicitly to HTTPXRequest: http://127.0.0.1:7890` when it auto-detects a proxy.
- **WeChat "Unauthorized user"**: The iLink bot generates `@im.bot` and `@im.wechat` user IDs. New users must be approved via `~/.hermes/pairing/weixin-approved.json` (auto-managed by the pairing system) or by the gateway's `/approve` command. Check `~/.hermes/pairing/weixin-pending.json` for pending users.
- **Feishu config: app_id must be in extra** — The feishu adapter reads `app_id` from `extra.get("app_id")` OR `os.getenv("FEISHU_APP_ID")`. If you only set `token` (the App ID) without `app_id` in `extra`, and `FEISHU_APP_ID` env var is not set, the adapter logs "FEISHU_APP_ID or FEISHU_APP_SECRET not set" and fails to connect. Fix: add `app_id` under `extra:` matching the `token` value. The env var fallback (`~/.hermes/.env`) also works but config.yaml is preferred for visibility.

### Auxiliary models not working
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
```bash
hermes config set auxiliary.vision.provider <your_provider>
hermes config set auxiliary.vision.model <model_name>
```

---

## Where to Find Things

| Looking for... | Location |
|----------------|----------|
| Config options | `hermes config edit` or [Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) |
| Available tools | `hermes tools list` or [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) |
| Slash commands | `/help` in session or [Slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands) |
| Skills catalog | `hermes skills browse` or [Skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) |
| Provider setup | `hermes model` or [Providers guide](https://hermes-agent.nousresearch.com/docs/integrations/providers) |
| Platform setup | `hermes gateway setup` or [Messaging docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) |
| MCP servers | `hermes mcp list` or [MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) |
| Profiles | `hermes profile list` or [Profiles docs](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) |
| Cron jobs | `hermes cron list` or [Cron docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) |
| Memory | `hermes memory status` or [Memory docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) |
| Env variables | `hermes config env-path` or [Env vars reference](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) |
| CLI commands | `hermes --help` or [CLI reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) |
| Gateway logs | `~/.hermes/logs/gateway.log` |
| Session files | `~/.hermes/sessions/` or `hermes sessions browse` |
| Source code | `~/.hermes/hermes-agent/` |

---

## Contributor Quick Reference

For occasional contributors and PR authors. Full developer docs: https://hermes-agent.nousresearch.com/docs/developer-guide/

### Project Layout

```
hermes-agent/
├── run_agent.py          # AIAgent — core conversation loop
├── model_tools.py        # Tool discovery and dispatch
├── toolsets.py           # Toolset definitions
├── cli.py                # Interactive CLI (HermesCLI)
├── hermes_state.py       # SQLite session store
├── agent/                # Prompt builder, context compression, memory, model routing, credential pooling, skill dispatch
├── hermes_cli/           # CLI subcommands, config, setup, commands
│   ├── commands.py       # Slash command registry (CommandDef)
│   ├── config.py         # DEFAULT_CONFIG, env var definitions
│   └── main.py           # CLI entry point and argparse
├── tools/                # One file per tool
│   └── registry.py       # Central tool registry
├── gateway/              # Messaging gateway
│   └── platforms/        # Platform adapters (telegram, discord, etc.)
├── cron/                 # Job scheduler
├── tests/                # ~3000 pytest tests
└── website/              # Docusaurus docs site
```

Config: `~/.hermes/config.yaml` (settings), `~/.hermes/.env` (API keys).

### Adding a Tool (3 files)

**1. Create `tools/your_tool.py`:**
```python
import json, os
from tools.registry import registry

def check_requirements() -> bool:
    return bool(os.getenv("EXAMPLE_API_KEY"))

def example_tool(param: str, task_id: str = None) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="example_tool",
    toolset="example",
    schema={"name": "example_tool", "description": "...", "parameters": {...}},
    handler=lambda args, **kw: example_tool(
        param=args.get("param", ""), task_id=kw.get("task_id")),
    check_fn=check_requirements,
    requires_env=["EXAMPLE_API_KEY"],
)
```

**2. Add to `toolsets.py`** → `_HERMES_CORE_TOOLS` list.

Auto-discovery: any `tools/*.py` file with a top-level `registry.register()` call is imported automatically — no manual list needed.

All handlers must return JSON strings. Use `get_hermes_home()` for paths, never hardcode `~/.hermes`.

### Adding a Slash Command

1. Add `CommandDef` to `COMMAND_REGISTRY` in `hermes_cli/commands.py`
2. Add handler in `cli.py` → `process_command()`
3. (Optional) Add gateway handler in `gateway/run.py`

All consumers (help text, autocomplete, Telegram menu, Slack mapping) derive from the central registry automatically.

### Agent Loop (High Level)

```
run_conversation():
  1. Build system prompt
  2. Loop while iterations < max:
     a. Call LLM (OpenAI-format messages + tool schemas)
     b. If tool_calls → dispatch each via handle_function_call() → append results → continue
     c. If text response → return
  3. Context compression triggers automatically near token limit
```

### Testing

```bash
python -m pytest tests/ -o 'addopts=' -q   # Full suite
python -m pytest tests/tools/ -q            # Specific area
```

- Tests auto-redirect `HERMES_HOME` to temp dirs — never touch real `~/.hermes/`
- Run full suite before pushing any change
- Use `-o 'addopts='` to clear any baked-in pytest flags

### Commit Conventions

```
type: concise subject line

Optional body.
```

Types: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`

### Key Rules

- **Never break prompt caching** — don't change context, tools, or system prompt mid-conversation
- **Message role alternation** — never two assistant or two user messages in a row
- Use `get_hermes_home()` from `hermes_constants` for all paths (profile-safe)
- Config values go in `config.yaml`, secrets go in `.env`
- New tools need a `check_fn` so they only appear when requirements are met
