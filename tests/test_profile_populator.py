
"""test profile_populator module."""
import random
import string
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest

from melissa.profile_populator import profile_populator


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


@pytest.mark.xfail
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
