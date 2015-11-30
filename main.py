import os
import sys
import time
import pywapi
import random
import speech_recognition as sr
from selenium import webdriver

# Functioning Variables
name = 'Tanay'
music_path = '.'
city = 'INXX0096'

def tts(message):
    if sys.platform == 'darwin':
        tts_engine = 'say'
        return os.system(tts_engine + ' ' + message)
    elif sys.platform == 'linux':
        tts_engine = 'espeak'
        return os.system(tts_engine + ' ' + message)

tts('Welcome ' + name + ', systems are now ready to run. How can I help you?')

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

try:
    print("Melissa thinks you said '" + r.recognize_google(audio) + "'")
except sr.UnknownValueError:
    print("Melissa could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
words = r.recognize_google(audio).split()
#print words

if r.recognize_google(audio)=='how are you':
    tts('I am fine, thank you.')

elif r.recognize_google(audio)=='play music':
    
    # This function is not currently working. The function will make a list of all music files and use random.choice to play music out of the retrieved files.
    def mp3gen():
        for root, dirs, files in os.walk(music_path):
            for filename in files:
                if os.path.splitext(filename)[1] == ".mp3":
                    yield os.path.join(root, filename)

    for mp3file in mp3gen():
        print mp3file 

    os.system("afplay demons.mp3")

elif r.recognize_google(audio)=='how is weather':
    weather_com_result = pywapi.get_weather_from_weather_com(city)
    weather_result = "Weather.com says: It is " + weather_com_result['current_conditions']['text'].lower() + " and " + weather_com_result['current_conditions']['temperature'] + "degree celcius now in New Delhi."
    tts(weather_result)
    
elif r.recognize_google(audio)=='connect to proxy':
    tts("Connecting to proxy server.")
    browser = webdriver.Firefox()
    browser.get('http://10.1.1.9:8090/httpclient.html')
    
    id_number = browser.find_element_by_name('username')
    password = browser.find_element_by_name('password')
    
    id_number.send_keys('Something')
    password.send_keys('Something')
    
    browser.find_element_by_name('btnSubmit').click()
    

elif r.recognize_google(audio)=='goodbye':
    tts('Goodbye!')

elif r.recognize_google(audio)=='open Firefox':
    tts('Aye aye captain, opening Firefox')
    webdriver.Firefox()

else:
    tts('I dont know what that means!')