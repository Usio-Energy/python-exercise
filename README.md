# Python Exercise

## Architecture 

For scheduled query of currencies the following stack implementation was used:
* flask server 
* crontab via celery scheduling 
* sqlight through sqlalchemy
* switching between development and production `app/config.py`
This architecture enables scalable deployment to a cloud platform in an agnostic manner (as opposed to using platform specific schedulers)
Scheduling is set as required by specs `app/celeryapp.json`, but for development / assessment purposes a more frequent scheduling is used by default

## Installation and deployment 

1. Package can be installed and build using Dockerfile 
`cd app` and `docker build --tag fixer .`
This can be run either locally or on any cloud platform. For example, top run on AWS instance 
`docker run -v /mydir:/apt fixer -e AWS_ACCESS_KEY_ID=MyKey -e AWS_SECRET_ACCESS_KEY=MyKey -p:5000:5000` (access keys not needed for local machine) 

2. Pull from Dockerhub `docker pull sivakhno/fixer:v0.1` and run with `docker run -v /mydir:/apt sivakhno/fixer:v0.1`

3. Installation using `requirements.txt` file. For this redis will need to be manually installed (see Dockerfile) and launched along with celery beforehand. Am example of running from `app` on MacOS with 
```
redis-stable/src/redis-server &
celery worker -A flask_server.celery --loglevel=DEBUG -B -c 1 && sleep 60 &
python3 flask_server.py &
```

## Usage
The scheduling protocol can be modified and expanded by altering `app/celeryapp.json`. Logs are written to `app.log` in current workdir.

## Testing 
### Unit testing 
Currently unit tests are set up for assessing database logic. Run from the base directory with 
`python3 -m unittest tests/tests.py` 
### Integration testing 
Use development configuration from `app/config.py` to test scheduler

## Improvements 

* Didn’t have time to do more integration testing and create error-handling logic - i.e. dealing with failed API requests 

* Adjustable logging information for various environments (development, testing and production) via python decorators 

* Running server and database in different containers and using docker compose for orchestration