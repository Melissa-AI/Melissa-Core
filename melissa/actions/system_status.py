import psutil
import platform

# Melissa
from melissa.tts import tts

WORDS = {'system_status': {'groups': [['how', 'systems'], ['how', 'system'], 'status']}}

def system_status(text):
    os, name, version, _, _, _ = platform.uname()
    version = version.split('-')[0]
    cores = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory()[2]
    response = "I am currently running on %s version %s. " %(os, version)
    response += "This system is named %s and has %s CPU cores. " %(name, cores)
    response += "Current CPU utilization is %s percent. " %cpu_percent
    response += "Current memory utilization is %s percent." %memory_percent
    tts(response)