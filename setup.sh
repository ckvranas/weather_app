#!/bin/bash

set -e  # Exit on error
source .env
VENV_DIR=".venv"

# Check if 'uv' is installed
if ! command -v uv &> /dev/null; then
    echo "'uv' not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
else
    echo "'uv' is already installed."
fi

# Create virtual environment if it doesn't exist
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment '$VENV_DIR' already exists."
else
    echo "Creating virtual environment with 'uv'..."
    uv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

uv sync

echo "Setup complete!"