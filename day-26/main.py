import geojson
import random
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geojson import LineString,Feature,FeatureCollection,dump
from datetime import datetime, timedelta
from functions import WGS_to_UTM, route_to_points, get_station_index, set_schedule_dt, route_details
import os
import sys


# Set working directory to the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)  # optional, ensures imports from this folder work

# ---------------------------- RAW INPUTS ---------------------------- #

routes_path = "./routes/cleaned_routes.geojson"
stations_path = "./stations/cleaned_stations.geojson"
schedule_path = "./schedule/qc_bus_schedule_conso.csv"

with open(routes_path, 'r') as route_gdf:
   route_geojson = geojson.load(route_gdf)

with open(stations_path, 'r') as stations_path:
   station_geojson = geojson.load(stations_path)

distance_bw_points = 10

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
   all_routes_gdf.at[idx, "route_points"] = route_to_points(row, distance_bw_points).tolist()
   
   # identify stations along interpolated points via their indices
   stations = station_gdf[station_gdf["route_name"]==route_name]
   station_indices = list(map(int, get_station_index(route_points, stations=stations)))
   all_routes_gdf.at[idx, "station_indices"] = station_indices

# project from UTM back to WGS as Kepler only accepts WGS format
all_routes_gdf = all_routes_gdf.to_crs("EPSG:4326")
station_gdf = station_gdf.to_crs("EPSG:4326")

# ----------------------------- TIMESTAMP ----------------------------- #


bus_schedule_df = pd.read_csv(schedule_path)
arbitrary_date_str = "2025-01-24"
arbitrary_speed = 5.55               # m/s or ~20 kph
time_to_add = distance_bw_points / arbitrary_speed   # add a certain time per meter—the distance b/w each points
load_unload_time = 5 * 60            # 5 minutes -> seconds

features = []
for _, row in bus_schedule_df.iterrows():
   number_of_trips = int(row["num_trips"])
   route_name = row["route_name_py"]

   schedule_interval = row["interval_mins"]
   schedule_day = row["day"]
   schedule_start = row['schedule_start']
   schedule_end = row['schedule_end']

   schedule_start_dt = datetime.strptime(f"{arbitrary_date_str} {schedule_start}:00", "%Y-%m-%d %H:%M:%S")
   schedule_end_dt = datetime.strptime(f"{arbitrary_date_str} {schedule_end}:00", "%Y-%m-%d %H:%M:%S")

   start_timestamp, end_timestamp = set_schedule_dt(day=schedule_day, start_dt=schedule_start_dt, end_dt=schedule_end_dt)

   route_gdf = all_routes_gdf[all_routes_gdf.Name == route_name].iloc[0]
   route_stations = route_gdf.station_indices
   route_points = gpd.GeoDataFrame(route_gdf.route_points, columns=["geometry"], crs="EPSG:32651")
   route_points = route_points.to_crs("EPSG:4326")

   # add timedelta per point (time spent to travel from a point to the next one)
   
   route_points["timedelta"] = route_points.apply(lambda row: load_unload_time if row.name in route_stations else time_to_add, axis=1)
   route_points["cum_time"] = route_points["timedelta"].cumsum()

   for trip_num in range(number_of_trips):
      trip_id = f"{route_name}-{schedule_day}-{trip_num}"
      current_timestamp = start_timestamp + timedelta(minutes=trip_num * schedule_interval)
      route_points["timestamp"] = route_points.apply(lambda x: current_timestamp + timedelta(seconds=x["cum_time"]), axis=1)
      route_points["lon"] = route_points.geometry.x
      route_points["lat"] = route_points.geometry.y
      route_points["z"] = route_details[route_name]["altitude"] * 10 # exaggerate

      route = LineString(list(zip(
            route_points["lon"],
            route_points["lat"],
            route_points["z"],
            route_points["timestamp"].astype("int64")//1000000,
      )))

      features.append(
         Feature(
            geometry=route,
            properties={
               "id": trip_id,
               "route_num": route_details[route_name]["route"], 
               "route_name": route_name,
               "schedule_day": schedule_day,
               "trip_number": trip_num,
            }
         )
      )

feature_collection = FeatureCollection(features)
with open('final.geojson', 'w') as f:
   dump(feature_collection, f)

# ---------------------- PLOT STATIONS + ROUTES ------------------------ #

route_names = route_details.keys()
colors = [route["color"] for _, route in route_details.items()]
print(colors)

# there are two linestrings per route (back and forth) they must be the same colors
color_list  = [x for x in colors for _ in range(2)]
color_map = dict(zip(route_names, color_list))
all_routes_gdf['color'] = all_routes_gdf['Name'].map(color_map)
station_gdf['color'] = station_gdf['route_name'].map(color_map)

fig, ax = plt.subplots()
all_routes_gdf.plot(ax=ax, color=all_routes_gdf['color'], linewidth=1, legend=True)
station_gdf.plot(ax=ax, color=station_gdf['color'], markersize=20)
plt.show()
