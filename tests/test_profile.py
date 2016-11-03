"""test profile module."""
import os
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


NOT_WORKING_ON_FULL_TEST = "Not working on full test."


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


@pytest.mark.xfail(reason=NOT_WORKING_ON_FULL_TEST)
def test_import():
    """test normal import.

    the error happened because
    module run the profile populator in testing mode.
    in profile_populator it need IO where it disable on testing.
    """
    with pytest.raises(IOError, message=profile_file_info()):
        from melissa import profile  # NOQA


@pytest.mark.xfail(reason=NOT_WORKING_ON_FULL_TEST)
def test_import_with_mock_profile_populator():
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
