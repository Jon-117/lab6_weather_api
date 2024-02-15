import requests
import json
from pprint import pprint
import os
import logging
from datetime import datetime

logging.basicConfig(filename='weather_api.log')
base_url = 'https://api.openweathermap.org/data/2.5/forecast'

try:
    KEY = os.environ.get('OPENWEATHER_API_KEY')
    if KEY is None:
        raise ValueError('API key is missing or is invalid.')
except ValueError as e:
    logging.error(f'{e}')
    pprint(e)
    print('Exiting program')
    exit()

params = {'q': None, 'units': 'imperial', 'appid': KEY}  # 'q' is location, set before request


def get_location():
    """
    Grab the user's location.
    """
    # location can be zip, city, city+country, city+state
    location = input("Enter location using format 'city,country code' here: ")
    params['q'] = location


def get_weather() -> json:
    get_location()
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"Weather forecast for {data['city']['name']}")

        timezone_offset = data["city"]["timezone"]
        weather_report = []

        for each in data['list']:
            timestamp = each["dt"]
            time = datetime.utcfromtimestamp(timestamp - timezone_offset)
            conditions = each["weather"][0]["description"]
            temp = each["main"]["temp"]
            windspeed = each["wind"]["speed"]

            weather_report_section = f"{time} :: Conditions: {conditions} :: Temp {temp}°F :: Winds at {windspeed} MPH"
            formatted_report_section = f"{'=' * len(weather_report_section)}\n{weather_report_section}\n{'=' * len(weather_report_section)}\n"

            weather_report.append(formatted_report_section)
        return weather_report

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logging.error("Error: " + str(e) + "\nYour city may not exist. Check spelling and try again. ")
            print("Error Occured: " + str(e) + "\nYour city may not exist. Check spelling and try again. ")
    except Exception as e:
        print("Something went wrong: " + str(e))
        logging.error("Something went wrong: " + str(e))


def main():
    weather_report = get_weather()
    try:
        for each in weather_report:
            print(each)
    except TypeError as e:
        "Error: Unable to complete your request"

if __name__ == "__main__":
    main()
