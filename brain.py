from GreyMatter import \
  business_news_reader, \
  define_subject, \
  general_conversations, \
  imgur_handler, \
  lighting, \
  notes, \
  sleep, \
  tell_time, \
  twitter_interaction, \
  play_music, \
  weather

def brain(profile_data, speech_text):
    def check_message(check):
        """
        This function checks if the items in the list (specified in argument) are present in the user's input speech.
        """

        words_of_message = speech_text.split()
        if set(check).issubset(set(words_of_message)):
            return True
        else:
            return False

    if check_message(['who','are', 'you']):
        general_conversations.who_are_you()

    elif check_message(['tweet']):
        twitter_interaction.post_tweet(
            speech_text,
            profile_data['twitter']['consumer_key'],
            profile_data['twitter']['consumer_secret'],
            profile_data['twitter']['access_token'],
            profile_data['twitter']['access_token_secret'])

    elif check_message(['business', 'news']):
        business_news_reader.news_reader()

    elif check_message(['how', 'i', 'look']) \
      or check_message(['how', 'am', 'i']):
        general_conversations.how_am_i()

    elif check_message(['all', 'note']) \
      or check_message(['all', 'notes']) \
      or check_message(['notes']):
        notes.show_all_notes()

    elif check_message(['note']):
        notes.note_something(speech_text)

    elif check_message(['define']):
        define_subject.define_subject(speech_text)

    elif check_message(['tell', 'joke']):
        general_conversations.tell_joke()

    elif check_message(['who', 'am', 'i']):
        general_conversations.who_am_i(profile_data['name'])

    elif check_message(['where', 'born']):
        general_conversations.where_born()

    elif check_message(['how', 'are', 'you']):
        general_conversations.how_are_you()

    elif check_message(['party', 'time']) \
      or check_message(['party', 'mix']):
        play_music.play_shuffle(profile_data['music_path'])

    elif check_message(['play', 'music']) \
      or check_message(['music']):
        play_music.play_random(profile_data['music_path'])

    elif check_message(['play']):
        play_music.play_specific_music(
            speech_text,
            profile_data['music_path'])

    elif check_message(['how', 'weather']) \
      or check_message(['hows', 'weather']):
        weather.weather(
            profile_data['city_name'],
            profile_data['city_code'])

    elif check_message(['time']):
        tell_time.what_is_time()

    elif check_message(['upload']):
        imgur_handler.image_uploader(
            speech_text,
            profile_data['imgur']['client_id'],
            profile_data['imgur']['client_secret'],
            profile_data['images_path'])

    elif check_message(['all', 'uploads']) \
      or check_message(['all', 'images']) \
      or check_message(['uploads']):
        imgur_handler.show_all_uploads()

    elif check_message(['feeling', 'angry']):
        lighting.feeling_angry()

    elif check_message(['feeling', 'creative']):
        lighting.feeling_creative()

    elif check_message(['feeling', 'lazy']):
        lighting.feeling_lazy()

    elif check_message(['dark']):
        lighting.very_dark()

    elif check_message(['lights', 'off']):
        lighting.turn_off()

    elif check_message(['sleep']):
        sleep.go_to_sleep()

    else:
        general_conversations.undefined()

