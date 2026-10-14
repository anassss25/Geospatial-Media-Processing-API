from fastapi import APIRouter, UploadFile, File, HTTPException
import zipfile
import io
import pandas as pd
# Make sure to import your processing functions!
from src.processing.exif_parser import process_zip_buffer
from src.processing.spatial_calc import calculate_trajectory_metrics
from src.api.schemas import ProcessBatchResponse, RouteMetrics

router = APIRouter()

@router.post("/process-batch", response_model=ProcessBatchResponse)
async def process_image_batch(file: UploadFile = File(...)):
    # 1. Validate the file type
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Uploaded file must be a .zip archive")
    
    try:
        # 2. Read file into memory
        contents = await file.read()
        zip_buffer = io.BytesIO(contents)
        
        # 3. Check if it's a valid zip
        if not zipfile.is_zipfile(zip_buffer):
            raise HTTPException(status_code=400, detail="Invalid zip file format")
            
        zip_buffer.seek(0)
        
        # 4. Extract GPS data (this should return a list of dicts)
        extracted_data = process_zip_buffer(zip_buffer)
        
        if not extracted_data:
            raise HTTPException(status_code=422, detail="No valid GPS/EXIF data found in the images.")
            
        # 5. Convert to Pandas and calculate metrics
        df = pd.DataFrame(extracted_data)
        
        # Ensure we have the right columns before doing math
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            raise HTTPException(status_code=422, detail="Missing coordinate data in images.")
            
        metrics_dict, path_preview = calculate_trajectory_metrics(df)
        
        # 6. Return the perfectly formatted Pydantic response
        return ProcessBatchResponse(
            status="success",
            processed_frames=len(extracted_data),
            metrics=RouteMetrics(
                total_distance_meters=metrics_dict.get('total_distance_meters', 0.0),
                total_duration_seconds=metrics_dict.get('total_duration_seconds', 0.0),
                average_velocity_kmh=metrics_dict.get('average_velocity_kmh', 0.0)
            ),
            path_preview=path_preview
        )
        
    except Exception as e:
        # Catch any unexpected errors so they don't crash the server silently
        raise HTTPException(status_code=500, detail=str(e))