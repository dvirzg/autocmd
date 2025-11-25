#!/usr/bin/env python3
import sys, os, subprocess, readline, re, getpass, shutil
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

def get_config_dir():
    """Get the config directory path"""
    return Path.home() / ".config" / "autocmd"

def is_shell_setup():
    """Check if shell integration is already set up"""
    config_dir = get_config_dir()
    setup_marker = config_dir / ".shell_setup_done"
    return setup_marker.exists()

def detect_shell():
    """Detect user's shell and return shell type and rc file path"""
    shell = os.environ.get("SHELL", "")

    if "zsh" in shell:
        return "zsh", Path.home() / ".zshrc"
    elif "bash" in shell:
        # Check for .bashrc first, then .bash_profile
        bashrc = Path.home() / ".bashrc"
        if bashrc.exists():
            return "bash", bashrc
        return "bash", Path.home() / ".bash_profile"
    else:
        return None, None

def setup_shell_integration():
    """Set up shell integration for autocmd"""
    shell_type, rc_file = detect_shell()

    if not shell_type:
        print("Warning: Could not detect shell type (zsh or bash).")
        print("Shell integration setup skipped. Commands will be printed only.")
        return False

    print(f"autocmd works best with shell integration.")
    print(f"This will add a small function to your {rc_file.name}.")
    response = input("Set up shell integration? (y/n): ").strip().lower()

    if response != 'y':
        print("Shell integration skipped. Commands will be printed only.")
        return False

    # Find where autocmd is installed
    autocmd_path = shutil.which("autocmd")
    if not autocmd_path:
        # Fallback: use uv run with the module
        autocmd_cmd = "uv tool run autocmd"
    else:
        autocmd_cmd = autocmd_path

    # Generate shell wrapper function
    if shell_type == "zsh":
        wrapper = f'''
# autocmd shell integration
autocmd() {{
    local cmd=$({autocmd_cmd} "$@" 2>/dev/null)
    if [ -n "$cmd" ]; then
        print -z "$cmd"
    fi
}}
'''
    else:  # bash
        wrapper = f'''
# autocmd shell integration
autocmd() {{
    local cmd=$({autocmd_cmd} "$@" 2>/dev/null)
    if [ -n "$cmd" ]; then
        READLINE_LINE="$cmd"
        READLINE_POINT=${{#READLINE_LINE}}
    fi
}}
bind -x '"\\C-x\\C-a": autocmd'
'''

    # Check if already added
    if rc_file.exists():
        content = rc_file.read_text()
        if "# autocmd shell integration" in content:
            print(f"Shell integration already exists in {rc_file}")
            return True

    # Append to rc file
    with open(rc_file, "a") as f:
        f.write(wrapper)

    print(f"\n✓ Shell integration added to {rc_file}")
    print(f"Run: source {rc_file}")
    print("Or restart your terminal for changes to take effect.\n")

    # Mark setup as done
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / ".shell_setup_done").touch()

    return True

def get_api_key():
    """Get API key from env or config file, prompt if missing"""
    if key := os.environ.get("ANTHROPIC_API_KEY"):
        return key

    config_path = get_config_dir() / "config"
    if config_path.exists():
        return config_path.read_text().strip()

    # First run - prompt for key
    print("Welcome to autocmd! Please enter your Anthropic API key:")
    key = getpass.getpass("API Key: ").strip()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(key)
    print(f"API key saved to {config_path}\n")
    return key

def clean_command(cmd):
    """Remove markdown code blocks and clean output"""
    cmd = re.sub(r'^```\w*\n?', '', cmd)
    cmd = re.sub(r'\n?```$', '', cmd)
    return cmd.strip()

def main():
    # Load environment variables from .env if present
    load_dotenv()

    # Check if shell integration setup is needed (first run)
    if not is_shell_setup():
        setup_shell_integration()
        print("\nSetup complete! Please run your command again.")
        sys.exit(0)

    # Check API key
    api_key = get_api_key()

    if len(sys.argv) < 2:
        print("Usage: autocmd \"natural language command\"")
        sys.exit(1)

    # Get shell command from Claude
    model = os.environ.get("MODEL", "claude-haiku-4-5-20251001")
    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=200,
            messages=[{"role": "user",
                    "content": f"Convert to a {os.environ.get('SHELL', 'bash')} command. Reply with ONLY the command, no markdown: {' '.join(sys.argv[1:])}"}]
        )
        cmd = clean_command(response.content[0].text)

        if not cmd:
            print("Error: No command generated")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Just print the command - the shell wrapper will handle the rest
    print(cmd)

if __name__ == "__main__":
    main()
