#!/usr/bin/env bash
set -o errexit
set -o nounset

echo "📦 Downloading precompiled Chromium..."

mkdir -p /tmp/chrome
cd /tmp/chrome

curl -sSL https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1193136/chrome-linux.zip -o chrome.zip
unzip -q chrome.zip
chmod +x chrome-linux/chrome

echo "/tmp/chrome/chrome-linux/chrome" > "$RENDER_PROJECT_ROOT/.chrome-bin"
