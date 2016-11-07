"""test ip_address module."""
import itertools
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


@pytest.mark.parametrize(
    'ifs_retval, setdefault_retval',
    itertools.product(
        ['lo', 'eth0'],
        [
            [{'addr': '127.0.0.1'}, {'addr': None}],
            [{'addr': '127.0.0.1'}]
        ]
    )
)
def test_ip_address(ifs_retval, setdefault_retval):
    """test ip_address."""
    m_text = mock.Mock()
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.ip_address.tts') as m_tts, \
                mock.patch('melissa.actions.ip_address.AF_INET') \
                as m_af_inet, \
                mock.patch('melissa.actions.ip_address.ifaddresses') \
                as m_ifa, \
                mock.patch('melissa.actions.ip_address.interfaces') as m_ifs:
            m_ifs.return_value = [ifs_retval]
            m_ifa.return_value.setdefault.return_value = setdefault_retval
            from melissa.actions import ip_address
            ip_address.ip_address(m_text)
            if ifs_retval == ['lo']:
                m_tts.assert_has_calls([
                    mock.call('Here are my available I.P. addresses.'),
                    mock.call('Those are all my I.P. addresses.')
                ])
            elif ifs_retval == ['eth0']:
                m_tts.assert_has_calls([
                    mock.call('Here are my available I.P. addresses.'),
                    mock.call(
                        'interface: eth0, I.P. Address : '
                        '127 dot 0 dot 0 dot 1'),
                    mock.call('Those are all my I.P. addresses.')
                ])
            m_ifa.assert_has_calls([
                mock.call(ifs_retval),
                mock.call().setdefault(m_af_inet, [{'addr': None}])
            ])
