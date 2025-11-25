#!/usr/bin/env python3
import sys, os, subprocess, readline, re, getpass
from pathlib import Path
from anthropic import Anthropic

def get_api_key():
    """Get API key from env or config file, prompt if missing"""
    if key := os.environ.get("ANTHROPIC_API_KEY"):
        return key

    config_path = Path.home() / ".config" / "autocmd" / "config"
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
    # Check API key first (even before validating args)
    api_key = get_api_key()

    if len(sys.argv) < 2:
        print("Usage: autocmd \"natural language command\"")
        sys.exit(1)

    # Get shell command from Claude
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=200,
        messages=[{"role": "user",
                "content": f"Convert to a {os.environ.get('SHELL', 'bash')} command. Reply with ONLY the command, no markdown: {' '.join(sys.argv[1:])}"}]
    )
    cmd = clean_command(response.content[0].text)

    # Let user edit
    readline.set_startup_hook(lambda: readline.insert_text(cmd))
    try:
        final = input("$ ")
    finally:
        readline.set_startup_hook()

    # Execute
    if final:
        subprocess.run(final, shell=True)

if __name__ == "__main__":
    main()
