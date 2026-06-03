# Xiaomi MiMo Model Switching

## Problem
Switching between Xiaomi MiMo models (e.g., mimo-v2-pro → mimo-v2.5-pro) requires updating THREE locations in config.yaml.

## Three Required Changes

1. **Default model**: `model.default`
2. **Provider model list**: `custom_providers[].models` (add new model if not present)
3. **Provider default model**: `custom_providers[].model`

## Step-by-Step

```bash
# 1. Query available models from API
curl -s https://token-plan-cn.xiaomimimo.com/v1/models \
  -H "Authorization: Bearer $(grep XIAOMI_API_KEY ~/.hermes/.env | cut -d= -f2)"

# 2. Update config.yaml (three changes required)
hermes config set model.default mimo-v2.5-pro

# 3. Edit config.yaml manually:
#    a) Under custom_providers → xiaomi → models, add:
#       mimo-v2.5-pro:
#         name: MiMo v2.5 Pro
#    b) Update provider's model field to: mimo-v2.5-pro

# 4. Restart gateway
hermes gateway restart

# 5. Verify
hermes status | grep "Model:"
```

## Pitfalls

- **Missing model in provider list**: If new model not in `custom_providers[].models`, Hermes may fall back or error
- **Gateway vs CLI independence**: Changing `model.default` affects gateway only after restart. CLI sessions use their own model selection
- **API key location**: Keys in `~/.hermes/.env`, NOT config.yaml. Use `hermes config set` only for config.yaml values

## Available Models (as of 2026-05)

```
mimo-v2-omni      - Multi-modal (possibly vision)
mimo-v2-pro       - Professional text
mimo-v2-tts       - Text-to-speech
mimo-v2.5         - Updated base
mimo-v2.5-pro     - Updated professional
mimo-v2.5-tts     - Updated TTS
mimo-v2.5-tts-voiceclone
mimo-v2.5-tts-voicedesign
```

## Image Recognition Testing Results (2026-05-23)

- `mimo-v2.5`: Returns "failed to download url data" for image_url requests
- `mimo-v2-omni`: Same error
- Possible causes: API doesn't support URL-based images, needs base64 encoding, or vision not supported yet