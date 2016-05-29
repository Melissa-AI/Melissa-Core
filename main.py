import os
import wave
import yaml
import speech_recognition as sr

try:
    from pocketsphinx.pocketsphinx import *
    from sphinxbase.sphinxbase import *
except:
    pass

from brain import brain
from GreyMatter.SenseCells.tts import tts

def main():
    if os.path.isfile('profile.yaml'):
        profile = open('profile.yaml')
        profile_data = yaml.safe_load(profile)
        profile.close()
    else:
        print('profile.yaml not found')
        exit()

    r = sr.Recognizer()

    tts('Welcome ' + profile_data['name'] + ', systems are now ready to run. How can I help you?')

    if profile_data['stt'] == 'google':
        while True:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Say something!")
                audio = r.listen(source)

            try:
                speech_text = r.recognize_google(audio).lower().replace("'", "")
                print("Melissa thinks you said '" + speech_text + "'")
            except sr.UnknownValueError:
                print("Melissa could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            else:
                brain(profile_data, speech_text)

    elif profile_data['stt'] == 'sphinx':

        def sphinx_stt():
            modeldir = profile_data['pocketsphinx']['modeldir']
            hmm = profile_data['pocketsphinx']['hmm']
            lm = profile_data['pocketsphinx']['lm']
            dic = profile_data['pocketsphinx']['dic']

            config = Decoder.default_config()
            config.set_string('-hmm', os.path.join(modeldir, hmm))
            config.set_string('-lm', os.path.join(modeldir, lm))
            config.set_string('-dict', os.path.join(modeldir, dic))
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

        while True:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Say something!")
                audio = r.listen(source)

            with open("recording.wav", "wb") as f:
                f.write(audio.get_wav_data())

            brain(profile_data, sphinx_stt())

main()
