#!/usr/bin/env python3
import sys, os, subprocess, re, getpass, shutil
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

def get_config_dir():
    return Path.home() / ".config" / "autocmd"

def is_shell_setup():
    return (get_config_dir() / ".shell_setup_done").exists()

def detect_shell():
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        return "zsh", Path.home() / ".zshrc"
    elif "bash" in shell:
        bashrc = Path.home() / ".bashrc"
        return "bash", bashrc if bashrc.exists() else Path.home() / ".bash_profile"
    return None, None

def setup_shell_integration():
    shell_type, rc_file = detect_shell()
    if not shell_type:
        print("Unsupported shell.", file=sys.stderr)
        return False

    print("\nLet's go through a quick setup.", file=sys.stderr)
    print("Shell integration injects commands into your shell for easy editing.", file=sys.stderr)
    print("Enable? (y/n): ", end='', file=sys.stderr, flush=True)
    if input().strip().lower() != 'y':
        print("Skipping shell integration. Commands will be printed only.", file=sys.stderr)
        return False

    autocmd_cmd = shutil.which("autocmd") or "uv tool run autocmd"

    if shell_type == "zsh":
        wrapper = f'\n# autocmd\nautocmd() {{ local cmd=$({autocmd_cmd} "$@"); [ -n "$cmd" ] && print -z "$cmd"; }}\n'
    else:
        wrapper = f'\n# autocmd\nautocmd() {{ local cmd=$({autocmd_cmd} "$@"); [ -n "$cmd" ] && {{ READLINE_LINE="$cmd"; READLINE_POINT=${{#READLINE_LINE}}; }}; }}\n'

    if rc_file.exists() and "# autocmd" in rc_file.read_text():
        return True

    with open(rc_file, "a") as f:
        f.write(wrapper)

    get_config_dir().mkdir(parents=True, exist_ok=True)
    (get_config_dir() / ".shell_setup_done").touch()
    return True

def get_api_key():
    if key := os.environ.get("ANTHROPIC_API_KEY"):
        return key

    config_path = get_config_dir() / "config"
    if config_path.exists():
        return config_path.read_text().strip()

    print("Anthropic API key: ", end='', file=sys.stderr, flush=True)
    key = getpass.getpass("").strip()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(key)
    return key

def reset_autocmd():
    config_dir = get_config_dir()
    if config_dir.exists():
        shutil.rmtree(config_dir)

    shell_type, rc_file = detect_shell()
    if rc_file and rc_file.exists():
        content = rc_file.read_text()
        if "# autocmd" in content:
            lines = content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if "# autocmd" in line:
                    skip = True
                elif skip and '}' in line:
                    skip = False
                    continue
                elif not skip:
                    new_lines.append(line)
            rc_file.write_text('\n'.join(new_lines))
            print(f"Reset complete. Run: source {rc_file}", file=sys.stderr)
        else:
            print("Reset complete.", file=sys.stderr)

def main():
    load_dotenv()

    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_autocmd()
        sys.exit(0)

    if not is_shell_setup():
        print("Welcome to autocmd! The text-to-command assistant.", file=sys.stderr)
        setup_shell_integration()
        get_api_key()
        shell_type, rc_file = detect_shell()
        if rc_file:
            print(f"Setup complete! Reload your shell to activate:", file=sys.stderr)
            print(f"  source {rc_file}", file=sys.stderr)
        sys.exit(0)

    api_key = get_api_key()

    if len(sys.argv) < 2:
        print('autocmd: The text-to-command assistant', file=sys.stderr)
        sys.exit(1)

    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=os.environ.get("MODEL", "claude-haiku-4-5-20251001"),
            max_tokens=200,
            messages=[{"role": "user", "content": f"Convert to {os.environ.get('SHELL', 'bash')} command (no markdown): {' '.join(sys.argv[1:])}"}]
        )
        cmd = re.sub(r'^```\w*\n?|```$', '', response.content[0].text).strip()
        if not cmd:
            print("No command generated", file=sys.stderr)
            sys.exit(1)
        print(cmd)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
