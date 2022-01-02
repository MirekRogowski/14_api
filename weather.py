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

