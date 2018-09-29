FROM ubuntu:18.04

# install depenencies

RUN apt-get update -y
RUN apt-get install -y python3.6 python-pip python3-pip

# setup python environment, we want to default to python 3.6

RUN rm -f /usr/bin/python && ln -s /usr/bin/python3.6 /usr/bin/python

ADD ./requirements.txt /src/requirements.txt

RUN pip install -r /src/requirements.txt

WORKDIR "src"
