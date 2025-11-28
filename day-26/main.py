import geojson, utm
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
from shapely.geometry import shape, Point, LineString
from shapely.ops import nearest_points

# in EPSG 4326 (Google's default) -> convert it to meters
def WGS_to_UTM(raw_geojson):
    geometry_coords_df = gpd.GeoDataFrame.from_features(raw_geojson)
    geometry_coords_df = geometry_coords_df.set_crs("EPSG:4326")
    geometry_coords_df = geometry_coords_df.to_crs("EPSG:32651")
    return geometry_coords_df

# ---------------------------- RAW INPUTS ---------------------------- #

with open('./routes/route02_from_QCircle.geojson', 'r') as route:
   route_geojson = geojson.load(route)

route_gdf = WGS_to_UTM(route_geojson)

print(route_gdf.head())
print(route_gdf.crs)

# Create linestring from point
linestring = shape(route_gdf.loc[0, "geometry"])

with open('./stations/route02_from_QCircle_station.geojson', 'r') as stations:
   station_geojson = geojson.load(stations)

station_gdf = WGS_to_UTM(station_geojson)
print(station_gdf.head())
print(station_gdf.crs)

# ------------- CONVERT ROUTE TO POINTS EVERY n distance --------------- #
distance = 0        ##  starting at length 0
add_distance = 10   ## interpoalte every 10 meter

print(linestring.length)

list_of_points = []
while distance < linestring.length:
   new_point = linestring.interpolate(distance)
   list_of_points.append(new_point)
   distance += add_distance ## add more

gdf = gpd.GeoDataFrame({
    'geometry': list_of_points
})

# ------------ TAG STATIONS ALONG THE INTERPOLATED POINTS -------------- #
multipoint = gdf.union_all()
print(station_gdf.columns)

station_along_route = [nearest_points(row["geometry"], multipoint)[1] for _, row in station_gdf.iterrows()]
station_along_route_gdf = gpd.GeoDataFrame({
   'geometry': station_along_route
})
print(station_along_route_gdf)

fig, ax = plt.subplots()
route_gdf.plot(ax=ax, color='blue')
station_along_route_gdf.plot(ax=ax, color='red', markersize=40)

plt.show()

# -------------------- PUT STATION to the point ----------------------- #

