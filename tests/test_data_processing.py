import pytest
import geopandas
import pandas as pd
from src.data_processing import process_power_plants_data

@pytest.fixture
def sample_gdf():
    """
    Provides a sample GeoDataFrame for testing data processing functions.
    """
    data = {
        'Plant Code': [1, 2, 3],
        'Plant.Name': ['Plant A', 'Plant B', 'Plant C'],
        'Install_MW': [100, None, 200],
        'Total_MW': [150, 250, None],
        'State': ['CA', 'TX', 'NY'],
        'Latitude': [34.05, 32.78, 40.71],
        'Longitude': [-118.25, -96.80, -74.00]
    }
    geometry = geopandas.points_from_xy(data['Longitude'], data['Latitude'])
    gdf = geopandas.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")
    return gdf

def test_column_standardization(sample_gdf):
    """
    Tests if column names are correctly standardized to snake_case.
    """
    processed_gdf = process_power_plants_data(sample_gdf.copy())
    expected_columns = [
        'plant_code', 'plant_name', 'install_mw', 'total_mw', 'state',
        'latitude', 'longitude', 'geometry'
    ]
    assert all(col in processed_gdf.columns for col in expected_columns)
    assert 'Plant Code' not in processed_gdf.columns
    assert 'Plant.Name' not in processed_gdf.columns

def test_missing_value_handling(sample_gdf):
    """
    Tests if missing numerical and categorical values are handled.
    """
    gdf_with_missing = sample_gdf.copy()
    gdf_with_missing.loc[0, 'State'] = None # Introduce a missing categorical value
    
    processed_gdf = process_power_plants_data(gdf_with_missing)
    
    # Check if numerical NaNs are filled with 0
    assert processed_gdf['install_mw'].isnull().sum() == 0
    assert processed_gdf['total_mw'].isnull().sum() == 0
    
    # Check if categorical NaNs are filled with 'Unknown'
    assert processed_gdf.loc[0, 'state'] == 'Unknown'

def test_crs_conversion():
    """
    Tests if CRS conversion works correctly.
    """
    # Create a GeoDataFrame with a different CRS (e.g., EPSG:3857 - Web Mercator)
    data = {
        'name': ['Point1'],
        'geometry': [geopandas.points_from_xy([0], [0], crs="EPSG:3857")[0]]
    }
    gdf_mercator = geopandas.GeoDataFrame(data, crs="EPSG:3857")

    processed_gdf = process_power_plants_data(gdf_mercator.copy())
    assert processed_gdf.crs == "EPSG:4326"

def test_feature_selection(sample_gdf):
    """
    Tests if only relevant features are selected.
    """
    processed_gdf = process_power_plants_data(sample_gdf.copy())
    # Check if the number of columns is as expected after selection
    # This test assumes a fixed set of selected columns in process_power_plants_data
    # Adjust expected_num_columns if the selection logic changes
    expected_num_columns = 8 # Based on the selected_columns in data_processing.py for the sample_gdf
    assert len(processed_gdf.columns) == expected_num_columns
    assert 'FID' not in processed_gdf.columns # Example of a column that should be dropped