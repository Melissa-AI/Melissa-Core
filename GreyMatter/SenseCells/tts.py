import os
import sys
import json
import subprocess

from GreyMatter.profile_populator import profile_populator

def tts(message):
    """
    This function takes a message as an argument and converts it to speech depending on the OS.
    """
    if os.path.isfile('profile.json'):
        profile = open('profile.json')
        profile_data = json.load(profile)
        profile.close()
    else:
        profile_populator()
        main()

    if sys.platform == 'darwin':
        tts_engine = 'say'

        if profile_data['va_gender'] == 'male':
            language = '-valex'
            return subprocess.call([tts_engine, language, message])
        else:
            return subprocess.call([tts_engine, message])

    elif sys.platform == 'linux2' or sys.platform == 'linux' or sys.platform == 'win32':
        tts_engine = 'espeak'

        if profile_data['va_gender'] == 'female':
            language = '-ven+f4'
            speed = '-s170'
            return subprocess.call([tts_engine, language, speed, message])
        else:
            speed = '-s170'
            return subprocess.call([tts_engine, speed, message])
