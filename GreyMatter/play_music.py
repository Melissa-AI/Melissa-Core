import os
import sys
import random

from SenseCells.tts import tts

def mp3gen(music_path):
    """
    This function finds all the mp3 files in a folder and it's subfolders and returns a list.
    """
    music_list = []
    for root, dirs, files in os.walk(music_path):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                music_list.append(os.path.join(root, filename.lower()))
    return music_list

def music_player(file_name):
    """
    This function takes the name of a music file as an argument and plays it depending on the OS.
    """
    if sys.platform == 'darwin':
        player = "afplay '" + file_name + "'"
        return os.system(player)
    elif sys.platform == 'linux2' or sys.platform == 'linux' or sys.platform == 'win32':
        player = "mpg123 '" + file_name + "'"
        return os.system(player)

def play_random(music_path):
    try:
        music_listing = mp3gen(music_path)
        music_playing = random.choice(music_listing)
        tts("Now playing: " + music_playing)
        music_player(music_playing)
    except IndexError as e:
        tts('No music files found.')
        print("No music files found: {0}".format(e))

def play_specific_music(speech_text, music_path):
    words_of_message = speech_text.split()
    words_of_message.remove('play')
    cleaned_message = ' '.join(words_of_message)
    music_listing = mp3gen(music_path)

    for i in range(0, len(music_listing)):
        if cleaned_message in music_listing[i]:
            music_player(music_listing[i])

def play_shuffle(music_path):
    try:
        music_listing = mp3gen(music_path)
        random.shuffle(music_listing)
        for i in range(0, len(music_listing)):
            music_player(music_listing[i])
    except IndexError as e:
        tts('No music files found.')
        print("No music files found: {0}".format(e))
