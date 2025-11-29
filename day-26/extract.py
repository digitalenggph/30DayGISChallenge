import geopandas as gpd 
import pandas as pd
import fiona
import os
from shapely.ops import linemerge
import matplotlib.pyplot as plt

kml_files = os.listdir("./kml")
columns = ["Name", "geometry"]
spliced_routes = [ # google my maps only allows 10 stops per routes so some routes has to be split
                   # spliced parts are indicated by (A) & (B)
    "Route 3 - to LRT Katipunan",
    "Route 3 - from LRT Katipunan",
    "Route 4 - from QC Hall",
    "Route 4 - to QC Hall",
    "Route 6 - from QC Hall",
    "Route 6 - to QC Hall",
]

# --------------------------------- GET ALL ROUTES & ROUTES --------------------------------- #

routes_list = []
stations_gdf = gpd.GeoDataFrame()

for kml in kml_files:
    kml_path = os.path.join("./kml", kml)
    layers = fiona.listlayers(kml_path)

    for layer in layers:
        # a layer contains a route and its corresponding stations
        geo_df = gpd.read_file(kml_path, layer=layer, columns=columns)
        geo_df["type"] = geo_df.geometry.type

        # route
        route_row = geo_df[geo_df["type"]=="LineString"].drop(["type"], axis=1)
        route_data = route_row.iloc[0].to_dict()
        routes_list.append(route_data)

        # stations
        stations_rows = geo_df[geo_df["type"]=="Point"].drop(["type"], axis=1)
        stations_rows["route_name"] = route_data["Name"]
        stations_gdf = pd.concat([stations_gdf,stations_rows], ignore_index=True)

routes_gdf = gpd.GeoDataFrame(routes_list, geometry="geometry")
# print(stations_gdf.head(20))

# ----------------------------- PROCESS SPLICED ROUTES & STATIONS ----------------------------- #

# get routes that doesn't need to be processed
simplified_routes_gdf = routes_gdf[~routes_gdf["Name"].str.contains("|".join(spliced_routes))]
simplified_stations_gdf = stations_gdf[~stations_gdf["route_name"].str.contains("|".join(spliced_routes))]

spliced_routes_list = []
cleaned_stations_gdf = simplified_stations_gdf.copy()

for spliced_route in spliced_routes:
    filtered_routes_gdf = routes_gdf[routes_gdf["Name"].str.contains(spliced_route)]
    filtered_stations_gdf = stations_gdf[stations_gdf["route_name"].str.contains(spliced_route)]

    # get lines
    lineA = filtered_routes_gdf[filtered_routes_gdf["Name"].str.contains(r"\(A\)")].iloc[0]["geometry"]
    lineB = filtered_routes_gdf[filtered_routes_gdf["Name"].str.contains(r"\(B\)")].iloc[0]["geometry"]

    # merge them
    merged_line_data = {
        "Name": spliced_route,
        "geometry": linemerge([lineA, lineB])
    }

    spliced_routes_list.append(merged_line_data)

    # get stations
    stationsA = filtered_stations_gdf[filtered_stations_gdf["route_name"].str.contains(r"\(A\)")]
    stationsB = filtered_stations_gdf[filtered_stations_gdf["route_name"].str.contains(r"\(B\)")]

    # path A's last station is path B's first station -> delete path B's first station to avoid duplicates

    merged_station_data = pd.concat([stationsA, stationsB.iloc[1:]], ignore_index=True)
    merged_station_data["route_name"] = spliced_route
    cleaned_stations_gdf = pd.concat([cleaned_stations_gdf, merged_station_data])

    print(spliced_route)
    print(stationsA.tail())
    print(stationsB.head())
    print(merged_station_data.head(20))

# convert list of dicts to geodataframe -> merge with simplified routes
spliced_routes_gdf = gpd.GeoDataFrame(spliced_routes_list, geometry="geometry")
cleaned_routes_gdf = pd.concat([simplified_routes_gdf, spliced_routes_gdf], ignore_index=True)

print(cleaned_routes_gdf.head())
print(cleaned_stations_gdf.head())

fig, ax = plt.subplots()
cleaned_routes_gdf.plot(ax=ax, color='blue', linewidth=2)
cleaned_stations_gdf.plot(ax=ax, color='red', markersize=40)

cleaned_routes_gdf.to_file("./routes/cleaned_routes.geojson", driver="GeoJSON")
cleaned_stations_gdf.to_file("./stations/cleaned_stations.geojson", driver="GeoJSON")
plt.show()
