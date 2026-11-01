from fastapi import FastAPI
from datetime import datetime, timezone
from services.api.routers import incidents

app = FastAPI(title="Deep Lens API", version="1.0.0")

app.include_router(incidents.router)

@app.get("/")
def root():
    return {"message": "Deep Lens API is running"}

@app.get("/health")
@app.get("/api/v1/health")
def health_check():
    """
    Health and readiness probe endpoint for Docker healthchecks,
    Kubernetes liveness probes, and monitoring services.
    """
    return {
        "status": "healthy",
        "service": "deep-lens-api",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
