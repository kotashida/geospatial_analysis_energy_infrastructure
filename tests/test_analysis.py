import pytest
import geopandas
import pandas as pd
from src.analysis import analyze_power_plant_density

@pytest.fixture
def sample_processed_gdf():
    """
    Provides a sample processed GeoDataFrame for testing analysis functions.
    """
    data = {
        'plant_code': [1, 2, 3, 4, 5],
        'state': ['CA', 'TX', 'CA', 'NY', 'TX'],
        'latitude': [34.05, 32.78, 34.06, 40.71, 32.79],
        'longitude': [-118.25, -96.80, -118.26, -74.00, -96.81]
    }
    geometry = geopandas.points_from_xy(data['longitude'], data['latitude'])
    gdf = geopandas.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")
    return gdf

def test_analyze_power_plant_density(sample_processed_gdf):
    """
    Tests if power plant density is correctly calculated by state.
    """
    density_results = analyze_power_plant_density(sample_processed_gdf)

    assert density_results is not None
    assert isinstance(density_results, pd.DataFrame)
    assert 'state' in density_results.columns
    assert 'plant_count' in density_results.columns

    # Check counts for specific states
    ca_count = density_results[density_results['state'] == 'CA']['plant_count'].iloc[0]
    tx_count = density_results[density_results['state'] == 'TX']['plant_count'].iloc[0]
    ny_count = density_results[density_results['state'] == 'NY']['plant_count'].iloc[0]

    assert ca_count == 2
    assert tx_count == 2
    assert ny_count == 1

def test_analyze_power_plant_density_no_state_column():
    """
    Tests if analyze_power_plant_density handles missing 'state' column.
    """
    data = {
        'plant_code': [1, 2],
        'latitude': [34.05, 32.78],
        'longitude': [-118.25, -96.80]
    }
    geometry = geopandas.points_from_xy(data['longitude'], data['latitude'])
    gdf_no_state = geopandas.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")

    density_results = analyze_power_plant_density(gdf_no_state)
    assert density_results is None
