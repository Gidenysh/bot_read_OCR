#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bot/main.py - Точка входа"""

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import datetime
from loguru import logger

from bot.config import BOT_TOKEN, TARGET_CHAT_ID, ADMIN_LOG_CHAT_ID
from bot.ocr_service import OCRService
from bot.sheets_service import SheetsService

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ocr = OCRService()
sheets = SheetsService()

async def scan_history():
    """Сканирование истории чата"""
    logger.info("Запуск сканирования...")
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    db_plates = await sheets.get_today_plates_set()
    messages = await bot.get_chat_history(TARGET_CHAT_ID, limit=100)
    
    alerts_count = 0
    logs_count = 0
    
    for msg in messages:
        if msg.date < start_of_day:
            break
        
        if msg.photo:
            photo = msg.photo[-1]
            file = await bot.download(photo)
            image_bytes = file.read()
            
            plate = await ocr.recognize_plate(image_bytes)
            
            if plate:
                if not await sheets.is_plate_allowed(plate, db_plates):
                    message_text = "⚠️ Номер не найден в базе\n"
                    message_text += f"🚗 <code>{plate}</code>\n"
                    message_text += f"🔗 {msg.link}"
                    
                    await bot.send_message(
                        TARGET_CHAT_ID,
                        message_text,
                        parse_mode="HTML"
                    )
                    alerts_count += 1
            else:
                log_text = "🔍 Требуется ручная проверка\n"
                log_text += f"🔗 {msg.link}"
                
                await bot.send_message(
                    ADMIN_LOG_CHAT_ID,
                    log_text
                )
                logs_count += 1
            
            file.close()
    
    logger.info(f"Завершено. Алерты: {alerts_count}, Логи: {logs_count}")

@dp.message(Command("check"))
async def cmd_check(message: types.Message):
    """Обработчик команды /check"""
    await message.answer("🔄 Запуск сканирования...")
    try:
        await scan_history()
        await message.answer("✅ Завершено.")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("❌ Ошибка.")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer("👋 Используйте /check для сканирования.")

async def main():
    """Точка входа"""
    logger.info("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())