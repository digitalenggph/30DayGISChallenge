import geojson
import random
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiPoint, Point
from functions import WGS_to_UTM, route_to_points, get_station_index


# ---------------------------- RAW INPUTS ---------------------------- #

routes_path = "./routes/cleaned_routes.geojson"
stations_path = "./stations/cleaned_stations.geojson"

with open(routes_path, 'r') as route_gdf:
   route_geojson = geojson.load(route_gdf)

with open(stations_path, 'r') as stations_path:
   station_geojson = geojson.load(stations_path)

# ----------------------------- TRANSFORM ----------------------------- #

# project from WGS84 to UTM 51N
all_routes_gdf = WGS_to_UTM(route_geojson)
station_gdf = WGS_to_UTM(station_geojson)

all_routes_gdf["route_points"] = None
all_routes_gdf["station_indices"] = None

for idx, row in all_routes_gdf.iterrows():
   route_name = row["Name"]

   # iterate points every 10 meters
   route_points = route_to_points(row, 10)
   all_routes_gdf.at[idx, "route_points"] = route_to_points(row, 10).tolist()
   
   # identify stations along interpolated points via their indices
   stations = station_gdf[station_gdf["route_name"]==route_name]
   station_indices = list(map(int, get_station_index(route_points, stations=stations)))
   all_routes_gdf.at[idx, "station_indices"] = station_indices

print(all_routes_gdf.head())

# ---------------------- PLOT STATIONS + ROUTES ------------------------ #

route_names = all_routes_gdf.Name.unique()
colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(8)]

# there are two linestrings per route (back and forth) they must be the same colors
color_list  = [x for x in colors for _ in range(2)]
color_map = dict(zip(route_names, color_list))
all_routes_gdf['color'] = all_routes_gdf['Name'].map(color_map)
station_gdf['color'] = station_gdf['route_name'].map(color_map)

fig, ax = plt.subplots()
all_routes_gdf.plot(ax=ax, color=all_routes_gdf['color'], linewidth=1, legend=True)
station_gdf.plot(ax=ax, color=station_gdf['color'], markersize=20)
plt.show()
