from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class LogEntryIn(BaseModel):
    ip: str
    method: str
    endpoint: str
    status_code: int
    response_time_ms: int = 0
    user_agent: str = ""
    is_mobile: bool = True
    platform: str = "unknown"
    country: str = "unknown"
    device_model: str = "unknown"
    device_type: str = "unknown"
    source: str = "api"
    timestamp: Optional[datetime] = None


class LogEntryOut(LogEntryIn):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class AnalyzeResponse(BaseModel):
    ip: str
    risk_score: int
    risk_level: str
    attack_type: str
    action: str
    blocked: bool
    rule_score: int
    ai_score: float
    recommendation: str
    details: dict


class ThreatEventOut(BaseModel):
    id: int
    detected_at: datetime
    ip: str
    attack_type: str
    risk_score: int
    risk_level: str
    endpoint: str
    rule_score: int
    ai_score: float
    details: Optional[Any]
    resolved: bool

    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    id: int
    created_at: datetime
    ip: str
    risk_level: str
    risk_score: int
    attack_type: str
    endpoint: str
    message: str
    recommendation: str
    acknowledged: bool

    class Config:
        from_attributes = True


class IPProfileOut(BaseModel):
    id: int
    ip: str
    first_seen: datetime
    last_seen: Optional[datetime]
    total_requests: int
    failed_auth_count: int
    blocked: bool
    risk_score: int
    risk_level: str
    country: Optional[str]
    device_fingerprint: Optional[str]
    tags: Optional[List[str]]

    class Config:
        from_attributes = True


class TrafficStats(BaseModel):
    total_requests: int
    unique_ips: int
    threats_detected: int
    blocked_ips: int
    avg_risk_score: float
    top_attack_types: List[dict]
    requests_per_minute: List[dict]


class LogUploadResult(BaseModel):
    parsed: int
    failed: int
    threats_detected: int
    message: str
