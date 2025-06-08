#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi-functional Telegram Bot
Features:
- QR code reading and generation
- YouTube song download
- Song lyrics extraction
- Image enhancement
"""

import os
import logging
import tempfile
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)

# Import custom modules
from qr_module import generate_qr_code, read_qr_code
from youtube_module import search_youtube, download_youtube_audio
from lyrics_module import get_lyrics
from image_module import process_image
from dollar import get_rates_from_sptoday


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get the bot token from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Create temp directory if it doesn't exist
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# Define conversation states
(
    WAITING_FOR_QR_TEXT,
    WAITING_FOR_QR_IMAGE,
    WAITING_FOR_SONG_NAME,
    WAITING_FOR_SONG_URL,
    WAITING_FOR_LYRICS_NAME,
    WAITING_FOR_IMAGE,
) = range(6)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm your multi-functional bot.\n\n"
        "Here's what I can do:\n"
        "/qrgen - Generate a QR code from text\n"
        "/qrread - Read a QR code from an image\n"
        "/download - Download a song from YouTube\n"
        "/lyrics - Get lyrics for a song\n"
        "/enhance - Enhance an image quality\n"
        "/dollar - Dollar Price in Syria\n"
        "/help - Show this help message"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Here's what I can do:\n"
        "/qrgen - Generate a QR code from text\n"
        "/qrread - Read a QR code from an image\n"
        "/download - Download a song from YouTube\n"
        "/lyrics - Get lyrics for a song\n"
        "/enhance - Enhance an image quality\n"
        "/dollar - Dollar Price in Syria\n"
        "/help - Show this help message"
    )

# QR Code Generation - Start conversation
async def qr_gen_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the QR code generation conversation."""
    await update.message.reply_text(
        "Please send me the text you want to convert to a QR code:"
    )
    return WAITING_FOR_QR_TEXT

# QR Code Generation - Process text
async def qr_gen_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Generate QR code from text."""
    text = update.message.text
    await update.message.reply_text(f"Generating QR code for: {text}")
    
    try:
        # Generate QR code
        qr_image = generate_qr_code(text)
        
        # Send the QR code image
        await update.message.reply_photo(
            photo=qr_image,
            caption=f"QR code for: {text}"
        )
        await update.message.reply_text("QR code generated successfully!")
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        await update.message.reply_text(f"Error generating QR code: {e}")
    
    return ConversationHandler.END

# QR Code Reading - Start conversation
async def qr_read_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the QR code reading conversation."""
    await update.message.reply_text(
        "Please send me an image containing a QR code to read:"
    )
    return WAITING_FOR_QR_IMAGE

# QR Code Reading - Process image
async def qr_read_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Read QR code from image."""
    # Get the photo with the highest resolution
    photo = update.message.photo[-1]
    
    try:
        # Download the photo
        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()
        
        # Read QR code
        qr_text = read_qr_code(image_bytes)
        
        # Send the decoded text
        await update.message.reply_text(f"QR code content: {qr_text}")
    except Exception as e:
        logger.error(f"Error reading QR code: {e}")
        await update.message.reply_text(f"Error reading QR code: {e}")
    
    return ConversationHandler.END

# YouTube Download - Start conversation
async def download_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the YouTube download conversation."""
    await update.message.reply_text(
        "Please send me a YouTube URL or a song name to download:"
    )
    return WAITING_FOR_SONG_NAME

# YouTube Download - Process song name or URL
async def download_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process song name or URL for download."""
    user_input = update.message.text
    
    # Check if input is a URL
    if user_input.startswith("http://") or user_input.startswith("https://"):
        context.user_data["youtube_url"] = user_input
        await update.message.reply_text(f"Downloading song from URL: {user_input}")
        
        try:
            # Download the song
            file_path, title = download_youtube_audio(user_input)
            
            # Send the audio file
            await update.message.reply_audio(
                audio=open(file_path, "rb"),
                title=title,
                caption=f"Downloaded: {title}"
            )
            
            # Clean up
            os.remove(file_path)
            
        except Exception as e:
            logger.error(f"Error downloading song: {e}")
            await update.message.reply_text(f"Error downloading song: {e}")
        
        return ConversationHandler.END
    else:
        # Search for the song
        try:
            await update.message.reply_text(f"Searching for: {user_input}")
            search_results = search_youtube(user_input)
            
            if not search_results:
                await update.message.reply_text(f"No results found for: {user_input}")
                return ConversationHandler.END
            
            # Store search results in context
            context.user_data["search_results"] = search_results
            
            # Create inline keyboard with search results
            keyboard = []
            for i, result in enumerate(search_results):
                keyboard.append([
                    InlineKeyboardButton(
                        f"{i+1}. {result['title']} ({result['uploader']})",
                        callback_data=f"download_{i}"
                    )
                ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "Please select a song to download:",
                reply_markup=reply_markup
            )
            
            return WAITING_FOR_SONG_URL
            
        except Exception as e:
            logger.error(f"Error searching for song: {e}")
            await update.message.reply_text(f"Error searching for song: {e}")
            return ConversationHandler.END

# YouTube Download - Process song selection
async def download_song_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process song selection from search results."""
    query = update.callback_query
    await query.answer()
    
    # Get the selected song index
    data = query.data
    index = int(data.split("_")[1])
    
    # Get the selected song URL
    search_results = context.user_data.get("search_results", [])
    if not search_results or index >= len(search_results):
        await query.edit_message_text("Invalid selection or search results expired.")
        return ConversationHandler.END
    
    selected_song = search_results[index]
    url = selected_song["url"]
    
    await query.edit_message_text(f"Downloading: {selected_song['title']}")
    
    try:
        # Download the song
        file_path, title = download_youtube_audio(url)
        
        # Send the audio file
        await context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=open(file_path, "rb"),
            title=title,
            caption=f"Downloaded: {title}"
        )
        
        # Clean up
        os.remove(file_path)
        
    except Exception as e:
        logger.error(f"Error downloading song: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Error downloading song: {e}"
        )
    
    return ConversationHandler.END

# Lyrics Extraction - Start conversation
async def lyrics_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the lyrics extraction conversation."""
    await update.message.reply_text(
        "Please send me the name of the song you want lyrics for:"
    )
    return WAITING_FOR_LYRICS_NAME

# Lyrics Extraction - Process song name
async def lyrics_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Extract lyrics for a song."""
    song_name = update.message.text
    await update.message.reply_text(f"Searching for lyrics of: {song_name}")
    
    try:
        # Get lyrics
        lyrics = get_lyrics(song_name)
        
        # Check if lyrics are too long for a single message
        if len(lyrics) > 4000:
            # Split lyrics into chunks
            chunks = [lyrics[i:i+4000] for i in range(0, len(lyrics), 4000)]
            
            for i, chunk in enumerate(chunks):
                await update.message.reply_text(
                    f"Lyrics for '{song_name}' (Part {i+1}/{len(chunks)}):\n\n{chunk}"
                )
        else:
            await update.message.reply_text(
                f"Lyrics for '{song_name}':\n\n{lyrics}"
            )
            
    except Exception as e:
        logger.error(f"Error extracting lyrics: {e}")
        await update.message.reply_text(f"Error extracting lyrics: {e}")
    
    return ConversationHandler.END

# Image Enhancement - Start conversation
async def enhance_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the image enhancement conversation."""
    await update.message.reply_text(
        "Please send me an image to enhance:"
    )
    return WAITING_FOR_IMAGE

# Image Enhancement - Process image
async def enhance_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Enhance an image."""
    # Get the photo with the highest resolution
    photo = update.message.photo[-1]
    
    try:
        # Download the photo
        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()
        
        await update.message.reply_text("Enhancing image... This may take a moment.")
        
        # Process the image
        enhanced_image = process_image(image_bytes, enhance=True, upscale=True, scale_factor=1.5)
        
        # Send the enhanced image
        await update.message.reply_photo(
            photo=enhanced_image,
            caption="Enhanced image"
        )
        
    except Exception as e:
        logger.error(f"Error enhancing image: {e}")
        await update.message.reply_text(f"Error enhancing image: {e}")
    
    return ConversationHandler.END


async def dollar_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetch and send the dollar exchange rate."""
    try:
        rates = get_rates_from_sptoday()
        # await update.message.reply_text(rates)
        await update.message.reply_text(get_rates_from_sptoday())

    except Exception as e:
        logger.error(f"Error fetching dollar rate: {e}")
        await update.message.reply_text("Failed to fetch dollar rates. Please try again later.")
        



# Cancel conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the current conversation."""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to the user."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text("Sorry, an error occurred. Please try again later.")
    except:
        pass

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # QR Code Generation conversation handler
    qr_gen_handler = ConversationHandler(
        entry_points=[CommandHandler("qrgen", qr_gen_start)],
        states={
            WAITING_FOR_QR_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, qr_gen_text)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(qr_gen_handler)
    
    # QR Code Reading conversation handler
    qr_read_handler = ConversationHandler(
        entry_points=[CommandHandler("qrread", qr_read_start)],
        states={
            WAITING_FOR_QR_IMAGE: [MessageHandler(filters.PHOTO, qr_read_image)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(qr_read_handler)
    
    # YouTube Download conversation handler
    download_handler = ConversationHandler(
        entry_points=[CommandHandler("download", download_start)],
        states={
            WAITING_FOR_SONG_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, download_song)],
            WAITING_FOR_SONG_URL: [CallbackQueryHandler(download_song_selection, pattern=r"^download_\d+$")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(download_handler)
    
    # Lyrics Extraction conversation handler
    lyrics_handler = ConversationHandler(
        entry_points=[CommandHandler("lyrics", lyrics_start)],
        states={
            WAITING_FOR_LYRICS_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, lyrics_song)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(lyrics_handler)
    
    # Image Enhancement conversation handler
    enhance_handler = ConversationHandler(
        entry_points=[CommandHandler("enhance", enhance_start)],
        states={
            WAITING_FOR_IMAGE: [MessageHandler(filters.PHOTO, enhance_image)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(enhance_handler)


    # Dollar rate handler (simple command, no conversation needed)
    application.add_handler(CommandHandler("dollar", dollar_start))

    
    # Add error handler
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

