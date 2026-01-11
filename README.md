# AI Architect Plugin

Configure AI roles and providers for Claude Code.

## What this plugin does

- Stores role and provider settings in `.claude/settings.json` under `aiArchitect`.
- Provides a single configuration command that shows a fast menu.
- Statusline is enabled by default and shows enabled roles/providers.

## Install for local testing

```bash
claude --plugin-dir /home/codex/claude-marketplace/ai-architect
```

## Configuration

Run:

```
/cc-distribution:config
```

Then read the menu files:

- `menu/main.md`
- `menu/help.md`
- `menu/roles.md`
- `menu/providers.md`
- `menu/settings.md`

## Statusline format

Enabled roles are shown as:

```
Planning [Claude] | Architect [Codex] | Review [Gemini]
```

Disabled roles are omitted.

## Roles (default)

- planning
- architect
- review
- qa

Each role can be enabled/disabled and assigned to a provider. Role names must be kebab-case.

## Providers

- `claude` (always available)
- `codex`
- `gemini`
- custom command providers

## Auth options

- Codex: `codex login`, `codex login --device-auth`, or `printenv OPENAI_API_KEY | codex login --with-api-key`.
- Gemini: Google OAuth login via `gemini`, API key via `GEMINI_API_KEY`, or Vertex AI via `GOOGLE_API_KEY` + `GOOGLE_GENAI_USE_VERTEXAI=true`.

## Slash commands

- `/cc-distribution:config` - show the fast menu

## Disable statusline

Remove the `statusLine` block from `.claude/settings.json` for this project.
