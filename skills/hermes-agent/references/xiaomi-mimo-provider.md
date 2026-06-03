# Xiaomi MiMo Provider Details

## API Discovery
Query available models: `curl -s https://token-plan-cn.xiaomimimo.com/v1/models -H "Authorization: Bearer <key>"`

## Available Models (as of 2026-05-23)
| Model | Notes |
|-------|-------|
| mimo-v2-omni | "Omni" - likely multimodal (vision+audio+text) |
| mimo-v2-pro | Text-focused professional model |
| mimo-v2-tts | Text-to-speech |
| mimo-v2.5 | Newer base version |
| mimo-v2.5-pro | Newer professional version |
| mimo-v2.5-tts | TTS |
| mimo-v2.5-tts-voiceclone | Voice cloning TTS |
| mimo-v2.5-tts-voicedesign | Voice design TTS |

## Image Recognition Testing Results
- **mimo-v2.5**: Returns `"failed to download url data"` for image_url requests
- **mimo-v2-omni**: Same error
- **Possible causes**: API doesn't support URL-based images, needs base64 encoding, or vision not supported
- **Config limitation**: `config.yaml` only shows `mimo-v2-pro` - must query API to see full model list

## API Format
- Base URL: `https://token-plan-cn.xiaomimimo.com/v1`
- OpenAI-compatible chat completions format
- Returns `reasoning_content` in responses (chain-of-thought visible)