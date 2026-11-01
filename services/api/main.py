from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.api.routers import incidents

app = FastAPI(title="Deep Lens API", version="1.0.0")

# Configure Cross-Origin Resource Sharing (CORS) for web client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incidents.router)

@app.get("/")
def root():
    return {"message": "Deep Lens API is running"}
