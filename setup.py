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
    version="0.1.0",
    description=description,
    long_description=long_description,
    author='Tanay Pant',
    author_email='tanay1337@gmail.com',
    url='https://github.com/Melissa-AI/Melissa-Core/',
    license="MIT",
    packages=find_packages(),
    package_data={'': ['LICENSE.md', 'README.rst']},
    package_dir={'melissa': 'melissa'},
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
