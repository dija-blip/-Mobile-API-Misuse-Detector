from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db.database import init_db
from backend.api.routes.analyze import router as analyze_router
from backend.api.routes.logs import router as logs_router
from backend.api.routes.threats import router as threats_router
from backend.api.routes.stats import router as stats_router
from backend.api.routes.ws import router as ws_router

app = FastAPI(title="Mobile API Misuse Detector", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(analyze_router)
app.include_router(logs_router)
app.include_router(threats_router)
app.include_router(stats_router)
app.include_router(ws_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
