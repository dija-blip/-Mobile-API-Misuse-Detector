from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from backend.ingestion.parser import parse_line
from backend.db.models import LogEntry
from backend.schemas.schemas import LogEntryIn


async def ingest_lines(
    lines: List[str],
    source: str,
    db: AsyncSession,
) -> Tuple[int, int]:
    """Parse lines, bulk-insert valid entries. Returns (parsed, failed)."""
    entries, failed = [], 0
    for line in lines:
        if not line.strip():
            continue
        parsed = parse_line(line, source)
        if parsed:
            entries.append(_to_dict(parsed))
        else:
            failed += 1

    if entries:
        await db.execute(insert(LogEntry), entries)
        await db.commit()

    return len(entries), failed


def _to_dict(entry: LogEntryIn) -> dict:
    d = entry.model_dump()
    if d.get("timestamp") is None:
        from datetime import datetime
        d["timestamp"] = datetime.utcnow()
    return d
