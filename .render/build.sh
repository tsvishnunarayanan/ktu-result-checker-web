#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create directory for Chromium if not exists
mkdir -p /opt/render/project/src/chrome
cd /opt/render/project/src/chrome

# ✅ Use a known working Chromium version
CHROMIUM_URL="https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1142525/chrome-linux.zip"

# Clean any previous downloads (optional safety)
rm -rf chrome-linux*
wget $CHROMIUM_URL -O chrome-linux.zip

# Unzip and make the Chrome binary executable
unzip chrome-linux.zip
chmod +x chrome-linux/chrome

# Save binary path to .chrome-bin for use in Python
echo "/opt/render/project/src/chrome/chrome-linux/chrome" > /opt/render/project/src/.chrome-bin
