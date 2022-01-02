import sys
import requests
import json
from datetime import datetime
from datetime import timedelta
import csv
import os

csv_data = []
dict_weather = {"Rain": "Będzie padać.",
                "Snow": "Będzie padać",
                "Sun": "Nie będzie padać",
                "Clear": "Nie będzie padać",
                "Clouds": "Nie będzie padać"
                }

def file_csv(file,attr, csv_data):
    with open(file, attr, newline="") as f:
            csv_writer = csv.writer(f)
            for line in csv_data:
                csv_writer.writerow(line)


def write_file_csv(csv_data):
    file_csv("data.csv", "w", csv_data) if not os.path.isfile("data.csv") else file_csv("data.csv", "a", csv_data)


def read_json_file():
    with open("out.json", 'r') as f:
        out = json.load(f)
        return out


def write_loop(out):
    for i in range(len(out['list'])):
        day = str(datetime.fromtimestamp(out['list'][i]['dt']).date())
        weather = out['list'][i]['weather'][0]['main']
        csv_data.append([day, weather])
    write_file_csv(csv_data)

def write_loop_add(out):
    for i in range(len(out['list'])):
        day = str(datetime.fromtimestamp(out['list'][i]['dt']).date())
        if read_csv_file("data.csv", day) == day:
            weather = out['list'][i]['weather'][0]['main']
            csv_data.append([day, weather])
            write_file_csv(csv_data)

def read_api():
    url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
    querystring = {"q": "Konin", "lat": "35", "lon": "139", "cnt": "10", "units": "metric or imperial"}
    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': sys.argv[1]
    }
    if not os.path.isfile("out.jason"):
        response = requests.request("GET", url, headers=headers, params=querystring)
        out_url = response.json()
        with open("out.json", 'w') as json_file:
             json.dump(out_url, json_file)
    write_loop(read_json_file()) if not os.path.isfile("data.csv") else write_loop_add(read_json_file())
