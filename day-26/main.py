import geojson, utm
import pandas as pd
import geopandas as gpd
import shapely
from shapely.geometry import shape, Point, LineString


# ---------------------------- RAW INPUTS ---------------------------- #

with open('./routes/route02_from_QCircle.geojson', 'r') as sample:
   geojson_raw = geojson.load(sample)

# in EPSG 4326 (Google's default) -> convert it to meters
geometry_coords_df = gpd.GeoDataFrame.from_features(geojson_raw)
geometry_coords_df = geometry_coords_df.set_crs("EPSG:4326")
geometry_coords_df = geometry_coords_df.to_crs("EPSG:32651")
print(geometry_coords_df.head())
print(geometry_coords_df.crs)

# Create linestring from point
linestring = shape(geometry_coords_df.loc[0, "geometry"])


# ------------------------- CUSTOM INPUTS ---------------------------- #
distance = 0        ##  starting at length 0
add_distance = 10   ## interpoalte every 10 meter

print(type(linestring))
print(linestring.length)

list_of_points = []
while distance < linestring.length:
   new_point = linestring.interpolate(distance)
   list_of_points.append(new_point)
   distance += add_distance ## add more
   if distance > 50:
      break
# You will have to convert that list of tuples into actual LineString:
# list_of_points = [Point(tuple) for tuple in list]
line = LineString(list_of_points)

print(list_of_points)

