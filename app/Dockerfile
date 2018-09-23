FROM ubuntu:18.10
ENV FLASK_APP flask_server.py
COPY . /app
RUN mkdir -p /app/out
RUN apt-get update \
  && apt-get install -y wget \
  && apt-get install -y build-essential 

RUN wget http://download.redis.io/redis-stable.tar.gz \
    && tar xvzf redis-stable.tar.gz \
    && cd redis-stable && make

RUN apt-get update &&  apt-get install -y python3-pip python3.6-dev && pip3 install --upgrade pip 
RUN pip3 install -r /app/requirements.txt
RUN redis-stable/src/redis-server &
RUN celery worker -A flask_server.celery --loglevel=DEBUG -B -c 1 && sleep 60 &
CMD ["python3.6", "flask_server.py"]
WORKDIR /app

