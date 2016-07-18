# Change to class, check Jasper.
# Put in test for OK import of pocketsphinx when it is being used.
#   See Jasper method.
# Select either Google or pocketsphinx as in Jasper
#   without using an if statement.

import os
import speech_recognition as sr

try:
    from pocketsphinx.pocketsphinx import *
    from sphinxbase.sphinxbase import *
except:
    pass

# Melissa
import profile
from tts import tts
import brain

def stt():
    va_name = profile.data['va_name']
    r = sr.Recognizer()
    tts('Welcome ' + profile.data['name'] + ', systems are now ready to run. How can I help you?')
    if profile.data['stt'] == 'google':
        while True:
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            try:
                speech_text = r.recognize_google(audio).lower().replace("'", "")
                print(va_name + " thinks you said '" + speech_text + "'")
            except sr.UnknownValueError:
                print(va_name + " could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            else:
                brain.query(speech_text)

    elif profile.data['stt'] == 'sphinx':

        modeldir = profile.data['pocketsphinx']['modeldir']
        hmm = profile.data['pocketsphinx']['hmm']
        lm = profile.data['pocketsphinx']['lm']
        dic = profile.data['pocketsphinx']['dic']

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

            hyp = decoder.hyp()
            if hasattr(hyp, 'hypstr'):
                speech_text = hyp.hypstr
                print(profile.data['va_name'] + " thinks you said '"
                      + speech_text + "'")
                return speech_text.lower().replace("'", "")
            else:
                return ''

        while True:
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            with open("recording.wav", "wb") as f:
                f.write(audio.get_wav_data())

            brain.query(sphinx_stt())

    elif profile.data['stt'] == 'keyboard':
        while True:
            keyboard_text = raw_input('Write something: ')
            brain.query(keyboard_text)
