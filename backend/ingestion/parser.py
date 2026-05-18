import re
from datetime import datetime
from typing import Optional
from backend.schemas.schemas import LogEntryIn

# Nginx combined log format
_NGINX_RE = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>\w+) (?P<endpoint>\S+) HTTP/[\d\.]+" '
    r'(?P<status>\d+) \d+ "[^"]*" "(?P<ua>[^"]*)" '
    r'(?P<rt>[\d\.]+)?'
)

# Spring Boot default log pattern
_SPRING_RE = re.compile(
    r'(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+).*'
    r'(?P<method>GET|POST|PUT|DELETE|PATCH) (?P<endpoint>\S+).*'
    r'(?P<status>\d{3}).*?(?P<rt>\d+)ms'
)


def _parse_nginx(line: str) -> Optional[LogEntryIn]:
    m = _NGINX_RE.match(line.strip())
    if not m:
        return None
    try:
        ts = datetime.strptime(m.group("ts"), "%d/%b/%Y:%H:%M:%S %z")
    except ValueError:
        ts = datetime.utcnow()
    return LogEntryIn(
        ip=m.group("ip"),
        method=m.group("method"),
        endpoint=m.group("endpoint"),
        status_code=int(m.group("status")),
        response_time_ms=int(float(m.group("rt") or 0) * 1000),
        user_agent=m.group("ua"),
        source="nginx",
        timestamp=ts,
    )


def _parse_express(line: str) -> Optional[LogEntryIn]:
    """Parse Winston JSON log lines from Express backend."""
    import json
    try:
        data = json.loads(line.strip())
        msg = data.get("message", data)
        if isinstance(msg, str):
            try:
                msg = json.loads(msg)
            except Exception:
                return None
        return LogEntryIn(
            ip=msg.get("ip", "0.0.0.0"),
            method=msg.get("method", "GET"),
            endpoint=msg.get("endpoint", "/"),
            status_code=int(msg.get("status", 200)),
            response_time_ms=int(msg.get("response_time_ms", 0)),
            user_agent=msg.get("user_agent", ""),
            country=msg.get("country", "unknown"),
            device_model=msg.get("device_model", "unknown"),
            device_type=msg.get("device_type", "mobile"),
            source="express",
            timestamp=datetime.fromisoformat(str(msg.get("timestamp", datetime.utcnow().isoformat()))),
        )
    except Exception:
        return None


def _parse_springboot(line: str) -> Optional[LogEntryIn]:
    m = _SPRING_RE.search(line)
    if not m:
        return None
    try:
        ts = datetime.strptime(m.group("ts"), "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        ts = datetime.utcnow()
    return LogEntryIn(
        ip="0.0.0.0",
        method=m.group("method"),
        endpoint=m.group("endpoint"),
        status_code=int(m.group("status")),
        response_time_ms=int(m.group("rt")),
        source="springboot",
        timestamp=ts,
    )


def parse_line(line: str, source: str = "auto") -> Optional[LogEntryIn]:
    if source == "nginx":
        return _parse_nginx(line)
    if source == "express":
        return _parse_express(line)
    if source == "springboot":
        return _parse_springboot(line)
    # auto-detect
    if line.strip().startswith("{"):
        return _parse_express(line)
    if _NGINX_RE.match(line.strip()):
        return _parse_nginx(line)
    return _parse_springboot(line)
