import os
import geopandas as gpd
import numpy as np
import enahaplots

def run_gis_solution():
    # Path to the Mauritania Shapefile folder
    path = "mrshape/mrt_admbnda_adm2_ansade_20240327.shp"
    
    if not os.path.exists(path):
        print("Data Error: Ensure 'mrshape' folder is present.")
        return

    # Load data
    gdf = gpd.read_file(path)
    
    # Simulate election results (Column names from notebook)
    gdf['election_results'] = np.random.uniform(5, 95, size=len(gdf))

    print("Generating Ameliorated GIS Map (Cyberpunk Theme)...")
    
    # Execute the solution
    enahaplots.styled_map(
        gdf=gdf,
        column='election_results',
        title="Mauritania Election Narrative 2024",
        style="cyberpunk",
        add_basemap=True,
        save_path="enaha_gis_demo.png"
    )

if __name__ == "__main__":
    run_gis_solution()
