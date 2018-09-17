# Simple periodic data ingestion service

A very basic service to periodically ingest and store data from a remote
source, in this case fx rates from [https://fixer.io/](Fixer).

## Contents
 - [Prerequisites](#prerequisites)
 - [Running](#running)

## Prerequisites
This project requires [Docker](https://docs.docker.com/install/) and
[Docker Compose](https://docs.docker.com/compose/install/). An API key must
be acquired from [Fixer](https://fixer.io/signup/free), tell the application
about your API key by copying the provided example Docker Compose overrides
file to its proper address and subsituting the example value of `FIXER_API_KEY`
with your key.

```
cp xdocker-compose.override.yml docker-compose.override.yml
```

## Running
Running the application is very easy. Clone this repository onto a computer
that satisfies the prerequisites outlined above, `cd` into the root of the
repository and invoke with
```
docker-compose up --build
```
