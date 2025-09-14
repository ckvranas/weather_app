#!/bin/bash

VENV_DIR=".venv"
REL_WEATHER_APP_PATH="src/weather_app"

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

if ! [ -d "${REL_WEATHER_APP_PATH}/packet-api-client" ]; then
    echo "Creating packet-api-client..."
    openapi-python-client generate --path ${REL_WEATHER_APP_PATH}/api_spec/openapi.yaml --output-path ${REL_WEATHER_APP_PATH}/packet-api-client
    uv pip install -e ${REL_WEATHER_APP_PATH}/packet-api-client
fi

echo "Setup complete!"