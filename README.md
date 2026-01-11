# AI Architect Plugin

Configure AI roles and providers for Claude Code.

## What this plugin does

- Stores role and provider settings in `.claude/settings.json` under `aiArchitect`.
- Provides a single interactive configuration command.

## Install for local testing

```bash
claude --plugin-dir /home/codex/claude-marketplace/ai-architect
```

## Configuration

Run:

```
/cc-distribution:config
```

This opens an interactive menu to manage roles and providers.

## Roles (default)

- planning
- architect
- review
- qa

Each role can be enabled/disabled and assigned to a provider.

## Providers

- `claude` (always available)
- `codex`
- `gemini`
- custom command providers

## Auth options (shown in the config menu)

- Codex: `codex login`, `codex login --device-auth`, or `printenv OPENAI_API_KEY | codex login --with-api-key`.
- Gemini: Google OAuth login via `gemini`, API key via `GEMINI_API_KEY`, or Vertex AI via `GOOGLE_API_KEY` + `GOOGLE_GENAI_USE_VERTEXAI=true`.

## Slash commands

- `/cc-distribution:config` - interactive configuration and provider registration
