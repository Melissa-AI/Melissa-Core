import os
import sys
import subprocess
import json
from getpass import getpass

# Melissa
from tts import tts

def tts_local(message):
    if sys.platform == 'darwin':
        tts_engine = 'say'
        return subprocess.call([tts_engine, message])
    elif sys.platform.startswith('linux') or sys.platform == 'win32':
        tts_engine = 'espeak'
        speed = '-s170'
        return subprocess.call([tts_engine, speed, message])

def profile_populator():
    def empty(variable):
        if variable:
            return False
        else:
            return True

    tts_local('Welcome to Melissa. Let us generate your profile!')
    print('Welcome to Melissa. Let us generate your profile!')
    print('Press Enter for using default values.')

    va_name = raw_input('What would you like to name me?: ')
    if empty(va_name):
        va_name = 'Melissa'

    while(True):
        va_gender = raw_input('What is my gender ((m)ale/(f)emale)?: ')
        if va_gender in ('male', 'm', 'female', 'f', ''):
            if empty(va_gender):
                va_gender = 'female'
            elif va_gender == 'm':
                va_gender = 'male'
            elif va_gender == 'f':
                va_gender = 'female'
            break
        print('Invalid input, please enter male, female or <ENTER>.')

    name = raw_input('Your name: ')
    if empty(name):
        name = 'Tanay'

    while(True):
        stt = raw_input('STT Engine ((g)oogle/(s)phinx/(k)eyboard): ').lower()
        if stt in ('g','google', 's','sphinx', 'k','keyboard', ''):
            if empty(stt) or stt == 'g':
                stt = 'google'
            elif stt == 's':
                stt = 'sphinx'
            elif stt == 'k':
                stt = 'keyboard'
            break
        print('Invalid input, please enter (g)oogle, (s)phinx, (k)eyboard or <ENTER>.')

    while(True):
        music_path = raw_input('Path to your music directory: ')
        if empty(music_path):
            music_path = '.'
            break
        if os.path.isdir(music_path):
            break
        print('Invalid input, please enter a valid directory path or <ENTER>.')

    while(True):
        images_path = raw_input('Path to your images directory: ')
        if empty(images_path):
            images_path = '.'
            break
        if os.path.isdir(images_path):
            break
        print('Invalid input, please enter a valid directory path or <ENTER>.')

    city_name = raw_input('Name of city where you live: ')
    if empty(city_name):
        city_name = 'New Delhi'

    city_code = raw_input('Code of city from weather.com: ')
    if empty(city_code):
        city_code = 'INXX0096'

    while(True):
        degrees = raw_input('(c)elsius/(f)ahrenheit): ').lower()
        if degrees in ('c','celsius', 'f','fahrenheit', ''):
            if empty(degrees) or degrees == 'c':
                degrees = 'celsius'
            elif degrees == 'f':
                degrees = 'fahrenheit'
            break
        print('Invalid input, please enter (c)elsius, (f)ahrenheit) or <ENTER>.')

    gmail_address = raw_input('Enter your gmail address (???@gmail.com): ')
    gmail_password = ''
    if len(gmail_address) > 0:
        gmail_password = getpass()

    access_token = 'xxxx'
    access_token_secret = 'xxxx'
    consumer_key = 'xxxx'
    consumer_secret = 'xxxx'

    client_id = 'xxxx'
    client_secret = 'xxxx'

    modeldir = './data/model/'
    hmm = 'hmm/en_US/hub4wsj_sc_8k'
    lm = 'lm/sphinx.lm'
    dic = 'lm/sphinx.dic'

    modules = 'melissa.actions'
    actions_db_file = ':memory:'
    memory_db = './memory.db'

    profile_data = {
        'va_name': va_name,
        'va_gender': va_gender, 
        'name': name,
        'stt': stt,
        'music_path': music_path,
        'images_path': images_path,
        'city_name': city_name,
        'city_code': city_code,
        'degrees': degrees,
        'pocketsphinx': {
            'modeldir': modeldir,
            'hmm': hmm,
            'lm': lm,
            'dic': dic
        },
        'twitter': {
            'access_token': access_token,
            'access_token_secret': access_token_secret,
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret
        },
        'imgur': {
            'client_id': client_id,
            'client_secret': client_secret
        },
        'gmail': {
            'address': gmail_address,
            'password': gmail_password
        },
        'modules': modules,
        'actions_db_file': actions_db_file,
        'memory_db': memory_db
    }

    with open('profile.json', 'w') as outfile:
        json.dump(profile_data, outfile, indent=4)
