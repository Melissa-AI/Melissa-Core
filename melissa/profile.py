import os
import json

# Melissa
from utilities import json_decode as jd
from profile_populator import profile_populator

data = {}

def load_profile():
    global data
    profile_json = open('profile.json')
    data = json.load(profile_json, object_hook=jd.decode_dict)
    profile_json.close()

if len(data) == 0:
    print "Loading profile data"
    if os.path.isfile('profile.json'):
        load_profile()
    else:
        profile_populator()
        load_profile()

