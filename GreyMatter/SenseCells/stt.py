import os

import speech_recognition as sr
try:
    from pocketsphinx.pocketsphinx import *
    from sphinxbase.sphinxbase import *
except:
    pass

from brain import brain

def stt(profile_data):
    va_name = profile_data['va_name']
    r = sr.Recognizer()
    if profile_data['stt'] == 'google':
        while True:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Say something!")
                audio = r.listen(source)

            try:
                speech_text = r.recognize_google(audio).lower().replace("'", "")
                print(va_name + " thinks you said '" + speech_text + "'")
            except sr.UnknownValueError:
                print(va_name + " could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except AttributeError:
                print('You are not connected to the internet, please enter "sphinx" in the "stt" field of your "profile.json" file to work offline.')
                exit()
            else:
                brain(profile_data, speech_text)

    elif profile_data['stt'] == 'sphinx':

        modeldir = profile_data['pocketsphinx']['modeldir'].encode("ascii")
        hmm = profile_data['pocketsphinx']['hmm'].encode("ascii")
        lm = profile_data['pocketsphinx']['lm'].encode("ascii")
        dic = profile_data['pocketsphinx']['dic'].encode("ascii")

        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(modeldir, hmm))
        config.set_string('-lm', os.path.join(modeldir, lm))
        config.set_string('-dict', os.path.join(modeldir, dic))
        config.set_string('-logfn', '/dev/null')
        decoder = Decoder(config)

        def sphinx_stt():
            stream = open('recording.wav', 'rb')
            stream.seek(44) # bypasses wav header

            data = stream.read()
            decoder.start_utt()
            decoder.process_raw(data, False, True)
            decoder.end_utt()

            speech_text = decoder.hyp().hypstr
            print(va_name + " thinks you said '" + speech_text + "'")
            return speech_text.lower().replace("'", "")

        while True:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Say something!")
                audio = r.listen(source)

            with open("recording.wav", "wb") as f:
                f.write(audio.get_wav_data())

            brain(profile_data, sphinx_stt())

