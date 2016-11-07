"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock


def test_repeat_text():
    """test func."""
    m_text = 'repeat this text'
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.repeat.tts') as m_tts:
            from melissa.actions import repeat
            repeat.repeat_text(m_text)
            m_tts.assert_called_once_with('this text')
