---
allowed-tools: Bash(python3:*)
description: Initialize AI routing settings for this project
---

## Initialize AI routing

- Setup defaults and show current routing:
  - !`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ai_config.py setup`

## Next

Use `/cc-distribution:target` to change a category target, or `/cc-distribution:implicit on|off` to toggle automatic routing.
