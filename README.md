# API Abuse Detector v4.0

> **An AI-Powered Real-Time Mobile API Misuse Detection and Threat Intelligence Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue)](https://reactjs.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://docker.com)
[![Redis](https://img.shields.io/badge/Redis-7-red)](https://redis.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://postgresql.org)

---

**Supervised by:** Prof. Mohamed Lachgar  
**Institution:** Cadi Ayyad University — National School of Applied Sciences (ENSA), Marrakech, Morocco  
**Authors:** Elgadaoui Chaimaa · Elkissany Kawtar · Essaidi Sara · Lakbita Khadija  
**Version:** v4.0 · May 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Technology Stack](#technology-stack)
5. [Dataset](#dataset)
6. [AI Models](#ai-models)
7. [Hybrid Scoring & AHP](#hybrid-scoring--ahp)
8. [Detection Pipeline](#detection-pipeline)
9. [Dashboard Pages](#dashboard-pages)
10. [Installation & Quick Start](#installation--quick-start)
11. [API Endpoints](#api-endpoints)
12. [Project Structure](#project-structure)
13. [Performance Results](#performance-results)
14. [Quality Assurance](#quality-assurance)
15. [Comparison with Existing Solutions](#comparison-with-existing-solutions)
16. [Future Work](#future-work)

---

## Overview

The rapid growth of mobile applications and cloud-connected APIs has significantly increased the attack surface of modern digital ecosystems. Malicious activities such as API abuse, brute-force attacks, endpoint enumeration, credential stuffing, and automated bot exploitation represent major cybersecurity challenges for enterprises and mobile platforms alike.

**API Abuse Detector** is a distributed cybersecurity monitoring platform designed for real-time detection of malicious API behaviors. The system leverages:

- **FastAPI** microservices for high-performance async backend
- **Redis** in-memory temporal aggregation (5-minute sliding windows)
- **PostgreSQL** for persistent threat storage
- **Machine Learning** anomaly detection (Isolation Forest, DBSCAN, Autoencoder)
- **WebSocket** real-time event broadcasting
- **React** 10-page interactive dashboard

The platform combines behavioral analysis, statistical anomaly detection, and deterministic cybersecurity rules to generate adaptive threat scores and automated mitigation strategies.

> Evaluated on a real-world dataset of **49,456 API requests** from a production e-commerce platform, achieving an **F1-score of 0.89** with **sub-millisecond inference** (0.8 ms).

---

## Key Features

- **Real-time API monitoring** via REST endpoints and WebSocket streaming
- **10-step detection pipeline** combining rule-based and ML-based analysis
- **Three complementary AI models**: Isolation Forest (primary), DBSCAN, Autoencoder
- **19 behavioral features** extracted per IP address via temporal aggregation
- **AHP-justified hybrid scoring**: 60% rules + 40% AI (CR = 0.015, validated)
- **Automated mitigation**: IP blocking (Redis TTL 15 min), rate limiting, alert broadcasting
- **10-page React dashboard** with live WebSocket visualization
- **Multi-format log ingestion**: Nginx, Express.js Winston JSON, Spring Boot
- **Docker Compose** single-command deployment

---

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
│  │Ingestion │  │  Rules   │  │    ML    │  │Recommendations│  │
│  │  Parser  │  │  Engine  │  │  Engine  │  │    Engine     │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │  Risk    │  │WebSocket │  │  Redis   │  │  PostgreSQL   │  │
│  │ Scoring  │  │ Manager  │  │  Store   │  │     ORM       │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │                              │
    ┌────▼────┐                   ┌─────▼─────┐
    │  Redis  │                   │ PostgreSQL │
    └─────────┘                   └───────────┘
```

### Backend Modules

| Module | Path | Responsibility |
|--------|------|----------------|
| Ingestion | `backend/ingestion/` | Parses raw API logs (Nginx, Winston JSON, Spring Boot) |
| Detection Engine | `backend/detection/` | 7 deterministic cybersecurity rules |
| ML Engine | `backend/ml/` | Isolation Forest anomaly scoring |
| Redis Store | `backend/core/redis_store.py` | Per-IP sliding window counters + IP blocking |
| WebSocket Manager | `backend/core/websocket.py` | Real-time broadcast to dashboard clients |
| Database Layer | `backend/db/` | SQLAlchemy ORM with asyncpg (PostgreSQL) |

---

## Technology Stack

| Layer | Technology | Justification |
|-------|-----------|---------------|
| Backend | Python 3.11 + FastAPI + Uvicorn | Native async, OpenAPI docs, Pydantic validation |
| Frontend | React 18 + Vite + Tailwind CSS | SPA with WebSocket auto-reconnection |
| Cache | Redis 7 | Rich data structures for 5-min sliding windows, TTL-based blocking |
| Database | PostgreSQL 16 | ACID compliance, JSONB flexibility, relational structure |
| ML | Scikit-learn (Isolation Forest, DBSCAN) | Unsupervised, fast inference, no labeled data required |
| Deep Learning | TensorFlow/Keras (Autoencoder) | Reconstruction-error anomaly detection |
| Deployment | Docker + Docker Compose | Single-command deployment, containerized microservices |

---

## Dataset

### Source

The anomaly detection dataset was generated from real-world API access logs collected from **zanbil.ir**, an Iranian e-commerce platform. The logs are publicly available on [Kaggle](https://www.kaggle.com/datasets/eliasdabbas/web-server-access-logs).

### Statistics

| Metric | Value |
|--------|-------|
| Total API requests | 49,456 |
| Unique IP addresses | 2,173 |
| Unique endpoints | 29,886 |
| Time span | ~3 hours (Jan 22, 2019) |
| HTTP methods | GET (98.2%), POST (1.8%) |
| Mean requests per IP | 22.8 |
| Max requests per IP | 6,557 |
| IPs with >100 requests | 47 (2.2%) |
| Bot traffic ratio | 18.3% |
| Mobile traffic ratio | 52.7% |

### 19 Behavioral Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | `request_count` | Total number of requests |
| 2 | `max_req_count_5min` | Maximum requests in any 5-min window |
| 3 | `avg_req_count_5min` | Average requests per 5-min window |
| 4 | `requests_per_second` | Request rate (req/sec) |
| 5 | `avg_time_between_requests` | Mean inter-request time (seconds) |
| 6 | `unique_endpoints` | Number of distinct endpoints accessed |
| 7 | `unique_ids_accessed` | Number of distinct resource IDs |
| 8 | `status_404_count` | Number of 404 responses |
| 9 | `max_error_rate_5min` | Maximum error rate in any 5-min window |
| 10 | `suspicious_ua_ratio` | Ratio of suspicious user agents |
| 11 | `bot_ratio` | Ratio of bot user agents |
| 12 | `mobile_ratio` | Ratio of mobile user agents |
| 13 | `post_frequency` | Ratio of POST requests |
| 14 | `max_repeated_endpoint_hits` | Max hits on a single endpoint |
| 15 | `login_attempt_count` | Number of login attempts |
| 16 | `failed_login_count` | Number of failed logins (401/403) |
| 17 | `failed_login_rate` | Ratio of failed to total login attempts |
| 18 | `max_login_req_per_min` | Max login requests per minute |
| 19 | `avg_time_between_login_attempts` | Mean time between login attempts |

---

## AI Models

Three complementary unsupervised anomaly detection models are implemented:

### Isolation Forest (Primary)

Selected for real-time inference based on:
- **Inference speed**: 0.8 ms per prediction
- **Memory efficiency**: 2.1 MB model size
- **Unsupervised**: No labeled attack data required
- **Explainability**: Path-length-based score interpretable per feature

```python
IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
```

### DBSCAN (Secondary)

Density-based clustering; points in low-density regions labeled as anomalies (`label = -1`).

```python
DBSCAN(eps=0.5, min_samples=5)
```

### Autoencoder (Validation)

Neural network trained to reconstruct input; anomalies detected via high reconstruction error.

Architecture: `[19 → 12 → 8 → 4] → [4 → 8 → 12 → 19]` (ReLU, MSE loss, 50 epochs, batch size 32)

### Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score | Inference (ms) | Memory (MB) |
|-------|----------|-----------|--------|----------|----------------|-------------|
| **Isolation Forest** | **0.91** | **0.90** | **0.89** | **0.89** | **0.8** | **2.1** |
| DBSCAN | 0.88 | 0.87 | 0.86 | 0.86 | 12.4 | 8.7 |
| Autoencoder | 0.90 | 0.89 | 0.88 | 0.88 | 3.2 | 5.4 |

---

## Hybrid Scoring & AHP

### Scoring Formula

```
RiskScore = 0.6 × RuleScore + 0.4 × AIScore
```

Where:
- `RuleScore ∈ [0, 100]` — cumulative score from 7 detection rules
- `AIScore = anomaly_score × 100 ∈ [0, 100]` — normalized Isolation Forest score

### AHP Weight Justification

The 60/40 split is scientifically derived using the **Analytic Hierarchy Process (AHP)** with 5 evaluation criteria:

| Criterion | Weight |
|-----------|--------|
| C1 — Detection Speed | 16.1% |
| C2 — Detection Accuracy | **41.6%** |
| C3 — Explainability | 9.9% |
| C4 — Adaptability | 26.2% |
| C5 — Operational Cost | 6.2% |

**Consistency Ratio: CR = 0.015 < 0.10** — pairwise comparisons are validated and consistent.

| Approach | Weighted Score | Final Weight |
|----------|---------------|--------------|
| Rule-Based | 6.17 | **60%** |
| AI-Based (Isolation Forest) | 5.43 | **40%** |

### Risk Level Classification

| Risk Score | Level | Automated Action |
|-----------|-------|-----------------|
| 0–24 | LOW | Log only |
| 25–49 | MEDIUM | Monitor + soft rate limiting (20 req/min) |
| 50–74 | HIGH | Strict rate limiting (10 req/min) + LLM recommendations |
| 75–100 | CRITICAL | Block IP (Redis TTL 15 min) + Slack alert |

---

## Detection Pipeline

The system operates through a **10-step real-time pipeline**:

| Step | Name | Description |
|------|------|-------------|
| 01 | Request Ingestion | FastAPI receives raw API log via `POST /api/v1/analyze` |
| 02 | Block Check | Redis queried — blocked IPs return 403 immediately |
| 03 | Persistence | Log entry stored in PostgreSQL (`log_entries` table) |
| 04 | Redis Aggregation | Per-IP counters updated in 5-minute sliding window |
| 05 | Rule-Based Detection | 7 deterministic rules evaluated → RuleScore (0–100) |
| 06 | ML Inference | 19-feature vector scored by Isolation Forest → AIScore |
| 07 | Hybrid Scoring | `RiskScore = 0.6 × RuleScore + 0.4 × AIScore` |
| 08 | Action Execution | Action applied based on risk level (log / rate-limit / block) |
| 09 | Threat Persistence | HIGH/CRITICAL events stored with recommendations |
| 10 | WebSocket Broadcast | Threat event sent to all connected dashboard clients |

### Detection Rules

| Attack Type | Trigger Condition | Score Delta |
|-------------|-------------------|-------------|
| Burst | >100 requests in 5-min window | +35 |
| Brute-force | >5 login attempts, >70% failure rate | +45 |
| Endpoint Hammering | >50 requests on ≤2 unique endpoints | +30 |
| Enumeration | >15 consecutive 404 errors | +35 |
| Suspicious User-Agent | Matches bot/scanner pattern | +25 |
| Sensitive Endpoint | /admin, /debug, /.env, /actuator | +20 |
| Injection Payload | SQL/XSS/path traversal in endpoint | +40 |

---

## Dashboard Pages

The React frontend includes 10 pages:

| Page | Description |
|------|-------------|
| Overview | Key metrics (RPM, unique IPs, threats, blocked IPs), attack type breakdown |
| Live Traffic | Real-time WebSocket event stream |
| Threats | Filterable threat event table with severity and AI score |
| Alerts | Actionable alerts with automated recommendations |
| Timeline | Chronological attack visualization |
| Risk Heatmap | IP risk score grid |
| Devices | Device/platform/User-Agent analytics |
| Logs | Raw log browser with pagination |
| Recommendations | Automated defensive advice per attack type |
| Import Logs | Drag-and-drop log file upload |

---

## Installation & Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

### One-Command Deployment

```bash
# 1. Clone the repository
git clone https://github.com/essaidisara/-Mobile-API-Misuse-Detector
cd -Mobile-API-Misuse-Detector

# 2. Copy environment file
cp .env.example .env

# 3. Start all services
docker compose up --build

# 4. Access the dashboard
open http://localhost:3000

# 5. Access API documentation
open http://localhost:8000/docs
```

### Environment Variables

```env
# PostgreSQL
POSTGRES_USER=apidetector
POSTGRES_PASSWORD=your_password
POSTGRES_DB=apidetector

# Redis
REDIS_URL=redis://redis:6379

# FastAPI
SECRET_KEY=your_secret_key
```

### Simulate Attacks (Testing)

```bash
# Run the attack simulation script
python simulate_attacks.ps1

# Or use the realistic simulation
python simulate_realistic_attacks.py
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/analyze` | Analyze a single log entry |
| POST | `/api/v1/logs/upload` | Upload a log file |
| GET | `/api/v1/logs` | Browse log entries |
| GET | `/api/v1/threats` | List threat events |
| GET | `/api/v1/alerts` | List alerts |
| PATCH | `/api/v1/alerts/{id}/acknowledge` | Acknowledge an alert |
| GET | `/api/v1/stats` | Dashboard statistics |
| GET | `/api/v1/stats/heatmap` | Risk heatmap data |
| GET | `/api/v1/stats/timeline` | Attack timeline |
| GET | `/api/v1/ip/{ip}` | IP profile |
| POST | `/api/v1/ip/{ip}/block` | Manually block an IP |
| DELETE | `/api/v1/ip/{ip}/block` | Unblock an IP |
| WS | `/ws/live` | Real-time WebSocket event stream |

---

## Project Structure

```
├── backend/
│   ├── api/routes/          # FastAPI route handlers
│   ├── core/                # Redis store, WebSocket manager
│   ├── db/                  # SQLAlchemy models & database
│   ├── detection/           # Rules engine, scoring, recommendations
│   ├── ingestion/           # Log parser & ingestor
│   ├── ml/                  # Anomaly detection (Isolation Forest)
│   ├── schemas/             # Pydantic schemas
│   └── main.py              # FastAPI app entry point
├── frontend/
│   └── src/
│       ├── api/             # API client
│       ├── components/      # Shared UI components
│       ├── hooks/           # useWebSocket, useFetch
│       └── pages/           # Dashboard pages (10 pages)
├── models/
│   ├── isolation_forest.pkl # Pre-trained Isolation Forest
│   ├── dbscan_scaler.pkl    # DBSCAN StandardScaler
│   └── autoencoder.h5       # Trained Autoencoder
├── data/processed/          # CSV datasets (features, results)
├── tests/                   # Pytest unit tests
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Performance Results

### Anomaly Detection

| Model | F1-Score | Inference Time |
|-------|----------|----------------|
| Isolation Forest | **0.89** | **0.8 ms** |
| Autoencoder | 0.88 | 3.2 ms |
| DBSCAN | 0.86 | 12.4 ms |

### System Scalability

- Tested on 49,456 real API requests (2,173 unique IPs)
- Sub-millisecond inference for real-time scoring
- Containerized microservices for horizontal scalability
- WebSocket alerting latency: < 50 ms

---

## Quality Assurance

SonarQube analysis confirms strong software reliability:

| Metric | Backend (Python) | Frontend (React) | Overall |
|--------|-----------------|-----------------|---------|
| Reliability | A | B | A |
| Security | A | A | A |
| Maintainability | A | B | A |
| Code Duplication | 1.4% | 2.1% | 1.8% |
| Test Coverage | 82% | 74% | 78% |

---

## Comparison with Existing Solutions

| Feature | API Abuse Detector | WAF | SIEM | IDS/IPS | Cloudflare | Datadog |
|---------|:-----------------:|:---:|:----:|:-------:|:----------:|:-------:|
| AI Anomaly Detection | Yes (3 models) | No | Partial | Partial | Partial | Partial |
| Real-time WebSocket | Yes | No | No | No | Yes | Yes |
| AHP Explainability | Yes | No | No | No | No | No |
| Auto IP Blocking | Yes | Yes | No | Yes | Yes | No |
| Open Source | Yes | No | No | Partial | No | No |
| <1ms Inference | Yes | Yes | No | Partial | Yes | No |
| API-Native | Yes | Partial | No | No | Yes | Yes |
| Behavioral Analytics (19 features) | Yes | No | Partial | Partial | No | Partial |
| Automated Recommendations | Yes | No | No | No | No | No |
| Hybrid Rules + ML | Yes | No | No | No | No | No |

---

## Future Work

- Integration of **transformer-based anomaly detection** for complex attack patterns
- **Federated learning** for privacy-preserving threat intelligence sharing
- **Adaptive threshold tuning** using reinforcement learning
- **Kubernetes orchestration** for distributed cloud-native deployment
- **SIEM integration** (Splunk, ELK) via standardized connectors


---

<div align="center">

**API Abuse Detector v4.0** — ENSA Marrakech · 2026  
Elgadaoui Chaimaa · Elkissany Kawtar · Essaidi Sara · Lakbita Khadija  
Supervised by Prof. Mohamed Lachgar  

</div>
