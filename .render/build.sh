#!/usr/bin/env bash

# Install dependencies and Chrome
apt-get update && apt-get install -y wget curl unzip gnupg
mkdir -p .local/chrome
cd .local/chrome

# Download and install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb || true

# Get chrome binary path
CHROME_PATH=$(which google-chrome || which google-chrome-stable)

# Write the path to a known file that Python reads
cd ../../
echo "$CHROME_PATH" > .chrome-bin
