# delete_webhook.py
import asyncio
from aiogram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def delete_webhook():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.delete_webhook()
        print("✅ Webhook успешно удалён!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(delete_webhook())