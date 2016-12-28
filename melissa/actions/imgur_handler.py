import os
import sqlite3
from datetime import datetime
from imgurpython import ImgurClient

# Melissa
from melissa import profile
from melissa.tts import tts

WORDS = {'image_uploader': {'groups': ['upload']},
         'show_all_uploads': {'groups': [['all', 'uploads'],
                                         ['all', 'images'], ['uploads']]}}


def img_list_gen():
    image_list = []
    valid_image_extensions = [".tiff", ".png", ".gif", ".jpg"]
    for root, _, files in os.walk(profile.data['images_path']):
        for filename in files:
            if os.path.splitext(filename)[1] in valid_image_extensions:
                image_list.append(os.path.join(root, filename.lower()))
    return image_list


def image_uploader(speech_text):

    if profile.data['imgur']['client_id'] == "xxxx" \
            or profile.data['imgur']['client_secret'] == "xxxx":
        msg = 'upload requires a client id and secret'
        print msg
        tts(msg)
        return

    words_of_message = speech_text.split()
    words_of_message.remove('upload')
    cleaned_message = ' '.join(words_of_message)
    if len(cleaned_message) == 0:
        tts('upload requires a picture name')
        return

    image_listing = img_list_gen()

    client = ImgurClient(profile.data['imgur']['client_id'],
                         profile.data['imgur']['client_secret'])

    for i in range(0, len(image_listing)):
        if cleaned_message in image_listing[i]:
            result = client.upload_from_path(image_listing[i], config=None,
                                             anon=True)

            conn = sqlite3.connect(profile.data['memory_db'])
            conn.execute("INSERT INTO image_uploads "
                         "(filename, url, upload_date) VALUES (?, ?, ?)",
                         (image_listing[i], result['link'],
                          datetime.strftime(datetime.now(), '%d-%m-%Y')))
            conn.commit()
            conn.close()

            print result['link']
            tts('Your image has been uploaded')


def show_all_uploads(text):
    conn = sqlite3.connect(profile.data['memory_db'])
    cursor = conn.execute("SELECT * FROM image_uploads")

    for row in cursor:
        print(row[0] + ': (' + row[1] + ') on ' + row[2])

    tts('Requested data has been printed on your terminal')

    conn.close()
