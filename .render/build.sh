#!/bin/bash

echo "👉 Installing Chromium"

mkdir -p .chrome
curl -SL https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.57/linux64/chrome-linux64.zip -o chrome-linux.zip
unzip chrome-linux.zip -d .chrome
chmod +x .chrome/chrome-linux64/chrome

# Save the binary path
echo "$(pwd)/.chrome/chrome-linux64/chrome" > .chrome-bin

echo "✅ Chromium installed"
