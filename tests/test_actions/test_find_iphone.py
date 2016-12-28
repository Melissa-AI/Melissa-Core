"""test find_iphone modulue."""
from unittest import TestCase
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

from pyicloud.exceptions import PyiCloudFailedLoginException


M_USERNAME = 'm_username'
M_PASSWORD = 'm_password'


def test_find_iphone():
    """test find_iphone func.

    when given with all mocked dependencies,
    find_iphone will only give warning
    about there is no iphone in the given account.
    """
    m_text = mock.Mock()
    with mock.patch('melissa.profile_loader.load_profile'):
        from melissa import profile
        profile.data = {
            'icloud': {'username': M_USERNAME, 'password': M_PASSWORD}}
        with mock.patch('melissa.actions.find_iphone.PyiCloudService') \
                as m_pc_service, \
                mock.patch('melissa.actions.find_iphone.tts') as m_tts:
            from melissa.actions import find_iphone
            find_iphone.profile.data = {
                'icloud': {'username': M_USERNAME, 'password': M_PASSWORD}}
            # run the func
            find_iphone.find_iphone(m_text)
            # testing.
            m_pc_service.assert_called_once_with(M_USERNAME, M_PASSWORD)
            m_tts.assert_called_once_with('No iPhones found in your account')


class WithProfileTest(TestCase):
    """test case with profile."""

    def test_find_iphone_with_profile(self):
        """test find_iphone func.

        when given with all mocked dependencies,
        find_iphone will only give warning
        about there is no iphone in the given account.
        """
        m_text = mock.Mock()
        from melissa.actions import find_iphone
        with mock.patch('melissa.actions.find_iphone.PyiCloudService') \
                as m_pc_service, \
                mock.patch('melissa.actions.find_iphone.tts') as m_tts:
            # run the func
            find_iphone.find_iphone(m_text)
            # testing.
            m_pc_service.assert_called_once_with(M_USERNAME, M_PASSWORD)
            m_tts.assert_called_once_with('No iPhones found in your account')

    def test_find_iphone_with_a_phone(self):
        """test find_iphone func."""
        m_text = mock.Mock()
        m_device = mock.Mock()
        m_device.status.return_value = {'deviceDisplayName': 'iPhone'}
        from melissa.actions.find_iphone import find_iphone
        with mock.patch('melissa.actions.find_iphone.PyiCloudService') \
                as m_pc_service, \
                mock.patch('melissa.actions.find_iphone.tts') as m_tts:
            m_pc_service.return_value.devices = [m_device]
            # run the func
            find_iphone(m_text)
            # testing.
            m_pc_service.assert_called_once_with(M_USERNAME, M_PASSWORD)
            m_tts.assert_called_once_with(
                'Sending ring command to the phone now')
            m_device.status.assert_called_once_with()
            m_device.play_sound.assert_called_once_with()

    def test_find_iphone_with_2_phones(self):
        """test find_iphone func."""
        m_text = mock.Mock()
        m_device1 = mock.Mock()
        m_device1.status.return_value = {'deviceDisplayName': 'iPhone'}
        m_device2 = mock.Mock()
        m_device2.status.return_value = {'deviceDisplayName': 'iPhone'}
        from melissa.actions.find_iphone import find_iphone
        with mock.patch('melissa.actions.find_iphone.PyiCloudService') \
                as m_pc_service, \
                mock.patch('melissa.actions.find_iphone.tts') as m_tts:
            m_pc_service.return_value.devices = [m_device1, m_device2]
            # run the func
            find_iphone(m_text)
            # testing.
            m_pc_service.assert_called_once_with(M_USERNAME, M_PASSWORD)
            m_tts.assert_called_with(
                'Sending ring command to the phone now')
            m_device1.status.assert_called_once_with()
            m_device1.play_sound.assert_called_once_with()
            m_device2.status.assert_called_once_with()
            m_device2.play_sound.assert_called_once_with()

    def test_find_iphone_raise_failed_login(self):
        """test find iphone but raise failed login error."""
        m_text = mock.Mock()
        from melissa.actions.find_iphone import find_iphone
        with mock.patch('melissa.actions.find_iphone.PyiCloudService') \
                as m_pc_service, \
                mock.patch('melissa.actions.find_iphone.tts') as m_tts:
            m_pc_service.side_effect = PyiCloudFailedLoginException()
            # run
            find_iphone(m_text)
            # testing
            m_pc_service.assert_called_once_with(M_USERNAME, M_PASSWORD)
            m_tts.assert_called_once_with('Invalid Username & Password')

    def test_iphone_battery_raise_failed_login(self):
        """test find iphone but raise failed login error."""
        m_text = mock.Mock()
        from melissa.actions.find_iphone import iphone_battery
        with mock.patch('melissa.actions.find_iphone.PyiCloudService') \
                as m_pc_service, \
                mock.patch('melissa.actions.find_iphone.tts') as m_tts:
            m_pc_service.side_effect = PyiCloudFailedLoginException()
            # run
            iphone_battery(m_text)
            # testing
            m_pc_service.assert_called_once_with(M_USERNAME, M_PASSWORD)
            m_tts.assert_called_once_with('Invalid Username & Password')

    def test_iphone_battery_with_a_phone(self):
        """test find_iphone func."""
        m_text = mock.Mock()
        m_device = mock.Mock()
        m_battery_level = 0.5
        expected_percentage = int(float(m_battery_level) * 100)
        m_tts_expected_arg = '{}percent battery left in m_name'.format(
            expected_percentage)
        m_device_name = 'm_name'
        m_device.status.return_value = {
            'deviceDisplayName': 'iPhone',
            'batteryLevel': m_battery_level,
            'name': m_device_name,
        }
        from melissa.actions.find_iphone import iphone_battery
        with mock.patch('melissa.actions.find_iphone.PyiCloudService') \
                as m_pc_service, \
                mock.patch('melissa.actions.find_iphone.tts') as m_tts:
            m_pc_service.return_value.devices = [m_device]
            # run the func
            iphone_battery(m_text)
            # testing.
            m_pc_service.assert_called_once_with(M_USERNAME, M_PASSWORD)
            m_tts.assert_called_once_with(m_tts_expected_arg)
            assert m_device.status.call_count == 2
            m_device.status.assert_called_with()
