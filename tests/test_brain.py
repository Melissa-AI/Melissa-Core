"""test for brain module."""
import json
import os
import unittest
from shutil import copyfile
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


def test_simple_import():
    """test simple error import.

    the first error raised because IO is disable when testing.
    IO error is on profile_populator module.
    """
    with pytest.raises(IOError):
        from melissa import brain  # NOQA


def test_import_and_mock_populator():
    """test mock profile_populator module when import this module.

    this still raise error because profile.json is missing.
    IO error is raised on profile module
    """
    with pytest.raises(IOError):
        with mock.patch('melissa.profile_populator.profile_populator'):
            from melissa import brain  # NOQA


class WithProfileTest(unittest.TestCase):
    """test case using temp profile."""

    def setUp(self):
        """setup func."""
        profile = {
            'actions_db_file': ':memory:',
            'modules': 'melissa.actions',
        }
        self.json_file = 'profile.json'
        self.bak_file = self.json_file + 'brain-test.bak'
        if os.path.isfile(self.json_file):
            self.json_file_exist = True
            copyfile(self.json_file, self.bak_file)
        else:
            self.json_file_exist = False
        with open(self.json_file, 'w') as f:
            json.dump(profile, f)

    def tearDown(self):
        """tear down func."""
        os.remove(self.json_file)
        # restore the backup
        if self.json_file_exist:
            copyfile(self.bak_file, self.json_file)

    def test_simple_mock_input(self):
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

    def test_simple_text_input(self):
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
