#!/usr/bin/env bash

# Install Chromium manually
mkdir -p ~/.local/bin
apt-get update && apt-get install -y chromium-browser

# Mark the binary location for later
which chromium-browser > .chromium-path

# Install Python deps
pip install -r requirements.txt
