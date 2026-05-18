"""
Risk scoring engine.
Final score = 60% rule score + 40% ML score.
"""


def compute_final_score(rule_score: int, ai_score: float) -> int:
    if ai_score > 0:
        return min(int(rule_score * 0.6 + ai_score * 100 * 0.4), 100)
    return min(rule_score, 100)


def get_risk_level(score: int) -> str:
    if score < 25:
        return "LOW"
    if score < 50:
        return "MEDIUM"
    if score < 75:
        return "HIGH"
    return "CRITICAL"


def get_action(score: int) -> str:
    if score < 25:
        return "log_only"
    if score < 50:
        return "monitor"
    if score < 75:
        return "rate_limit"
    return "block_and_alert"
