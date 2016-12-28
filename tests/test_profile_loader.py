"""test for profile_loader module."""
from StringIO import StringIO
import itertools
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


@pytest.mark.parametrize(
    'skip_message, isfile_retval',
    itertools.product([True, False], repeat=2)
)
def test_load_profile(skip_message, isfile_retval):
    """test load_profile func."""
    m_open = mock.mock_open()
    m_open_path = 'melissa.profile_loader.open'
    with mock.patch('melissa.profile_loader.profile_populator') as m_pp, \
            mock.patch('melissa.profile_loader.os') as m_os, \
            mock.patch('sys.stdout', new_callable=StringIO) as m_stdout, \
            mock.patch(m_open_path, m_open, create=True), \
            mock.patch('melissa.profile_loader.json') as m_json:
        m_os.path.isfile.return_value = isfile_retval
        from melissa.profile_loader import load_profile
        from melissa.utilities import json_decode as jd
        res = load_profile(skip_message=skip_message)
        # testing
        assert res == m_json.load.return_value
        m_os.path.isfile.assert_called_once_with('profile.json')
        if isfile_retval:
            m_pp.assert_not_called()
        else:
            m_pp.assert_called_once_with()
        if skip_message:
            assert m_stdout.getvalue() == ''
        else:
            assert "Loading profile data" in m_stdout.getvalue()
        m_open.assert_has_calls(
            [mock.call('profile.json'), mock.call().close()])
        m_json.load.assert_called_once_with(
            m_open.return_value, object_hook=jd.decode_dict)
