# Geospatial Media Processing API

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458.svg?logo=pandas&logoColor=white)

A backend REST API service built with **FastAPI** and **Pandas** that ingests batches of consecutive GPS-tagged images (`.zip`), extracts EXIF metadata entirely in-memory, and calculates spatial trajectory metrics (distance, velocity, and time intervals) between frames.

## 🚀 Key Features

* **Zero-Disk In-Memory Processing:** Uses Python's `io.BytesIO` and `zipfile` to extract and parse image binary streams directly in RAM, eliminating disk I/O bottlenecks.
* **EXIF Metadata Extraction:** Parses raw DMS (Degrees, Minutes, Seconds) GPS coordinates and timestamps using `ExifRead` and converts them to decimal degrees.
* **Vectorized Spatial Math:** Leverages `Pandas` and `NumPy` to chronologically align frames and apply the Haversine formula across coordinate arrays to compute distance (meters) and velocity (km/h).
* **Automated Validation:** Enforces strict input/output data contracts using `Pydantic` schemas and includes automated endpoint testing via `Pytest`.

## 📂 Project Structure

```text
├── src/
│   ├── main.py                 # FastAPI application entrypoint
│   ├── api/
│   │   ├── routes.py           # REST API endpoints (/process-batch)
│   │   └── schemas.py          # Pydantic response models
│   └── processing/
│       ├── exif_parser.py      # In-memory ZIP & EXIF extraction logic
│       └── spatial_calc.py     # Vectorized Haversine & velocity calculations
├── tests/
│   ├── test_api.py             # FastAPI endpoint integration tests
│   └── test_parser.py          # Unit tests for coordinate conversion
├── Dockerfile                  # Containerization configuration
└── requirements.txt            # Python dependencies
