import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")
ADMIN_LOG_CHAT_ID = os.getenv("ADMIN_LOG_CHAT_ID")
SHEET_ID = os.getenv("SHEET_ID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "credentials.json")
DB_PLATE_COLUMN = int(os.getenv("DB_PLATE_COLUMN", "1"))
DB_DATE_COLUMN = int(os.getenv("DB_DATE_COLUMN", "2"))
OCR_LANGS = os.getenv("OCR_LANGS", "ru,en").split(",")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger.remove()
logger.add(LOG_DIR / "bot.log", rotation="10 MB", retention="7 days", level=LOG_LEVEL)
logger.add(LOG_DIR / "error.log", rotation="10 MB", retention="7 days", level="ERROR")
