"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


@pytest.mark.parametrize(
    'arg, blink1_arg, tts_arg',
    [
        ('very_dark', '--white', 'Better now?'),
        ('feeling_angry', '--cyan', 'Calm down dear!'),
        ('feeling_creative', '--magenta', 'So good to hear that!'),
        ('feeling_lazy', '--yellow', 'Rise and shine dear!'),
        ('turn_off', '--off', None),
    ]
)
def test_lighting(arg, blink1_arg, tts_arg):
    """test func."""
    m_text = mock.Mock()
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.lighting.subprocess') \
                as m_subprocess, \
                mock.patch('melissa.actions.lighting.tts') \
                as m_tts:
            from melissa.actions import lighting
            if arg == 'very_dark':
                lighting.very_dark(m_text)
            elif arg == 'feeling_angry':
                lighting.feeling_angry(m_text)
            elif arg == 'feeling_creative':
                lighting.feeling_creative(m_text)
            elif arg == 'feeling_lazy':
                lighting.feeling_lazy(m_text)
            elif arg == 'turn_off':
                lighting.turn_off(m_text)
            m_subprocess.call.assert_called_once_with(
                ['blink1-tool', blink1_arg])
            if tts_arg is not None:
                m_tts.assert_called_once_with(tts_arg)
