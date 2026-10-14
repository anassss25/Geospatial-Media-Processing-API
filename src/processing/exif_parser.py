import zipfile
import exifread
from datetime import datetime

def _convert_to_decimal_degrees(dms_values, ref):
    """Converts EXIF DMS (Degrees, Minutes, Seconds) to Decimal Degrees."""
    degrees = float(dms_values.values[0].num) / float(dms_values.values[0].den)
    minutes = float(dms_values.values[1].num) / float(dms_values.values[1].den)
    seconds = float(dms_values.values[2].num) / float(dms_values.values[2].den)
    
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def process_zip_buffer(zip_buffer):
    """Reads a zip file from memory, extracts GPS data from each image."""
    extracted_data = []
    
    with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            # Skip macOS hidden files and directories
            if file_name.startswith('__MACOSX') or file_name.startswith('.') or file_name.endswith('/'):
                continue
                
            # Read image file into memory
            with zip_ref.open(file_name) as file:
                tags = exifread.process_file(file, details=False)
                
                # Check if the photo actually has GPS data
                if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                    lat_dms = tags['GPS GPSLatitude']
                    lat_ref = tags.get('GPS GPSLatitudeRef', 'N').printable
                    lon_dms = tags['GPS GPSLongitude']
                    lon_ref = tags.get('GPS GPSLongitudeRef', 'E').printable
                    
                    # Extract timestamp (fallback to current time if missing)
                    time_str = tags.get('EXIF DateTimeOriginal', str(datetime.now().strftime("%Y:%m:%d %H:%M:%S"))).printable
                    
                    try:
                        timestamp = datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")
                    except ValueError:
                        timestamp = datetime.now()
                    
                    extracted_data.append({
                        "filename": file_name,
                        "timestamp": timestamp,
                        "latitude": _convert_to_decimal_degrees(lat_dms, lat_ref),
                        "longitude": _convert_to_decimal_degrees(lon_dms, lon_ref)
                    })
                    
    return extracted_data