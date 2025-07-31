import pytest
import geopandas
import pandas as pd
import os
from src.visualization import plot_power_plant_density, create_power_plant_map

@pytest.fixture
def sample_density_df():
    """
    Provides a sample DataFrame for testing density plotting.
    """
    data = {'state': ['CA', 'TX', 'NY'], 'plant_count': [100, 75, 50]}
    df = pd.DataFrame(data)
    return df

@pytest.fixture
def sample_processed_gdf():
    """
    Provides a sample processed GeoDataFrame for testing map creation.
    """
    data = {
        'plant_name': ['Plant A', 'Plant B', 'Plant C'],
        'primsource': ['Solar', 'Wind', 'Coal'],
        'total_mw': [100, 150, 200],
        'latitude': [34.05, 32.78, 40.71],
        'longitude': [-118.25, -96.80, -74.00]
    }
    geometry = geopandas.points_from_xy(data['longitude'], data['latitude'])
    gdf = geopandas.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")
    return gdf

def test_plot_power_plant_density(sample_density_df, tmp_path):
    """
    Tests if the density plot is generated and saved.
    """
    output_path = tmp_path / "power_plant_density.png"
    plot_power_plant_density(sample_density_df, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0 # Check if file is not empty

def test_create_power_plant_map(sample_processed_gdf, tmp_path):
    """
    Tests if the interactive map is generated and saved.
    """
    output_path = tmp_path / "power_plants_map.html"
    create_power_plant_map(sample_processed_gdf, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0 # Check if file is not empty
