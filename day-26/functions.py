import geopandas as gpd
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from shapely.geometry import shape
from shapely.ops import nearest_points


route_details= {
    'Route 1 - from QC Hall': {"altitude": 1, "color": "red", "route": "Route 1"},
    'Route 1 - to QC Hall': {"altitude": 1, "color": "red", "route": "Route 1"},
    'Route 2 - from QC Hall': {"altitude": 2, "color": "orange", "route": "Route 2"},
    'Route 2 - to QC Hall': {"altitude": 2, "color": "orange", "route": "Route 2"},
    'Route 3 - from LRT Katipunan': {"altitude": 3, "color": "yellow", "route": "Route 3"},
    'Route 3 - to LRT Katipunan': {"altitude": 3, "color": "yellow", "route": "Route 3"},
    'Route 4 - from QC Hall': {"altitude": 4, "color": "green", "route": "Route 4"},
    'Route 4 - to QC Hall': {"altitude": 4, "color": "green", "route": "Route 4"},
    'Route 5 - from QC Hall': {"altitude": 5, "color": "blue", "route": "Route 5"},
    'Route 5 - to QC Hall': {"altitude": 5, "color": "blue", "route": "Route 5"},
    'Route 6 - from QC Hall': {"altitude": 6, "color": "indigo", "route": "Route 6"},
    'Route 6 - to QC Hall': {"altitude": 6, "color": "indigo", "route": "Route 6"},
    'Route 7 - from QC Hall': {"altitude": 7, "color": "violet", "route": "Route 7"},
    'Route 7 - to QC Hall': {"altitude": 7, "color": "violet", "route": "Route 7"},
    'Route 8 - from QC Hall': {"altitude": 8, "color": "white", "route": "Route 8"},
    'Route 8 - to QC Hall': {"altitude": 8, "color": "white", "route": "Route 8"}
}



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
    :param gdf_row: geoseries of route to be converted
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


def set_schedule_dt(day, start_dt, end_dt):
    if day == "saturday":
      start_dt += timedelta(days=1)
      end_dt += timedelta(days=1)

    elif day == "sunday":
      start_dt += timedelta(days=2)
      end_dt += timedelta(days=2)    
    
    return start_dt, end_dt

