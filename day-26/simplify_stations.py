import geojson
import pandas as pd
from functions import route_details

with open('./stations/cleaned_stations.geojson', 'r') as stations:
   stations_geojson = geojson.load(stations)

stations = stations_geojson["features"]

station_list = []
for station in stations:
    route_name = station["properties"]["route_name"]
    route_num = route_details[route_name]["route"]
    lon = station["geometry"]["coordinates"][0]
    lat = station["geometry"]["coordinates"][1]
    station_dict = {
        "route_num": route_num,
        "route_name": route_name,
        "lon": lon,
        "lat": lat
    }
    station_list.append(station_dict)

stations_df = pd.DataFrame(station_list)
print(stations_df.head())

stations_df.to_csv("./stations/simplified_stations.csv")