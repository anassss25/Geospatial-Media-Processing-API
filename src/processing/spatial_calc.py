import pandas as pd
import numpy as np

def calculate_trajectory_metrics(df: pd.DataFrame):
    """Calculates distances and velocities between consecutive GPS points."""
    # Ensure chronological order
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    # Haversine formula vectorized in Pandas
    R = 6371000 # Earth radius in meters
    
    # Convert coordinates to radians
    lat1 = np.radians(df['latitude'].shift(1))
    lon1 = np.radians(df['longitude'].shift(1))
    lat2 = np.radians(df['latitude'])
    lon2 = np.radians(df['longitude'])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    
    # Calculate distance in meters
    df['distance_m'] = R * c
    df['distance_m'] = df['distance_m'].fillna(0)
    
    # Calculate time difference in seconds
    df['time_diff_s'] = df['timestamp'].diff().dt.total_seconds()
    df['time_diff_s'] = df['time_diff_s'].fillna(0)
    
    # Calculate velocity (km/h) safely (avoid division by zero)
    df['velocity_kmh'] = np.where(
        df['time_diff_s'] > 0, 
        (df['distance_m'] / df['time_diff_s']) * 3.6, 
        0
    )
    
    # Aggregate final metrics
    metrics = {
        "total_distance_meters": round(df['distance_m'].sum(), 2),
        "total_duration_seconds": round(df['time_diff_s'].sum(), 2),
        "average_velocity_kmh": round(df['velocity_kmh'].mean(), 2) if not df.empty else 0.0
    }
    
    # Format the preview path for the API response
    # Convert timestamps back to strings for JSON serialization
    df['timestamp'] = df['timestamp'].astype(str)
    path_preview = df[['timestamp', 'latitude', 'longitude', 'velocity_kmh']].to_dict(orient='records')
    
    return metrics, path_preview