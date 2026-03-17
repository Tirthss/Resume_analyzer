# ============================================================
# extractor.py - IMPROVED VERSION
# Better OCR with image preprocessing for clearer text reading
# ============================================================

import os
from docx import Document
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract

# Windows path - uncomment if on Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def extract_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])


def preprocess_image(img):
    """
    Improve image quality before OCR so Tesseract reads more accurately.
    Steps:
    1. Convert to grayscale (removes color noise)
    2. Increase contrast (makes text darker, background lighter)
    3. Sharpen (makes text edges cleaner)
    4. Resize to 2x (Tesseract works better on larger images)
    """
    # 1. Grayscale
    img = img.convert('L')

    # 2. Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)

    # 3. Sharpen
    img = img.filter(ImageFilter.SHARPEN)

    # 4. Resize to 2x for better OCR
    w, h = img.size
    img = img.resize((w * 2, h * 2), Image.LANCZOS)

    return img


def extract_from_image(file_path):
    """
    Extract text from image using OCR with preprocessing.
    """
    img = Image.open(file_path)

    # Preprocess for better accuracy
    img = preprocess_image(img)

    # OCR config: treat as single column of text, best accuracy mode
    config = '--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=config)

    return text


def extract_text(file_path):
    """
    Main function — detects file type and extracts text.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.txt':
        return extract_from_txt(file_path)
    elif ext == '.docx':
        return extract_from_docx(file_path)
    elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
        return extract_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    print("extractor.py ready!")
    print("Supported: .txt  .docx  .png  .jpg  .jpeg")
