#!/bin/bash

# --- Twitch Bot Runner ---
# This script activates the virtual environment and runs the Twitch bot.
# Logs output to bot.log for easy debugging.

cd "$(dirname "$0")"  # Always go to this script's directory
source .venv/bin/activate

# Run the bot and log both stdout and stderr to a file
echo "[$(date)] Starting Twitch bot..." | tee -a bot.log
python main.py >> bot.log 2>&1

# If the bot exits, log the time
echo "[$(date)] Bot stopped." | tee -a bot.log
