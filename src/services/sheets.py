import json
import gspread
from google.oauth2.service_account import Credentials
from src.config import GOOGLE_CREDENTIALS_JSON, SHEET_ID, SHEET_NAME
from src.models.schemas import ScanResult
from datetime import datetime

def get_sheet():
    # Преобразуем JSON-строку в словарь
    creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    return sheet

def append_to_sheet(result: ScanResult):
    sheet = get_sheet()
    timestamp = datetime.now().isoformat()

    if result.order_numbers:
        for order in result.order_numbers:
            row = [
                timestamp,
                result.user_id,
                result.username,
                order,
                ", ".join(result.barcodes) if result.barcodes else "",
                result.message_link
            ]
            sheet.append_row(row, value_input_option='USER_ENTERED')
    else:
        row = [
            timestamp,
            result.user_id,
            result.username,
            "",
            ", ".join(result.barcodes) if result.barcodes else "",
            result.message_link
        ]
        sheet.append_row(row, value_input_option='USER_ENTERED')