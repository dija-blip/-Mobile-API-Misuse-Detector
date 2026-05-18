from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from backend.db.database import Base


class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    ip = Column(String(45), index=True)
    method = Column(String(10))
    endpoint = Column(String(512))
    status_code = Column(Integer, index=True)
    response_time_ms = Column(Integer)
    user_agent = Column(Text)
    is_mobile = Column(Boolean, default=True)
    platform = Column(String(50))
    country = Column(String(10))
    device_model = Column(String(100))
    device_type = Column(String(50))
    source = Column(String(50), default="api")  # nginx | express | springboot | api


class ThreatEvent(Base):
    __tablename__ = "threat_events"

    id = Column(Integer, primary_key=True, index=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    ip = Column(String(45), index=True)
    attack_type = Column(String(50), index=True)
    risk_score = Column(Integer)
    risk_level = Column(String(20), index=True)
    endpoint = Column(String(512))
    rule_score = Column(Integer)
    ai_score = Column(Float)
    details = Column(JSON)
    resolved = Column(Boolean, default=False)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    ip = Column(String(45))
    risk_level = Column(String(20))
    risk_score = Column(Integer)
    attack_type = Column(String(50))
    endpoint = Column(String(512))
    message = Column(Text)
    recommendation = Column(Text)
    acknowledged = Column(Boolean, default=False)


class IPProfile(Base):
    __tablename__ = "ip_profiles"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(45), unique=True, index=True)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), onupdate=func.now())
    total_requests = Column(Integer, default=0)
    failed_auth_count = Column(Integer, default=0)
    blocked = Column(Boolean, default=False)
    risk_score = Column(Integer, default=0)
    risk_level = Column(String(20), default="LOW")
    country = Column(String(10))
    device_fingerprint = Column(String(256))
    tags = Column(JSON, default=list)
