#!/usr/bin/env python3
import re
from ai_lib import load_config, project_root

ROLE_TITLE_OVERRIDES = {
    "qa": "QA",
}
PROVIDER_TITLE_OVERRIDES = {
    "claude": "Claude",
    "codex": "Codex",
    "gemini": "Gemini",
}


def _titleize(name: str, overrides: dict) -> str:
    if name in overrides:
        return overrides[name]
    parts = re.split(r"[-_]+", name)
    return " ".join(part.capitalize() for part in parts if part)


def main() -> int:
    root = project_root()
    config = load_config(root)
    roles = config.get("roles", {})

    entries = []
    for role_name, role_cfg in roles.items():
        if not role_cfg.get("enabled", True):
            continue
        provider = role_cfg.get("provider", "claude")
        role_title = _titleize(role_name, ROLE_TITLE_OVERRIDES)
        provider_title = _titleize(provider, PROVIDER_TITLE_OVERRIDES)
        entries.append(f"{role_title} [{provider_title}]")

    if entries:
        print(" | ".join(entries))
    else:
        print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
