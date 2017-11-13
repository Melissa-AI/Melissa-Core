FROM ubuntu:latest

MAINTAINER Tanay Pant "tanay1337@gmail.com"


RUN apt-get update -y 
RUN apt-get install -y gcc automake autoconf libtool bison swig python-dev libpulse-dev espeak multimedia-jack

COPY . /app

WORKDIR /app

COPY melissa/data/memory.db.default melissa/data/memory.db

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["FLASK_APP=melissa/__main__.py", "flask", "run"]

