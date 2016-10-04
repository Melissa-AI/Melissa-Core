import sqlite3
from datetime import datetime

# Melissa
from melissa import profile
from melissa.tts import tts

WORDS = {
    'show_all_notes': {
        'groups': [
            ['all', 'note'],
            ['all', 'notes'],
            'notes'
        ]
    },
    'note_something': {
        'groups': ['note']
    },
}


def show_all_notes(text):
    conn = sqlite3.connect(profile.data['memory_db'])
    tts('Your notes are as follows:')

    cursor = conn.execute("SELECT notes FROM notes")

    for row in cursor:
        tts(row[0])

    conn.close()


def note_something(speech_text):
    conn = sqlite3.connect(profile.data['memory_db'])
    words_of_message = speech_text.split()
    words_of_message.remove('note')
    cleaned_message = ' '.join(words_of_message)

    conn.execute("INSERT INTO notes (notes, notes_date) VALUES (?, ?)", (
        cleaned_message, datetime.strftime(datetime.now(), '%d-%m-%Y')))
    conn.commit()
    conn.close()

    tts('Your note has been saved.')
