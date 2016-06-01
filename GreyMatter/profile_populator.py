import json

def profile_populator():
    def empty(variable):
        if variable:
            return False
        else:
            return True

    print('Welcome to Melissa. Let us generate your profile!')
    print(' Press Enter for using default values.')

    name = raw_input('Your name: ')
    if empty(name):
        name = 'Tanay'

    stt = raw_input('STT Engine (google/sphinx): ')
    if empty(stt):
        stt = 'google'

    music_path = raw_input('Path to your music directory: ')
    if empty(music_path):
        music_path = '.'

    images_path = raw_input('Path to your images directory: ')
    if empty(images_path):
        images_path = '.'

    city_name = raw_input('Name of city where you live: ')
    if empty(city_name):
        city_name = 'New Delhi'

    city_code = raw_input('Code of city from weather.com: ')
    if empty(city_code):
        city_code = 'INXX0096'

    access_token = 'xxxx'
    access_token_secret = 'xxxx'
    consumer_key = 'xxxx'
    consumer_secret = 'xxxx'

    client_id = 'xxxx'
    client_secret = 'xxxx'

    modeldir = '/usr/local/share/pocketsphinx/model/'
    hmm = 'en-us/en-us'
    lm = 'lm/2854.lm'
    dic = 'lm/2854.dic'

    profile_data = {'name': name, 'stt': stt, 'music_path': music_path, 'images_path': images_path, 'city_name': city_name, 'city_code': city_code, 'pocketsphinx': {'modeldir': modeldir, 'hmm': hmm, 'lm': lm, 'dic': dic}, 'twitter': {'access_token': access_token, 'access_token_secret': access_token_secret, 'consumer_key': consumer_key, 'consumer_secret': consumer_secret}, 'imgur': {'client_id': client_id, 'client_secret': client_secret}}

    with open('profile.json', 'w') as outfile:
        json.dump(profile_data, outfile, indent=4)