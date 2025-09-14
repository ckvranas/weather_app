#!/bin/bash

VENV_DIR=".venv"

if [ -d "$VENV_DIR" ]; then
    deactivate
    echo "Remving virtual environment '$VENV_DIR' ..."
    rm -rf .venv
fi

if [ -d "src/weather_app/packet-api-client" ]; then
    echo "Removing packet-api-client..."
    rm -rf src/weather_app/packet-api-client
fi