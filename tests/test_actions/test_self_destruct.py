"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


def test_self_destruct():
    """test func."""
    m_text = ''
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.self_destruct.tts') as m_tts, \
                mock.patch('melissa.actions.self_destruct.subprocess') \
                as m_subprocess:
            from melissa.actions import self_destruct
            with pytest.raises(SystemExit):
                self_destruct.self_destruct(m_text)
            m_subprocess.call.assert_called_once_with(
                ['sudo', 'rm', '-r', '../Melissa-Core']
            )
            m_tts.assert_called_once_with(
                'Self destruction mode engaged, over and out.')
