import os
import sqlite3
from datetime import datetime

from imgurpython import ImgurClient

from SenseCells.tts import tts

def img_list_gen(images_path):

    image_list = []
    for root, dirs, files in os.walk(images_path):
        for filename in files:
            if os.path.splitext(filename)[1] == ".tiff" or os.path.splitext(filename)[1] == ".png" or os.path.splitext(filename)[1] == ".gif" or os.path.splitext(filename)[1] == ".jpg":
                image_list.append(os.path.join(root, filename.lower()))
    return image_list

def image_uploader(speech_text, client_id, client_secret, images_path):

    words_of_message = speech_text.split()
    words_of_message.remove('upload')
    cleaned_message = ' '.join(words_of_message)

    image_listing = img_list_gen(images_path)

    client = ImgurClient(client_id, client_secret)

    for i in range(0, len(image_listing)):
        if cleaned_message in image_listing[i]:
            result = client.upload_from_path(image_listing[i], config=None, anon=True)

            conn = sqlite3.connect('memory.db')
            conn.execute("INSERT INTO image_uploads (filename, url, upload_date) VALUES (?, ?, ?)", (image_listing[i], result['link'], datetime.strftime(datetime.now(), '%d-%m-%Y')))
            conn.commit()
            conn.close()

            print result['link']
            tts('Your image has been uploaded')

def show_all_uploads():
    conn = sqlite3.connect('memory.db')

    cursor = conn.execute("SELECT * FROM image_uploads")

    for row in cursor:
        print(row[0] + ': (' + row[1] + ') on ' + row[2])

    tts('Requested data has been printed on your terminal')

    conn.close()
