# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
# Actions are called after every intent, this will need fixed

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
from datetime import datetime

apikey = 'e74a0e76b219fdc73d7011c2190babfb'


def strip_time(duckTime):
    date = duckTime[:duckTime.find("T")]

    frstdash = date.find("-")
    snddash = date.find("-", frstdash+1)

    year = date[:frstdash]
    month = date[frstdash+1:snddash]
    day = date[snddash+1:]

    return int(year), int(month), int(day)


class GetRequestInfo(Action):
    def name(self) -> Text:
        return "get_request_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        wind = tracker.get_slot("wind")
        humidity = tracker.get_slot("humidity")
        request = tracker.get_slot("request")

        if not wind and not humidity:
            return []

        if "wind" in request and "humidity" in request:
            dispatcher.utter_message(response = "utter_humidity_and_wind")
        elif "wind" in request:
            dispatcher.utter_message(response = "utter_wind_details")
        elif "humidity" in request:
            dispatcher.utter_message(response = "utter_humidity_details")
        
        return []

class GetWeatherDetails(Action):

    def name(self) -> Text:
        return "get_weather_details"

    # Dispatcher can send messages to the user
    # Tracker has slot vals, intent info etc

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        current_city = next(tracker.get_latest_entity_values("city"), None)
        date = next(tracker.get_latest_entity_values("date"), None)
        days_away = 0

        if not current_city:
            return []

        weather_res = requests.get(
            f"http://pro.openweathermap.org/data/2.5/forecast/climate?q={current_city}&appid={apikey}&units=metric")

        weather_info = weather_res.json()

        if date:
            year, month, day = strip_time(date)
            days_away = (datetime(year, month, day) - datetime.now()).days
            if (len(weather_info['list']) < days_away):
                days_away = 0
            if (days_away > 29):
                days_away = 29
            if (days_away < 0):
                days_away = 0

        if 'list' not in weather_info:
            # Default values
            return [SlotSet("temp", 42), SlotSet("humidity", 42), SlotSet("wind", 42), SlotSet("rain", 42), SlotSet("hot", True)]

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

        return [SlotSet("temp", temp), SlotSet("humidity", humidity), SlotSet("wind", wind), SlotSet("rain", rain), SlotSet("hot", hot)]

