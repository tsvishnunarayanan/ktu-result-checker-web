#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create directories
mkdir -p /opt/render/project/src/chrome
mkdir -p /opt/render/project/src/chromedriver

# Download Chromium (version 1142525 = Chrome 115.0.5764.0)
cd /opt/render/project/src/chrome
wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1142525/chrome-linux.zip
unzip chrome-linux.zip
chmod +x chrome-linux/chrome

# Save Chromium path
echo "/opt/render/project/src/chrome/chrome-linux/chrome" > /opt/render/project/src/.chrome-bin

# Download matching Chromedriver (version 1142525)
cd /opt/render/project/src/chromedriver
wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1142525/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver

# Save Chromedriver path
echo "/opt/render/project/src/chromedriver/chromedriver-linux64/chromedriver" > /opt/render/project/src/.chromedriver-bin
