#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Make directory
mkdir -p /opt/render/project/src/chrome
cd /opt/render/project/src/chrome

# Fetch the latest known good version for Linux
CFT_JSON=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json)

# Extract download URLs for Linux
CHROME_URL=$(echo "$CFT_JSON" | jq -r '.channels.Stable.downloads.chrome[] | select(.platform=="linux64") | .url')
DRIVER_URL=$(echo "$CFT_JSON" | jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url')

# Download and unzip
wget -O chrome-linux64.zip "$CHROME_URL"
wget -O chromedriver-linux64.zip "$DRIVER_URL"

unzip chrome-linux64.zip
unzip chromedriver-linux64.zip

# Make them executable
chmod +x chrome-linux64/chrome
chmod +x chromedriver-linux64/chromedriver

# Save paths for Python
echo "/opt/render/project/src/chrome/chrome-linux64/chrome" > /opt/render/project/src/.chrome-bin
echo "/opt/render/project/src/chrome/chromedriver-linux64/chromedriver" > /opt/render/project/src/.chromedriver-bin
