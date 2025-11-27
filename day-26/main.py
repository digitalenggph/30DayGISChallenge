import utm
import pandas as pd

print("Start!")

bus_schedule_df = pd.read_csv("bus_schedule.csv")
bus_schedule_df["lat"], bus_schedule_df["lon"] = utm.to_latlon(bus_schedule_df["X"], bus_schedule_df["Y"], 51, "N")

print(bus_schedule_df.head())
bus_schedule_df.to_csv("bus_schedule_wgs84.csv")

