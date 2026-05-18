"""
Rule-based detection engine.
Each detector returns (score_delta: int, attack_type: str | None).
"""
from dataclasses import dataclass, field
from typing import Optional
import re

SUSPICIOUS_UA_PATTERNS = re.compile(
    r"(python-requests|curl|wget|scrapy|go-http|java/|libwww|nikto|sqlmap|masscan|zgrab)",
    re.IGNORECASE,
)

SENSITIVE_ENDPOINTS = re.compile(
    r"(/admin|/config|/debug|/env|/\.env|/actuator|/swagger|/api-docs|/metrics|/health/internal)",
    re.IGNORECASE,
)

INJECTION_PATTERNS = re.compile(
    r"(union\s+select|drop\s+table|insert\s+into|etc/passwd|<script|onerror=|javascript:|base64,)",
    re.IGNORECASE,
)


@dataclass
class RequestContext:
    ip: str
    method: str
    endpoint: str
    status_code: int
    user_agent: str
    response_time_ms: int
    # Redis-backed counters (5-min window)
    req_count: int = 0
    failed_auth_count: int = 0
    unique_endpoints: int = 1
    login_attempts: int = 0
    consecutive_404s: int = 0


@dataclass
class DetectionResult:
    score: int = 0
    attack_type: str = "none"
    triggers: list = field(default_factory=list)


def detect(ctx: RequestContext) -> DetectionResult:
    result = DetectionResult()

    # 1. Burst traffic — >100 req in 5 min window
    if ctx.req_count > 100:
        result.score += 35
        result.triggers.append(f"burst:{ctx.req_count}_req")
        result.attack_type = "burst"

    # 2. Bruteforce — many failed auth on /login
    if ctx.login_attempts > 5 and ctx.failed_auth_count / max(ctx.login_attempts, 1) > 0.7:
        result.score += 45
        result.triggers.append(f"bruteforce:{ctx.failed_auth_count}_failures")
        result.attack_type = "bruteforce"

    # 3. Endpoint hammering — same endpoint hit repeatedly
    if ctx.req_count > 50 and ctx.unique_endpoints <= 2:
        result.score += 30
        result.triggers.append("endpoint_hammering")
        if result.attack_type == "none":
            result.attack_type = "endpoint_hammering"

    # 4. Enumeration — many sequential 404s
    if ctx.consecutive_404s > 15:
        result.score += 35
        result.triggers.append(f"enumeration:{ctx.consecutive_404s}_404s")
        result.attack_type = "enumeration"

    # 5. Suspicious user-agent
    if SUSPICIOUS_UA_PATTERNS.search(ctx.user_agent):
        result.score += 25
        result.triggers.append(f"suspicious_ua:{ctx.user_agent[:40]}")
        if result.attack_type == "none":
            result.attack_type = "suspicious_ua"

    # 6. Sensitive endpoint access
    if SENSITIVE_ENDPOINTS.search(ctx.endpoint):
        result.score += 20
        result.triggers.append(f"sensitive_endpoint:{ctx.endpoint}")

    # 7. Injection payload in endpoint
    if INJECTION_PATTERNS.search(ctx.endpoint):
        result.score += 40
        result.triggers.append("injection_payload")
        result.attack_type = "injection"

    # 8. High error rate (4xx/5xx)
    if ctx.status_code in (401, 403):
        result.score += 15
    elif ctx.status_code == 429:
        result.score += 10
    elif ctx.status_code >= 500:
        result.score += 10

    result.score = min(result.score, 100)
    return result
