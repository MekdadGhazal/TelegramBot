#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image Enhancement Module for Telegram Bot
- Enhance image quality
"""

import os
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from typing import Tuple

def enhance_image(image_data: bytes) -> BytesIO:
    """
    Enhance an image by improving sharpness, contrast, and color.
    
    Args:
        image_data: Image data as bytes
        
    Returns:
        Enhanced image as BytesIO object
    """
    # Open the image from bytes
    img = Image.open(BytesIO(image_data))
    
    # Apply a series of enhancements
    
    # 1. Sharpen the image
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)  # Increase sharpness by 50%
    
    # 2. Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)  # Increase contrast by 30%
    
    # 3. Enhance color
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.2)  # Increase color saturation by 20%
    
    # 4. Enhance brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)  # Increase brightness by 10%
    
    # 5. Apply a subtle unsharp mask filter for additional sharpness
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # Save the enhanced image to a BytesIO object
    bio = BytesIO()
    bio.name = 'enhanced_image.png'
    
    # Preserve original format if possible
    original_format = img.format if img.format else 'PNG'
    img.save(bio, format=original_format)
    bio.seek(0)
    
    return bio

def upscale_image(image_data: bytes, scale_factor: float = 2.0) -> BytesIO:
    """
    Upscale an image by a given factor.
    
    Args:
        image_data: Image data as bytes
        scale_factor: Factor by which to upscale the image
        
    Returns:
        Upscaled image as BytesIO object
    """
    # Open the image from bytes
    img = Image.open(BytesIO(image_data))
    
    # Get original dimensions
    width, height = img.size
    
    # Calculate new dimensions
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Resize the image with high-quality resampling
    img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # Apply a subtle sharpening after resize
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.3)
    
    # Save the upscaled image to a BytesIO object
    bio = BytesIO()
    bio.name = 'upscaled_image.png'
    
    # Preserve original format if possible
    original_format = img.format if img.format else 'PNG'
    img.save(bio, format=original_format)
    bio.seek(0)
    
    return bio

def process_image(image_data: bytes, enhance: bool = True, upscale: bool = True, scale_factor: float = 1.5) -> BytesIO:
    """
    Process an image with enhancement and optional upscaling.
    
    Args:
        image_data: Image data as bytes
        enhance: Whether to enhance the image
        upscale: Whether to upscale the image
        scale_factor: Factor by which to upscale the image
        
    Returns:
        Processed image as BytesIO object
    """
    # Open the image from bytes
    img = Image.open(BytesIO(image_data))
    
    if enhance:
        # Apply enhancements
        # 1. Sharpen the image
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        
        # 2. Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.3)
        
        # 3. Enhance color
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.2)
        
        # 4. Enhance brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
        # 5. Apply a subtle unsharp mask filter
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    if upscale:
        # Get original dimensions
        width, height = img.size
        
        # Calculate new dimensions
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        # Resize the image with high-quality resampling
        img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Apply a subtle sharpening after resize
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)
    
    # Save the processed image to a BytesIO object
    bio = BytesIO()
    bio.name = 'processed_image.png'
    
    # Preserve original format if possible
    original_format = img.format if img.format else 'PNG'
    img.save(bio, format=original_format)
    bio.seek(0)
    
    return bio

