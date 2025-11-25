# autocmd

Natural language to shell command translator using Claude Haiku.

## Installation

```bash
# Install globally with uv
uv tool install git+https://github.com/dvirzagury/autocmd.git

# Or install from local directory
cd /path/to/autocmd
uv tool install .
```

On first run, you'll be prompted to enter your Anthropic API key (stored in `~/.config/autocmd/config`).

## Usage

```bash
autocmd "git fetch all updates from remote"
# $ git fetch --all█
# Press Enter to run, or edit first with arrow keys
```

The tool will:
1. Convert your natural language to a shell command using Claude Haiku
2. Pre-fill an editable prompt with the suggested command
3. Let you edit it (arrow keys, backspace, etc.)
4. Execute when you press Enter

## Examples

```bash
autocmd "show git log for last 5 commits"
autocmd "find all python files modified today"
autocmd "kill process on port 3000"
autocmd "compress images in current folder"
```

## Uninstall

```bash
uv tool uninstall autocmd
```
