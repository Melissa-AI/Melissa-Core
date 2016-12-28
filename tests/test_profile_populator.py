"""test profile_populator module."""
import random
import string
from StringIO import StringIO
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest

from melissa.profile_populator import (
    profile_populator,
    tts_local,
)


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


class InputSideEffect:
    """side effect for mock input."""

    def __init__(self, question, first_return_value, other_return_value='',
                 non_match_return_value=''):
        """init func."""
        self.question_counter = 0
        self.question = question
        self.first_return_value = first_return_value
        self.other_return_value = other_return_value
        self.non_match_return_value = non_match_return_value

    def func(self, arg):
        """func to be run as side effect."""
        if arg == self.question:
            if self.question_counter == 0:
                self.question_counter += 1
                return self.first_return_value
            else:
                return self.other_return_value
        else:
            return self.non_match_return_value


def test_run():
    """test run profile_populator without mocking anything.

    function will fail with IOError because
    raw_input can't get used in test.
    """
    with pytest.raises(IOError):
        profile_populator()


def test_run_empty_input():
    """test profile_populator with mocking raw_input func.

    for this test mocked raw_input will only return empty string.
    """
    m = mock.mock_open()
    with mock.patch(
            'melissa.profile_populator.raw_input',
            return_value='') as mock_input, \
            mock.patch(
                'melissa.profile_populator.open',
                m, create=True) as mock_open, \
            mock.patch('melissa.profile_populator.json') as mock_json:
        profile_populator()

        assert mock_input.call_count == 13
        input_calls = [
            mock.call('What would you like to name me?: '),
            mock.call('What is my gender ((m)ale/(f)emale)?: '),
            mock.call('Your name: '),
            mock.call(
                'STT Engine ((g)oogle/(s)phinx/(t)elegram/(k)eyboard): '),
            mock.call('Your username at Telegram: '),
            mock.call('Path to your music directory: '),
            mock.call('Path to your images directory: '),
            mock.call('Name of city where you live: '),
            mock.call(
                'Code of city from weather.com '
                'or <ENTER> for a search '
                'based on the name of the city you live in: '),
            mock.call('Enter the index of the city of your choice: '),
            mock.call('(c)elsius/(f)ahrenheit): '),
            mock.call('Enter your gmail address (???@gmail.com): '),
            mock.call('Enter your icloud username/address (???@???.com): ')
        ]
        for call in input_calls:
            assert call in mock_input.mock_calls
        mock_open.assert_called_once_with('profile.json', 'w')

        keys_with_dict_value = (
            'gmail', 'icloud', 'imgur', 'ivona', 'pocketsphinx', 'twitter', )
        default_json = {
            'actions_db_file': ':memory:',
            'city_code': 'INXX0096',
            'city_name': 'New Delhi',
            'degrees': 'celsius',
            'gmail': {'address': '', 'password': ''},
            'hotword_detection': 'on',
            'icloud': {'password': '', 'username': ''},
            'images_path': '.',
            'imgur': {'client_id': 'xxxx', 'client_secret': 'xxxx'},
            'ivona': {'access_key': 'xxxx', 'secret_key': 'xxxx'},
            'memory_db': './data/memory.db',
            'modules': 'melissa.actions',
            'music_path': '.',
            'name': 'Tanay',
            'pocketsphinx': {
                'dic': 'lm/sphinx.dic', 'hmm': 'hmm/en_us/hub4wsj_sc_8k',
                'lm': 'lm/sphinx.lm', 'modeldir': './data/model/'},
            'stt': 'google',
            'telegram_token': 'xxxx',
            'telegram_username': 'tanay1337',
            'tts': 'xxxx',
            'twitter': {
                'access_token': 'xxxx', 'access_token_secret': 'xxxx',
                'consumer_key': 'xxxx', 'consumer_secret': 'xxxx'},
            'va_gender': 'female',
            'va_name': 'Melissa'
        }
        assert mock_json.dump.call_args[0][1] == mock_open.return_value
        result_json = mock_json.dump.call_args[0][0]
        assert len(result_json) == len(default_json)
        for key in result_json:
            if key not in keys_with_dict_value:
                assert result_json[key] == default_json[key]
            else:
                # keys with dict value
                assert len(result_json[key]) == len(default_json[key])
                for subdict_key in result_json[key]:
                    subdict_value = result_json[key][subdict_key]
                    assert subdict_value == default_json[key][subdict_key]


def test_pywapi_string_input():
    """test when giving pywapi func a string input."""
    random_city = get_random_string()

    def mock_input_side_effect(arg):
        """return empty string except when city is asked."""
        if arg == 'Name of city where you live: ':
            return random_city
        else:
            return ''

    m = mock.mock_open()
    with mock.patch(
            'melissa.profile_populator.raw_input',
            return_value='') as mock_input, \
        mock.patch(
            'melissa.profile_populator.pywapi') as mock_pywapi, \
            mock.patch(
                'melissa.profile_populator.open',
                m, create=True), \
            mock.patch('melissa.profile_populator.json'):
        mock_input.side_effect = mock_input_side_effect
        profile_populator()
        pywapi_func_input = \
            mock_pywapi.get_loc_id_from_weather_com.call_args[0][0]
        assert pywapi_func_input == random_city
        assert isinstance(pywapi_func_input, unicode)


def test_random_gender():
    """test random gender input."""
    random_gender = get_random_string(
        exclude_list=('male', 'm', 'female', 'f', ''))
    invalid_input_message = (
        'Invalid input, please enter male, female or <ENTER>.')
    gender_question = 'What is my gender ((m)ale/(f)emale)?: '
    m = mock.mock_open()

    with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
            mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
            mock.patch(
                'melissa.profile_populator.open',
                m, create=True
            ), \
            mock.patch('melissa.profile_populator.json') as mock_json:
        side_effect = InputSideEffect(gender_question, random_gender)
        mock_input.side_effect = side_effect.func
        # run the func.
        profile_populator()
        result_json = mock_json.dump.call_args[0][0]

        assert result_json['va_gender'] == 'female'
        assert invalid_input_message in mock_stdout.getvalue()


def test_valid_gender():
    """test random gender input."""
    data = (
        ('male', 'male'),
        ('m', 'male'),
        ('female', 'female'),
        ('f', 'female'),
        ('', 'female'),
    )
    for gender, expected_value in data:
        gender_question = 'What is my gender ((m)ale/(f)emale)?: '
        m = mock.mock_open()

        def mock_input_side_effect(arg):
            if arg == gender_question:
                return gender
            return ''

        with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
                mock.patch('melissa.profile_populator.tts_local'), \
                mock.patch(
                    'melissa.profile_populator.open',
                    m, create=True
                ), \
                mock.patch('melissa.profile_populator.json') as mock_json:
            mock_input.side_effect = lambda x: \
                gender if x == gender_question else ''
            # run the func.
            profile_populator()
            result_json = mock_json.dump.call_args[0][0]

            assert result_json['va_gender'] == expected_value


def test_random_stt():
    """test random stt."""
    valid_stt = (
        'g', 'google', 's', 'sphinx', 'k', 'keyboard', 't', 'telegram', '')

    random_stt = get_random_string(exclude_list=valid_stt)
    invalid_input_message = (
        'Invalid input, please enter(g)oogle, (s)phinx, (t)elegram,(k)eyboard '
        'or < ENTER > .')
    stt_question = 'STT Engine ((g)oogle/(s)phinx/(t)elegram/(k)eyboard): '
    m = mock.mock_open()

    with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
            mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
            mock.patch(
                'melissa.profile_populator.open',
                m, create=True
            ), \
            mock.patch('melissa.profile_populator.json') as mock_json:
        side_effect = InputSideEffect(stt_question, random_stt)
        mock_input.side_effect = side_effect.func
        # run the func.
        profile_populator()
        result_json = mock_json.dump.call_args[0][0]

        assert result_json['stt'] == 'google'
        assert invalid_input_message in mock_stdout.getvalue()


def test_valid_stt_input():
    """test valid stt input."""
    data = (
        # lowercase input
        ('g', 'google'),
        ('google', 'google'),
        ('s', 'sphinx'),
        ('sphinx', 'sphinx'),
        ('k', 'keyboard'),
        ('keyboard', 'keyboard'),
        ('t', 'telegram'),
        ('telegram', 'telegram'),
        ('', 'google'),
        # uppercase input
        ('G', 'google'),
        ('GOOGLE', 'google'),
        ('K', 'keyboard'),
        ('KEYBOARD', 'keyboard'),
        ('S', 'sphinx'),
        ('SPHINX', 'sphinx'),
        ('T', 'telegram'),
        ('TELEGRAM', 'telegram'),
    )
    for stt_code, expected_value in data:
        m = mock.mock_open()
        stt_question = (
            'STT Engine ((g)oogle/(s)phinx/(t)elegram/(k)eyboard): ')

        def mock_input_side_effect(arg):
            if arg == stt_question:
                return stt_code
            return ''

        with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
                mock.patch('melissa.profile_populator.tts_local'), \
                mock.patch(
                    'melissa.profile_populator.open',
                    m, create=True
                ), \
                mock.patch('melissa.profile_populator.json') as mock_json:
            mock_input.side_effect = mock_input_side_effect
            # run the func.
            profile_populator()

            result_json = mock_json.dump.call_args[0][0]
            assert result_json['stt'] == expected_value


def test_existing_path():
    """test existing path."""
    data = (
        # data key, question
        ('music_path', 'Path to your music directory: '),
        ('images_path', 'Path to your images directory: '),
    )
    random_path = mock.Mock()
    for data_key, question in data:
        m = mock.mock_open()

        def mock_input_side_effect(arg):  # NOQA
            if arg == question:
                return random_path
            return ''

        with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
                mock.patch('melissa.profile_populator.tts_local'), \
                mock.patch(
                    'melissa.profile_populator.open',
                    m, create=True
                ), \
                mock.patch('melissa.profile_populator.os') as mock_os, \
                mock.patch('melissa.profile_populator.json') as mock_json:
            mock_input.side_effect = mock_input_side_effect
            mock_os.path.isdir.return_value = True
            # run the func.
            profile_populator()
            mock_os.path.isdir.assert_called_once_with(random_path)
            result_json = mock_json.dump.call_args[0][0]
            assert result_json[data_key] == random_path


def test_invalid_path():
    """test random path."""
    random_path = mock.Mock()
    default_path = '.'
    invalid_input_message = (
        'Invalid input, please enter a valid directory path or <ENTER>.')
    data = (
        # data key, question
        ('music_path', 'Path to your music directory: '),
        ('images_path', 'Path to your images directory: '),
    )
    m = mock.mock_open()

    for data_key, question in data:
        with mock.patch(
                'melissa.profile_populator.raw_input') as mock_input, \
                mock.patch(
                    'sys.stdout', new_callable=StringIO) as mock_stdout, \
                mock.patch('melissa.profile_populator.os') as mock_os, \
                mock.patch(
                    'melissa.profile_populator.open',
                    m, create=True
                ), \
                mock.patch('melissa.profile_populator.json') as mock_json:
            side_effect = InputSideEffect(question, random_path)
            mock_input.side_effect = side_effect.func
            mock_os.path.isdir.return_value = False
            # run the func.
            profile_populator()
            result_json = mock_json.dump.call_args[0][0]

            assert result_json[data_key] == default_path
            assert invalid_input_message in mock_stdout.getvalue()


def test_empty_result_from_pywapi():
    """test when pywapi return empty list."""
    m = mock.mock_open()
    emtpy_result_message = 'Sorry, search results were empty.'
    default_city_code = 'INXX0096'
    with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
            mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
            mock.patch('melissa.profile_populator.pywapi') as mock_pywapi, \
            mock.patch(
                'melissa.profile_populator.open',
                m, create=True
            ), \
            mock.patch('melissa.profile_populator.json') as mock_json:
        mock_input.return_value = ''
        mock_pywapi.get_loc_id_from_weather_com.return_value = {'count': 0}
        # run the func.
        profile_populator()
        result_json = mock_json.dump.call_args[0][0]
        assert result_json['city_code'] == default_city_code
        assert emtpy_result_message in mock_stdout.getvalue()


def test_char_as_input_on_city_choices():
    """test when char on city choices."""
    question = 'Enter the index of the city of your choice: '
    random_city = get_random_string()
    random_city_code = get_random_string()
    mock_input_call = 'Enter the index of the city of your choice: '
    with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
            mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
            mock.patch('melissa.profile_populator.pywapi') as mock_pywapi:
        mock_input.side_effect = (
            lambda x: get_random_string() if x == question else '')
        # example of the actual pywapi return_value
        # {0: (u'INXX0096', u'New Delhi, DL, India'),
        # 1: (u'USNY0378', u'Delhi, NY'),
        # 2: (u'INXX0142', u'New Delhi/Safdarjung, DL, India'),
        # 'count': 3}
        mock_pywapi.get_loc_id_from_weather_com.return_value = {
            0: (random_city_code, random_city),
            'count': 1}

        # run the func.
        with pytest.raises(ValueError):
            profile_populator()

        assert '1: {}'.format(random_city) in mock_stdout.getvalue()
        mock_input.assert_called_with(mock_input_call)


def test_invalid_choose_the_city():
    """test choose the city."""
    question = 'Enter the index of the city of your choice: '
    random_city = get_random_string()
    random_city_code = get_random_string()
    m = mock.mock_open()
    invalid_input_message = \
        'Enter an index from one of the choices. Try again!'

    with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
            mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
            mock.patch('melissa.profile_populator.pywapi') as mock_pywapi, \
            mock.patch('melissa.profile_populator.open', m, create=True), \
            mock.patch('melissa.profile_populator.json') as mock_json:
        side_effect = InputSideEffect(question, 100, 1)
        mock_input.side_effect = side_effect.func
        # example of the actual pywapi return_value
        # {0: (u'INXX0096', u'New Delhi, DL, India'),
        # 1: (u'USNY0378', u'Delhi, NY'),
        # 2: (u'INXX0142', u'New Delhi/Safdarjung, DL, India'),
        # 'count': 3}
        mock_pywapi.get_loc_id_from_weather_com.return_value = {
            0: (random_city_code, random_city),
            'count': 1}
        # run the func.
        profile_populator()
        result_json = mock_json.dump.call_args[0][0]
        assert result_json['city_code'] == random_city_code
        assert '1: {}'.format(random_city) in mock_stdout.getvalue()
        assert invalid_input_message in mock_stdout.getvalue()


def test_invalid_degree_unit():
    """test invalid degree unit."""
    valid_unit = ('c', 'celsius', 'f', 'fahrenheit', '')
    random_unit = get_random_string(exclude_list=valid_unit)
    default_unit = 'celsius'
    m = mock.mock_open()
    invalid_input_message = \
        'Invalid input, please enter(c)elsius, (f)ahrenheit) or<ENTER > .'
    m = mock.mock_open()
    question = '(c)elsius/(f)ahrenheit): '

    with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
            mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
            mock.patch('melissa.profile_populator.open', m, create=True), \
            mock.patch('melissa.profile_populator.json') as mock_json:
        side_effect = InputSideEffect(question, random_unit)
        mock_input.side_effect = side_effect.func

        profile_populator()

        result_json = mock_json.dump.call_args[0][0]
        assert result_json['degrees'] == default_unit
        assert invalid_input_message in mock_stdout.getvalue()


def test_valid_degree_unit():
    """test valid degree unit."""
    question = '(c)elsius/(f)ahrenheit): '
    data = (
        ('', 'celsius'),
        # lowercase
        ('c', 'celsius'),
        ('celsius', 'celsius'),
        ('f', 'fahrenheit'),
        ('fahrenheit', 'fahrenheit'),
        # uppercase
        ('C', 'celsius'),
        ('CELSIUS', 'celsius'),
        ('F', 'fahrenheit'),
        ('FAHRENHEIT', 'fahrenheit'),
    )
    for degree, expected_value in data:
        m = mock.mock_open()

        with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
                mock.patch('melissa.profile_populator.open', m, create=True), \
                mock.patch('melissa.profile_populator.tts_local'), \
                mock.patch('melissa.profile_populator.json') as mock_json:
            side_effect = InputSideEffect(question, degree)
            mock_input.side_effect = side_effect.func

            profile_populator()

            result_json = mock_json.dump.call_args[0][0]
            assert result_json['degrees'] == expected_value


def test_gmail_account():
    """test gmail input."""
    question = 'Enter your gmail address (???@gmail.com): '
    random_address = get_random_string()
    random_password = get_random_string()
    m = mock.mock_open()

    with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
            mock.patch('melissa.profile_populator.open', m, create=True), \
            mock.patch('melissa.profile_populator.tts_local'), \
            mock.patch('melissa.profile_populator.getpass') as mock_getpass, \
            mock.patch('melissa.profile_populator.json') as mock_json:
        side_effect = InputSideEffect(question, random_address)
        mock_input.side_effect = side_effect.func
        mock_getpass.return_value = random_password

        profile_populator()

        result_json = mock_json.dump.call_args[0][0]
        assert random_address == result_json['gmail']['address']
        assert random_password == result_json['gmail']['password']
        mock_getpass.assert_called_once_with()


def test_icloud_account():
    """test gmail input."""
    question = \
        'Enter your icloud username/address (???@???.com): '

    random_address = get_random_string()
    random_password = get_random_string()
    m = mock.mock_open()

    with mock.patch('melissa.profile_populator.raw_input') as mock_input, \
            mock.patch('melissa.profile_populator.open', m, create=True), \
            mock.patch('melissa.profile_populator.tts_local'), \
            mock.patch('melissa.profile_populator.getpass') as mock_getpass, \
            mock.patch('melissa.profile_populator.json') as mock_json:
        side_effect = InputSideEffect(question, random_address)
        mock_input.side_effect = side_effect.func
        mock_getpass.return_value = random_password

        profile_populator()

        result_json = mock_json.dump.call_args[0][0]
        assert random_address == result_json['icloud']['username']
        assert random_password == result_json['icloud']['password']
        mock_getpass.assert_called_once_with()


def test_valid_platform_tts_local():
    """test tts local for darwin platform."""
    mock_message = mock.Mock()
    data = (
        ('darwin', ['say', mock_message]),
        ('linux', ['espeak', '-s170', mock_message]),
        ('win32', ['espeak', '-s170', mock_message]),
    )
    for platform, subprocess_call in data:
        with mock.patch('melissa.profile_populator.sys') as mock_sys, \
                mock.patch(
                    'melissa.profile_populator.subprocess') as mock_subprocess:
            mock_sys.platform = platform
            res = tts_local(mock_message)
            mock_subprocess.call.assert_called_once_with(subprocess_call)
            assert res == mock_subprocess.call.return_value


def test_random_platform_tts_local():
    """test tts local for random platform."""
    mock_message = mock.Mock()
    valid_platform = ('darwin', 'linux', 'win32')
    with mock.patch('melissa.profile_populator.sys') as mock_sys, \
            mock.patch(
                'melissa.profile_populator.subprocess') as mock_subprocess:
        mock_sys.platform = get_random_string(exclude_list=valid_platform)
        res = tts_local(mock_message)
        assert not mock_subprocess.call_count
        assert res is None
