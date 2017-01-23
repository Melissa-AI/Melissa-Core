"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock


def test_push():
    info = mock.Mock()
    m_profile = {'push_bullet': '', 'va_name': 'Melissa'}
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.notification.Pushbullet') as m_push:
            from melissa.actions import notification
            notification.profile.data = m_profile
            notification.push(info)
            m_push.assert_has_calls([mock.call(
                notification.profile.data['push_bullet']),
                mock.call(
                    notification.profile.data['push_bullet']).push_note(
                        notification.profile.data['va_name'], info)])
