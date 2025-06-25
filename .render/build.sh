#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Fetch latest matching Chrome + ChromeDriver (Chrome for Testing)
mkdir -p /opt/render/project/src/chrome
cd /opt/render/project/src/chrome

# Fetch version info
CFT_JSON=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json)
CHROME_URL=$(echo "$CFT_JSON" | grep -oP 'https://.*?chrome-linux64.zip' | head -1)
DRIVER_URL=$(echo "$CFT_JSON" | grep -oP 'https://.*?chromedriver-linux64.zip' | head -1)

# Download both
wget -O chrome-linux64.zip "$CHROME_URL"
wget -O chromedriver-linux64.zip "$DRIVER_URL"

# Extract
unzip chrome-linux64.zip
unzip chromedriver-linux64.zip

# Make executables
chmod +x chrome-linux64/chrome
chmod +x chromedriver-linux64/chromedriver

# Save paths for Python to use
echo "/opt/render/project/src/chrome/chrome-linux64/chrome" > /opt/render/project/src/.chrome-bin
echo "/opt/render/project/src/chrome/chromedriver-linux64/chromedriver" > /opt/render/project/src/.chromedriver-bin
