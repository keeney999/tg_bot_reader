import cv2
import re
from pyzbar.pyzbar import decode
import pytesseract
from src.services.image_utils import preprocess_for_ocr

def extract_barcodes(image: np.ndarray) -> list[str]:
    """Извлечь все штрихкоды"""
    barcodes = decode(image)
    return [barcode.data.decode('utf-8') for barcode in barcodes if barcode.data]

def extract_order_numbers(image: np.ndarray) -> list[str]:
    """Найти номера заказов в формате 12345678-9012-3"""
    # Предобработка для OCR
    processed = preprocess_for_ocr(image)
    text = pytesseract.image_to_string(processed, lang='eng', config='--psm 6')
    pattern = r'\b\d{8}-\d{4}-\d\b'
    matches = re.findall(pattern, text)
    return list(set(matches))