#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for the Telegram bot
This script checks if all required modules are installed and if the bot can be started
"""

import os
import sys
import importlib.util

def check_module(module_name):
    """Check if a module is installed."""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return False
    return True

def main():
    """Run tests for the Telegram bot."""
    print("Testing Telegram bot setup...")
    
    # Check required modules
    required_modules = [
        "telegram", 
        "qrcode", 
        "cv2", 
        "yt_dlp", 
        "requests", 
        "bs4", 
        "PIL", 
        "dotenv"
    ]
    
    missing_modules = []
    for module in required_modules:
        if not check_module(module):
            missing_modules.append(module)
    
    if missing_modules:
        print("Error: The following required modules are missing:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nPlease install them using:")
        print("pip install python-telegram-bot qrcode[pil] opencv-python-headless yt-dlp requests beautifulsoup4 pillow python-dotenv")
        return False
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("Warning: .env file not found. Creating a template...")
        with open(".env", "w") as f:
            f.write("# Telegram Bot API Token (get from BotFather)\n")
            f.write("TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here\n")
        print("Please edit the .env file and add your Telegram Bot Token.")
        return False
    
    # Check if token is set
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        print("Error: Telegram Bot Token not set in .env file.")
        print("Please edit the .env file and add your Telegram Bot Token.")
        return False
    
    # Check if temp directory exists
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
    if not os.path.exists(temp_dir):
        print(f"Creating temp directory: {temp_dir}")
        os.makedirs(temp_dir)
    
    # Check if all required files exist
    required_files = [
        "bot.py",
        "qr_module.py",
        "youtube_module.py",
        "lyrics_module.py",
        "image_module.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Error: The following required files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("All checks passed! The bot is ready to run.")
    print("Run the bot using: python bot.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

