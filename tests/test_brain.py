"""test for brain module."""
import unittest
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


NOT_WORKING_ON_FULL_TEST = "Not working on full test."


@pytest.mark.xfail(reason=NOT_WORKING_ON_FULL_TEST)
def test_simple_import():
    """test simple error import.

    the first error raised because IO is disable when testing.
    IO error is on profile_populator module.
    """
    with pytest.raises(IOError):
        from melissa import brain  # NOQA


@pytest.mark.xfail(reason=NOT_WORKING_ON_FULL_TEST)
def test_import_and_mock_populator():
    """test mock profile_populator module when import this module.

    this still raise error because profile.json is missing.
    IO error is raised on profile module
    """
    with pytest.raises(IOError):
        with mock.patch('melissa.profile_populator.profile_populator'):
            from melissa import brain  # NOQA


@mock.patch(
    'melissa.profile_loader.load_profile',
    return_value={
            'actions_db_file': ':memory:',
            'modules': 'melissa.actions',
        }
)
class WithProfileTest(unittest.TestCase):
    """test case using temp profile."""

    def test_simple_mock_input(self, m_load_profile):
        """test run til finished with multiple mock."""
        mock_text = mock.Mock()
        with mock.patch(
                'melissa.profile_populator.profile_populator') as mock_pp:
            # preparation for creating temp file
            with mock.patch('melissa.actions_db.assemble_actions_db') \
                    as mock_acdb:
                with mock.patch('melissa.brain.actions_db') as mock_adb:
                    from melissa.brain import query
                    with pytest.raises(TypeError):
                        query(mock_text)
                    assert not mock_pp.called
                    assert not mock_acdb.called
                    assert not mock_adb.called

    def test_simple_text_input(self, m_load_profile):
        """test run til finished with multiple mock."""
        mock_text = 'hello world'
        with mock.patch(
                'melissa.profile_populator.profile_populator') as mock_pp:
            with mock.patch(
                    'melissa.actions_db.assemble_actions_db') \
                    as mock_acdb:
                with mock.patch('melissa.brain.actions_db') as mock_adb:
                    from melissa.brain import query
                    res = query(mock_text)
                    assert res is None
                    assert not mock_pp.called
                    assert not mock_acdb.called
                    assert not mock_adb.called

                    assert len(mock_adb.mock_calls) == 12
                    # cur.execute
                    cur_exec_calls = [
                        mock.call('DELETE FROM expression'),
                        mock.call(
                            'SELECT e.word, e.word_order,   '
                            'g.word_group, g.word_count, g.function '
                            'FROM expression e '
                            'JOIN words w ON w.word = e.word '
                            'JOIN word_groups g '
                            'ON g.word_group = w.word_group '
                            'WHERE g.word_count > 1 '
                            'ORDER BY e.word_order, g.word_group'),
                        mock.call(
                            'SELECT g.function, count(*) '
                            'as words_matched,     f.priority '
                            'FROM expression e '
                            'JOIN words w ON w.word = e.word '
                            'JOIN word_groups g '
                            'ON g.word_group = w.word_group '
                            'JOIN functions f '
                            'ON g.function = f.function '
                            'WHERE g.word_count = 1 '
                            'GROUP BY g.function ORDER BY word_count '
                            'DESC, f.priority, g.function')
                    ]
                    assert len(mock_adb.cur.execute.mock_calls) == 3
                    for ce_call in cur_exec_calls:
                        ce_call in mock_adb.cur.execute.mock_calls
                    # cur.executemany
                    assert mock_adb.cur.executemany.call_count == 1
                    mock_adb.cur.executemany.assert_called_once_with(
                        'INSERT OR IGNORE INTO expression values (?,?)',
                        [('hello', 0), ('world', 1)]),
                    # con.commit
                    mock_adb.con.commit.assert_called_once_with()
                    # cur.fetchall
                    assert len(mock_adb.cur.fetchall.mock_calls) == 5
                    mock_adb.cur.fetchall.assert_called_with()
