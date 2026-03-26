import cv2
import numpy as np
from io import BytesIO
from PIL import Image

def load_image_from_bytes(image_bytes: BytesIO) -> np.ndarray:
    """Конвертирует байты изображения в numpy array (BGR)"""
    img = Image.open(image_bytes)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    """Предобработка для OCR: серый, бинаризация"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh