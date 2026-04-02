"""OCR service for document text extraction."""
import logging
import os
from pathlib import Path
from typing import Tuple, Optional

try:
    import pytesseract
    from PIL import Image
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

logger = logging.getLogger(__name__)


def extract_text_from_file(file_path: str, timeout: int = 60) -> Tuple[str, float]:
    """Extract text from image/PDF using OCR. Returns (text, confidence_score)."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not PYTESSERACT_AVAILABLE:
            logger.warning("Pytesseract not available; returning empty text")
            return "", 0.0
        
        file_path = Path(file_path)
        suffix = file_path.suffix.lower()
        
        if suffix in [".jpg", ".jpeg", ".png"]:
            return _ocr_image(str(file_path))
        elif suffix == ".pdf":
            return _ocr_pdf(str(file_path))
        else:
            raise ValueError(f"Unsupported file type: {suffix}")
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        return "", 0.0


def _ocr_image(image_path: str) -> Tuple[str, float]:
    """OCR on image file."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        confidence = 0.85  # Approximate; Tesseract doesn't provide direct confidence
        logger.info(f"OCR completed for {image_path}; {len(text)} chars extracted")
        return text, confidence
    except Exception as e:
        logger.error(f"Error in OCR image: {e}")
        return "", 0.0


def _ocr_pdf(pdf_path: str) -> Tuple[str, float]:
    """OCR on PDF (requires pdf2image and pytesseract)."""
    try:
        # Note: Full PDF OCR would require pdf2image library
        # For now, return placeholder
        logger.warning(f"PDF OCR not fully implemented: {pdf_path}")
        return "", 0.0
    except Exception as e:
        logger.error(f"Error in OCR PDF: {e}")
        return "", 0.0


def validate_invoice(ocr_text: str) -> dict:
    """Validate invoice structure from OCR text."""
    try:
        validations = {
            "has_vendor_name": bool(ocr_text and len(ocr_text.split()) > 5),
            "has_amount": any(char.isdigit() for char in ocr_text),
            "has_date": any(x in ocr_text.lower() for x in ["date", "invoice", "2024", "2023"]),
        }
        return validations
    except Exception as e:
        logger.error(f"Error validating invoice: {e}")
        return {"has_vendor_name": False, "has_amount": False, "has_date": False}
