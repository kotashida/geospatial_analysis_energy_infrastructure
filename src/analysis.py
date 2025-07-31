import geopandas

def analyze_power_plant_density(gdf):
    """Calculates the number of power plants in each state."""
    print("Performing geospatial analysis: Power plant density...")

    # Group by state and count the number of power plants.
    if 'state' in gdf.columns:
        state_density = gdf.groupby('state').size().reset_index(name='plant_count')
        print("Power plant count by state (first 5 rows):")
        print(state_density.head())
        return state_density
    else:
        print("'state' column not found for density analysis.")
        return None
