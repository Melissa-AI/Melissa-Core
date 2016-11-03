"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock


def test_spell_text():
    """test func."""
    m_text = mock.Mock()
    sub_text = 'm_sub_text'
    expected_tts_arg = 'm _ s u b _ t e x t'
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.spelling.tts') as m_tts:
            from melissa.actions import spelling
            m_text.split.return_value = [None, sub_text]
            spelling.spell_text(m_text)
            m_text.split.assert_called_once_with(' ', 1)
            m_tts.assert_called_once_with(expected_tts_arg)
