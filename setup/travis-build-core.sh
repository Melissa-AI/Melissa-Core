#!/bin/sh
sudo apt-get update
sudo apt-get install libasound-dev mpg123 espeak swig
sudo pip install -r requirements.txt
wget https://launchpad.net/python-weather-api/trunk/0.3.8/+download/pywapi-0.3.8.tar.gz
tar xzvf pywapi-0.3.8.tar.gz && cd pywapi-0.3.8
python setup.py build
sudo python setup.py install
cd .. && rm -r pywapi-0.3.8.tar.gz
