from shapely.geometry import shape
import geopandas as gpd
from shapely.ops import nearest_points


def WGS_to_UTM(raw_geojson):
    """
    transform vectors from EPSG 4326 (Google's default) to UTM 51N (32651)
    :param raw_geojson: vector in geojson format
    :return: geodataframe of transformed vector
    """
    geometry_coords_df = gpd.GeoDataFrame.from_features(raw_geojson)
    geometry_coords_df = geometry_coords_df.set_crs("EPSG:4326")
    geometry_coords_df = geometry_coords_df.to_crs("EPSG:32651")
    return geometry_coords_df


def route_to_points(gdf_row, n_meters):
   """
   converts route (line) to series of points
   :param gdf_row: geodataframe row of route to be converted
   :param n_meters: distance between the points in meters
   :return: geoseries of the points every n_meters
   """

   distance = 0        #  starting at length 0
   n_meters = 10   # interpoalte every 10 meter

   # Create linestring from point
   linestring = shape(gdf_row.geometry)

   route_points = []
   while distance < linestring.length:
      new_point = linestring.interpolate(distance)
      route_points.append(new_point)
      distance += n_meters

   return gpd.GeoSeries(route_points)

#    return gpd.GeoDataFrame({
#             'geometry': route_points
#          })


def get_station_index(route_points: gpd.GeoSeries, stations: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
   """
   using the stations geoseries, detect which point along the route will be treated as the "station"
   :param route_points: geoseries containing the route represented by points
   :param stations: geodataframe of stations represented by a point per station
   :return: list of indices of the points to be labelled as "stations"

   Notes: 
   - The stations are assumed to be in order.
   """
   
   multipoint = route_points.union_all()
   
   stations_list = []
   for _, row in stations.iterrows():
      nearest_pt = nearest_points(row["geometry"], multipoint)[1]
          # find matching row index with tolerance
      nearest_index = route_points[route_points.geometry.distance(nearest_pt) < 1e-6].index[0]
      stations_list.append(nearest_index)
   return stations_list