# autocmd

Natural language to shell command.

## Installation

```bash
# Install from PyPI (recommended)
uv tool install autocmd-cli

# Or directly from git
uv tool install git+https://github.com/dvirzg/autocmd.git
```

## Quick start

The first time you run `autocmd`, it will:

1. **Ask for your Anthropic API key** – saved to `~/.config/autocmd/config`.
2. **Offer shell integration** (recommended) – adds a small wrapper to `.zshrc`/`.bashrc`
   so commands appear on your prompt, ready to edit before running.

Trigger setup with any command:

```bash
autocmd "check git status"
```

After setup:

```bash
autocmd "git fetch all updates from remote"
# → git fetch --all  (lands on your prompt, you hit Enter or edit)
```

More examples:

```bash
autocmd "show git log for last 5 commits"
autocmd "find all python files modified today"
autocmd "kill process on port 3000"

```

## Configuration

**Settings**

Configure `autocmd` behavior with:

```bash
autocmd --settings
```

This allows you to:
- Toggle streaming output on/off (default: on)

**Model selection**

By default `autocmd` uses `claude-haiku-4-5-20251001`. To change it, set `AUTOCMD_MODEL`:

```bash
# One-time use
AUTOCMD_MODEL=claude-sonnet-4-20250514 autocmd "your command here"

# In your shell config (~/.zshrc or ~/.bashrc)
export AUTOCMD_MODEL=claude-sonnet-4-20250514
```

**Reset configuration**

To reset all settings and API key:

```bash
autocmd --reset
```

## Development

```bash
git clone https://github.com/dvirzg/autocmd.git
cd autocmd
./dev-setup.sh
source ~/.zshrc  # or ~/.bashrc

# Always uses the local code
autocmd-dev "check git status"
```

## Uninstall

```bash
uv tool uninstall autocmd
```

Then remove the `autocmd` line from your shell config if you want to fully clean it up.
