import asyncio
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from loguru import logger
from bot.config import SHEET_ID, SERVICE_ACCOUNT_FILE, DB_PLATE_COLUMN, DB_DATE_COLUMN
from bot.utils import normalize_plate

class SheetsService:
    def __init__(self):
        self.scope = ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_key(SHEET_ID).sheet1

    async def get_today_plates_set(self):
        try:
            all_records = await asyncio.to_thread(self.sheet.get_all_values)
            today_str = datetime.now().strftime("%d.%m.%Y")
            valid_plates = set()
            for row in all_records[1:]:
                if len(row) < max(DB_PLATE_COLUMN, DB_DATE_COLUMN):
                    continue
                plate_raw = row[DB_PLATE_COLUMN - 1]
                date_raw = row[DB_DATE_COLUMN - 1]
                if date_raw != today_str:
                    continue
                normalized_plate = normalize_plate(plate_raw)
                if normalized_plate:
                    valid_plates.add(normalized_plate)
            logger.info(f"Loaded {len(valid_plates)} plates from DB")
            return valid_plates
        except Exception as e:
            logger.error(f"Sheets API Error: {e}")
            return set()

    async def is_plate_allowed(self, plate, today_plates):
        return plate in today_plates
