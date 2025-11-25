# autocmd

Natural language to shell command translator using Claude Haiku 4.5.

## Installation

```bash
# Install globally with uv
uv tool install git+https://github.com/dvirzagury/autocmd.git

# Or install from local directory
cd /path/to/autocmd
uv tool install .
```

## First Run Setup

The first time you run `autocmd`, it will:

1. **Ask for your Anthropic API key** - Get one at https://console.anthropic.com
   - Saved securely to `~/.config/autocmd/config`

2. **Offer to set up shell integration** (recommended)
   - Adds a small wrapper function to your `.zshrc` or `.bashrc`
   - Makes commands appear directly on your prompt, editable before execution
   - If you skip this, commands will just be printed (you can copy/paste them)

Just run any autocmd command to start setup:

```bash
autocmd "check git status"
```

## Usage

After setup, commands appear on your prompt line as if you typed them:

```bash
$ autocmd "git fetch all updates from remote"
$ git fetch --all█  # ← appears on your prompt, press Enter to run or edit first
```

## Examples

```bash
autocmd "show git log for last 5 commits"
autocmd "find all python files modified today"
autocmd "kill process on port 3000"
autocmd "compress images in current folder"
autocmd "create a new branch called feature-x"
```

## How It Works

- Uses Claude Haiku 4.5 for fast, accurate command translation
- Isolated dependencies (won't interfere with other Python projects)
- Shell integration uses `print -z` (zsh) or `READLINE_LINE` (bash)
- Works from any directory after installation

## Development

To contribute or develop locally:

```bash
# Clone the repo
git clone https://github.com/dvirzagury/autocmd.git
cd autocmd

# Run the dev setup script
./dev-setup.sh

# Reload your shell
source ~/.zshrc  # or ~/.bashrc

# Use autocmd-dev for development (always uses latest code)
autocmd-dev "check git status"
```

The `autocmd-dev` alias lets you test changes immediately without reinstalling. Just edit the code and run `autocmd-dev` - it always uses your latest changes with full shell integration.

## Uninstall

```bash
uv tool uninstall autocmd

# Optionally remove the shell integration line from ~/.zshrc or ~/.bashrc
# (Look for "# autocmd shell integration")
```
