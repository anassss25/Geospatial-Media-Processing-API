# Geospatial Media Processing API

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458.svg?logo=pandas&logoColor=white)

A backend REST API service built with **FastAPI** and **Pandas** that ingests `.zip` batches of GPS-tagged photos, extracts EXIF metadata entirely in-memory, and calculates spatial trajectory metrics (distance, velocity, and time intervals).

---

## 🛠️ Prerequisites
* **Python 3.10+** installed on your machine
* **Git**

---

## 💻 Step-by-Step Installation

**1. Clone the repository to your computer:**
```bash
git clone [https://github.com/anassss25/Geospatial-Media-Processing-API.git](https://github.com/anassss25/Geospatial-Media-Processing-API.git)
cd Geospatial-Media-Processing-API
```

**2. Create and activate a virtual environment:**
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

**3. Install the required packages:**
```bash
pip install fastapi uvicorn pandas numpy exifread folium python-multipart pydantic pytest httpx
```

---

## 🚀 How to Use the API

**1. Start the local server:**
```bash
uvicorn src.main:app --reload
```

**2. Open the interactive testing dashboard:**
Open your web browser and go to:
```text
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
```

**3. Upload your data:**
1. Prepare a `.zip` file containing original photos taken with GPS/Location enabled on your smartphone or camera.
2. In the Swagger UI dashboard, click on **`POST /api/v1/process-batch`**.
3. Click **Try it out** in the top-right corner of the tab.
4. Click **Choose File**, select your `.zip` archive, and click **Execute**.

**4. Example Response:**
The API will return the calculated distance, duration, average speed, and coordinate path in JSON format:
```json
{
  "status": "success",
  "processed_frames": 5,
  "metrics": {
    "total_distance_meters": 145.2,
    "total_duration_seconds": 65.0,
    "average_velocity_kmh": 8.04
  },
  "path_preview": [
    {
      "timestamp": "2026-10-14 14:32:01",
      "latitude": 51.5132,
      "longitude": 7.4651,
      "velocity_kmh": 0.0
    }
  ]
}
```

---

## 🧪 Running Automated Tests

To verify that the API endpoints and EXIF parser are working properly, run:
```bash
python3 -m pytest
```
