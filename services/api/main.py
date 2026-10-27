from fastapi import FastAPI
from services.api.routers import incidents, data_sources

app = FastAPI(title="Deep Lens API", version="1.0.0")

app.include_router(incidents.router)
app.include_router(data_sources.router)

@app.get("/")
def root():
    return {"message": "Deep Lens API is running"}
