import configparser
import requests
import calendar
import time
import datetime
from timeit import default_timer as timer

def api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def epoch_convert(epoch):
    return time.strftime("%H:%M", time.localtime(epoch))


def data_week(city, state):
    processed = {}
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},{state}&appid={api_key()}"
    params = {"units": "imperial"}
    data = requests.get(url, params=params)

    try:
        country = data.json()["city"]["country"]
        data = (data.json())["list"]

        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        data = [set for set in data if set["dt_txt"][:10] != date]

        for i in range(1, 6):
            temp_min = 0
            temp_max = 0
            humidity = 0
            tomorrow = datetime.date.today() + datetime.timedelta(days=i)
            day_of_week = calendar.day_name[tomorrow.weekday()]
            set_day = tomorrow.strftime("%Y-%m-%d")
            processed[day_of_week] = {}
            for set in data:
                if set["dt_txt"][:10] == set_day:
                    temp_min += set["main"]["temp_min"]
                    temp_max += set["main"]["temp_max"]
                    humidity += set["main"]["humidity"]
                    processed[day_of_week]["icon"] = set["weather"][0]["icon"]
                else:
                    processed[day_of_week]["temp_min"] = round(temp_min/8,1)
                    processed[day_of_week]["temp_max"] = round(temp_max/8,1)
                    processed[day_of_week]["humidity"] = round(humidity/8,1)
        processed["country"] = country

        return processed

    except KeyError:
        return "City Not Found"


def data_now(city, state):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api_key()}"
    params = {"units": "imperial"}
    data = requests.get(url, params=params)
    data = (data.json())

    try:
        data["main"]["sunrise"] = epoch_convert(data["sys"]["sunrise"])
        data["main"]["sunset"] = epoch_convert(data["sys"]["sunset"])
        data["main"]["description"] = data["weather"][0]["description"]
        data["main"]["icon"] = data["weather"][0]["icon"]
        data["main"]["wind_speed"] = data["wind"]["speed"]

        return data["main"]

    except KeyError:
        return data["message"].title()

