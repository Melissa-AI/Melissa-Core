import os
import json

from GreyMatter.profile_populator import profile_populator
from GreyMatter.SenseCells.tts import tts
from GreyMatter.SenseCells.stt import stt

def main():
    if os.path.isfile('profile.json'):
        profile = open('profile.json')
        profile_data = json.load(profile)
        profile.close()
    else:
        profile_populator()
        main()

    tts('Welcome ' + profile_data['name'] + ', systems are now ready to run. How can I help you?')
    stt(profile_data)

main()
