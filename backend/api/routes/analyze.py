from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from datetime import datetime

from backend.db.database import get_db
from backend.db.models import LogEntry, ThreatEvent, Alert, IPProfile
from backend.schemas.schemas import LogEntryIn, AnalyzeResponse
from backend.detection.rules import RequestContext, detect
from backend.detection.scoring import compute_final_score, get_risk_level, get_action
from backend.detection.recommendations import get_recommendations
from backend.ml.anomaly import MLFeatures, predict
from backend.core.redis_store import aggregate, is_blocked, block_ip
from backend.core.websocket import manager

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.post("", response_model=AnalyzeResponse)
async def analyze(entry: LogEntryIn, db: AsyncSession = Depends(get_db)):
    # Check if IP is already blocked
    if await is_blocked(entry.ip):
        raise HTTPException(status_code=403, detail="IP is blocked")

    # Persist log entry
    await db.execute(insert(LogEntry), [{
        **entry.model_dump(),
        "timestamp": entry.timestamp or datetime.utcnow(),
    }])
    await db.commit()

    # Aggregate Redis counters
    feats = await aggregate(entry.ip, entry.endpoint, entry.status_code,
                            entry.user_agent, entry.method)

    # Rule-based detection
    ctx = RequestContext(
        ip=entry.ip,
        method=entry.method,
        endpoint=entry.endpoint,
        status_code=entry.status_code,
        user_agent=entry.user_agent,
        response_time_ms=entry.response_time_ms,
        req_count=feats["req_count"],
        failed_auth_count=feats["failed_count"],
        unique_endpoints=feats["unique_endpoints"],
        login_attempts=feats["login_attempts"],
        consecutive_404s=feats["status_404_count"],
    )
    detection = detect(ctx)

    # ML scoring
    ml_feats = MLFeatures(**{k: feats[k] for k in MLFeatures.__dataclass_fields__})
    ai_score, _ = predict(ml_feats)

    # Final score
    risk_score = compute_final_score(detection.score, ai_score)
    risk_level = get_risk_level(risk_score)
    action = get_action(risk_score)
    recommendation = get_recommendations(detection.attack_type, risk_level)
    blocked = action == "block_and_alert"

    if blocked:
        await block_ip(entry.ip)

    # Persist threat event if score > 0
    if risk_score > 0:
        await db.execute(insert(ThreatEvent), [{
            "ip": entry.ip,
            "attack_type": detection.attack_type,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "endpoint": entry.endpoint,
            "rule_score": detection.score,
            "ai_score": ai_score,
            "details": {"triggers": detection.triggers},
        }])

        if risk_level in ("MEDIUM", "HIGH", "CRITICAL"):
            await db.execute(insert(Alert), [{
                "ip": entry.ip,
                "risk_level": risk_level,
                "risk_score": risk_score,
                "attack_type": detection.attack_type,
                "endpoint": entry.endpoint,
                "message": f"{risk_level} threat detected: {detection.attack_type}",
                "recommendation": recommendation,
            }])

        await db.commit()

    # Upsert IP profile
    existing = await db.execute(select(IPProfile).where(IPProfile.ip == entry.ip))
    profile = existing.scalar_one_or_none()
    if profile:
        await db.execute(
            update(IPProfile).where(IPProfile.ip == entry.ip).values(
                total_requests=IPProfile.total_requests + 1,
                failed_auth_count=IPProfile.failed_auth_count + (1 if entry.status_code in (401, 403) else 0),
                blocked=blocked,
                risk_score=risk_score,
                risk_level=risk_level,
                last_seen=datetime.utcnow(),
            )
        )
    else:
        await db.execute(insert(IPProfile), [{
            "ip": entry.ip,
            "total_requests": 1,
            "failed_auth_count": 1 if entry.status_code in (401, 403) else 0,
            "blocked": blocked,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "country": entry.country,
        }])
    await db.commit()

    result = AnalyzeResponse(
        ip=entry.ip,
        risk_score=risk_score,
        risk_level=risk_level,
        attack_type=detection.attack_type,
        action=action,
        blocked=blocked,
        rule_score=detection.score,
        ai_score=ai_score,
        recommendation=recommendation,
        details={"triggers": detection.triggers, "features": feats},
    )

    # Broadcast via WebSocket
    await manager.broadcast("threat", result.model_dump())

    return result
