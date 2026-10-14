import folium
import pandas as pd

def generate_route_map(df: pd.DataFrame) -> str:
    """
    Takes a trajectory DataFrame and generates an interactive HTML map.
    Returns the raw HTML string so the FastAPI endpoint can serve it directly.
    """
    if df.empty:
        return "<p>No spatial data available to map.</p>"

    # Center the map on the very first extracted coordinate
    start_lat = df.iloc[0]['latitude']
    start_lon = df.iloc[0]['longitude']
    
    m = folium.Map(location=[start_lat, start_lon], zoom_start=15)

    # Extract all coordinate pairs to draw the continuous path
    coordinates = list(zip(df['latitude'], df['longitude']))
    
    # Draw the trajectory line
    folium.PolyLine(
        coordinates,
        weight=4,
        color='blue',
        opacity=0.8,
        tooltip="Camera Path"
    ).add_to(m)

    # Add explicit markers for the start and end of the batch
    folium.Marker(coordinates[0], popup="Start Point", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(coordinates[-1], popup="End Point", icon=folium.Icon(color='red')).add_to(m)

    # Render to HTML string
    return m.get_root().render()