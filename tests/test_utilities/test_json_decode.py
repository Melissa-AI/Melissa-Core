"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


@pytest.mark.parametrize(
    'data',
    [
        [u'item'],
        [[u'item']],
        [{'key': 'value'}]
    ]
)
def test_decode_list(data):
    """test func."""
    with mock.patch('melissa.utilities.json_decode.decode_dict') \
            as m_decode_dict:
        from melissa.utilities import json_decode
        res = json_decode.decode_list(data)
        assert isinstance(res, list)
        if data == [u'item']:
            assert res == ['item']
            assert isinstance(res[0], str)
        elif data == [[u'item']]:
            assert res == [['item']]
            assert isinstance(res[0][0], str)
        elif data == [{'key': 'value'}]:
            m_decode_dict.assert_called_once_with({'key': "value"})
            assert res == [m_decode_dict.return_value]


@pytest.mark.parametrize(
    'data',
    [
        {u'key': u'value'},
        {u'key': {u'subkey': 'subvalue'}},
        {u'key': [u'item']},
    ]
)
def test_decode_dict(data):
    """test func."""
    with mock.patch('melissa.utilities.json_decode.decode_list') \
            as m_decode_list:
        from melissa.utilities import json_decode
        res = json_decode.decode_dict(data)
        # test
        assert isinstance(res, dict)
        assert isinstance(res.items()[0], tuple)
        assert isinstance(res.items()[0][0], str)
        assert res.items()[0][0] == 'key'
        if data == {u'key': u'value'}:
            assert isinstance(res.items()[0][1], str)
            assert res.items()[0][1] == 'value'
        elif data == {u'key': {u'subkey': 'subvalue'}}:
            assert isinstance(res.items()[0][1], dict)
            assert res.items()[0][1] == {'subkey': 'subvalue'}
        elif data == {u'key': [u'item']}:
            m_decode_list.assert_called_once_with([u'item'])
            assert isinstance(res.items()[0][1], mock.Mock)
            assert res.items()[0][1] == m_decode_list.return_value
