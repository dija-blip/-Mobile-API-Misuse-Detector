from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List

from backend.db.database import get_db
from backend.db.models import ThreatEvent, Alert, IPProfile
from backend.schemas.schemas import ThreatEventOut, AlertOut, IPProfileOut
from backend.core.redis_store import unblock_ip

router = APIRouter(tags=["threats"])


# ── Threats ──────────────────────────────────────────────────────────────────

@router.get("/threats", response_model=List[ThreatEventOut])
async def list_threats(
    limit: int = Query(50, le=200),
    risk_level: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    q = select(ThreatEvent).order_by(ThreatEvent.detected_at.desc()).limit(limit)
    if risk_level:
        q = q.where(ThreatEvent.risk_level == risk_level.upper())
    result = await db.execute(q)
    return result.scalars().all()


@router.patch("/threats/{threat_id}/resolve")
async def resolve_threat(threat_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(update(ThreatEvent).where(ThreatEvent.id == threat_id).values(resolved=True))
    await db.commit()
    return {"ok": True}


# ── Alerts ───────────────────────────────────────────────────────────────────

@router.get("/alerts", response_model=List[AlertOut])
async def list_alerts(
    limit: int = Query(50, le=200),
    unacknowledged: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    q = select(Alert).order_by(Alert.created_at.desc()).limit(limit)
    if unacknowledged:
        q = q.where(Alert.acknowledged == False)
    result = await db.execute(q)
    return result.scalars().all()


@router.patch("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(update(Alert).where(Alert.id == alert_id).values(acknowledged=True))
    await db.commit()
    return {"ok": True}


# ── IP Profiles ───────────────────────────────────────────────────────────────

@router.get("/ips", response_model=List[IPProfileOut])
async def list_ip_profiles(
    limit: int = Query(50, le=200),
    blocked_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    q = select(IPProfile).order_by(IPProfile.risk_score.desc()).limit(limit)
    if blocked_only:
        q = q.where(IPProfile.blocked == True)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/ips/{ip}", response_model=IPProfileOut)
async def get_ip_profile(ip: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(IPProfile).where(IPProfile.ip == ip))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="IP not found")
    return profile


@router.post("/ips/{ip}/unblock")
async def unblock_ip_route(ip: str, db: AsyncSession = Depends(get_db)):
    await unblock_ip(ip)
    await db.execute(update(IPProfile).where(IPProfile.ip == ip).values(blocked=False))
    await db.commit()
    return {"ok": True}
