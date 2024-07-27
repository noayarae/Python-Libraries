# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 21:08:44 2024

@author: efrain.noa-yarasca
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


# Read the data
df = pd.read_csv('D:/work/research_t/corn_field/ml_modeling/rgb_7_s.csv', header=0, index_col=0)

# Create a GeoDataFrame
geometry = [Point(xy) for xy in zip(df['LON'], df['LAT'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Check the current CRS
print("Current CRS:", gdf.crs)

# Set the CRS if it's not already set (assuming WGS 84 here)
if gdf.crs is None:
    gdf.set_crs(epsg=4326, inplace=True) # WGS84 Lat & Long in degrees
print("Set CRS:", gdf.crs)

# Transform to another CRS if needed
gdf = gdf.to_crs(epsg=32614)  # Transform to UTM zone 14N for example

# Verify the CRS
print("Transformed CRS:", gdf.crs)


# Extract coordinates and save them as new columns
gdf['long2'] = gdf.geometry.x
gdf['lat2'] = gdf.geometry.y

# Drop the geometry column if you don't need it
gdf = gdf.drop(columns='geometry')

# Save the updated DataFrame to a new CSV file
gdf.to_csv('D:/work/research_t/corn_field/ml_modeling/rgb_7_s_transformed.csv', index=True)

# Verify the new data
print(gdf.head())