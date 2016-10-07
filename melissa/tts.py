import sys
import subprocess

import pyvona

# Melissa
import profile


def tts(message):
    """
    This function takes a message as an argument and converts it to
    speech depending on the OS.
    """
    if profile.data['tts'] == 'ivona':
        access_key = profile.data['ivona']['access_key']
        secret_key = profile.data['ivona']['secret_key']
        tts_engine = pyvona.create_voice(access_key, secret_key)
        if profile.data['va_gender'] == 'female':
            tts_engine.voice_name = 'Salli'
        else:
            tts_engine.voice_name = 'Joey'
        tts_engine.speak(message)

    else:
        if sys.platform == 'darwin':
            tts_engine = 'say'
            if profile.data['va_gender'] == 'male':
                language = '-valex'
                return subprocess.call([tts_engine, language, message])
            else:
                return subprocess.call([tts_engine, message])

        elif sys.platform.startswith('linux') or sys.platform == 'win32':
            tts_engine = 'espeak'
            if profile.data['va_gender'] == 'female':
                language = '-ven+f3'
                speed = '-s170'
                return subprocess.call([tts_engine, language, speed, message])
            else:
                speed = '-s170'
                return subprocess.call([tts_engine, speed, message])
