"""test imgur_handler module."""
import itertools
from StringIO import StringIO
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest

# imgur key
M_CLIENT_ID = 'm_client_id'
M_CLIENT_SECRET = 'm_client_secret'
# memory key
M_MEMORY_DB = 'm_memory_db'
# image path key
M_IMAGES_PATH = 'm_images_path'


@pytest.mark.parametrize(
    'm_ext',
    ['.tiff', '.png', '.gif', '.jpg']
)
def test_img_list_gen(m_ext):
    """test img_list_gen func."""
    m_root = mock.Mock()
    m_file = mock.Mock()
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.imgur_handler.os') as m_os:
            # pre run.
            m_os.walk.return_value = [(m_root, '', [m_file])]
            m_os.path.splitext.return_value = ['', m_ext]
            # run
            from melissa.actions import imgur_handler
            imgur_handler.profile.data = {
                'images_path': M_IMAGES_PATH
            }
            res = imgur_handler.img_list_gen()
            # test
            m_os.assert_has_calls([
                mock.call.walk(M_IMAGES_PATH),
                mock.call.path.splitext(m_file),
                mock.call.path.join(m_root, m_file.lower.return_value)
            ])
            assert res == [m_os.path.join.return_value]


def test_img_list_gen_incorrect_ext():
    """test img_list_gen func but with incorrect extension."""
    m_ext = '.mp3'
    m_root = mock.Mock()
    m_file = mock.Mock()
    with mock.patch('melissa.actions.imgur_handler.os') as m_os:
        # pre run.
        m_os.walk.return_value = [(m_root, '', [m_file])]
        m_os.path.splitext.return_value = ['', m_ext]
        # run
        from melissa.actions import imgur_handler
        res = imgur_handler.img_list_gen()
        # test
        assert res == []
        m_os.assert_has_calls([
            mock.call.walk(M_IMAGES_PATH),
            mock.call.path.splitext(m_file)
        ])


@pytest.mark.parametrize(
    'arg, m_image, gen_return_image',
    itertools.product(
        (mock.Mock(), 'upload image', 'upload'),
        ('image', 'nothing'),
        (True, False),
    )
)
def test_img_uploader(arg, m_image, gen_return_image):
    """test image uploader."""
    m_result_link = 'm_result_link'
    m_datetime_strftime = '04-11-2016'
    with mock.patch('melissa.actions.imgur_handler.tts') as m_tts, \
            mock.patch('melissa.actions.imgur_handler.ImgurClient') \
            as m_i_client, \
            mock.patch('sys.stdout', new_callable=StringIO) \
            as m_stdout, \
            mock.patch('melissa.actions.imgur_handler.sqlite3') \
            as m_sqlite3, \
            mock.patch('melissa.actions.imgur_handler.datetime') \
            as m_datetime, \
            mock.patch('melissa.actions.imgur_handler.img_list_gen') \
            as m_img_list_gen:
        from melissa.actions import imgur_handler
        imgur_handler.profile.data = {
            'imgur': {
                'client_id': M_CLIENT_ID,
                'client_secret': M_CLIENT_SECRET,
            },
            'memory_db': M_MEMORY_DB,
        }
        if isinstance(arg, mock.Mock):
            # run
            with pytest.raises(TypeError):
                imgur_handler.image_uploader(arg)
            # test
            arg.assert_has_calls([
                mock.call.split(),
                mock.call.split().remove('upload')
            ])

        elif arg == 'upload':
            imgur_handler.image_uploader(arg)
            m_tts.assert_called_once_with(
                'upload requires a picture name')
        elif arg == 'upload image':
            if not gen_return_image:
                imgur_handler.image_uploader(arg)
                m_tts.assert_not_called()
            elif m_image == 'nothing':
                m_img_list_gen.return_value = [m_image]
                imgur_handler.image_uploader(arg)
            elif m_image == 'image':
                # pre run
                m_img_list_gen.return_value = [m_image]
                m_i_client.return_value.upload_from_path.return_value = {
                    'link': m_result_link}
                m_datetime.strftime.return_value = m_datetime_strftime
                # run
                imgur_handler.image_uploader(arg)
                # test
                m_tts.assert_called_once_with(
                    'Your image has been uploaded')
                m_i_client.return_value.upload_from_path(
                    m_image, anon=True, config=None)
                m_sqlite3.assert_has_calls([
                    mock.call.connect(M_MEMORY_DB),
                    mock.call.connect().execute(
                        (
                            'INSERT INTO image_uploads '
                            '(filename, url, upload_date) '
                            'VALUES (?, ?, ?)'
                        ),
                        (
                            m_image,
                            m_result_link,
                            m_datetime_strftime
                        )
                    ),
                    mock.call.connect().commit(),
                    mock.call.connect().close()
                ])
                m_datetime.assert_has_calls([
                    mock.call.now(),
                    mock.call.strftime(
                        m_datetime.now.return_value, '%d-%m-%Y')
                ])
                assert m_result_link in m_stdout.getvalue()
            m_i_client.assert_called_once_with(
                M_CLIENT_ID,
                M_CLIENT_SECRET,
            )
            m_img_list_gen.assert_called_once_with()


def test_show_all_uploads():
    """test show_all_uploads."""
    m_text = mock.Mock()
    exe_retval = [['row0', 'row1', 'row2']]
    with mock.patch('melissa.actions.imgur_handler.sqlite3') as m_sqlite3, \
            mock.patch('sys.stdout', new_callable=StringIO) as m_stdout, \
            mock.patch('melissa.actions.imgur_handler.tts') as m_tts:
        m_sqlite3.connect.return_value.execute.return_value = exe_retval
        # run
        from melissa.actions import imgur_handler
        imgur_handler.show_all_uploads(m_text)
        # test
        assert 'row0: (row1) on row2' in m_stdout.getvalue()
        m_tts.assert_called_once_with(
            'Requested data has been printed on your terminal')
        m_sqlite3.assert_has_calls([
            mock.call.connect(M_MEMORY_DB),
            mock.call.connect().execute('SELECT * FROM image_uploads'),
            mock.call.connect().close()
        ])


def test_img_uploader_with_default_imgur_acc():
    """test func."""
    speech_text = mock.Mock()
    msg = 'upload requires a client id and secret'
    with mock.patch('sys.stdout', new_callable=StringIO) \
            as m_stdout, \
            mock.patch('melissa.actions.imgur_handler.tts') \
            as m_tts:
        from melissa.actions import imgur_handler
        imgur_handler.profile.data = {
            'imgur': {
                'client_id': "xxxx",
                'client_secret': "xxxx",
            },
            'memory_db': 'm_memory_db',
        }
        imgur_handler.image_uploader(speech_text)
        assert msg in m_stdout.getvalue()
        m_tts.assert_called_once_with(msg)
