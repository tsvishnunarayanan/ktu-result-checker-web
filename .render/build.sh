#!/usr/bin/env bash
set -o errexit

echo "👉 Installing Chromium..."
apt-get update && apt-get install -y chromium-browser

echo "👉 Locating Chrome binary..."
which chromium-browser > .chrome-bin

echo "✅ Chrome path saved to .chrome-bin"
