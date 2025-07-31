import os
import pytest
from src.data_ingestion import load_local_geojson

# Define the path to the test GeoJSON file
TEST_DATA_DIR = "data/raw"
TEST_FILE_NAME = "power_plants.geojson"
TEST_FILE_PATH = os.path.join(TEST_DATA_DIR, TEST_FILE_NAME)

@pytest.fixture(scope="module")
def setup_test_data():
    """
    Fixture to ensure the test GeoJSON file exists for testing.
    In a real scenario, you might create a dummy file here.
    For this project, we assume the user has manually placed the file.
    """
    if not os.path.exists(TEST_FILE_PATH):
        # This is a placeholder. In a robust test, you'd create a minimal dummy GeoJSON.
        # For now, we'll just print a message if the file is missing.
        print(f"Warning: Test file {TEST_FILE_PATH} not found. Please ensure it exists for tests to pass.")
        pytest.skip(f"Test file {TEST_FILE_PATH} not found.")

def test_load_local_geojson_success(setup_test_data):
    """
    Tests if load_local_geojson successfully loads a valid GeoJSON file.
    """
    gdf = load_local_geojson(TEST_FILE_PATH)
    assert gdf is not None
    assert not gdf.empty
    assert 'geometry' in gdf.columns

def test_load_local_geojson_file_not_found():
    """
    Tests if load_local_geojson handles a non-existent file gracefully.
    """
    non_existent_path = "non_existent_file.geojson"
    gdf = load_local_geojson(non_existent_path)
    assert gdf is None
