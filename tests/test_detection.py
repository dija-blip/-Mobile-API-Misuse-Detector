import pytest
from backend.detection.rules import detect, RequestContext
from backend.detection.scoring import compute_final_score, get_risk_level, get_action
from backend.detection.recommendations import get_recommendations
from backend.ingestion.parser import parse_line


# ── Detection rules ──────────────────────────────────────────────────────────

def make_ctx(**kwargs):
    defaults = dict(
        ip="1.2.3.4", method="GET", endpoint="/api/data",
        status_code=200, user_agent="Android-App/4.2",
        response_time_ms=100, req_count=1, failed_auth_count=0,
        unique_endpoints=5, login_attempts=0, consecutive_404s=0,
    )
    defaults.update(kwargs)
    return RequestContext(**defaults)


def test_burst_detection():
    ctx = make_ctx(req_count=150, unique_endpoints=10)
    result = detect(ctx)
    assert result.attack_type == "burst"
    assert result.score >= 35


def test_bruteforce_detection():
    ctx = make_ctx(login_attempts=10, failed_auth_count=9, endpoint="/login")
    result = detect(ctx)
    assert result.attack_type == "bruteforce"
    assert result.score >= 45


def test_enumeration_detection():
    ctx = make_ctx(consecutive_404s=20)
    result = detect(ctx)
    assert result.attack_type == "enumeration"
    assert result.score >= 35


def test_suspicious_ua_detection():
    ctx = make_ctx(user_agent="python-requests/2.28")
    result = detect(ctx)
    assert result.attack_type == "suspicious_ua"
    assert result.score >= 25


def test_injection_detection():
    ctx = make_ctx(endpoint="/search?q=UNION SELECT password FROM users")
    result = detect(ctx)
    assert result.attack_type == "injection"
    assert result.score >= 40


def test_endpoint_hammering():
    ctx = make_ctx(req_count=80, unique_endpoints=1)
    result = detect(ctx)
    assert result.attack_type == "endpoint_hammering"


def test_clean_request_low_score():
    ctx = make_ctx()
    result = detect(ctx)
    assert result.score < 25


# ── Scoring ───────────────────────────────────────────────────────────────────

def test_final_score_with_ai():
    score = compute_final_score(60, 0.8)
    assert score == min(int(60 * 0.6 + 0.8 * 100 * 0.4), 100)


def test_final_score_no_ai():
    assert compute_final_score(70, 0.0) == 70


def test_risk_levels():
    assert get_risk_level(10)  == "LOW"
    assert get_risk_level(30)  == "MEDIUM"
    assert get_risk_level(60)  == "HIGH"
    assert get_risk_level(80)  == "CRITICAL"


def test_actions():
    assert get_action(10)  == "log_only"
    assert get_action(30)  == "monitor"
    assert get_action(60)  == "rate_limit"
    assert get_action(80)  == "block_and_alert"


# ── Recommendations ───────────────────────────────────────────────────────────

def test_recommendations_bruteforce():
    rec = get_recommendations("bruteforce", "HIGH")
    assert "CAPTCHA" in rec or "lockout" in rec


def test_recommendations_critical_extras():
    rec = get_recommendations("burst", "CRITICAL")
    assert "Block" in rec or "block" in rec


# ── Log parser ────────────────────────────────────────────────────────────────

NGINX_LINE = '192.168.1.1 - - [10/Jun/2024:12:00:00 +0000] "GET /api/users HTTP/1.1" 200 512 "-" "Android-App/4.2" 0.045'

EXPRESS_LINE = '{"message": "{\\"ip\\": \\"10.0.0.1\\", \\"method\\": \\"POST\\", \\"endpoint\\": \\"/login\\", \\"status\\": 401, \\"response_time_ms\\": 120, \\"user_agent\\": \\"curl/7.68\\", \\"timestamp\\": \\"2024-06-10T12:00:00\\"}"}'


def test_parse_nginx():
    entry = parse_line(NGINX_LINE, "nginx")
    assert entry is not None
    assert entry.ip == "192.168.1.1"
    assert entry.method == "GET"
    assert entry.status_code == 200
    assert entry.source == "nginx"


def test_parse_express():
    entry = parse_line(EXPRESS_LINE, "express")
    assert entry is not None
    assert entry.ip == "10.0.0.1"
    assert entry.status_code == 401
    assert entry.source == "express"


def test_parse_invalid_returns_none():
    assert parse_line("not a valid log line at all", "nginx") is None


def test_parse_auto_detect_nginx():
    entry = parse_line(NGINX_LINE, "auto")
    assert entry is not None
    assert entry.source == "nginx"
