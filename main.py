import os
import yaml

from GreyMatter.SenseCells.tts import tts
from GreyMatter.SenseCells.stt import stt

def main():
    if os.path.isfile('profile.yaml'):
        profile = open('profile.yaml')
        profile_data = yaml.safe_load(profile)
        profile.close()
    else:
        print('profile.yaml not found')
        exit()

    tts('Welcome ' + profile_data['name'] + ', systems are now ready to run. How can I help you?')
    stt(profile_data)

main()
