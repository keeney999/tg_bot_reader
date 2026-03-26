# Telegram бот для распознавания штрихкодов и номеров заказов

Бот принимает фото, распознаёт штрихкоды и номера заказов (формат `12345678-9012-3`) и записывает результат в Google Таблицу.

## Технологии
- Python 3.12+
- aiogram 3.x
- OpenCV, pyzbar, pytesseract
- Google Sheets API (gspread)

## Установка

1. Клонировать репозиторий
2. Установить Poetry: `pip install poetry`
3. Установить зависимости:  
   ```bash
   poetry install
   ```
4. Установить системные зависимости:
   - **Windows**:  
     - Скачать и установить Tesseract OCR с [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)  
     - Добавить `tesseract` в PATH
   - **Linux/macOS**:  
     ```bash
     sudo apt install tesseract-ocr libzbar0   # Linux
     brew install tesseract zbar               # macOS
     ```
5. Скопировать `.env.example` в `.env` и заполнить переменные (токен бота, JSON-ключ Google, ID таблицы)
6. Запустить бота:  
   ```bash
   poetry run python src/main.py
   ```

## Использование

1. Добавить бота в группу Telegram, дать права на чтение сообщений
2. В группе нажать `/start`, затем `/scan` (или кнопку «Отсканировать»)
3. Отправить фото с товаром
4. Бот вернёт распознанные штрихкоды и номера заказов и запишет их в Google Таблицу
