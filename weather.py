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
