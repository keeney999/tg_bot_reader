import cv2
import numpy as np
import re
import pytesseract
from src.services.image_utils import preprocess_for_ocr
from src.utils.logger import logger

def extract_barcodes(image: np.ndarray) -> list[str]:
    codes = []
    # 1. QR-коды (всегда работают)
    qr = cv2.QRCodeDetector()
    ret_qr, decoded_info_qr, _, _ = qr.detectAndDecodeMulti(image)
    if ret_qr and decoded_info_qr:
        codes.extend(decoded_info_qr)
        logger.info(f"QR codes found: {decoded_info_qr}")

    # 2. 1D штрихкоды (EAN, Code128 и др.)
    try:
        barcode = cv2.barcode_BarcodeDetector()
        res = barcode.detectAndDecode(image)
        # Проверяем, сколько значений вернулось
        if isinstance(res, tuple):
            if len(res) == 4:
                ret_bc, decoded_info_bc, _, _ = res
            elif len(res) == 3:
                ret_bc, decoded_info_bc, _ = res
            else:
                ret_bc, decoded_info_bc = False, []
        else:
            ret_bc, decoded_info_bc = False, []

        if ret_bc and decoded_info_bc:
            codes.extend(decoded_info_bc)
            logger.info(f"1D barcodes found: {decoded_info_bc}")
    except Exception as e:
        logger.warning(f"Barcode detector failed: {e}. Try installing opencv-contrib-python.")

    # Убираем дубли и пустые строки
    codes = [c for c in codes if c]
    codes = list(set(codes))
    if not codes:
        logger.info("No barcodes found")
    return codes

def extract_order_numbers(image: np.ndarray) -> list[str]:
    processed = preprocess_for_ocr(image)
    text = pytesseract.image_to_string(processed, lang='eng', config='--psm 6')
    logger.info(f"OCR text: {text}")

    # Паттерн по ТЗ: 8 цифр - 4 цифры - 1 цифра
    pattern_strict = r'\b\d{8}-\d{4}-\d\b'
    # Расширенный: 5-15 цифр - 4-6 цифр - 1-3 цифры (охватывает большинство форматов)
    pattern_loose = r'\b\d{5,15}-\d{4,6}-\d{1,3}\b'

    matches_strict = re.findall(pattern_strict, text)
    matches_loose = re.findall(pattern_loose, text)

    # Объединяем и убираем дубликаты
    all_matches = list(set(matches_strict + matches_loose))
    logger.info(f"Order numbers found: {all_matches}")
    return all_matches