import gspread
from google.oauth2.service_account import Credentials
from src.config import GOOGLE_CREDENTIALS_JSON, SHEET_ID, SHEET_NAME
from src.models.schemas import ScanResult
from datetime import datetime

def get_sheet():
    """Получить лист Google Sheets"""
    creds = Credentials.from_service_account_info(
        eval(GOOGLE_CREDENTIALS_JSON),  # если передаётся строка JSON
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    return sheet

def append_to_sheet(result: ScanResult):
    """Добавить запись(и) в таблицу"""
    sheet = get_sheet()
    timestamp = datetime.now().isoformat()

    # Если есть и номера заказов, и штрихкоды – создаём строки для каждой пары (или комбинации)
    # Упростим: одна строка – все номера заказов и все штрихкоды в соответствующих колонках.
    # Но можно и детализировать: для каждого номера заказа – строка со всеми штрихкодами.
    # Следуя логике, что связка "заказ – штрихкод" может быть множественной, выберем вариант:
    # если есть номера заказов, то для каждого номера создаём строку, в колонке "штрихкод" пишем все найденные штрихкоды через запятую.
    # Если номеров нет – одна строка с пустым номером.

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