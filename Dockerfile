FROM python:3.7-alpine

RUN apk add --no-cache openssl

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# https://github.com/pytest-dev/pytest/issues/2430
RUN pip install \
    celery==4.2.1 \
    ipdb==0.11 \
    pg8000==1.12.3 \
    pytest==3.0.7 \
    redis==2.10.6 \
    requests==2.19.1 \
    sqlalchemy==1.2

COPY src /app
COPY test /test
WORKDIR /app
