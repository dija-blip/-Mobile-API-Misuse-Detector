from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from datetime import datetime, timedelta

from backend.db.database import get_db
from backend.db.models import LogEntry, ThreatEvent, IPProfile
from backend.schemas.schemas import TrafficStats
from backend.core.websocket import manager

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", response_model=TrafficStats)
async def get_stats(db: AsyncSession = Depends(get_db)):
    # Total requests
    total_req = (await db.execute(select(func.count()).select_from(LogEntry))).scalar() or 0

    # Unique IPs
    unique_ips = (await db.execute(select(func.count(func.distinct(LogEntry.ip))))).scalar() or 0

    # Threats detected
    threats = (await db.execute(select(func.count()).select_from(ThreatEvent))).scalar() or 0

    # Blocked IPs
    blocked = (await db.execute(
        select(func.count()).select_from(IPProfile).where(IPProfile.blocked == True)
    )).scalar() or 0

    # Average risk score
    avg_score = (await db.execute(select(func.avg(ThreatEvent.risk_score)))).scalar() or 0.0

    # Top attack types
    attack_rows = (await db.execute(
        select(ThreatEvent.attack_type, func.count().label("count"))
        .group_by(ThreatEvent.attack_type)
        .order_by(func.count().desc())
        .limit(5)
    )).all()
    top_attacks = [{"attack_type": r[0], "count": r[1]} for r in attack_rows]

    # Requests per minute — last 30 minutes bucketed by minute
    since = datetime.utcnow() - timedelta(minutes=30)
    rpm_rows = (await db.execute(
        select(
            func.date_trunc("minute", LogEntry.timestamp).label("minute"),
            func.count().label("count"),
        )
        .where(LogEntry.timestamp >= since)
        .group_by(text("minute"))
        .order_by(text("minute"))
    )).all()
    rpm = [{"minute": str(r[0]), "count": r[1]} for r in rpm_rows]

    return TrafficStats(
        total_requests=total_req,
        unique_ips=unique_ips,
        threats_detected=threats,
        blocked_ips=blocked,
        avg_risk_score=round(float(avg_score), 2),
        top_attack_types=top_attacks,
        requests_per_minute=rpm,
    )


@router.get("/ws-connections")
async def ws_connections():
    return {"active_connections": manager.active_connections}
