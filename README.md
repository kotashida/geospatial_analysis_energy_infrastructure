# Geospatial Analysis of U.S. Power Plants

This project analyzes the distribution and capacity of power plants across the United States. It uses a dataset of U.S. power plants to generate an interactive map and a bar chart that visualize the density of power plants by state.

## Features

*   **Interactive Map:** An interactive map that displays the location of each power plant. The map includes the following features:
    *   **Layer Control:** Switch between different map layers to visualize the data in various ways:
        *   **All Plants:** A default view that shows all power plants with a single color.
        *   **By Type:** Colors the power plants based on their primary energy source (e.g., solar, wind, natural gas).
        *   **By Capacity:** Colors the power plants based on their total capacity, using a gradient from yellow (low capacity) to red (high capacity).
    *   **Conditional Legends:** Legends for the "By Type" and "By Capacity" layers automatically appear when the corresponding layer is selected.
    *   **Pop-ups:** Click on a power plant to see its name, type, and capacity.
*   **Bar Chart:** A bar chart that shows the number of power plants in each state.

## How to Run the Project

1.  **Set up the Python environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    pip install -r requirements.txt
    ```

2.  **Download the Data:**
    *   This project uses the "Power Plants in the U.S." dataset from ArcGIS Hub. You will need to download it manually.
    *   Go to the [ArcGIS Hub dataset page](https://hub.arcgis.com/datasets/b063316fac7345dba4bae96eaa813b2f/explore).
    *   Download the GeoJSON file and save it as `power_plants.geojson` in the `data/raw/` directory.

3.  **Run the Analysis:**
    ```bash
    python main.py
    ```
    This will load, process, and analyze the data, and then generate the map and bar chart.

4.  **View the Reports:**
    *   **Interactive Map:** Open `reports/power_plants_map.html` in your web browser.
    *   **Bar Chart:** Open `reports/power_plant_density.png` to view the bar chart.

## Running the Tests

To run the automated tests, use the following command:

```bash
python -m pytest
```
