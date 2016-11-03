"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock


M_MEMORY_DB = 'm_memory_db'


def test_show_all_notes():
    """test func."""
    row0 = mock.Mock()
    m_text = mock.Mock()
    with mock.patch('melissa.profile_loader.load_profile'):
        from melissa import profile
        profile.data = {'memory_db': M_MEMORY_DB}
        with mock.patch('melissa.actions.notes.sqlite3') as m_sqlite3, \
                mock.patch('melissa.actions.notes.tts') as m_tts:
            m_sqlite3.connect.return_value.execute.return_value = [[row0]]
            # run
            from melissa.actions import notes
            notes.show_all_notes(m_text)
            # test
            m_tts.assert_has_calls([
                mock.call('Your notes are as follows:'),
                mock.call(row0)
            ])
            m_sqlite3.assert_has_calls([
                mock.call.connect(M_MEMORY_DB),
                mock.call.connect().execute('SELECT notes FROM notes'),
                mock.call.connect().close()
            ])


def test_note_something():
    """test func."""
    m_text = "note something"
    with mock.patch('melissa.actions.notes.sqlite3') as m_sqlite3, \
            mock.patch('melissa.actions.notes.datetime') as m_datetime, \
            mock.patch('melissa.actions.notes.tts') as m_tts:
        # run
        from melissa.actions import notes
        notes.note_something(m_text)
        # test
        m_sqlite3.assert_has_calls([
            mock.call.connect(M_MEMORY_DB),
            mock.call.connect().execute(
                'INSERT INTO notes (notes, notes_date) VALUES (?, ?)',
                ('something', m_datetime.strftime.return_value)
            ),
            mock.call.connect().commit(),
            mock.call.connect().close()
        ])
        m_tts.assert_called_once_with('Your note has been saved.')
        m_datetime.assert_has_calls([
            mock.call.now(),
            mock.call.strftime(m_datetime.now.return_value, '%d-%m-%Y')
        ])
