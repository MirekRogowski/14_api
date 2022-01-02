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


def file_csv(file, attr, csv_file_write):
    with open(file, attr, newline="") as f:
        csv_writer = csv.writer(f)
        for line in csv_file_write:
            csv_writer.writerow(line)


def write_file_csv(csv_file_write):
    file_csv("data.csv", "w", csv_file_write) if not os.path.isfile("data.csv") \
        else file_csv("data.csv", "a", csv_file_write)


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
        # print(read_csv_file_date("data.csv", day))
        if not read_csv_file_date("data.csv", day):
            weather = out['list'][i]['weather'][0]['main']
            csv_data.append([day, weather])
    write_file_csv(csv_data)


def read_api():
    url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
    querystring = {"q": "Konin", "lat": "35", "lon": "139", "cnt": "16", "units": "metric or imperial"}
    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': sys.argv[1]
    }
    if not os.path.isfile("out.jason"):
        # print("Read api ")
        response = requests.request("GET", url, headers=headers, params=querystring)
        out_url = response.json()
        with open("out.json", 'w') as json_file:
             json.dump(out_url, json_file)
    write_loop(read_json_file()) if not os.path.isfile("data.csv") else write_loop_add(read_json_file())


def read_csv_file(file, date):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        # print("data", data)
        for i in data:
            if i[0] == date:
                return i[1]
        return False


def read_csv_file_date(file, date):
    # print("funkcja, read_csv_file_date")
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for i in data:
            if i[0] == date:
                return True
        return False


def check_weather(date):
    if not os.path.isfile("data.csv"):
        read_api()
    weather = read_csv_file("data.csv", date)
    if not weather:
        read_api()
    weather = read_csv_file("data.csv", date)
    text = "Nie wiem."
    print(f"W dniu {date} - {dict_weather.get(weather, text)}")


def main():
    check_weather(sys.argv[2]) if len(sys.argv) == 3 else check_weather(str(datetime.now().date() + timedelta(days=1)))


print("Brak api") if len(sys.argv) < 2 else main()
