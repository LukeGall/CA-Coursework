# Design 

## Rough specification (This will be simplified in the sport section)
The extension of the weather system will allow the user to get more information on the city they provide, including it's population and where it is located. They can then ask to get more information about the country which will provide it's capital city, number of regions, and a picture of its flag. The user will also be able to compare their city to another, which will compare the temperature, population etc and how far away they are. 

To extend the existing system users will now be presented with George the Geo surfer who will be happy to provide information on cities. The user can also ask george for sports information based on the temperature of their city. If the user doesn't like the sport they have been given, they can ask for another suggestion or a city where this sport is played a lot.

## Slots (not user entities)
- Existing slots
- Country name
- city population
- city region
- flag image
- capital city name
- num of different regions
- sport suggestion (likely not used in the implementation, will just have it as a list of different responses)
- hot
- cold
- average

## Entities
- Existing entities
- city info (ideally this would be a list but not in the implementation)
- country info 

## Intents
- GetWeather
- GetDetails
- GetCityDetails
- GetCountryDetails
- GetSportSuggestions
- GetCitySuggestion

## We need to produce three aspirational dialogues
1. User asks about the weather, gets some more info on the city, and then checks the country information
2. User asks about the weather, then queries information about the city, asks about some sport advice, then if there is another city that would be better
3. User asks about the weather, then asks for some sport advice, asks for another sport option and then checks if another city would be better for it

## Utterances
Actual responses from the system must match the persona that we will create for the system ("cool" surfer dude, sports enthusiast)

- utter_get_city
- utter_temp_details
- utter_humidity_details
- utter_wind_details
- utter_humidity_and_wind

- utter_city_options
    - Include prompt list
    *Will likely make users go through this prompt list, this will be to reduce flow complexity but users in the future should be able to just ask for population without needing a list first*
- utter_city_pop
- utter_city_country
- utter_city_region
- utter_all_info

- utter_capital_city
    - including flag image
    - What if the user then asks for the weather there (could be hard but talk about it)
- utter_different regions
    - including flag image
- utter_both_country_details

- utter_sports_suggestion
- utter_different_city

## System persona
Following the steps from the steps from the google conversation design site

Step 1: Adjectives
- Friendly, enthusiastic, sporty, interested in facts, happy, encouraging, confident, pleasant, knowledgeable, relaxed

Step 2: Core traits
- Friendly, enthusiastic, sporty, encouraging, knowledgeable 

Step 3: A couple of character ideas

- Weather reporter
- Travel Agent
- Geography teacher
- Surfing instructor 
- Professional free rock climber 

Step 4: A Few different characters with more fleshed out personas

Gina the travel agent. Gina is travel agent that loves travelling and booking holidays for couples and families that are looking for a more adventurous time. She has a vast knowledge of different locations and the best places for different sporting holidays. She is also friendly with customs and will encourage them to step out of their comfort zone when it comes to awesome activities. Gina is a passionate cyclist so is always up to date with the weather reports in different locations so she can plan out her rides effectively.

Harold the geography teacher. Harold has recently finished his geographer degree and had turned down research opportunities to follow his passion of teaching. He is always very enthusiastic about teaching others the joys of different locations and differences in climate between locations. In order to be the best teacher he can be, he ensures that he is always helpful and provides the best information that he knows. He is an amateur climber and is usually in the bouldering gym with his friends when not teaching but is interested in going on outdoors climbing trips so watches the weather reports closely for the best time to go out.   

Alex the surfer. David is a surfing instructor that lives in Cornwall. in order to provide the best experience for his clients, he is always friendly, open and encouraging to new surfers. David loves the outdoors and has a passion for a wide variety of sports, trying to have a selection that can be performed in a variety of weather conditions. He likes to impress his clientele with facts about different locations he has travelled to in order to surf or snowboard and likes to keep up to date with the weather to plan his trips. David is always happy to provide suggestions to clientele of great surfing or snowboarding locations in order to share his passions with others.  

Step 5: 

https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftheinscribermag.com%2Fwp-content%2Fuploads%2F2018%2F08%2Fimad_surf_berbere_taghazout_surf_school_instructor_morocco_holiday.jpg&f=1&nofb=1

https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.fistralbeachsurfschool.co.uk%2Fwp-content%2Fuploads%2F2019%2F01%2F-PTCREATIVE-Paul-Terry-4524-Copy-e1548078281645.jpg&f=1&nofb=1

https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.O-30O4eGKET7WnVeupl9EAHaEK%26pid%3DApi&f=1

Design seems pretty good atm, will create this persona on a chatbot as it's quite fun and then will write up the report 