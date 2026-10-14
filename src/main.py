from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="Geospatial Media Processing API",
    description="Backend service for extracting and aligning GPS metadata.",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "service": "geospatial-media-api"}