# Mobile API Abuse Detector v4.0

An intelligent platform for detecting abuse and malicious behaviors targeting backend APIs used by mobile applications.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        React Dashboard                          │
│  Overview │ Live Traffic │ Threats │ Alerts │ Timeline │ ...    │
└─────────────────────────┬───────────────────────────────────────┘
                          │ REST + WebSocket
┌─────────────────────────▼───────────────────────────────────────┐
│                      FastAPI Backend                            │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Ingestion│  │  Rules   │  │    ML    │  │ Recommendations│  │
│  │  Parser  │  │ Engine   │  │  Engine  │  │    Engine      │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │  Risk    │  │ WebSocket│  │  Redis   │  │  PostgreSQL   │  │
│  │ Scoring  │  │ Manager  │  │  Store   │  │     ORM       │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │                              │
    ┌────▼────┐                   ┌─────▼─────┐
    │  Redis  │                   │ PostgreSQL │
    └─────────┘                   └───────────┘
```

## Detection Engine

| Attack Type         | Trigger Condition                              | Score Delta |
|---------------------|------------------------------------------------|-------------|
| Burst               | >100 requests in 5-min window                  | +35         |
| Bruteforce          | >5 login attempts, >70% failure rate           | +45         |
| Endpoint Hammering  | >50 requests, ≤2 unique endpoints              | +30         |
| Enumeration         | >15 consecutive 404s                           | +35         |
| Suspicious UA       | Matches bot/scanner pattern                    | +25         |
| Sensitive Endpoint  | /admin, /debug, /.env, /actuator               | +20         |
| Injection Payload   | SQL/XSS/path traversal in endpoint             | +40         |

**Final Score** = 60% rule score + 40% ML (Isolation Forest) score

## Risk Levels

| Score   | Level    | Action           |
|---------|----------|------------------|
| 0–24    | LOW      | log_only         |
| 25–49   | MEDIUM   | monitor          |
| 50–74   | HIGH     | rate_limit       |
| 75–100  | CRITICAL | block_and_alert  |

## Quick Start

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Start all services
docker compose up --build

# 3. Access the dashboard
open http://localhost:3000

# 4. API docs
open http://localhost:8000/docs
```

## API Endpoints

| Method | Path                          | Description                    |
|--------|-------------------------------|--------------------------------|
| POST   | /api/v1/analyze               | Analyze a single log entry     |
| POST   | /api/v1/logs/upload           | Upload a log file              |
| GET    | /api/v1/logs                  | Browse log entries             |
| GET    | /api/v1/threats               | List threat events             |
| GET    | /api/v1/alerts                | List alerts                    |
| PATCH  | /api/v1/alerts/{id}/acknowledge | Acknowledge an alert         |
| GET    | /api/v1/stats                 | Dashboard statistics           |
| GET    | /api/v1/stats/heatmap         | Risk heatmap data              |
| GET    | /api/v1/stats/timeline        | Attack timeline                |
| GET    | /api/v1/ip/{ip}               | IP profile                     |
| POST   | /api/v1/ip/{ip}/block         | Manually block an IP           |
| DELETE | /api/v1/ip/{ip}/block         | Unblock an IP                  |
| WS     | /ws/live                      | Real-time event stream         |

## Project Structure

```
├── backend/
│   ├── api/routes/        # FastAPI route handlers
│   ├── core/              # Redis store, WebSocket manager
│   ├── db/                # SQLAlchemy models & database
│   ├── detection/         # Rules engine, scoring, recommendations
│   ├── ingestion/         # Log parser & ingestor
│   ├── ml/                # Anomaly detection (Isolation Forest)
│   ├── schemas/           # Pydantic schemas
│   └── main.py            # FastAPI app entry point
├── frontend/
│   └── src/
│       ├── api/           # API client
│       ├── components/    # Shared UI components
│       ├── hooks/         # useWebSocket, useFetch
│       └── pages/         # Dashboard pages
├── models/                # Pre-trained ML model files (.pkl)
├── data/processed/        # CSV datasets
├── tests/                 # Pytest unit tests
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```





## Dashboard Pages

- **Overview** — Key metrics, RPM chart, attack type breakdown
- **Live Traffic** — Real-time WebSocket event stream
- **Threats** — Filterable threat event table
- **Alerts** — Actionable alerts with recommendations
- **Timeline** — Chronological attack visualization
- **Risk Heatmap** — IP risk score grid
- **Devices** — Device/platform/UA analytics
- **Logs** — Raw log browser with pagination
- **Recommendations** — Automated defensive advice
