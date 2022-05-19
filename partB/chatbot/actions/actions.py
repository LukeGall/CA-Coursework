# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
from datetime import datetime

apikey = 'XXXXX'

headers = {
    'x-rapidapi-host': "XXXXX",
    'x-rapidapi-key': "XXXXX"
    }

geoUrl = "https://wft-geo-db.p.rapidapi.com/v1/geo/"

def strip_time(duckTime):
    date = duckTime[:duckTime.find("T")]

    frstdash = date.find("-")
    snddash = date.find("-", frstdash+1)

    year = date[:frstdash]
    month = date[frstdash+1:snddash]
    day = date[snddash+1:]

    return int(year), int(month), int(day)

class GetWeatherDetails(Action):

    def name(self) -> Text:
        return "get_weather_details"

    # Dispatcher can send messages to the user
    # Tracker has slot vals, intent info etc

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        current_city = next(tracker.get_latest_entity_values("city"), None)
        time = next(tracker.get_latest_entity_values("time"), None)
        days_away = 0

        if not current_city:
            return []

        weather_res = requests.get(f"http://pro.openweathermap.org/data/2.5/forecast/climate?q={current_city}&appid={apikey}&units=metric")

        weather_info = weather_res.json()

        if time:
            year, month, day = strip_time(time) 
            days_away = (datetime(year, month, day) - datetime.now()).days
            if (len(weather_info['list']) < days_away):
                days_away = 0
            if (days_away > 29):
                days_away = 29
        
        if 'list' not in weather_info:
            # Default values
            return [SlotSet("temp", 42), SlotSet("humidity", 42), SlotSet("wind", 42), SlotSet("rain", 42), SlotSet("hot", True), SlotSet("cold", False), SlotSet("average", False)]

        weather_info_for_day = weather_info['list'][days_away]

        temp = 0
        humidity = 0 
        wind = 0 
        rain = 0

        if 'temp' in weather_info_for_day:
            temp = weather_info_for_day['temp']['day']
        if 'humidity' in weather_info_for_day:
            humidity = weather_info_for_day['humidity']
        if 'speed' in weather_info_for_day:
            wind = weather_info_for_day['speed']
        if 'rain' in weather_info_for_day:
            rain = weather_info_for_day['rain']
        hot = True if temp > 20 else False
        cold = True if temp < 0 else False 
        average = not hot and not cold
        
        return [SlotSet("temp", temp), SlotSet("humidity", humidity), SlotSet("wind", wind), SlotSet("rain", rain), SlotSet("hot", hot), SlotSet("cold", cold), SlotSet("average", average)]

class ActionCityDetails(Action):
    def name(self) -> Text:
        return "action_city_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        current_city = tracker.get_slot("city")
        print("Running city details", current_city)
        
        if not current_city:
            return []

        weather_res = requests.get(f"http://pro.openweathermap.org/data/2.5/forecast/climate?q={current_city}&appid={apikey}&units=metric")

        weather_info = weather_res.json()
        lat = weather_info['city']['coord']['lat']
        long = weather_info['city']['coord']['lon']
        
        querystring = {"location":f"{lat}{long}"}
        cityRes = requests.request("GET", geoUrl+"cities/", headers=headers, params=querystring)
        cityInfo = cityRes.json()['data'][0]
        countryCode = cityInfo['countryCode']

        country = cityInfo['country']
        region = cityInfo['region']
        population = cityInfo['population']
        
        return [SlotSet("country_name", country), SlotSet("city_region", region), SlotSet("city_pop", population), SlotSet("country_code",countryCode)]

class ActionCountryDetails(Action):
    def name(self) -> Text: 
        return "action_country_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Running country details")

        countryCode = tracker.get_slot("country_code")

        if not countryCode:
            return []

        countryRes = requests.request("GET",geoUrl+f"countries/{countryCode}", headers=headers)
        countryInfo = countryRes.json()['data']

        capital = countryInfo['capital']
        flag = countryInfo['flagImageUri']
        regions = countryInfo['numRegions']

        return [SlotSet("capital_city", capital), SlotSet("num_of_regions",regions), SlotSet("flag_image",flag)]
