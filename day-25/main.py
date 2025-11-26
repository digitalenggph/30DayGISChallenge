import requests, json
import pandas as pd
from datetime import datetime as dt
from datetime import timezone, timedelta

URL = "https://earthquake.usgs.gov/fdsnws/event/1/"


# In UTC: starttime -> time of program run ; endtime = 60 days before starttime
starttime_epoch = dt.now(timezone.utc).timestamp()
endtime_epoch = (dt.now(timezone.utc) - timedelta(days=60)).timestamp()

starttime_date = dt.fromtimestamp(starttime_epoch).strftime('%Y-%m-%d')
endtime_date = dt.fromtimestamp(endtime_epoch).strftime('%Y-%m-%d')

params = {
    "method": "query",
    "format": "geojson",
    "starttime": endtime_date,
    "endtime": starttime_date,
}

# get earthquake data
response = requests.get(url=URL, params=params)
usgs_data = response.json()
earthquakes = usgs_data["features"]
print(response.status_code)

with open('earthquakes.json', 'w', encoding='utf-8') as f:
    json.dump(usgs_data, f, ensure_ascii=False, indent=4)

print("Data downloaded!")

earthquakes_list = []

for earthquake in earthquakes:
    time = earthquake["properties"]["time"] 
    epicenter_coordinates = earthquake["geometry"]["coordinates"]
    magnitude = earthquake["properties"]["mag"]
    title = earthquake["properties"]["title"]
    id = earthquake["id"]

    earthquake_dict = {
        "id": id,
        "title": title,
        "time": time,
        "lon": epicenter_coordinates[0],
        "lat": epicenter_coordinates[1],
        "magnitude": magnitude 
    }

    earthquakes_list.append(earthquake_dict)

earthquakes_df = pd.DataFrame(earthquakes_list)
earthquakes_df.to_csv("earthquakes.csv", index=False)


print("Data transformed!")
    


    
    
    


