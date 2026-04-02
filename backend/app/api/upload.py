"""File upload API endpoints."""
import os
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..config import get_settings

router = APIRouter()
settings = get_settings()

TRANSACTION_FILE_TYPES = {".csv", ".xlsx", ".xls"}
INVOICE_FILE_TYPES = {".pdf", ".jpg", ".jpeg", ".png"}


def _store_upload(file: UploadFile) -> tuple[str, str]:
    """Persist an uploaded file and return the saved path plus extension."""
    extension = Path(file.filename or "").suffix.lower()
    if not extension:
        raise HTTPException(status_code=400, detail="Uploaded file must include an extension")

    os.makedirs(settings.upload_dir, exist_ok=True)
    stored_filename = f"{uuid4().hex}{extension}"
    output_path = os.path.join(settings.upload_dir, stored_filename)

    with open(output_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return output_path, stored_filename


@router.post("/csv")
async def upload_csv(file: UploadFile = File(...)):
    """Upload a transaction file for automated audit analysis."""
    extension = Path(file.filename or "").suffix.lower()
    if extension not in TRANSACTION_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only CSV, XLSX, and XLS files are supported for analysis",
        )

    output_path, stored_filename = _store_upload(file)
    return {
        "message": "Transaction file uploaded",
        "filename": file.filename,
        "stored_filename": stored_filename,
        "path": output_path,
        "kind": "transactions",
    }


@router.post("/invoice")
async def upload_invoice(file: UploadFile = File(...)):
    """Upload an invoice (PDF or image)."""
    extension = Path(file.filename or "").suffix.lower()
    if extension not in INVOICE_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF, JPG, and PNG files are supported")

    output_path, stored_filename = _store_upload(file)
    return {
        "message": "Invoice uploaded",
        "filename": file.filename,
        "stored_filename": stored_filename,
        "path": output_path,
        "kind": "document",
    }


@router.get("/status")
async def upload_status():
    """Check upload status and stats."""
    return {
        "upload_dir": settings.upload_dir,
        "status": "ready",
        "supported_transaction_files": sorted(TRANSACTION_FILE_TYPES),
        "supported_invoice_files": sorted(INVOICE_FILE_TYPES),
    }
