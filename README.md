# Multi-functional Telegram Bot

A versatile Telegram bot that can perform multiple tasks:

1. Read QR codes from images
2. Generate QR codes from text
3. Download songs from YouTube (via URL or search)
4. Extract lyrics for songs
5. Enhance image quality

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- A Telegram account
- A Telegram Bot Token (obtained from BotFather)

### Installation

1. Clone this repository or download the code
2. Install the required dependencies using the requirements.txt file:

```bash
pip install -r requirements.txt
```

3. Configure the bot:
   - Edit the `.env` file and add your Telegram Bot Token:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   ```

### Getting a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather and send the command `/newbot`
3. Follow the instructions to create a new bot
4. Once created, BotFather will provide you with a token
5. Copy this token to the `.env` file

### Running the Bot

You can run the bot in two ways:

1. Using the provided shell script (recommended):

```bash
./run_bot.sh
```

This script will first check if your environment is set up correctly and then start the bot.

2. Running the Python script directly:

```bash
python bot.py
```

The bot will start and be available on Telegram.

## Usage Instructions

### Starting the Bot

1. Open Telegram and search for your bot by its username
2. Start a chat with the bot
3. Send the command `/start` to see the available commands

### Available Commands

- `/start` - Start the bot and see available commands
- `/help` - Show help message with available commands
- `/qrgen` - Generate a QR code from text
- `/qrread` - Read a QR code from an image
- `/download` - Download a song from YouTube
- `/lyrics` - Get lyrics for a song
- `/enhance` - Enhance an image quality
- `/cancel` - Cancel the current operation

### QR Code Generation

1. Send the command `/qrgen`
2. The bot will ask you to send the text you want to convert to a QR code
3. Send your text
4. The bot will generate and send you a QR code image

### QR Code Reading

1. Send the command `/qrread`
2. The bot will ask you to send an image containing a QR code
3. Send an image with a QR code
4. The bot will read and send you the content of the QR code

### YouTube Song Download

1. Send the command `/download`
2. The bot will ask you to send a YouTube URL or a song name
3. If you send a URL, the bot will download the song directly
4. If you send a song name, the bot will search YouTube and show you up to 3 results
5. Select a song from the results by clicking on it
6. The bot will download and send you the song as an audio file

### Song Lyrics Extraction

1. Send the command `/lyrics`
2. The bot will ask you to send the name of the song you want lyrics for
3. Send the song name (you can include the artist name for better results)
4. The bot will search for and send you the lyrics

### Image Enhancement

1. Send the command `/enhance`
2. The bot will ask you to send an image to enhance
3. Send an image
4. The bot will enhance the image quality and send you the enhanced version

## Project Structure

- `bot.py` - Main bot file with command handlers and conversation logic
- `qr_module.py` - QR code generation and reading functionality
- `youtube_module.py` - YouTube search and download functionality
- `lyrics_module.py` - Song lyrics extraction functionality
- `image_module.py` - Image enhancement functionality
- `test.py` - Test script to verify bot setup
- `run_bot.sh` - Shell script to run the bot with setup checks
- `requirements.txt` - Python dependencies list
- `.env` - Environment variables configuration
- `temp/` - Temporary directory for downloaded files

## Troubleshooting

- If the bot doesn't respond, make sure the bot is running and your Telegram Bot Token is correct
- If you encounter errors with YouTube downloads, make sure yt-dlp is up to date
- For QR code reading issues, ensure the QR code is clearly visible in the image
- For image enhancement, larger images may take longer to process

## License

This project is open source and available under the MIT License.

## Acknowledgements

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [qrcode](https://github.com/lincolnloop/python-qrcode) - QR code generation
- [opencv-python](https://github.com/opencv/opencv-python) - QR code reading
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloading
- [Pillow](https://github.com/python-pillow/Pillow) - Image processing

