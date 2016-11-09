"""test for brain module."""
import itertools
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


M_RETVAL = mock.Mock()
NOT_WORKING_ON_FULL_TEST = "Not working on full test."


@pytest.mark.parametrize(
    'm_text, fetchall_retval',
    itertools.product(
        [mock.Mock(), '', 'define programming'],
        [[], [M_RETVAL]],
    )
)
def test_run(m_text, fetchall_retval):
    """test run til finished with multiple mock."""
    # mocked value used on profile
    m_tts = 'xxxx'
    m_va_gender = 'female'
    # mocked value used on module
    m_gen_con = mock.Mock()
    with mock.patch('melissa.profile_loader.load_profile'):
        from melissa import profile
        profile.data = {
            'actions_db_file': ':memory:',
            'modules': 'melissa.actions',
            'tts': m_tts,
            'va_gender': m_va_gender,
        }
        with mock.patch('melissa.brain.actions_db') \
                as m_adb, \
                mock.patch('melissa.brain.getattr') \
                as m_getattr:
            # pre run
            from melissa import brain
            m_adb.modules = {
                'general_conversations': m_gen_con}
            m_adb.cur.fetchall.return_value = fetchall_retval
            if isinstance(m_text, mock.Mock):
                with pytest.raises(TypeError):
                    brain.query(m_text)
                assert not m_adb.mock_calls
            elif fetchall_retval == [M_RETVAL]:
                with pytest.raises(TypeError):
                    brain.query(m_text)
            elif m_text == '' or m_text == 'define programming':
                # run
                brain.query(m_text)
                # test
                getattr_calls = [
                    mock.call(m_gen_con, 'undefined'),
                    mock.call()('')
                ]
                m_getattr.assert_has_calls(getattr_calls)
                if m_text == '':
                    executemany_arg = []
                elif m_text == 'define programming':
                    executemany_arg = [('define', 0), ('programming', 1)]
                adb_calls = [
                    mock.call.cur.execute('DELETE FROM expression'),
                    mock.call.cur.executemany(
                        'INSERT OR IGNORE INTO expression values (?,?)',
                        executemany_arg),
                    mock.call.con.commit(),
                    mock.call.cur.execute(
                        'SELECT e.word, e.word_order,   '
                        'g.word_group, g.word_count, g.function '
                        'FROM expression e '
                        'JOIN words w ON w.word = e.word '
                        'JOIN word_groups g ON g.word_group = w.word_group '
                        'WHERE g.word_count > 1 '
                        'ORDER BY e.word_order, g.word_group'),
                    mock.call.cur.fetchall(),
                    mock.call.cur.execute(
                        'SELECT g.function, count(*) as words_matched,     '
                        'f.priority FROM expression e '
                        'JOIN words w ON w.word = e.word '
                        'JOIN word_groups g ON g.word_group = w.word_group '
                        'JOIN functions f ON g.function = f.function '
                        'WHERE g.word_count = 1 GROUP BY g.function '
                        'ORDER BY word_count DESC, f.priority, g.function'),
                    mock.call.cur.fetchall(),
                ]
                m_adb.assert_has_calls(adb_calls)


@pytest.mark.xfail(reason=NOT_WORKING_ON_FULL_TEST)
@pytest.mark.parametrize(
    'm_text',
    [
        'define define',
        'feeling',
        'feeling angry'
    ]
)
def test_run_least_mock(m_text):
    """test run til finished with least mock."""
    # mocked value used on profile
    m_tts = 'xxxx'
    m_va_gender = 'female'
    # mocked value used on module
    with mock.patch('melissa.profile_loader.load_profile'):
        from melissa import profile
        profile.data = {
            'actions_db_file': ':memory:',
            'modules': 'melissa.actions',
            'tts': m_tts,
            'va_gender': m_va_gender,
        }
        with mock.patch('melissa.brain.getattr') \
                as m_getattr:
            # pre run
            from melissa import brain
            # run
            brain.query(m_text)
            # test
            if m_text == 'define define':
                val_pack = ('define_subject', 'define define')
            elif m_text == 'feeling':
                val_pack = ('undefined', '')
            else:
                val_pack = ('feeling_angry', 'feeling angry')
            err_msg = (
                "Unexpected mock's calls. "
                "actual mock's call:\n{}".format(
                    '\n'.join(map(repr, m_getattr.mock_calls))))
            assert len(m_getattr.mock_calls) == 2, err_msg
            assert m_getattr.mock_calls[1][1][0] == val_pack[1], err_msg
            assert m_getattr.mock_calls[0][1][1] == val_pack[0], err_msg


@pytest.mark.parametrize(
    'm_text, fetchall_side_effect',
    [
        ('define define', [
            [],
            [('define_subject define_subject', 1, 0)],
        ]),
        ('feeling', [
            [
                ('feeling', 0, 'feeling angry', 2,
                 'lighting feeling_angry'),
                ('feeling', 0, 'feeling creative', 2,
                 'lighting feeling_creative'),
                ('feeling', 0, 'feeling lazy', 2,
                 'lighting feeling_lazy')
            ],
            []
        ]),
        ('feeling angry', [
            [
                ('feeling', 0, 'feeling angry', 2,
                 'lighting feeling_angry'),
                ('feeling', 0, 'feeling creative', 2,
                 'lighting feeling_creative'),
                ('feeling', 0, 'feeling lazy', 2,
                 'lighting feeling_lazy'),
                ('angry', 1, 'feeling angry', 2,
                 'lighting feeling_angry')
            ],
            []
        ]),
    ]
)
def test_run_least_mock_and_working_test(m_text, fetchall_side_effect):
    """test run til finished with least mock until test work.

    this similar to test_run_least_mock function but
    add additional mock to make test working on full test.
    """
    # mocked value used on profile
    m_tts = 'xxxx'
    m_va_gender = 'female'
    # mocked value used on module
    with mock.patch('melissa.profile_loader.load_profile'):
        from melissa import profile
        profile.data = {
            'actions_db_file': ':memory:',
            'modules': 'melissa.actions',
            'tts': m_tts,
            'va_gender': m_va_gender,
        }
        with mock.patch('melissa.brain.getattr') \
                as m_getattr, \
                mock.patch('melissa.brain.actions_db') \
                as m_adb:
            # pre run
            m_adb.cur.fetchall.side_effect = fetchall_side_effect
            from melissa import brain
            # run
            brain.query(m_text)
            # test
            if m_text == 'define define':
                val_pack = ('define_subject', 'define define')
            elif m_text == 'feeling':
                val_pack = ('undefined', '')
            else:
                val_pack = ('feeling_angry', 'feeling angry')
            err_msg = (
                "Unexpected mock\'s calls. "
                "actual mock\s call:\n{}".format(
                    '\n'.join(map(repr, m_getattr.mock_calls))))
            assert len(m_getattr.mock_calls) == 2, err_msg
            assert m_getattr.mock_calls[1][1][0] == val_pack[1], err_msg
            assert m_getattr.mock_calls[0][1][1] == val_pack[0], err_msg
