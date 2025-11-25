#!/bin/zsh
# Wrapper function for autocmd that injects the result into the command line

autocmd() {
    # Run the Python script and capture output
    local cmd=$(uv run /Users/dvirzagury/Development/autocmd/autocmd.py "$@")

    # Use print -z to push the command into the ZLE buffer
    # This makes it appear as if the user typed it
    print -z "$cmd"
}
