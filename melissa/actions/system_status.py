import datetime
import psutil
import platform

# Melissa
from melissa.tts import tts

WORDS = {
    'system_status': {
        'groups': [
            ['how', 'systems'],
            ['how', 'system'],
            'status'
        ]
    },
    'system_uptime': {
        'groups': ['uptime']
    }
}


def system_status(text):
    os, name, version, _, _, _ = platform.uname()
    version = version.split('-')[0]
    cores = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory()[2]
    disk_usage = psutil.disk_usage('/')
    disk_percent = disk_usage.percent
    response = "I am currently running on %s version %s. " % (os, version)
    response += "This system is named %s and has %s CPU cores. " \
        % (name, cores)
    response += "Current CPU utilization is %s percent. " % cpu_percent
    response += "Current memory utilization is %s percent. " % memory_percent
    response += "Current disk utilization is %s percent. " % disk_percent
    tts(response)


def system_uptime(text):
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    running_since = boot_time.strftime("%A %d. %B %Y")
    response = 'System has been running since ' + running_since
    tts(response)
