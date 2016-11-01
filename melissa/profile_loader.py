import os
import json

# Melissa
from utilities import json_decode as jd
from profile_populator import profile_populator


def load_profile(skip_message=False):
    if not skip_message:
        print "Loading profile data"
    if not os.path.isfile('profile.json'):
        profile_populator()
    profile_json = open('profile.json')
    data = json.load(profile_json, object_hook=jd.decode_dict)
    profile_json.close()
    return data
