import geopandas as gpd
import pandas as pd
import requests
import zipfile
import io
from datetime import datetime

# USDM weekly shapefile URL (latest week)
url = "https://droughtmonitor.unl.edu/data/shapefiles_m/USDM_current_M.zip"

# Download ZIP
response = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(response.content))

# Extract to raw folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
raw_path = f"../data_raw/usdm_raw_{timestamp}"
z.extractall(raw_path)

# Find the .shp file
shp_file = [f for f in z.namelist() if f.endswith(".shp")][0]
shp_path = f"{raw_path}/{shp_file.split('/')[-1]}"

# Load shapefile
gdf = gpd.read_file(shp_path)

# Keep only fields that exist
keep_fields = ["DM", "geometry"]
gdf = gdf[[c for c in keep_fields if c in gdf.columns]]

# Rename for consistency
gdf = gdf.rename(columns={"DM": "drought_level"})

# Save processed GeoJSON
processed_path = f"../data_processed/usdm_{timestamp}.geojson"
gdf.to_file(processed_path, driver="GeoJSON")

print("USDM drought data successfully downloaded and processed.")