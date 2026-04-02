"""AuditAI FastAPI backend entrypoint."""
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .config import get_settings
from .api import auth, upload, audit, chatbot, reports

# Setup logging
settings = get_settings()
os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup/shutdown."""
    logger.info("AuditAI backend starting...")
    yield
    logger.info("AuditAI backend shutting down...")


app = FastAPI(title="AuditAI", version="0.1.0", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted hosts middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])
app.include_router(chatbot.router, prefix="/api/chat", tags=["chatbot"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])


@app.get("/", tags=["health"])
async def root():
    return {"message": "AuditAI backend is running", "version": "0.1.0"}


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
