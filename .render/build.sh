#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Set up Chromium + Chromedriver (1148743 is known to match Chrome 115)
mkdir -p /opt/render/project/src/chrome
cd /opt/render/project/src/chrome

# Download Chromium
wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1148743/chrome-linux.zip
unzip chrome-linux.zip
chmod +x chrome-linux/chrome
echo "/opt/render/project/src/chrome/chrome-linux/chrome" > /opt/render/project/src/.chrome-bin

# Download Chromedriver
wget https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1148743/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver
echo "/opt/render/project/src/chrome/chromedriver-linux64/chromedriver" > /opt/render/project/src/.chromedriver-bin
