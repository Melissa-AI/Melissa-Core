"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


@pytest.mark.parametrize(
    'arg, strftime_expected_format',
    [
        ('date', '%m/%d/%Y'),
        ('day', '%A'),
        ('time', '%H:%M:%S'),
    ]
)
def test_tell_time(arg, strftime_expected_format):
    """test func."""
    strftime_retval = 'strftime_retval'
    m_text = mock.Mock()
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.tell_time.tts') \
                as m_tts, \
                mock.patch('melissa.actions.tell_time.datetime') \
                as m_datetime:
            m_datetime.strftime.return_value = strftime_retval
            from melissa.actions import tell_time
            if arg == 'date':
                tell_time.what_is_date(m_text)
            elif arg == 'time':
                tell_time.what_is_time(m_text)
            elif arg == 'day':
                tell_time.what_is_day(m_text)
            m_tts.assert_called_once_with(
                'The {} is {}'.format(arg, strftime_retval))
            m_datetime.assert_has_calls([
                mock.call.now(),
                mock.call.strftime(
                    m_datetime.now.return_value,
                    strftime_expected_format
                )
            ])
