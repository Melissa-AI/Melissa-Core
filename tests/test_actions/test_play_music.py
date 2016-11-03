"""test module."""
import itertools
from StringIO import StringIO
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


def test_music_player():
    """test fun."""
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.play_music.os') as m_os:
            from melissa.actions.play_music import music_player
            res = music_player(['item0', 'item1'])
            m_os.system.assert_called_once_with("item0 'item1'")
            assert res == m_os.system.return_value


@pytest.mark.parametrize('raise_index_error', [True, False])
def test_play_random(raise_index_error):
    """test func."""
    m_text = mock.Mock()
    m_file = 'm_file'
    choice_retval = ['', m_file]
    m_ext = 'm_ext'
    split_ext_retval = ['', m_ext]
    index_err_msg = 'error'
    with mock.patch('melissa.actions.play_music.mp3gen') as m_mp3gen, \
            mock.patch('melissa.actions.play_music.os') as m_os, \
            mock.patch('melissa.actions.play_music.tts') as m_tts, \
            mock.patch('sys.stdout', new_callable=StringIO) as m_stdout, \
            mock.patch('melissa.actions.play_music.random') as m_random, \
            mock.patch('melissa.actions.play_music.music_player') as m_mp:
        # prepare
        m_random.choice.return_value = choice_retval
        if raise_index_error:
            m_os.path.splitext.side_effect = IndexError(index_err_msg)
        else:
            m_os.path.splitext.return_value = split_ext_retval
        from melissa.actions.play_music import play_random
        # run
        play_random(m_text)
        # test
        m_mp3gen.assert_called_once_with()
        m_os.path.splitext.assert_called_once_with(m_file)
        m_random.choice.assert_called_once_with(None)
        if not raise_index_error:
            m_tts.assert_called_once_with('Now playing: ')
            assert m_stdout.getvalue() == ''
            m_mp.assert_called_once_with(choice_retval)
        else:
            m_tts.assert_called_once_with('No music files found.')
            assert 'No music files found: {}'.format(index_err_msg) \
                in m_stdout.getvalue()
            m_mp.assert_not_called()


def test_play_specific_music():
    """test func."""
    msg = 'm_music'
    speech_text = 'play {}'.format(msg)
    music_listing_item = ['', msg]
    with mock.patch('melissa.actions.play_music.mp3gen') \
            as m_mp3gen, \
            mock.patch('melissa.actions.play_music.music_player') \
            as m_music_player:
        # run
        from melissa.actions import play_music
        play_music.music_listing = [music_listing_item]
        play_music.play_specific_music(speech_text)
        # tests
        m_mp3gen.assert_called_once_with()
        m_music_player.assert_called_once_with(music_listing_item)


@pytest.mark.parametrize(
    'platform, m_file_ext',
    list(itertools.product(
        ['darwin', 'win32', 'linux', 'random'],
        ['.wav', '.flac', 'ogg', '.mp3', '.mp4']
    ))
)
def test_mp3gen(platform, m_file_ext):
    """test func."""
    m_music_path = 'm_music_path'
    splitext_retval = ['filename', m_file_ext]
    m_root = mock.Mock()
    m_file = mock.Mock()
    walk_retval = [(m_root, None, [m_file])]
    with mock.patch('melissa.actions.play_music.sys') \
            as m_sys, \
            mock.patch('sys.stdout', new_callable=StringIO) \
            as m_stdout, \
            mock.patch('melissa.actions.play_music.os') \
            as m_os:
        # pre run
        m_os.path.splitext.return_value = splitext_retval
        m_os.walk.return_value = walk_retval
        m_sys.platform = platform
        # run
        from melissa.actions import play_music
        play_music.profile.data = {'music_path': m_music_path}
        play_music.music_listing = None
        play_music.mp3gen()
        # test
        cmd = None
        if platform in ('win32', 'linux') and m_file_ext == '.mp3':
            cmd = 'mpg123'
        elif platform in ('win32', 'linux') and \
                m_file_ext in play_music.sox_file_types:
            cmd = 'play'
        elif platform == 'darwin' and m_file_ext == '.mp3':
            cmd = 'afplay'
        if platform == 'random':
            assert \
                'Music only enabled on darwin, win32, and linux.' in \
                m_stdout.getvalue()
            m_file.assert_not_called()
            assert not m_os.mock_calls
        else:
            if m_file_ext == '.mp3':
                m_os.assert_has_calls([
                    mock.call.walk(m_music_path),
                    mock.call.path.splitext(m_file),
                    mock.call.path.join(m_root, m_file.lower.return_value),
                ])
            elif m_file_ext in play_music.sox_file_types:
                m_os.assert_has_calls([
                    mock.call.walk(m_music_path),
                    mock.call.path.splitext(m_file),
                    mock.call.path.splitext(m_file)
                ])
            if cmd is not None:
                assert play_music.music_listing == [[
                    cmd, m_os.path.join.return_value]]
                m_file.lower.assert_called_once_with()
            else:
                assert not m_file.mock_calls
                m_os.assert_has_calls([
                    mock.call.walk(m_music_path),
                    mock.call.path.splitext(m_file),
                    mock.call.path.splitext(m_file)
                ])


def test_mp3gen_with_non_empty_music_listing():
    """test func."""
    music_item = mock.Mock()
    with mock.patch('melissa.actions.play_music.sys') \
            as m_sys, \
            mock.patch('sys.stdout', new_callable=StringIO) \
            as m_stdout, \
            mock.patch('melissa.actions.play_music.os') \
            as m_os:
        # run
        from melissa.actions import play_music
        play_music.music_listing = [[music_item]]
        play_music.mp3gen()
        assert play_music.music_listing == [[music_item]]
        assert not m_sys.mock_calls
        assert '' == m_stdout.getvalue()
        assert not m_os.mock_calls


@pytest.mark.parametrize('raise_index_error', [True, False])
def test_play_shuffle(raise_index_error):
    """test func."""
    music_item = mock.Mock()
    m_text = mock.Mock()
    m_index = 0
    with mock.patch('melissa.actions.play_music.mp3gen') \
            as m_mp3gen, \
            mock.patch('sys.stdout', new_callable=StringIO) \
            as m_stdout, \
            mock.patch('melissa.actions.play_music.tts') \
            as m_tts, \
            mock.patch('melissa.actions.play_music.music_player') \
            as m_music_player, \
            mock.patch('melissa.actions.play_music.random') \
            as m_random:
        # pre run
        if raise_index_error:
            m_music_player.side_effect = IndexError(m_index)
        # run
        from melissa.actions import play_music
        play_music.music_listing = [music_item]
        play_music.play_shuffle(m_text)
        # tests
        m_mp3gen.assert_called_once_with()
        m_random.shuffle.assert_called_once_with([music_item])
        if not raise_index_error:
            m_music_player.assert_called_once_with(music_item)
            m_tts.assert_not_called()
            assert '' == m_stdout.getvalue()
        else:
            m_tts.assert_called_once_with('No music files found.')
            assert 'No music files found: 0' in m_stdout.getvalue()
