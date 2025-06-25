#!/bin/bash

set -e

# Download Chrome
wget -q https://storage.googleapis.com/chrome-for-testing-public/118.0.5993.70/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
chmod +x chrome-linux64/chrome

# Download matching chromedriver
wget -q https://storage.googleapis.com/chrome-for-testing-public/118.0.5993.70/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver

# Save path for use in bot.py
echo "chrome-linux64/chrome" > .chrome-bin
