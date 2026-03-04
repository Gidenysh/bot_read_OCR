#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bot/ocr_service.py - OCR сервис"""

import asyncio
import easyocr
from loguru import logger
from bot.config import OCR_LANGS
from bot.utils import normalize_plate, validate_plate_format

class OCRService:
    def __init__(self):
        logger.info("Initializing OCR Engine...")
        try:
            # Убран параметр detail - не поддерживается в новых версиях
            self.reader = easyocr.Reader(OCR_LANGS, gpu=True)
            logger.info("OCR Engine ready.")
        except Exception as e:
            logger.error(f"Failed to initialize OCR: {e}")
            raise

    async def recognize_plate(self, image_bytes: bytes):
        """Распознавание номера с изображения"""
        try:
            results = await asyncio.to_thread(self.reader.readtext, image_bytes)
            
            best_candidate = None
            best_score = 0.0
            
            for result in results:
                # EasyOCR возвращает (bbox, text, confidence)
                if isinstance(result, (list, tuple)) and len(result) >= 2:
                    text = result[1]
                    confidence = result[2] if len(result) > 2 else 0.5
                else:
                    continue
                
                if not validate_plate_format(text):
                    continue
                
                normalized = normalize_plate(text)
                
                if confidence > best_score:
                    best_score = confidence
                    best_candidate = normalized
            
            return best_candidate
            
        except Exception as e:
            logger.error(f"OCR Error: {e}")
            return None