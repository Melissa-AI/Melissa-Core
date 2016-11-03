"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


@pytest.mark.parametrize(
    'degrees, expected_temp',
    [
        ('fahrenheit', 77),
        ('celcius', 25)
    ]
)
def test_post_tweet(degrees, expected_temp):
    """test func."""
    m_text = mock.Mock()
    actual_temp_in_celcius = 25
    city_name = 'city_name'
    city_code = mock.Mock()
    weather_cond = 'cloudy'
    profile_data = {
        'city_name': city_name,
        'city_code': city_code,
        'degrees': degrees,
    }
    weather_result = {
        'current_conditions': {
            'temperature': actual_temp_in_celcius,
            'text': weather_cond
        }
    }
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.weather.tts') \
                as m_tts, \
                mock.patch('melissa.actions.weather.pywapi') \
                as m_pywapi:
            # pre run
            from melissa.actions import weather
            weather.profile.data = profile_data
            m_pywapi.get_weather_from_weather_com.return_value = weather_result
            # run
            weather.weather(m_text)
            # test
            m_tts.assert_called_once_with(
                'Weather.com says: It is {} and {}degrees {} now '
                'in {}'.format(
                    weather_cond, float(expected_temp), degrees, city_name
                )
            )
            m_pywapi.get_weather_from_weather_com.assert_called_once_with(
                city_code
            )
