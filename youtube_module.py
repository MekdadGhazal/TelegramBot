#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YouTube Download Module for Telegram Bot
- Search for songs on YouTube
- Download songs from YouTube URLs
"""

import os
import yt_dlp
from typing import List, Dict, Any, Tuple

# Temporary directory for downloads
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

def search_youtube(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Search YouTube for a song and return a list of results.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        
    Returns:
        List of dictionaries with video information
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best',
        'noplaylist': True,
        'extract_flat': True,
        'default_search': 'ytsearch',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
        
    videos = []
    if 'entries' in search_results:
        for entry in search_results['entries']:
            videos.append({
                'id': entry.get('id', ''),
                'title': entry.get('title', 'Unknown Title'),
                'url': f"https://www.youtube.com/watch?v={entry.get('id', '')}",
                'duration': entry.get('duration', 0),
                'uploader': entry.get('uploader', 'Unknown Uploader'),
            })
    
    return videos

def download_youtube_audio(url: str) -> Tuple[str, str]:
    """
    Download audio from a YouTube URL.
    
    Args:
        url: YouTube URL
        
    Returns:
        Tuple of (file_path, title)
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(TEMP_DIR, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'Unknown Title')
        file_path = os.path.join(TEMP_DIR, f"{title}.mp3")
        
    return file_path, title

