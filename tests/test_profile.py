"""test profile module."""
from shutil import copyfile
import json
import os
import random
import unittest
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


xfail_brain_test_mixup = pytest.mark.xfail(
    reason='Mix up with brain module test.')


def profile_file_info():
    """get profile info."""
    json_file = 'profile.json'
    if os.path.isfile(json_file):
        with open(json_file) as f:
            data = f.read()
        result = 'json file exist and have following data\n{}'.format(data)
    else:
        result = 'json file is not exist.'
    return result


class WithoutProfileTest(unittest.TestCase):
    """test with non existent profile.json file."""

    def setUp(self):
        """set up func."""
        self.json_file = 'profile.json'
        self.bak_file = self.json_file + 'profile-test.bak'
        if os.path.isfile(self.json_file):
            self.json_file_exist = True
            copyfile(self.json_file, self.bak_file)
            os.remove(self.json_file)
        else:
            self.json_file_exist = False

    def tearDown(self):
        """tear down func."""
        # restore the backup
        if self.json_file_exist:
            copyfile(self.bak_file, self.json_file)

    @xfail_brain_test_mixup
    def test_import(self):
        """test normal import.

        the error happened because
        module run the profile populator in testing mode.
        in profile_populator it need IO where it disable on testing.
        """
        with pytest.raises(IOError, message=profile_file_info()):
            from melissa import profile  # NOQA

    @xfail_brain_test_mixup
    def test_import_with_mock_profile_populator(self):
        """test importing but mock some obj.

        the error happened because
        module run load_profile after run mocked profile_populator func.
        because it is not exist IOError is raised.
        """
        with mock.patch(
                'melissa.profile_populator.profile_populator') \
                as mock_profile_populator:
            with pytest.raises(IOError, message=profile_file_info()):
                from melissa import profile  # NOQA
            mock_profile_populator.assert_called_once_with()

    @xfail_brain_test_mixup
    def test_import_with_temp_file(self):
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
                assert profile.data == random_int, profile_file_info()
            finally:
                os.remove(json_file)
                # restore the backup
                if json_file_exist:
                    copyfile(bak_file, json_file)
        assert not mock_profile_populator.called
