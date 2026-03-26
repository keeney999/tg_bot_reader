import cv2
import numpy as np
import re
import pytesseract
from src.services.image_utils import preprocess_for_ocr
from src.utils.logger import logger

def extract_barcodes(image: np.ndarray) -> list[str]:
    codes = []
    # 1. QR-коды
    qr = cv2.QRCodeDetector()
    ret_qr, decoded_info_qr, _, _ = qr.detectAndDecodeMulti(image)
    if ret_qr and decoded_info_qr:
        codes.extend(decoded_info_qr)
        logger.info(f"QR codes found: {decoded_info_qr}")
    # 2. 1D штрихкоды (EAN, Code128 и др.)
    try:
        barcode = cv2.barcode_BarcodeDetector()
        ret_bc, decoded_info_bc, _, _ = barcode.detectAndDecode(image)
        if ret_bc and decoded_info_bc:
            codes.extend(decoded_info_bc)
            logger.info(f"1D barcodes found: {decoded_info_bc}")
    except Exception as e:
        logger.warning(f"Barcode detector failed: {e}. Try installing opencv-contrib-python.")

    # Убираем пустые и дубли
    codes = [c for c in codes if c]
    codes = list(set(codes))
    if not codes:
        logger.info("No barcodes found")
    return codes

def extract_order_numbers(image: np.ndarray) -> list[str]:
    processed = preprocess_for_ocr(image)
    text = pytesseract.image_to_string(processed, lang='eng', config='--psm 6')
    logger.info(f"OCR text: {text}")
    pattern = r'\b\d{8}-\d{4}-\d\b'
    matches = re.findall(pattern, text)
    logger.info(f"Order numbers found: {matches}")
    return list(set(matches))