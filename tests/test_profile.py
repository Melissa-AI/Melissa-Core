"""test profile module."""
from shutil import copyfile
import json
import os
import random
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


def test_import():
    """test normal import.

    the error happened because
    module run the profile populator in testing mode.
    in profile_populator it need IO where it disable on testing.
    """
    with pytest.raises(IOError):
        from melissa import profile  # NOQA


def test_import_with_mock_profile_populator():
    """test importing but mock some obj.

    the error happened because
    module run load_profile after run mocked profile_populator func.
    because it is not exist IOError is raised.
    """
    with mock.patch(
            'melissa.profile_populator.profile_populator') \
            as mock_profile_populator:
        with pytest.raises(IOError):
            from melissa import profile  # NOQA
        mock_profile_populator.assert_called_once_with()


def test_import_with_temp_file():
    """test importing but create temp file."""
    with mock.patch('melissa.profile_populator.profile_populator') \
            as mock_profile_populator:
        random_int = random.randint(0, 9)
        json_file = 'profile.json'
        bak_file = json_file + '.bak'
        json_file_exist = False
        try:
            # backup the file
            if os.path.isfile(json_file):
                json_file_exist = True
                copyfile(json_file, bak_file)
            with open(json_file, 'w') as f:
                json.dump(random_int, f)

            from melissa import profile
            assert profile.data == random_int
        finally:
            os.remove(json_file)
            # restore the backup
            if json_file_exist:
                copyfile(json_file, bak_file)
    assert not mock_profile_populator.called
