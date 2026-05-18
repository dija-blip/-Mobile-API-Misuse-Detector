"""
Recommendation engine — maps attack type + risk level to actionable advice.
"""
from typing import List

_RECOMMENDATIONS: dict[str, List[str]] = {
    "bruteforce": [
        "Implement account lockout after 5 failed attempts.",
        "Enable CAPTCHA on the login endpoint.",
        "Add multi-factor authentication (MFA).",
        "Rate-limit /login to 10 requests/minute per IP.",
        "Alert on >3 failed logins from the same IP within 60 seconds.",
    ],
    "burst": [
        "Apply token-bucket rate limiting per IP (100 req/min).",
        "Add a WAF rule to throttle burst traffic.",
        "Consider CDN-level DDoS protection (e.g., AWS Shield).",
        "Implement exponential backoff responses for repeat offenders.",
    ],
    "endpoint_hammering": [
        "Rate-limit the targeted endpoint per IP.",
        "Add caching to reduce backend load from repeated hits.",
        "Block the IP temporarily after 50 hits in 60 seconds.",
        "Add WAF rule targeting the specific endpoint pattern.",
    ],
    "enumeration": [
        "Replace sequential integer IDs with UUIDs.",
        "Return 404 for all unauthorized resource accesses (avoid 403 leaking existence).",
        "Rate-limit endpoints with path parameters.",
        "Log and alert on >10 consecutive 404s from the same IP.",
    ],
    "suspicious_ua": [
        "Block known bot/scanner user-agent strings at the WAF level.",
        "Require a valid mobile SDK user-agent header.",
        "Implement device fingerprinting to detect spoofed agents.",
        "Add certificate pinning in the mobile app.",
    ],
    "injection": [
        "Validate and sanitize all query parameters server-side.",
        "Use parameterized queries — never interpolate user input into SQL.",
        "Deploy a WAF with OWASP Core Rule Set (CRS).",
        "Enable input length limits on all API parameters.",
    ],
    "none": [
        "Continue monitoring — no immediate action required.",
        "Ensure logging is comprehensive for future forensics.",
    ],
}

_LEVEL_EXTRAS: dict[str, List[str]] = {
    "CRITICAL": [
        "Block this IP immediately for at least 24 hours.",
        "Escalate to the security team for manual review.",
        "Preserve logs for potential legal/forensic use.",
    ],
    "HIGH": [
        "Apply strict rate limiting to this IP.",
        "Add this IP to the watchlist for 48 hours.",
    ],
    "MEDIUM": [
        "Increase monitoring frequency for this IP.",
        "Consider soft rate limiting.",
    ],
    "LOW": [],
}


def get_recommendations(attack_type: str, risk_level: str) -> str:
    lines = _RECOMMENDATIONS.get(attack_type, _RECOMMENDATIONS["none"]).copy()
    lines += _LEVEL_EXTRAS.get(risk_level, [])
    return "\n".join(f"• {r}" for r in lines)
