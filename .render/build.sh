#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Download Chromium manually to a writable location
mkdir -p /opt/render/project/src/chrome
cd /opt/render/project/src/chrome

# Get a recent portable Chromium build (not Google Chrome)
wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1238505/chrome-linux.zip
unzip chrome-linux.zip
chmod +x chrome-linux/chrome

# Save path to a file so Python can read it
echo "/opt/render/project/src/chrome/chrome-linux/chrome" > /opt/render/project/src/.chrome-bin
