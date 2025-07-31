import geopandas
import os

def load_local_geojson(file_path):
    """Loads a GeoJSON file into a GeoDataFrame."""
    print(f"Attempting to load GeoJSON data from: {file_path}")
    try:
        gdf = geopandas.read_file(file_path)
        print(f"Successfully loaded data from {file_path}")
        return gdf
    except Exception as e:
        print(f"Error loading GeoJSON data from {file_path}: {e}")
        return None

# This allows the script to be run directly for testing.
if __name__ == "__main__":
    # The raw data is expected to be in the data/raw directory.
    data_dir = "..\data\raw"
    file_name = "power_plants.geojson"
    file_path = os.path.join(os.path.dirname(__file__), data_dir, file_name)
    
    if os.path.exists(file_path):
        gdf = load_local_geojson(file_path)
        if gdf is not None:
            print(f"Loaded GeoDataFrame with {len(gdf)} features.")
            print(gdf.head())
    else:
        print(f"File not found: {file_path}. Please ensure it's downloaded manually.")