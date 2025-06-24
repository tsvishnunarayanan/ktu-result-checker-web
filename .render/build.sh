#!/usr/bin/env bash

set -x  # Show commands as they run

# Install Chrome (headless)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt update && apt install -y ./google-chrome-stable_current_amd64.deb

# Install Python packages
pip install -r requirements.txt
