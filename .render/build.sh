#!/usr/bin/env bash

# Install Chromium on Debian/Ubuntu Render environment
apt-get update && \
apt-get install -y wget gnupg ca-certificates && \
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
apt-get update && \
apt-get install -y google-chrome-stable

# Save Chrome path for your Python app
which google-chrome > .chromium-path

# Install Python dependencies
pip install -r requirements.txt
