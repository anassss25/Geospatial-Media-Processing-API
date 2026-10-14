import io
import zipfile
from fastapi.testclient import TestClient
from src.main import app

# This creates a simulated client that bypasses the need to actually run the server on a port
client = TestClient(app)

def test_health_check():
    """Ensure the API boots up and the health endpoint is reachable."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "geospatial-media-api"}

def test_process_batch_invalid_file_type():
    """Ensure the API rejects non-zip files immediately."""
    # Simulate an uploaded text file
    files = {"file": ("test_image.txt", b"this is not an image", "text/plain")}
    response = client.post("/api/v1/process-batch", files=files)
    
    assert response.status_code == 400
    assert "must be a .zip archive" in response.json()["detail"]

def test_process_batch_empty_zip():
    """Ensure the API gracefully handles valid zip files that contain no valid GPS images."""
    # Generate an empty zip file entirely in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        pass 
    zip_buffer.seek(0)
    
    # Send the in-memory zip to the endpoint
    files = {"file": ("empty.zip", zip_buffer, "application/zip")}
    response = client.post("/api/v1/process-batch", files=files)
    
    # Should return a 422 Unprocessable Entity because the data pipeline failed safely
    assert response.status_code == 422
    assert "No valid GPS/EXIF data found" in response.json()["detail"]