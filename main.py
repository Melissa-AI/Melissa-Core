import os
import sys
import time
import audioop
import tempfile

import wave
import yaml
import pyaudio
import speech_recognition as sr

try:
    from pocketsphinx.pocketsphinx import *
    from sphinxbase.sphinxbase import *
except:
    pass

from brain import brain
from GreyMatter import play_music, imgur_handler
from GreyMatter.SenseCells.tts import tts

profile = open('profile.yaml')
profile_data = yaml.safe_load(profile)
profile.close()

# Functioning Variables
name = profile_data['name']
stt = profile_data['stt']
modeldir = profile_data['pocketsphinx']['modeldir']
hmm = profile_data['pocketsphinx']['hmm']
lm = profile_data['pocketsphinx']['lm']
dic = profile_data['pocketsphinx']['dic']
music_path = profile_data['music_path']
images_path = profile_data['images_path']
city_name = profile_data['city_name']
city_code = profile_data['city_code']
proxy_username = profile_data['proxy_username']
proxy_password = profile_data['proxy_password']
access_token = profile_data['twitter']['access_token']
access_token_secret = profile_data['twitter']['access_token_secret']
consumer_key = profile_data['twitter']['consumer_key']
consumer_secret = profile_data['twitter']['consumer_secret']
client_id = profile_data['imgur']['client_id']
client_secret = profile_data['imgur']['client_secret']

tts('Welcome ' + name + ', systems are now ready to run. How can I help you?')

# Thanks to Jasper for passive code snippet.

_audio = pyaudio.PyAudio()

def getScore(data):
    rms = audioop.rms(data, 2)
    score = rms / 3
    return score

def fetchThreshold():
    THRESHOLD_MULTIPLIER = 1.8
    RATE = 16000
    CHUNK = 1024
    THRESHOLD_TIME = 1

    stream = _audio.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)

    frames = []
    lastN = [i for i in range(20)]

    for i in range(0, RATE / CHUNK * THRESHOLD_TIME):
        data = stream.read(CHUNK)
        frames.append(data)

        lastN.pop(0)
        lastN.append(getScore(data))
        average = sum(lastN) / len(lastN)

    stream.stop_stream()
    stream.close()

    THRESHOLD = average * THRESHOLD_MULTIPLIER
    return THRESHOLD


def passiveListen():
    THRESHOLD_MULTIPLIER = 1.8
    RATE = 16000
    CHUNK = 1024
    THRESHOLD_TIME = 1
    LISTEN_TIME = 300

    stream = _audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)

    frames = []
    lastN = [i for i in range(30)]

    for i in range(0, RATE / CHUNK * THRESHOLD_TIME):
        data = stream.read(CHUNK)
        frames.append(data)

        lastN.pop(0)
        lastN.append(getScore(data))
        average = sum(lastN) / len(lastN)

    THRESHOLD = average * THRESHOLD_MULTIPLIER
    frames = []
    didDetect = False

    for i in range(0, RATE / CHUNK * LISTEN_TIME):
        data = stream.read(CHUNK)
        frames.append(data)
        score = getScore(data)

        if score > THRESHOLD:
            didDetect = True
            stream.stop_stream()
            stream.close()
            time.sleep(1)
            tts('Yes?')
            main()

    if not didDetect:
        print "No disturbance detected"
        stream.stop_stream()
        stream.close()

def main():
    try:
        if sys.argv[1] == '--text' or sys.argv[1] == '-t':
            text_mode = True
            speech_text = raw_input("Write something: ").lower().replace("'", "")
    except IndexError:
        text_mode = False

        if stt == 'google':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            try:
                speech_text = r.recognize_google(audio).lower().replace("'", "")
                print("Melissa thinks you said '" + speech_text + "'")
            except sr.UnknownValueError:
                print("Melissa could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

            play_music.mp3gen(music_path)
            imgur_handler.img_list_gen(images_path)

            brain(name, speech_text, music_path, city_name, city_code, proxy_username, proxy_password, consumer_key, consumer_secret, access_token, access_token_secret, client_id, client_secret, images_path)

        elif stt == 'sphinx':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            with open("recording.wav", "wb") as f:
                f.write(audio.get_wav_data())

            def sphinx_stt():
                MODELDIR = modeldir

                config = Decoder.default_config()
                config.set_string('-hmm', os.path.join(MODELDIR, hmm))
                config.set_string('-lm', os.path.join(MODELDIR, lm))
                config.set_string('-dict', os.path.join(MODELDIR, dic))
                config.set_string('-logfn', '/dev/null')
                decoder = Decoder(config)

                stream = open('recording.wav', 'rb')

                in_speech_bf = False
                decoder.start_utt()
                while True:
                    buf = stream.read(1024)
                    if buf:
                        decoder.process_raw(buf, False, False)
                        if decoder.get_in_speech() != in_speech_bf:
                            in_speech_bf = decoder.get_in_speech()
                            if not in_speech_bf:
                                decoder.end_utt()
                                speech_text = decoder.hyp().hypstr
                                print speech_text
                                decoder.start_utt()
                    else:
                        break
                decoder.end_utt()
                return speech_text.lower().replace("'", "")

            play_music.mp3gen(music_path)
            imgur_handler.img_list_gen(images_path)

            brain(name, sphinx_stt(), music_path, city_name, city_code, proxy_username, proxy_password, consumer_key, consumer_secret, access_token, access_token_secret, client_id, client_secret, images_path)


    if text_mode:
        main()
    else:
        passiveListen()

main()
