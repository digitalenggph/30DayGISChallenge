import geojson
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiPoint, Point
from functions import WGS_to_UTM, route_to_points, get_station_index


# ---------------------------- RAW INPUTS ---------------------------- #

routes_path = "./routes/cleaned_routes.geojson"
stations_path = "./stations/cleaned_stations.geojson"

with open(routes_path, 'r') as route:
   route_geojson = geojson.load(route)

with open(stations_path, 'r') as stations_path:
   station_geojson = geojson.load(stations_path)

# ----------------------------- TRANSFORM ----------------------------- #

# project from WGS84 to UTM 51N
route_gdf = WGS_to_UTM(route_geojson)
station_gdf = WGS_to_UTM(station_geojson)

routes = route_gdf["Name"].unique()
"""
'Route 1 - from QC Hall'   'Route 1 - to QC Hall' 
'Route 5 - to QC Hall'  'Route 5 - from QC Hall' 'Route 2 - to QC Hall' 'Route 2 - from QC Hall'
 'Route 7 - from QC Hall' 'Route 7 - to QC Hall' 'Route 8 - from QC Hall'
 'Route 8 - to QC Hall' 'Route 3 - to LRT Katipunan'
 'Route 3 - from LRT Katipunan' 'Route 4 - from QC Hall'
 'Route 4 - to QC Hall' 'Route 6 - from QC Hall' 'Route 6 - to QC Hall']
 """

for route_name in routes:
   print(route_name)
   # iterate points every 10 meters
   route = route_gdf[route_gdf["Name"] == route_name]
   route_points_gdf = route_to_points(route, 10)
   
   # tag stations along interpolated points
   stations = station_gdf[station_gdf["route_name"]==route_name]
   station_indices = list(map(int, get_station_index(route_points_gdf, stations=stations)))
   print(station_indices)

# ------------ TAG STATIONS ALONG THE INTERPOLATED POINTS -------------- #

fig, ax = plt.subplots()
route_gdf.plot(ax=ax, color='blue', linewidth=2)
# station_along_route_gdf.plot(ax=ax, color='red', markersize=40)

plt.show()

# -------------------- PUT STATION to the point ----------------------- #

