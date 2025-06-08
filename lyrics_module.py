#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Lyrics Extraction Module for Telegram Bot
- Extract lyrics from song name using free websites
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

def extract_lyrics_from_azlyrics(song_name: str) -> str:
    """
    Extract lyrics from AZLyrics.com
    
    Args:
        song_name: Name of the song (can include artist)
        
    Returns:
        Lyrics as text or error message
    """
    try:
        # Format the search query
        search_query = quote(song_name.lower().replace(' ', '+'))
        search_url = f"https://search.azlyrics.com/search.php?q={search_query}"
        
        # Send request to search page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        # Parse search results
        soup = BeautifulSoup(response.text, 'html.parser')
        song_results = soup.select('td.text-left a')
        
        if not song_results:
            return f"No lyrics found for '{song_name}'"
        
        # Get the first result URL
        lyrics_url = song_results[0]['href']
        
        # Get the lyrics page
        lyrics_response = requests.get(lyrics_url, headers=headers)
        lyrics_response.raise_for_status()
        
        # Parse lyrics page
        lyrics_soup = BeautifulSoup(lyrics_response.text, 'html.parser')
        
        # Find the lyrics div (AZLyrics has a specific structure)
        lyrics_div = lyrics_soup.find('div', class_=None, id=None, attrs={'style': None})
        
        if lyrics_div:
            # Extract the text and clean it up
            lyrics = lyrics_div.get_text().strip()
            # Remove any script or comment content
            lyrics = re.sub(r'<!--.*?-->', '', lyrics, flags=re.DOTALL)
            lyrics = re.sub(r'<script.*?>.*?</script>', '', lyrics, flags=re.DOTALL)
            return lyrics
        else:
            return f"Could not extract lyrics for '{song_name}'"
            
    except Exception as e:
        return f"Error extracting lyrics: {str(e)}"

def extract_lyrics_from_genius(song_name: str) -> str:
    """
    Extract lyrics from Genius.com as a fallback
    
    Args:
        song_name: Name of the song (can include artist)
        
    Returns:
        Lyrics as text or error message
    """
    try:
        # Format the search query
        search_query = quote(song_name.lower().replace(' ', '-'))
        search_url = f"https://genius.com/search?q={search_query}"
        
        # Send request to search page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        # Parse search results
        soup = BeautifulSoup(response.text, 'html.parser')
        song_results = soup.select('a.mini_card')
        
        if not song_results:
            return f"No lyrics found for '{song_name}' on Genius"
        
        # Get the first result URL
        lyrics_url = song_results[0]['href']
        
        # Get the lyrics page
        lyrics_response = requests.get(lyrics_url, headers=headers)
        lyrics_response.raise_for_status()
        
        # Parse lyrics page
        lyrics_soup = BeautifulSoup(lyrics_response.text, 'html.parser')
        
        # Find the lyrics div
        lyrics_div = lyrics_soup.select_one('div[class*="Lyrics__Container"]')
        
        if lyrics_div:
            # Extract the text and clean it up
            lyrics = lyrics_div.get_text(separator='\n').strip()
            return lyrics
        else:
            return f"Could not extract lyrics for '{song_name}' from Genius"
            
    except Exception as e:
        return f"Error extracting lyrics from Genius: {str(e)}"

def get_lyrics(song_name: str) -> str:
    """
    Get lyrics for a song by trying multiple sources
    
    Args:
        song_name: Name of the song (can include artist)
        
    Returns:
        Lyrics as text or error message
    """
    # Try AZLyrics first
    lyrics = extract_lyrics_from_azlyrics(song_name)
    
    # If AZLyrics fails, try Genius
    if "Error extracting lyrics" in lyrics or "No lyrics found" in lyrics or "Could not extract lyrics" in lyrics:
        lyrics = extract_lyrics_from_genius(song_name)
    
    return lyrics

