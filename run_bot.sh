#!/bin/bash

# Run the test script first
echo "Testing bot setup..."
python3 test.py

# Check if the test was successful
if [ $? -ne 0 ]; then
    echo "Setup test failed. Please fix the issues before running the bot."
    exit 1
fi

# Run the bot
echo "Starting the Telegram bot..."
python3 bot.py

