import geopandas
import pandas as pd

def process_power_plants_data(gdf):
    """Cleans and prepares the power plant GeoDataFrame for analysis."""
    print("Processing power plant data...")

    # Standardize column names to a consistent format (e.g., lowercase_with_underscores).
    original_columns = gdf.columns
    new_columns = []
    for col in original_columns:
        new_col = col.replace(' ', '_').replace('.', '_').lower()
        new_columns.append(new_col)
    gdf.columns = new_columns
    print("Standardized column names.")

    # Handle any missing values.
    print("Missing values before handling:")
    missing_values = gdf.isnull().sum()
    print(missing_values[missing_values > 0])

    # A simple strategy for now: fill missing numbers with 0 and text with 'Unknown'.
    # This might need to be adjusted depending on the data.
    for col in gdf.columns:
        if gdf[col].dtype in ['int64', 'float64']:
            gdf[col] = gdf[col].fillna(0)
        elif gdf[col].dtype == 'object':
            gdf[col] = gdf[col].fillna('Unknown')
    print("Filled missing values.")

    # Ensure all capacity columns are numeric.
    mw_columns = [col for col in gdf.columns if '_mw' in col]
    for col in mw_columns:
        if col in gdf.columns:
            gdf[col] = pd.to_numeric(gdf[col], errors='coerce').fillna(0)
    print("Converted MW columns to numeric.")

    # Check if the coordinate reference system (CRS) is set to EPSG:4326.
    if gdf.crs is None or gdf.crs.to_epsg() != 4326:
        print(f"Original CRS: {gdf.crs}. Converting to EPSG:4326...")
        gdf = gdf.to_crs(epsg=4326)
        print("CRS converted to EPSG:4326.")
    else:
        print(f"CRS is already EPSG:4326 ({gdf.crs}). No conversion needed.")

    # Select a subset of columns for the analysis.
    selected_columns = [
        'plant_code',
        'plant_name',
        'utility_id',
        'utility_na',
        'sector_nam',
        'street_add',
        'city',
        'county',
        'state',
        'zip',
        'primsource',
        'source_des',
        'tech_desc',
        'install_mw',
        'total_mw',
        'bat_mw',
        'bio_mw',
        'coal_mw',
        'geo_mw',
        'hydro_mw',
        'hydrops_mw',
        'ng_mw',
        'nuclear_mw',
        'crude_mw',
        'solar_mw',
        'wind_mw',
        'other_mw',
        'source',
        'period',
        'longitude',
        'latitude',
        'geometry'
    ]
    # Make sure to only keep columns that actually exist in the GeoDataFrame.
    selected_columns = [col for col in selected_columns if col in gdf.columns]
    gdf = gdf[selected_columns]
    print("Selected relevant features.")

    return gdf

def inspect_gdf_columns(gdf):
    """A helper function to print the columns of a GeoDataFrame."""
    print("GeoDataFrame Columns:")
    for col in gdf.columns:
        print(f"- {col}")
