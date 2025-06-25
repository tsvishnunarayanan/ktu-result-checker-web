#!/usr/bin/env bash
set -o errexit
set -o nounset

echo "📦 Downloading precompiled Chromium..."

# Set download directory inside Render project root
CHROME_DIR="$RENDER_PROJECT_ROOT/.chrome"
mkdir -p "$CHROME_DIR"
cd "$CHROME_DIR"

# Use known working build of Chromium (this URL is stable)
curl -sSL https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1193136/chrome-linux.zip -o chrome.zip
unzip -q chrome.zip

# Save the path to the Chrome binary
chmod +x chrome-linux/chrome
echo "$CHROME_DIR/chrome-linux/chrome" > "$RENDER_PROJECT_ROOT/.chrome-bin"

echo "✅ Chrome downloaded to $CHROME_DIR"
