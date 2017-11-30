#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import dirname, join

from setuptools import setup, find_packages

import melissa

description = 'A lovely virtual assistant for OS X, Windows and Linux systems.'
try:
    long_description = open("README.rst").read()
except IOError:
    long_description = description

setup(
    name="melissa",
    version="0.0.1",
    description=description,
    long_description=long_description,
    author='Tanay Pant',
    author_email='tanay1337@gmail.com',
    url='https://github.com/Melissa-AI/Melissa-Core/',
    license="MIT",
    packages=find_packages(),
    package_data={'': ['LICENSE.md', 'README.rst']
          },
    package_dir={'melissa': 'melissa'},
    include_package_data=True,
    python_requires='==2.7',
    install_requires=[
          'markdown', 
          'wheel==0.24.0',
          'six==1.10.0', 
          'oauthlib==1.0.3',
          'requests-oauthlib==0.5.0', 
          'eventlet==0.20.0', 
          'Flask==0.12',
          'Flask-SocketIO==2.8.6',    
          'python-socketio==1.6.1',
          'beautifulsoup4==4.4.1',  
          'requests==2.8.1', 
          'wikipedia==1.4.0',
          'pyicloud==0.9.1', 
          'HoroscopeGenerator==0.1.8',
          'imgurpython==1.1.6', 
          'netifaces==0.10.5', 
          'psutil==4.3.0',
          'tweepy==3.5.0', 
          'telepot==4.1', 
          'pygame>=1.9.2b6',
          'pyvona==1.1', 
          'poster==0.8.1', 
          'pushbullet.py==0.10.0'
    ],
    dependency_links=['git+https://github.com/jtasker/python-weather-api@cf79f478c26dd244e0c90e10d6df91bb4ea8cd5e#egg=pywapi'],
    extras_require={
        'dev': ['flake8==3.0.4', 
                'mock==2.0.0', 
                'pytest==3.0.3',
                'pytest-cov==2.4.0', 
                'pytest-flake8==0.8.1'],
         },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'melissa = melissa.__main__:main',
        ],
    },
    zip_safe=False,
    keywords="virtual assistant speech-to-text text-to-speech melissa jarvis",
)
