import pywapi

# Melissa
from melissa import profile
from melissa.tts import tts

WORDS = {'weather': {'groups': ['weather', ['how', 'weather'],
                                ['hows', 'weather']]}}


def weather(text):
    weather_com_result = pywapi.get_weather_from_weather_com(
        profile.data['city_code'])

    current_conditions = weather_com_result['current_conditions']
    temperature = float(current_conditions['temperature'])
    degrees_type = 'celcius'

    if profile.data['degrees'] == 'fahrenheit':
        temperature = (temperature * 9 / 5) + 32
        degrees_type = 'fahrenheit'

    weather_result = "Weather.com says: It is " + \
        weather_com_result['current_conditions']['text'].lower() + \
        " and " + str(temperature) + "degrees " + degrees_type + \
        " now in " + profile.data['city_name']
    tts(weather_result)
