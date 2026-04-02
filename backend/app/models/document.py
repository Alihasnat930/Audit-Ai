"""Document model for invoice and PDF management."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db.base import Base


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(String(36), primary_key=True, unique=True, index=True)
    transaction_id = Column(String(36), ForeignKey("transactions.transaction_id"), nullable=True, index=True)
    
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)  # S3 or local storage
    file_type = Column(String(50), nullable=False)  # pdf, csv, jpg, png, etc.
    file_size = Column(Integer, nullable=False)  # bytes
    
    ocr_text = Column(Text, nullable=True)  # Extracted OCR text
    ocr_confidence = Column(String(50), nullable=True)  # Confidence score of OCR
    processed_flag = Column(Integer, nullable=False, default=0)  # 0=not processed, 1=processed
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transaction = relationship("Transaction", back_populates="documents")
