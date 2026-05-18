from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://detector:detector@postgres:5432/detector"
)

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


_TABLES = [
    """CREATE TABLE IF NOT EXISTS log_entries (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ DEFAULT now(),
        ip VARCHAR(45), method VARCHAR(10), endpoint VARCHAR(512),
        status_code INTEGER, response_time_ms INTEGER,
        user_agent TEXT, is_mobile BOOLEAN, platform VARCHAR(50),
        country VARCHAR(10), device_model VARCHAR(100),
        device_type VARCHAR(50), source VARCHAR(50)
    )""",
    """CREATE TABLE IF NOT EXISTS threat_events (
        id SERIAL PRIMARY KEY,
        detected_at TIMESTAMPTZ DEFAULT now(),
        ip VARCHAR(45), attack_type VARCHAR(50), risk_score INTEGER,
        risk_level VARCHAR(20), endpoint VARCHAR(512),
        rule_score INTEGER, ai_score FLOAT,
        details JSONB, resolved BOOLEAN DEFAULT false
    )""",
    """CREATE TABLE IF NOT EXISTS alerts (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMPTZ DEFAULT now(),
        ip VARCHAR(45), risk_level VARCHAR(20), risk_score INTEGER,
        attack_type VARCHAR(50), endpoint VARCHAR(512),
        message TEXT, recommendation TEXT,
        acknowledged BOOLEAN DEFAULT false
    )""",
    """CREATE TABLE IF NOT EXISTS ip_profiles (
        id SERIAL PRIMARY KEY,
        ip VARCHAR(45) UNIQUE,
        first_seen TIMESTAMPTZ DEFAULT now(),
        last_seen TIMESTAMPTZ,
        total_requests INTEGER DEFAULT 0,
        failed_auth_count INTEGER DEFAULT 0,
        blocked BOOLEAN DEFAULT false,
        risk_score INTEGER DEFAULT 0,
        risk_level VARCHAR(20) DEFAULT 'LOW',
        country VARCHAR(10),
        device_fingerprint VARCHAR(256),
        tags JSONB DEFAULT '[]'
    )""",
]


async def init_db():
    async with engine.begin() as conn:
        for stmt in _TABLES:
            await conn.execute(text(stmt))
