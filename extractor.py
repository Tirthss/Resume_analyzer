# ============================================================
# extractor.py - WITH PDF SUPPORT
# Supports: TXT, DOCX, PDF, PNG, JPG, JPEG
# ============================================================

import os
from docx import Document
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import pdfplumber

# Windows only — uncomment if running locally on Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def extract_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])


def extract_from_pdf(file_path):
    """Extract text from PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        text = extract_pdf_with_ocr(file_path)

    return text


def extract_pdf_with_ocr(file_path):
    """Fallback OCR for scanned PDFs."""
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(file_path, dpi=200)
        all_text = ""
        for img in images:
            img = preprocess_image(img)
            config = '--oem 3 --psm 6'
            all_text += pytesseract.image_to_string(img, config=config) + "\n"
        return all_text
    except Exception as e:
        return f"Could not extract text from scanned PDF: {e}"


def preprocess_image(img):
    """Improve image quality for better OCR accuracy."""
    img = img.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    img = img.filter(ImageFilter.SHARPEN)
    w, h = img.size
    img = img.resize((w * 2, h * 2), Image.LANCZOS)
    return img


def extract_from_image(file_path):
    """Extract text from image using Tesseract OCR."""
    img = Image.open(file_path)
    img = preprocess_image(img)
    config = '--oem 3 --psm 6'
    return pytesseract.image_to_string(img, config=config)


def extract_text(file_path):
    """
    Main function — auto detects file type and extracts text.
    Supports: .txt .docx .pdf .png .jpg .jpeg
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.txt':
        return extract_from_txt(file_path)
    elif ext == '.docx':
        return extract_from_docx(file_path)
    elif ext == '.pdf':
        return extract_from_pdf(file_path)
    elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
        return extract_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    print("extractor.py ready!")
    print("Supported: .txt  .docx  .pdf  .png  .jpg  .jpeg")
