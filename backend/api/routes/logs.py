from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from backend.db.database import get_db
from backend.db.models import LogEntry
from backend.ingestion.ingestor import ingest_lines
from backend.schemas.schemas import LogUploadResult, LogEntryOut

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/upload", response_model=LogUploadResult)
async def upload_logs(
    file: UploadFile = File(...),
    source: str = Query("nginx", enum=["nginx", "express", "springboot", "api"]),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    lines = content.decode("utf-8", errors="ignore").splitlines()
    parsed, failed = await ingest_lines(lines, source, db)
    return LogUploadResult(
        parsed=parsed,
        failed=failed,
        threats_detected=0,
        message=f"Ingested {parsed} entries from {file.filename} ({failed} failed)",
    )


@router.get("", response_model=list[LogEntryOut])
async def get_logs(
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    ip: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    q = select(LogEntry).order_by(desc(LogEntry.timestamp)).offset(offset).limit(limit)
    if ip:
        q = q.where(LogEntry.ip == ip)
    result = await db.execute(q)
    return result.scalars().all()
