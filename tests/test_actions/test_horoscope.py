"""test horoscope modulue."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock


def test_tell_horoscope():
    """test where_born func."""
    m_text = mock.Mock()
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.horoscope.tts') \
                as m_tts, \
                mock.patch(
                    'melissa.actions.horoscope.HoroscopeGenerator') \
                as m_h_gen:
            # run
            from melissa.actions.horoscope import tell_horoscope
            tell_horoscope(m_text)
            # test
            m_tts.assert_called_once_with(
                m_h_gen.format_sentence.return_value)
            m_h_gen.assert_has_calls = [
                mock.call.get_sentence(),
                mock.call.format_sentence(
                    m_h_gen.get_sentence.return_value
                )
            ]
