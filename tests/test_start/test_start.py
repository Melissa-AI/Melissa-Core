"""test start module."""
from itertools import product
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


M_TEXT = 'query_text'
NOT_WORKING_ON_FULL_TEST = "Not working on full test."
START_MODULE_REMOVED = 'start module removed'


@pytest.mark.xfail(reason=NOT_WORKING_ON_FULL_TEST)
def test_import():
    """test import.

    error is raised
    because profile populator run and raise error when testing.
    """
    with pytest.raises(IOError):
        from start import main  # NOQA


@pytest.mark.xfail(reason=NOT_WORKING_ON_FULL_TEST)
def test_mock_pp():
    """test with mocked populator."""
    with mock.patch('melissa.profile_populator.profile_populator'):
        with pytest.raises(IOError):
            from start import main  # NOQA


@pytest.mark.xfail(reason=NOT_WORKING_ON_FULL_TEST)
def test_import_module():
    """test simple import."""
    with pytest.raises(IOError):
        import start  # NOQA


@pytest.mark.xfail(reason=START_MODULE_REMOVED)
@pytest.mark.parametrize(
    'platform, m_stt_side_effect',
    product(
        ['linux', 'win32', 'darwin', 'random'],
        [
            KeyboardInterrupt,
            [None, KeyboardInterrupt],
            [M_TEXT, KeyboardInterrupt],
        ]
    )
)
def test_run_main(platform, m_stt_side_effect):
    """test run main func."""
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('start.tts') as m_tts, \
                mock.patch('start.subprocess') as m_subprocess, \
                mock.patch('start.stt') as m_stt, \
                mock.patch('start.load_profile') as m_load_profile, \
                mock.patch('start.sys') as m_sys, \
                mock.patch('start.query') as m_query:
            # pre run
            m_stt.side_effect = m_stt_side_effect
            m_sys.platform = platform
            # run
            import start
            with pytest.raises(KeyboardInterrupt):
                start.main()
            # test
            m_load_profile.assert_called_once_with(True)
            if platform.startswith('linux') or platform == 'win32':
                m_subprocess.call.assert_called_with(
                    ['mpg123', 'data/snowboy_resources/ding.wav'])
            elif platform == 'darwin':
                m_subprocess.call.assert_called_with(
                    ['afplay', 'data/snowboy_resources/ding.wav'])
            else:
                m_subprocess.call.assert_not_called()
            if m_stt_side_effect != KeyboardInterrupt:
                if m_stt_side_effect[0] == M_TEXT:
                    m_query.assert_called_once_with(M_TEXT)
                assert m_stt.call_count == 2
            else:
                m_query.assert_not_called()
                m_stt.assert_called_once_with()
            m_tts.assert_called()
