"""
Redis feature store — aggregates per-IP counters in a 5-minute window.
"""
import redis.asyncio as aioredis
import os
import json
import time

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
WINDOW = 300  # 5 minutes

_redis: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis


async def aggregate(ip: str, endpoint: str, status: int,
                    user_agent: str, method: str) -> dict:
    r = await get_redis()
    key = f"feat:{ip}"
    pipe = r.pipeline()

    pipe.hincrby(key, "req_count", 1)
    pipe.hincrby(key, "login_attempts", 1 if "/login" in endpoint else 0)
    pipe.hincrby(key, "failed_count", 1 if status in (401, 403) else 0)
    pipe.hincrby(key, "status_404", 1 if status == 404 else 0)
    pipe.hincrby(key, "post_count", 1 if method == "POST" else 0)
    pipe.hincrby(key, "bot_count", 1 if _is_bot(user_agent) else 0)

    # track unique endpoints via a set
    pipe.sadd(f"ep:{ip}", endpoint)
    pipe.expire(f"ep:{ip}", WINDOW)
    pipe.expire(key, WINDOW)
    await pipe.execute()

    data = await r.hgetall(key)
    unique_ep = await r.scard(f"ep:{ip}")

    req = max(int(data.get("req_count", 1)), 1)
    failed = int(data.get("failed_count", 0))
    login = int(data.get("login_attempts", 0))
    s404 = int(data.get("status_404", 0))
    bot = int(data.get("bot_count", 0))
    post = int(data.get("post_count", 0))

    return {
        "req_count": req,
        "requests_per_minute": req / (WINDOW / 60),
        "failed_auth_ratio": failed / max(login, 1),
        "unique_endpoints": int(unique_ep),
        "error_rate": failed / req,
        "request_interval_variance": 0.0,
        "sequential_endpoint_patterns": 1.0 if int(unique_ep) <= 2 else 0.0,
        "average_response_time": 0.0,
        "failed_count": failed,
        "status_404_count": s404,
        "bot_ratio": bot / req,
        "post_ratio": post / req,
        "login_attempts": login,
    }


async def is_blocked(ip: str) -> bool:
    r = await get_redis()
    return bool(await r.exists(f"block:{ip}"))


async def block_ip(ip: str, ttl: int = 900):
    r = await get_redis()
    await r.setex(f"block:{ip}", ttl, 1)


async def unblock_ip(ip: str):
    r = await get_redis()
    await r.delete(f"block:{ip}")


def _is_bot(ua: str) -> bool:
    bots = ("python-requests", "curl", "wget", "scrapy", "go-http", "java/", "nikto", "sqlmap")
    ua_lower = ua.lower()
    return any(b in ua_lower for b in bots)
