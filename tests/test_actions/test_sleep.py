"""test module."""
from StringIO import StringIO
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


@pytest.mark.parametrize('hotword_detection', ['on', 'off'])
def test_go_to_sleep(hotword_detection):
    """test func."""
    m_text = ''
    print_args = [
        '\nListening for Keyword...',
        'Press Ctrl+C to exit\n'
    ]
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.sleep.tts') as m_tts, \
                mock.patch('sys.stdout', new_callable=StringIO) \
                as m_stdout, \
                mock.patch('melissa.actions.sleep.random') \
                as m_random:
            # run
            from melissa.actions import sleep
            sleep.profile.data = {'hotword_detection': hotword_detection}
            with pytest.raises(SystemExit):
                sleep.go_to_sleep(m_text)
            # test
            m_stdout_value = m_stdout.getvalue()
            if hotword_detection == 'on':
                for arg in print_args:
                    assert arg in m_stdout_value
            else:
                assert not m_stdout_value
            m_tts.assert_called_once_with(m_random.choice.return_value)
            m_random.choice.assert_called_once_with(
                ['See you later!', "Just call my name and I'll be there!"])
