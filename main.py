import os
import pandas as pd
from src.data_ingestion import load_local_geojson
from src.data_processing import process_power_plants_data, inspect_gdf_columns
from src.analysis import analyze_power_plant_density
from src.visualization import plot_power_plant_density, create_power_plant_map

if __name__ == "__main__":
    print("Geospatial Analysis of Energy Infrastructure project started.")

    data_directory = "data/raw"
    file_name = "power_plants.geojson"
    file_path = os.path.join(data_directory, file_name)

    # Create the data directory if it doesn't already exist.
    os.makedirs(data_directory, exist_ok=True)

    # Create the reports directory if it doesn't already exist.
    reports_directory = "reports"
    os.makedirs(reports_directory, exist_ok=True)

    # Load the power plant data from the GeoJSON file.
    power_plants_gdf = load_local_geojson(file_path)

    if power_plants_gdf is not None:
        print("Power plant data loaded successfully.")
        print(f"Number of power plants: {len(power_plants_gdf)}")
        print("First 5 rows of the GeoDataFrame:")
        print(power_plants_gdf.head())

        # Display the columns of the GeoDataFrame.
        inspect_gdf_columns(power_plants_gdf)

        # Clean and prepare the data for analysis.
        processed_gdf = process_power_plants_data(power_plants_gdf)
        print("Data processing complete.")

        # Perform the analysis.
        if processed_gdf is not None:
            density_results = analyze_power_plant_density(processed_gdf)
            if density_results is not None:
                print("Analysis complete.")
                
                # Create and save the visualizations.
                plot_power_plant_density(density_results)
                create_power_plant_map(processed_gdf, output_path='reports/power_plants_map.html')
                print("Visualizations generated.")

            else:
                print("Analysis failed.")
        else:
            print("Skipping analysis due to processing failure.")

    else:
        print("Failed to load power plant data. Please ensure 'power_plants.geojson' is in 'data/raw'.")
