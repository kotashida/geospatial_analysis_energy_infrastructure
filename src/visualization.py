import matplotlib.pyplot as plt
import folium
import pandas as pd
import os
import matplotlib.cm as cm
import matplotlib.colors as colors

def plot_power_plant_density(density_df, output_path='reports/power_plant_density.png'):
    """Creates a bar chart showing the number of power plants per state."""
    print("Generating power plant density bar chart...")
    if density_df is not None and not density_df.empty:
        # Sort the data for a cleaner presentation.
        density_df = density_df.sort_values(by='plant_count', ascending=False)
        
        plt.figure(figsize=(12, 6))
        plt.bar(density_df['state'], density_df['plant_count'])
        plt.xlabel('State')
        plt.ylabel('Number of Power Plants')
        plt.title('Number of Power Plants by State')
        plt.xticks(rotation=90)
        plt.tight_layout()
        
        # Make sure the output directory exists.
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        print(f"Power plant density bar chart saved to {output_path}")
    else:
        print("No data to plot for power plant density.")

def create_power_plant_map(gdf, output_path='reports/power_plants_map.html'):
    """Creates an interactive map of power plants with different layers."""
    print(f"Creating combined interactive map of power plant locations...")
    if gdf is None or gdf.empty:
        print("No data to create power plant map.")
        return

    center_lat = gdf['latitude'].mean()
    center_lon = gdf['longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    # --- Layers ---
    default_fg = folium.FeatureGroup(name='All Plants', show=True).add_to(m)
    type_fg = folium.FeatureGroup(name='By Type', show=False).add_to(m)
    capacity_fg = folium.FeatureGroup(name='By Capacity', show=False).add_to(m)

    # --- Populate Layers ---
    type_to_hex_color = {}
    if 'primsource' in gdf.columns:
        # Sort the types alphabetically, but keep 'other' at the end.
        unique_types = sorted([t for t in gdf['primsource'].dropna().unique() if t != 'other'])
        if 'other' in gdf['primsource'].dropna().unique():
            unique_types.append('other')
        type_colormap = cm.get_cmap('tab20', len(unique_types))
        type_to_hex_color = {typ: colors.to_hex(type_colormap(i)) for i, typ in enumerate(unique_types)}

    min_capacity, max_capacity = gdf['total_mw'].min(), gdf['total_mw'].max()
    capacity_colormap = cm.get_cmap('YlOrRd', 256)
    normalize = colors.Normalize(vmin=min_capacity, vmax=max_capacity)

    for idx, row in gdf.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            popup_html = f"<b>{row['plant_name']}</b><br>Type: {row['primsource']}<br>Capacity: {row['total_mw']} MW"
            
            folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=3, color='blue', fill=True, fill_color='blue', fill_opacity=0.7, popup=popup_html).add_to(default_fg)

            if 'primsource' in gdf.columns and row['primsource'] in type_to_hex_color:
                color = type_to_hex_color[row['primsource']]
                folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=3, color=color, fill=True, fill_color=color, fill_opacity=0.7, popup=popup_html).add_to(type_fg)

            if pd.notnull(row['total_mw']):
                capacity_color = colors.to_hex(capacity_colormap(normalize(row['total_mw'])))
                folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=3, color=capacity_color, fill=True, fill_color=capacity_color, fill_opacity=0.7, popup=popup_html).add_to(capacity_fg)

    # --- Legends ---
    type_legend_items = ''.join([f'<div><span style="background-color:{{color}}; width: 15px; height: 15px; display: inline-block; border: 1px solid grey; vertical-align: middle;"></span>&nbsp;{{typ}}</div>'.format(color=color, typ=typ) for typ, color in type_to_hex_color.items()])
    type_legend_html = f'''<div id="legend-type" style="display:none; width: 180px; font-size:14px; background-color:rgba(255,255,255,0.85); padding: 10px; border-radius: 5px; border:1px solid grey;"><b>Power Plant Types</b><br>{type_legend_items}</div>'''

    gradient_colors_css = ', '.join([colors.to_hex(cm.get_cmap('YlOrRd')(i/255.0)) for i in range(256)])
    gradient_bar_html = f'<div style="background: linear-gradient(to right, {gradient_colors_css}); height: 10px; width: 100%; border-radius: 3px;"></div>'
    capacity_legend_html = f'''<div id="legend-capacity" style="display:none; width: 150px; font-size:12px; background-color:rgba(255,255,255,0.85); padding: 5px; border-radius: 5px; border:1px solid grey; margin-bottom: 10px;"><b>Capacity (MW)</b>{gradient_bar_html}<div style="display: flex; justify-content: space-between; font-size: 10px;"><span>{min_capacity:.0f}</span><span>{max_capacity:.0f}</span></div></div>'''

    legends_container_html = f'''<div style="position: fixed; bottom: 20px; left: 20px; z-index:9998;">{capacity_legend_html}{type_legend_html}</div>'''
    m.get_root().html.add_child(folium.Element(legends_container_html))

    # --- Layer Control ---
    folium.LayerControl(position='topleft', collapsed=False).add_to(m)

    # --- Custom JS & CSS ---
    # This script handles the radio button behavior and shows/hides the legends.
    map_id = m.get_name()
    custom_js_css = f"""
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const map = window['{map_id}'];
        const controlContainer = document.querySelector('.leaflet-control-layers-overlays');
        if (!map || !controlContainer) return;

        const mainInputs = Array.from(controlContainer.querySelectorAll('input.leaflet-control-layers-selector'));
        const legendType = document.getElementById('legend-type');
        const legendCapacity = document.getElementById('legend-capacity');

        function updateUI() {{
            const selectedInput = mainInputs.find(input => input.checked);
            if (!selectedInput) return;
            const layerName = selectedInput.parentElement.innerText.trim();

            if(legendType) legendType.style.display = (layerName === 'By Type') ? 'block' : 'none';
            if(legendCapacity) legendCapacity.style.display = (layerName === 'By Capacity') ? 'block' : 'none';
        }}

        mainInputs.forEach(input => {{
            input.type = 'radio';
            input.name = 'folium-layer-group';
            input.addEventListener('click', updateUI);
        }});

        if (mainInputs.length > 0 && !mainInputs.some(i => i.checked)) mainInputs[0].checked = true;
        updateUI();
    }});
    </script>
    <style>
        .leaflet-control-layers-selector[name="folium-layer-group"] {{ -webkit-appearance: radio !important; -moz-appearance: radio !important; appearance: radio !important; }}
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_js_css))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    m.save(output_path)
    print(f"Interactive map saved to {output_path}")


