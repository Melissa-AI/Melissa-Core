"""test stt module."""
import random
import string
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest

skip_because_stt_removed = pytest.mark.skip(reason='stt module removed.')


def get_random_string(exclude_list=None):
    """get random gender which is not 'female' or 'male'."""
    exclude_list = [] if exclude_list is None else exclude_list
    length = 10
    result = ''.join(random.choice(string.lowercase) for i in range(length))
    while result in exclude_list:
        result = ''.join(
            random.choice(string.lowercase) for i in range(length)
        )
    return result


# taken from http://stackoverflow.com/a/8658332
# mocking the import so mock_profile could be loaded.
# Store original __import__
orig_import = __import__
mock_name = get_random_string()
default_profile_data = {
    'va_name': mock.Mock(),
    'name': mock_name,
    'stt': mock.Mock()
}
mock_profile = mock.Mock()
mock_profile.data = default_profile_data
mock_tts = mock.Mock()


# mock_import side effect
def import_mock(name, *args):
    """import mock side effect."""
    names = ('profile_populator', 'profile', 'actions_db', 'pyvona')
    for n in names:
        if name == 'profile':
            return mock_profile
        elif n == name:
            return mock.Mock()
    return orig_import(name, *args)


@skip_because_stt_removed
def test_run():
    """test run."""
    with mock.patch('__builtin__.__import__', side_effect=import_mock), \
            mock.patch('melissa.stt.sr') as mock_sr, \
            mock.patch('melissa.stt.tts') as mock_tts:
        from melissa.stt import stt
        stt()
    mock_tts.assert_not_called()
    mock_sr.Recognizer.assert_called_once_with()


@skip_because_stt_removed
def test_run_google_stt_with_error():
    """test run with google stt with error.

    when this test run,
    an error will be raised when trying to print the speech_text.
    """
    profile_data = default_profile_data
    profile_data['stt'] = 'google'
    mock_profile.data = profile_data
    with mock.patch('__builtin__.__import__', side_effect=import_mock),\
            mock.patch('melissa.stt.sr') as mock_sr, \
            mock.patch('melissa.stt.tts'):
        from melissa.stt import stt
        with pytest.raises(TypeError):
            stt()
        assert len(mock_sr.mock_calls) == 8
        assert mock_sr.Microphone.call_count == 1
        mock_mic_enter = mock_sr.Microphone().__enter__()
        mock_recognizer_listen = mock_sr.Recognizer().listen()
        sr_calls = [
            mock.call.Recognizer(),
            mock.call.Microphone(),
            mock.call.Microphone().__enter__(),
            mock.call.Recognizer().listen(mock_mic_enter),
            mock.call.Microphone().__exit__(None, None, None),
            mock.call.Recognizer()
            .recognize_google(mock_recognizer_listen),
            mock.call.Recognizer()
            .recognize_google().lower(),
            mock.call.Recognizer()
            .recognize_google().lower().replace("'", ''),
        ]
        for call in sr_calls:
            assert call in mock_sr.mock_calls


@skip_because_stt_removed
def test_run_google_stt():
    """test run with google stt.

    At the first run, it will run normally.
    On the next run an error will be raised to stop the loop.
    """
    profile_data = default_profile_data
    profile_data['stt'] = 'google'
    va_name = get_random_string()
    profile_data['va_name'] = va_name
    mock_profile.data = profile_data
    random_audio_text = get_random_string()
    with mock.patch('__builtin__.__import__', side_effect=import_mock),\
            mock.patch('melissa.stt.sr') as mock_sr, \
            mock.patch('melissa.stt.tts'):
        from melissa.stt import stt
        raised_error = KeyboardInterrupt
        mock_sr.Recognizer.return_value.listen.side_effect = [
            mock.Mock(), raised_error()]
        mock_sr.Recognizer.return_value.recognize_google.return_value = \
            random_audio_text
        stt()


@skip_because_stt_removed
def test_run_sphinx_stt():
    """test run with sphinx stt.

    At the first run, it will run normally.
    On the next run an error will be raised to stop the loop.
    """
    profile_data = default_profile_data
    profile_data['stt'] = 'sphinx'
    mock_flag_modeldir = mock_flag_hmm = mock.Mock()
    mock_flag_lm = mock_flag_dic = mock.Mock()
    profile_data['pocketsphinx'] = {
        'modeldir': mock_flag_modeldir,
        'hmm': mock_flag_hmm,
        'lm': mock_flag_lm,
        'dic': mock_flag_dic,
    }
    mock_profile.data = profile_data

    mock_open = mock.mock_open()
    with mock.patch('__builtin__.__import__', side_effect=import_mock),\
            mock.patch('melissa.stt.sr') as mock_sr, \
            mock.patch('melissa.stt.Decoder') as mock_decoder, \
            mock.patch('melissa.stt.open', mock_open, create=True), \
            mock.patch('melissa.stt.tts'):
        from melissa.stt import stt
        raised_error = ValueError
        mock_audio = mock.Mock()
        mock_sr.Recognizer.return_value.listen.side_effect = [
            mock_audio, raised_error()]
        stt()
        mock_audio.get_wav_data.assert_called_once_with()
        assert len(mock_sr.mock_calls) == 5
        assert len(mock_open.mock_calls) == 7
        mock_open_data = [
            mock.call('recording.wav', 'wb'),
            mock.call().__enter__(),
            mock.call().write(mock_audio.get_wav_data()),
            mock.call().__exit__(None, None, None),
            mock.call('recording.wav', 'rb'),
            mock.call().seek(44),
            mock.call().read()
        ]
        for item in mock_open_data:
            assert item in mock_open.mock_calls

        mock_decoder_config = mock_decoder.default_profile_data()
        mock_decoder_data = [
            mock.call.default_config(),
            mock.call.default_config().set_string('-hmm', mock_flag_hmm),
            mock.call.default_config().set_string('-lm', mock_flag_lm),
            mock.call.default_config().set_string('-dict', mock_flag_dic),
            mock.call.default_config().set_string('-logfn', '/dev/null'),
            mock.call(mock_decoder_config()),
            mock.call().start_utt(),
            mock.call().process_raw('', False, True),
            mock.call().end_utt(),
            mock.call().hyp(),
            # mock.call().hyp().hypstr.__radd__().__add__("'"),
            # mock.call().hyp().hypstr.__radd__().__add__().__str__(),
            mock.call().hyp().hypstr.lower(),
            mock.call().hyp().hypstr.lower().replace("'", ''),
        ]
        for item in mock_decoder_data:
            assert item in mock_decoder.mock_calls


@skip_because_stt_removed
def test_run_keyboard_stt():
    """test run with keyboard stt.

    At the first run, it will run normally.
    On the next run an error will be raised to stop the loop.
    """
    profile_data = default_profile_data
    profile_data['stt'] = 'keyboard'
    with mock.patch('__builtin__.__import__', side_effect=import_mock),\
            mock.patch('melissa.stt.raw_input') as mock_input, \
            mock.patch('melissa.stt.tts'):
        from melissa.stt import stt
        mock_text = mock.Mock()
        raised_error = ValueError
        mock_input.side_effect = [mock_text, raised_error()]
        stt()
        assert mock_input.call_count == 1
        assert mock.call('Write something: ') in mock_input.mock_calls


@skip_because_stt_removed
def test_run_telegram_stt_wrong_token():
    """test run with telegram stt with wrong token."""
    profile_data = default_profile_data
    profile_data['stt'] = 'telegram'
    wrong_token = 'xxxx'
    profile_data['telegram_token'] = wrong_token

    with mock.patch('__builtin__.__import__', side_effect=import_mock),\
            mock.patch('melissa.stt.tts') as mock_tts:
        from melissa.stt import stt
        with pytest.raises(SystemExit):
            stt()
        mock_tts_call = (
            'Please enter a Telegram token or configure a different STT'
            ' in the profile.json file.')
        mock_tts.assert_called_with(mock_tts_call)
        assert mock_tts.call_count == 1


@skip_because_stt_removed
def test_run_telegram_stt():
    """test run with telegram stt with wrong token."""
    profile_data = default_profile_data
    profile_data['stt'] = 'telegram'
    mock_token = mock.Mock()
    profile_data['telegram_token'] = mock_token

    with mock.patch('__builtin__.__import__', side_effect=import_mock),\
            mock.patch('melissa.stt.tts'), \
            mock.patch('melissa.stt.time') as mock_time, \
            mock.patch('melissa.stt.telepot') as mock_telepot:
        raised_error = KeyboardInterrupt
        mock_time.sleep.side_effect = [mock.Mock(), raised_error()]
        from melissa.stt import stt
        with pytest.raises(raised_error):
            stt()
        assert len(mock_telepot.mock_calls) == 2
        mock_telepot.Bot.assert_called_with(mock_token)
        assert mock_telepot.Bot.return_value.notifyOnMessage.called
        assert mock_time.sleep.call_count == 2
        mock_time.sleep.called_with(10)
