#!/usr/bin/env python3
import json
import os
from pathlib import Path

PLUGIN_NAME = "cc-distribution"


def _settings_path(root: Path) -> Path:
    return root / ".claude" / "settings.json"


def _load_settings(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return {}


def _save_settings(path: Path, settings: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(settings, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _statusline_command() -> str:
    return (
        "bash -lc '"
        "plugin_dir=$(ls -td ~/.claude/plugins/cache/" + PLUGIN_NAME + "/" + PLUGIN_NAME + "/*/ 2>/dev/null | head -1);"
        "if [ -z \"$plugin_dir\" ]; then exit 0; fi;"
        "python3 \"${plugin_dir}scripts/statusline.py\"'"
    )


def main() -> int:
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
    settings_path = _settings_path(root)
    settings = _load_settings(settings_path)

    if "statusLine" in settings:
        return 0

    settings["statusLine"] = {
        "type": "command",
        "command": _statusline_command(),
    }
    _save_settings(settings_path, settings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
