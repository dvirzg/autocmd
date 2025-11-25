#!/usr/bin/env python3
import sys, os, subprocess, readline
from anthropic import Anthropic

def main():
    if len(sys.argv) < 2:
        print("Usage: autocmd \"natural language command\"")
        sys.exit(1)

    # Get shell command from Claude
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Convert to a {os.environ.get('SHELL', 'bash')} command. Reply with ONLY the command: {' '.join(sys.argv[1:])}"}]
    )
    cmd = response.content[0].text.strip()

    # Show and let user edit
    print(f"\nSuggested: {cmd}\n")
    readline.set_startup_hook(lambda: readline.insert_text(cmd))
    try:
        final = input("Command: ")
    finally:
        readline.set_startup_hook()

    # Execute
    if final:
        subprocess.run(final, shell=True)

if __name__ == "__main__":
    main()
