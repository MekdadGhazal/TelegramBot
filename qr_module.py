#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QR Code Module for Telegram Bot
- Generate QR codes from text
- Read QR codes from images
"""

import os
import qrcode
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def generate_qr_code(text: str) -> BytesIO:
    """Generate a QR code from text and return it as a BytesIO object."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image to a BytesIO object
    bio = BytesIO()
    bio.name = 'qrcode.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    
    return bio

def read_qr_code(image_data: bytes) -> str:
    """Read a QR code from an image and return the decoded text."""
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    
    # Decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Initialize QR code detector
    detector = cv2.QRCodeDetector()
    
    # Detect and decode
    data, bbox, _ = detector.detectAndDecode(img)
    
    if bbox is not None:
        return data
    else:
        raise ValueError("No QR code found in the image")

