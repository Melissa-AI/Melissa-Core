"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock


def test_system_status():
    """test func."""
    m_text = mock.Mock()
    m_os = mock.Mock()
    m_name = mock.Mock()
    m_version = mock.Mock()
    m_version_subinfo = mock.Mock()
    m_memory_percent = mock.Mock()
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.system_status.platform') \
                as m_platform, \
                mock.patch('melissa.actions.system_status.psutil') \
                as m_psutil, \
                mock.patch('melissa.actions.system_status.tts') \
                as m_tts:
            # pre run
            m_platform.uname.return_value = [
                m_os, m_name, m_version, None, None, None]
            m_version.split.return_value = [m_version_subinfo]
            m_psutil.virtual_memory.return_value = [
                None, None, m_memory_percent]
            # run
            from melissa.actions import system_status
            system_status.system_status(m_text)
            # test
            m_tts.assert_called_once_with(
                "I am currently running on {} version {}. "
                "This system is named {} and has {} CPU cores. "
                "Current CPU utilization is {} percent. "
                "Current memory utilization is {} percent. "
                "Current disk utilization is {} percent. ".format(
                    m_os, m_version_subinfo, m_name,
                    m_psutil.cpu_count.return_value,
                    m_psutil.cpu_percent.return_value,
                    m_memory_percent,
                    m_psutil.disk_usage.return_value.percent,
                )
            )
            m_platform.uname.assert_called_once_with()
            m_psutil.assert_has_calls([
                mock.call.cpu_count(),
                mock.call.cpu_percent(),
                mock.call.virtual_memory(),
                mock.call.disk_usage('/'),
            ])
            m_version.split.assert_called_once_with('-')


def test_system_uptime():
    """test func."""
    m_text = mock.Mock()
    strftime_retval = 'Sunday 06. November 2016'
    m_boot_time = mock.Mock()
    with mock.patch('melissa.actions.system_status.datetime') \
            as m_datetime, \
            mock.patch('melissa.actions.system_status.psutil') \
            as m_psutil, \
            mock.patch('melissa.actions.system_status.tts') \
            as m_tts:
        # pre run
        m_boot_time.strftime.return_value = strftime_retval
        m_datetime.datetime.fromtimestamp.return_value = m_boot_time
        # run
        from melissa.actions import system_status
        system_status.system_uptime(m_text)
        # test
        m_datetime.assert_has_calls([
            mock.call.datetime.fromtimestamp(
                m_psutil.boot_time.return_value),
            mock.call.datetime.fromtimestamp().strftime(
                '%A %d. %B %Y'),
        ])
        m_boot_time.strftime.assert_called_once_with("%A %d. %B %Y")
        m_psutil.boot_time.assert_called_once_with()
        m_tts.assert_called_once_with(
            'System has been running since {}'.format(
                strftime_retval
            )
        )
