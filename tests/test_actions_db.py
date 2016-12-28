"""test for actions_db module."""
import os
import unittest
from StringIO import StringIO
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest
import sqlite3


def test_simple_import():
    """test simple import.

    the first error raised because IO is disable when testing.
    IO error is on profile_populator module.
    """
    with pytest.raises(IOError):
        from melissa import actions_db  # NOQA


def test_import_and_mock_populator():
    """test mock profile_populator module when import this module.

    this still raise error because profile.json is missing.
    IO error is raised on profile module
    """
    with pytest.raises(IOError):
        with mock.patch('melissa.profile_populator.profile_populator'):
            from melissa import actions_db  # NOQA


@mock.patch(
    'melissa.profile_loader.load_profile',
    return_value={
            'actions_db_file': ':memory:',
            'modules': 'melissa.actions',
        }
)
class WithProfileTest(unittest.TestCase):
    """test case using temp profile."""

    def setUp(self):
        """setup func."""
        # execscript argument
        self.exec_script_arg = (
            '\n            '
            'CREATE TABLE synonyms ('
            '\n              synonym varchar(50) PRIMARY KEY,'
            '\n              word varchar(50)'
            '\n            );'
            '\n\n            CREATE TABLE words ('
            '\n              word varchar(50),'
            '\n              word_group varchar(255),'
            '\n              word_order integer'
            '\n            );'
            '\n\n            CREATE INDEX word_index ON words (word);'
            '\n\n            CREATE TABLE word_groups ('
            '\n              word_group varchar(255),'
            '\n              function varchar(255),'
            '\n              word_count integer'
            '\n            );'
            '\n\n            CREATE INDEX word_group_index '
            'ON word_groups (word_group);'
            '\n\n            CREATE TABLE functions ('
            '\n              function varchar(255) PRIMARY KEY,'
            '\n              priority integer'
            '\n            );'
            '\n\n            CREATE TABLE expression ('
            '\n              word varchar(50) PRIMARY KEY,'
            '\n              word_order integer'
            '\n            );'
            '\n            '
        )

    def test_actions_db_import(self, m_load_profile):
        """test run."""
        from melissa import actions_db  # NOQA

    def test_create_actions_db_mocked_inputs(self, m_load_profile):
        """test run create_actions_db with mocked inputs."""
        from melissa.actions_db import create_actions_db
        mock_con = mock.Mock()
        mock_cur = mock.Mock()
        create_actions_db(mock_con, mock_cur)
        mock_con.commit.assert_called_once_with()
        mock_cur.executescript.assert_called_once_with(self.exec_script_arg)

    def test_create_actions_db_raise_sqlite3_error(self, m_load_profile):
        """test run create_actions_db and raise sqlite3 error."""
        from melissa.actions_db import create_actions_db
        mock_con = mock.Mock()
        mock_cur = mock.Mock()
        mock_err_msg = 'Error'
        mock_con.commit.side_effect = sqlite3.Error(mock_err_msg)
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with pytest.raises(SystemExit):
                create_actions_db(mock_con, mock_cur)
            assert 'Error {}:\n'.format(mock_err_msg) in mock_stdout.getvalue()

    def test_assemble_actions_db(self, m_load_profile):
        """test run func."""
        from melissa.actions_db import assemble_actions_db
        assemble_actions_db()

    def test_assemble_actions_db_mock_sqlite(self, m_load_profile):
        """test run func and mock libs."""
        from melissa.actions_db import assemble_actions_db
        with mock.patch('melissa.actions_db.sqlite3') as mock_sq:
            assemble_actions_db()

        # preparation
        sql_cmd_basename = 'test_actions_db_sql_command.txt'
        script_folder = os.path.dirname(os.path.realpath(__file__))
        sql_cmd_path = os.path.join(
            script_folder, 'test_data', sql_cmd_basename)
        with open(sql_cmd_path) as f:
            sql_cmds = f.read().splitlines()

        # testing
        assert len(mock_sq.mock_calls) == 240
        # connect
        assert mock_sq.connect.call_count == 1
        mock_sq.connect.assert_called_once_with(
            ':memory:', check_same_thread=False)
        # connect().cursor
        mock_sq.connect.return_value.cursor.assert_called_once_with()
        # connect().cursor().executescript
        (mock_sq.connect.return_value.cursor.return_value
                .executescript.assert_called_once_with(self.exec_script_arg))
        # connect().commit
        mock_sq.connect.return_value.commit.assert_called_with()
        # test sql commands.
        call_result = (
            mock_sq.connect.return_value.cursor.return_value
            .execute.mock_calls)
        call_result_args = [x[1][0] for x in call_result]
        non_exist_expected_call = [
            x for x in sql_cmds if x not in call_result_args]
        not_expected_call = [
            x for x in call_result_args if x not in sql_cmds]
        # connect().cursor().execute
        err_msg = (
            'Expected calls which are not exist on actual call:\n{}\n'
            'Actual calls which are not expected:\n{}'
        )
        err_msg = err_msg.format(
            '\n'.join(non_exist_expected_call),
            '\n'.join(not_expected_call),
        )
        assert len(call_result_args) == len(sql_cmds), err_msg
        for cmd in sql_cmds:
            assert mock.call(cmd) in call_result, err_msg

    def test_insert_words_mock_input_and_name_input(self, m_load_profile):
        """test run insert_words with mock input."""
        m_name = mock.Mock()
        input_string = 'name'
        for mock_name in (m_name, input_string):
            mock_con = mock.Mock()
            mock_cur = mock.Mock()
            mock_words = mock.Mock()
            mock_priority = mock.Mock()
            from melissa.actions_db import insert_words
            with mock.patch('sys.stdout', new_callable=StringIO) \
                    as mock_stdout:
                insert_words(
                    mock_con, mock_cur, mock_name, mock_words, mock_priority)
                assert (
                    "Invalid WORDS type '<class 'mock.mock.Mock'>' "
                    "for module {}".format(mock_name)
                ) in mock_stdout.getvalue()

    def test_insert_words_mock_input_and_words_list(self, m_load_profile):
        """test run insert_words with mock input and words as list."""
        mock_name = 'how'
        mock_con = mock.Mock()
        mock_cur = mock.Mock()
        mock_words = ['how',  'are', 'you']
        mock_priority = mock.Mock()
        from melissa.actions_db import insert_words
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            insert_words(
                mock_con, mock_cur, mock_name, mock_words, mock_priority)
            cur_exec_calls = [
                mock.call(
                    "INSERT INTO functions (function, priority) "
                    "values ('{} handle',{})".format(
                        mock_name, mock_priority)),
            ]
            for word in mock_words:
                cur_exec_calls.append(mock.call(
                    "INSERT INTO words (word, word_group, word_order) "
                    "values ('{w}','{w}',0)".format(w=word)
                ))
                cur_exec_calls.append(mock.call(
                    "INSERT INTO word_groups "
                    "(word_group, function, word_count) "
                    "values ('{}','{} handle',1)".format(
                        word, mock_name, mock_priority)
                ))
            assert len(mock_cur.execute.mock_calls) == 7
            for call in cur_exec_calls:
                assert call in mock_cur.execute.mock_calls
            mock_con.commit.assert_called_once_with()
            assert '' in mock_stdout.getvalue()

    def test_insert_words_mock_input_and_words_dict(self, m_load_profile):
        """test run insert_words with mock input and words as dict."""
        mock_name = 'define'
        mock_con = mock.Mock()
        mock_cur = mock.Mock()
        mock_words = {'define_subject': {'groups': ['define']}}
        mock_priority = mock.Mock()
        from melissa.actions_db import insert_words
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            insert_words(
                mock_con, mock_cur, mock_name, mock_words, mock_priority)

            cur_exec_calls = [
                mock.call(
                    "INSERT INTO functions (function, priority) "
                    "values ('define define_subject',0)"),
                mock. call(
                    "INSERT INTO word_groups "
                    "(word_group, function, word_count) "
                    "values ('define','define define_subject',1)"),
                mock.call(
                    "INSERT INTO words (word, word_group, word_order) "
                    "values ('define','define',0)")
            ]
            mock_con.commit.assert_called_once_with()
            assert len(mock_cur.execute.mock_calls) == 3
            for call in cur_exec_calls:
                assert call in mock_cur.execute.mock_calls
            assert '' in mock_stdout.getvalue()
