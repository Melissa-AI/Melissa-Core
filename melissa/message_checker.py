def message_checker(message, words):
    words_of_message = message.split()
    if set(words).issubset(set(words_of_message)):
        return True
    else:
        return False
