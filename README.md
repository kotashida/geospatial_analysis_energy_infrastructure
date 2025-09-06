# Geospatial Analysis of U.S. Power Plant Infrastructure

## Project Overview

This project conducts a comprehensive geospatial and statistical analysis of power plant infrastructure across the United States. By leveraging a public dataset of U.S. power plants, it provides insights into the distribution, capacity, and types of energy sources at a state level. The primary outputs include an interactive geospatial map and a statistical bar chart, designed to highlight key trends in energy infrastructure.

This README is designed to showcase the application of quantitative analysis and data visualization skills in a real-world context, making it ideal for review by potential employers.

## Key Features

*   **Interactive Geospatial Map:** A `folium`-based interactive map that visualizes the location of each power plant. Key features include:
    *   **Layered Visualization:** Users can toggle between three distinct views:
        1.  **All Plants:** A general overview of all power plant locations.
        2.  **By Primary Fuel Type:** Power plants are color-coded based on their primary energy source (e.g., Solar, Wind, Natural Gas), allowing for a quick assessment of the energy mix.
        3.  **By Generation Capacity (MW):** A choropleth layer where plant colors correspond to their total megawatt capacity, using a yellow-to-red gradient to indicate low-to-high output.
    *   **Dynamic Legends:** Conditional legends for "By Type" and "By Capacity" layers appear automatically, ensuring a clean and intuitive user interface.
    *   **On-Click Data Pop-ups:** Clicking on a power plant reveals its name, primary fuel type, and total generation capacity in megawatts.

*   **Statistical Bar Chart:** A `matplotlib`-generated bar chart that displays the total number of power plants per state, sorted in descending order to easily identify states with the highest density of energy infrastructure.

## Methodology

The analysis follows a structured data processing and analysis pipeline, emphasizing robust and reproducible methods.

1.  **Data Ingestion & Cleaning:**
    *   The dataset, in GeoJSON format, is loaded into a `geopandas` GeoDataFrame, which provides a powerful, spatially-aware data structure.
    *   **Data Standardization:** Column names are programmatically standardized to a consistent `snake_case` format to facilitate reliable scripting.
    *   **Missing Value Imputation:** A systematic approach is taken to handle missing data. Numerical columns (e.g., `total_mw`) are imputed with `0`, while categorical columns (e.g., `primsource`) are filled with `'Unknown'`. This ensures that no data is lost during aggregation and that statistical summaries are comprehensive.
    *   **Coordinate Reference System (CRS) Validation:** The GeoDataFrame's CRS is validated and programmatically converted to `EPSG:4326` (WGS 84), the standard for global latitude-longitude data, to ensure accurate geospatial plotting.

2.  **Quantitative Analysis:**
    *   **Descriptive Statistics & Aggregation:** The core of the state-level analysis involves a `groupby()` operation on the `state` column. The `.size()` aggregation function is used to count the number of power plants in each state. This is a direct and efficient method for calculating frequency distributions across a key categorical variable.
    *   **Choice of Method:** This aggregation technique was chosen over other methods (like value counts) because it is computationally efficient and integrates seamlessly with the `geopandas` workflow, producing a clean DataFrame ready for visualization.

3.  **Data Visualization:**
    *   **Geospatial Plotting:** The interactive map uses `folium` to plot each power plant's latitude and longitude. The choice of color-mapping for fuel type and capacity was based on established data visualization principles to ensure clarity and accessibility.
    *   **Statistical Charting:** A bar chart was chosen to represent the state-level density as it provides a clear, at-a-glance comparison of counts across discrete categories (states).

## Key Quantitative Skills

This project demonstrates proficiency in the following quantitative and analytical skills:

*   **Statistical Analysis:**
    *   **Descriptive Statistics:** Calculating frequencies and distributions (e.g., power plant counts per state).
    *   **Data Aggregation:** Using `groupby()` operations to summarize data at different geographical scales.

*   **Geospatial Analysis:**
    *   **Coordinate Reference System (CRS) Management:** Understanding and transforming geospatial projections for accurate mapping.
    *   **Spatial Data Visualization:** Plotting and layering point data on interactive maps.

*   **Data Processing & Manipulation:**
    *   **Data Cleaning:** Systematic handling of missing values (imputation) and inconsistent data formats.
    *   **Feature Engineering:** Selecting and preparing relevant data columns for analysis.
    *   **Data Transformation:** Converting data types and standardizing formats for analytical consistency.

*   **Programming & Tooling:**
    *   **Python:** Advanced scripting for data analysis and automation.
    *   **Pandas & GeoPandas:** Expertise in using DataFrame and GeoDataFrame structures for complex data manipulation.
    *   **Matplotlib & Folium:** Proficiency in creating both static and interactive data visualizations.

## How to Run the Project

1.  **Set up the Python environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    pip install -r requirements.txt
    ```

2.  **Download the Data:**
    *   This project uses the "Power Plants in the U.S." dataset from ArcGIS Hub.
    *   Download the GeoJSON file from the [ArcGIS Hub dataset page](https://hub.arcgis.com/datasets/b063316fac7345dba4bae96eaa813b2f/explore).
    *   Save the file as `power_plants.geojson` in the `data/raw/` directory.

3.  **Run the Analysis:**
    ```bash
    python main.py
    ```
    This script will execute the entire pipeline: loading, processing, analyzing the data, and generating the final reports.

4.  **View the Reports:**
    *   **Interactive Map:** Open `reports/power_plants_map.html` in a web browser.
    *   **Bar Chart:** Open `reports/power_plant_density.png` to view the image.

## Running the Tests

To ensure the reliability and correctness of the data pipeline, a suite of automated tests is included. To run them, use `pytest`:

```bash
python -m pytest
```