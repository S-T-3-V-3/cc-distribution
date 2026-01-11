#!/usr/bin/env python3
import argparse
import sys

from ai_lib import ROLES, load_config, project_root, save_config, summarize_config


def _prompt(text: str) -> str:
    return input(text).strip()


def _print_auth_help() -> None:
    print("Codex auth options:")
    print("- Interactive login: codex login")
    print("- Device auth: codex login --device-auth")
    print("- API key: printenv OPENAI_API_KEY | codex login --with-api-key")
    print("")
    print("Gemini auth options (from gemini-cli README):")
    print("- Login with Google (OAuth): run 'gemini' and choose Login with Google")
    print("- Gemini API key: export GEMINI_API_KEY=... then run 'gemini'")
    print("- Vertex AI: export GOOGLE_API_KEY=... and GOOGLE_GENAI_USE_VERTEXAI=true")
    print("")
    print("Custom providers:")
    print("- Provide a command that accepts a prompt argument, or use {prompt} placeholder.")
    print("- Example: mycli --prompt '{prompt}'")


def _providers_in_use(config: dict) -> set[str]:
    roles = config.get("roles", {})
    used = set()
    for role in ROLES:
        provider = roles.get(role, {}).get("provider")
        if provider:
            used.add(provider)
    return used


def _list_providers(config: dict) -> list[str]:
    providers = config.get("providers", {})
    return sorted(providers.keys())


def _roles_menu(config: dict) -> None:
    while True:
        print("")
        print("Roles")
        print("1) Show roles")
        print("2) Enable/disable role")
        print("3) Assign provider to role")
        print("4) Back")
        choice = _prompt("> ")

        if choice == "1":
            print(summarize_config(config))
        elif choice == "2":
            role = _prompt(f"Role {ROLES}: ").lower()
            if role not in ROLES:
                print("Invalid role.")
                continue
            role_cfg = config.setdefault("roles", {}).setdefault(role, {})
            current = role_cfg.get("enabled", True)
            role_cfg["enabled"] = not current
            state = "on" if role_cfg["enabled"] else "off"
            print(f"{role} now {state}.")
        elif choice == "3":
            role = _prompt(f"Role {ROLES}: ").lower()
            if role not in ROLES:
                print("Invalid role.")
                continue
            providers = _list_providers(config)
            print(f"Available providers: {providers}")
            provider = _prompt("Provider name: ")
            if provider not in config.get("providers", {}):
                print("Unknown provider.")
                continue
            config.setdefault("roles", {}).setdefault(role, {})["provider"] = provider
            print(f"Assigned {provider} to {role}.")
        elif choice == "4":
            return
        else:
            print("Unknown selection.")


def _add_provider(config: dict) -> None:
    print("")
    print("Add provider")
    print("1) Codex")
    print("2) Gemini")
    print("3) Custom command")
    print("4) Back")
    choice = _prompt("> ")

    providers = config.setdefault("providers", {})

    if choice == "1":
        _print_auth_help()
        name = _prompt("Provider name (default 'codex'): ") or "codex"
        model = _prompt("Model (default gpt-5.2-codex): ") or "gpt-5.2-codex"
        providers[name] = {
            "kind": "codex",
            "model": model,
        }
        print(f"Added provider {name} (codex).")
    elif choice == "2":
        _print_auth_help()
        name = _prompt("Provider name (default 'gemini'): ") or "gemini"
        model = _prompt("Model (default gemini-1.5-pro): ") or "gemini-1.5-pro"
        providers[name] = {
            "kind": "gemini",
            "model": model,
        }
        print(f"Added provider {name} (gemini).")
    elif choice == "3":
        name = _prompt("Provider name: ")
        if not name:
            print("Name required.")
            return
        command = _prompt("Command (use {prompt} placeholder if needed): ")
        if not command:
            print("Command required.")
            return
        providers[name] = {
            "kind": "command",
            "command": command,
        }
        print(f"Added provider {name} (command).")
    elif choice == "4":
        return
    else:
        print("Unknown selection.")


def _edit_provider(config: dict) -> None:
    providers = config.get("providers", {})
    name = _prompt("Provider name to edit: ")
    if name not in providers:
        print("Provider not found.")
        return

    provider = providers[name]
    kind = provider.get("kind")

    if kind in ("codex", "gemini"):
        model = _prompt(f"Model (current {provider.get('model')}): ")
        if model:
            provider["model"] = model
            print("Updated model.")
    elif kind == "command":
        command = _prompt(f"Command (current {provider.get('command')}): ")
        if command:
            provider["command"] = command
            print("Updated command.")
    elif kind == "claude":
        print("Claude provider cannot be modified.")
    else:
        print("Unsupported provider type.")


def _remove_provider(config: dict) -> None:
    name = _prompt("Provider name to remove: ")
    if name == "claude":
        print("Claude provider cannot be removed.")
        return

    providers = config.get("providers", {})
    if name not in providers:
        print("Provider not found.")
        return

    used = _providers_in_use(config)
    if name in used:
        print("Provider is assigned to a role. Reassign roles before removing.")
        return

    providers.pop(name)
    print(f"Removed provider {name}.")


def _providers_menu(config: dict) -> None:
    while True:
        print("")
        print("Providers")
        print("1) List providers")
        print("2) Add provider")
        print("3) Edit provider")
        print("4) Remove provider")
        print("5) Back")
        choice = _prompt("> ")

        if choice == "1":
            print(summarize_config(config))
        elif choice == "2":
            _add_provider(config)
        elif choice == "3":
            _edit_provider(config)
        elif choice == "4":
            _remove_provider(config)
        elif choice == "5":
            return
        else:
            print("Unknown selection.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage AI routing settings")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("config", help="Interactive configuration")
    sub.add_parser("summary", help="Show current routing configuration")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = project_root()
    config = load_config(root)

    if args.command == "summary":
        print(summarize_config(config))
        return 0

    if args.command == "config":
        if not sys.stdin.isatty():
            print("Interactive configuration requires a TTY.")
            print("Run this command in a terminal:")
            print("python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ai_config.py config")
            return 0

        while True:
            print("")
            print("AI configuration")
            print("1) Show current config")
            print("2) Roles")
            print("3) Providers")
            print("4) Auth / install help")
            print("5) Save and exit")
            choice = _prompt("> ")

            if choice == "1":
                print(summarize_config(config))
            elif choice == "2":
                _roles_menu(config)
            elif choice == "3":
                _providers_menu(config)
            elif choice == "4":
                _print_auth_help()
            elif choice == "5":
                save_config(root, config)
                print(f"Saved settings at {root / '.claude' / 'settings.json'}")
                print(summarize_config(config))
                return 0
            else:
                print("Unknown selection.")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
