# autocmd

Natural language to shell command translator using Claude API.

## Setup

```bash
# Create venv and install dependencies with uv
uv venv
uv pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Make executable
chmod +x autocmd.py

# Optional: Add to PATH
ln -s $(pwd)/autocmd.py /usr/local/bin/autocmd
```

## Usage

```bash
autocmd "git fetch all updates from remote"
# Suggested: git fetch --all
# Command: git fetch --all█
# Press Enter to run, or edit first
```

The tool will:
1. Convert your natural language to a shell command using Claude
2. Show you the suggested command
3. Let you edit it (arrow keys, backspace, etc.)
4. Execute when you press Enter
