import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
SHEET_ID = os.getenv("SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "Лист1")

# ID группы и темы (для фильтрации, если нужно)
GROUP_ID = int(os.getenv("GROUP_ID", "0"))
TOPIC_ID = int(os.getenv("TOPIC_ID", "0"))

# Можно также ограничить бота только этой группой/темой
ONLY_GROUP = bool(GROUP_ID)
ONLY_TOPIC = bool(TOPIC_ID)