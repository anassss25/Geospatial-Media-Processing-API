# Geospatial Media Processing API
A REST API backend service that ingests consecutive GPS-tagged images, parses the EXIF metadata entirely in-memory, and uses Pandas vectorization to calculate spatial trajectory metrics.

## Local Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `uvicorn src.main:app --reload`
3. Test via Swagger UI at `http://127.0.0.1:8000/docs`
