#Refer to https://cusense.net/portal/#!/apis for CUSense API V1 documentation
# This is a Python API Wrapper for CUSense API V1 made by Punyathorn
import requests
import json
from datetime import datetime

base_url = "https://cusense.net:8082/api/v1"
headers = {
    "Content-Type": "application/json",
    "X-Gravitee-Api-Key": "YOUR_API_KEY_HERE"  # Replace with your actual API key
}

sensor_list = []

#/stationInfo/all Returns every station's information in the database.
def all_station_info():
    x = requests.get(base_url+'/stationInfo/all', headers=headers)
    return x.text

#/stationInfo/active Returns the active station's information.
def active_station_info():
    x = requests.get(base_url+'/stationInfo/active', headers=headers)
    return x.text

#/stationInfo/listProject Returns the list of available projects.
def list_project_station_info():
    x = requests.get(base_url+'/stationInfo/listProject', headers=headers)
    return x.text

#/stationInfo/byProject Returns the station information with the input project.
def station_info_by_project(project):
    body = {
    "project": str(project),
    }
    x = requests.post(base_url+'/stationInfo/byProject', headers=headers, json=body)
    return x.text

#/sensorData/realtime/{type} Get lastest 1 hour averaged data of all active stations.
#Return the lastest 1 hour averaged of pm / all sensor data up to the last 3 hours from all stations. If there is no data for the last hour, the result will be the average of the previous hour.
def sensor_data(type="all"):
    return_data = []
    if (type != "all") & (type != "pm"):
        return "Wrong type"
    x = requests.get(base_url+f'/sensorData/realtime/{type}', headers=headers)    
    data = json.loads(x.text)
    for sensors in data:
        return_data.append(data[sensors])
    return return_data

#/sensorData/realtime/{type} 
# Get lastest 1 hour averaged data of a specific station or project.
# Return the lastest 1 hour averaged of pm / all sensor data up to the last 3 hours from a specific station. 
# If there is no data for the last hour, the result will be the average of the previous hour.
def sensor_data_by_station(type,topic=None,project=None):
    if (type != "all") & (type != "pm"):
        return "Wrong type"
    if topic:
        body = {
        "topic": str(topic),
        }
    elif project:
        body = {
        "project": str(project),
        }
    else:
        return "Error please choose a station or a project"
    x = requests.post(base_url+f'/sensorData/realtime/{type}', headers=headers, json=body)
    return x.text

#/sensorData/day/{type} Get the past 24 hours averaged data of all active station
# Return the 24 hours average data of pm / all sensor from all active station.
def sensor_data_day(type="all"):
    return_data = []
    if (type != "all") & (type != "pm"):
        return "Wrong type"
    x = requests.get(base_url+f'/sensorData/day/{type}', headers=headers)    
    data = json.loads(x.text)
    for sensors in data:
        return_data.append(data[sensors])
    return return_data

#/sensorData/day/{type}
#Get the past 24 hours averaged data of a specific station or project
def sensor_data_day_by_station(type,topic=None,project=None):
    if (type != "all") & (type != "pm"):
        return "Wrong type"
    if topic:
        body = {
        "topic": str(topic),
        }
    elif project:
        body = {
        "project": str(project),
        }
    else:
        return "Error please choose a station or a project"
    x = requests.post(base_url+f'/sensorData/day/{type}', headers=headers, json=body)
    return x.text

#/sensorData/byStation/monthly/{month}
#Get a daily averaged data in a month of a station
#Returns sensor data of daily average for the specified month and year from a specified station.
def sensor_data_month_by_station(type, month, topic):
    if (type != "all") & (type != "pm"):
        return "Wrong type"
    body = {
    "topic": str(topic),
    }
    x = requests.post(base_url+f'/sensorData/byStation/monthly/{month}', headers=headers, json=body)
    return x.text

#/sensorData/byStation/daily/{date}
#Get an hourly averaged data in one day of a station
#Returns hourly average sensor data of a specified day of a specified station.
def sensor_data_hour_day_by_station(type, date, topic=None):
    if (type != "all") & (type != "pm"):
        return "Wrong type"

    body = {
    "topic": str(topic),
    }
    x = requests.post(base_url+f'/sensorData/byStation/daily/{date}', headers=headers, json=body)
    return x.text

#/sensorData/allStation/daily/{date} 
#Get a daily averaged data of all stations
#Returns daily average sensor data of a specified day of all stations.
def sensor_avg_day(date="now"):
    return_data = []
    if date == "now":
        date = datetime.now().strftime("%Y-%m-%d")
    x = requests.get(base_url+f'/sensorData/allStation/daily/{date}', headers=headers)
    print(x.json)    
    data = json.loads(x.text)
    for sensors in data:
        return_data.append(data[sensors])
    return return_data

#additional function returns average values of pm1.0 pm10 and pm2.5 of all active stations
def sensor_data_avg(type):
    pm1 = []
    pm10 = []
    pm25 = []
    a = []
    if (type != "all") & (type != "pm"):
        return "Wrong type"
    x = requests.get(base_url+f'/sensorData/realtime/{type}', headers=headers)    
    data = json.loads(x.text)
    for sensors in data:
        a.append(data[sensors]["data"][0]["pm25"])
        if (str(data[sensors]["data"][0]["pm1"]) != "None") and (str(data[sensors]["data"][0]["pm1"]) != "0") and (int(data[sensors]["data"][0]["pm1"]) <= 1000):
            pm1.append(int(data[sensors]["data"][0]["pm1"]))
        if (str(data[sensors]["data"][0]["pm10"]) != "None") and (str(data[sensors]["data"][0]["pm10"]) != "0") and (int(data[sensors]["data"][0]["pm10"]) <= 1000):
            pm10.append(int(data[sensors]["data"][0]["pm10"]))
        if (str(data[sensors]["data"][0]["pm25"]) != "None") and (str(data[sensors]["data"][0]["pm25"]) != "0") and (int(data[sensors]["data"][0]["pm25"]) <= 1000):
            pm25.append(int(data[sensors]["data"][0]["pm25"]))
    avg_pm1 = sum(pm1)/len(pm1)
    avg_pm10 = sum(pm10)/len(pm10)
    avg_pm25 = sum(pm25)/len(pm25)
    return avg_pm1, avg_pm10, avg_pm25

a = list(sensor_data(type="all"))
for d in a:
    if d["info"]['amphoe'] == "ปทุมวัน":
        print(d)
