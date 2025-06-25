#!/usr/bin/env bash

# Install dependencies
apt-get update
apt-get install -y wget gnupg2

# Download and install stable Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb || apt install -f -y

# Save path to chrome for later use
which google-chrome > /opt/render/project/src/.chrome-bin

# Install Python dependencies
pip install -r requirements.txt
