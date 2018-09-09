# Solution Clement Daubrenet

As nothing was specified in term of techno, I went for Celery/Redis + PosgreSQL in a Flask app.

The application is based on 2 tasks:

- One fetching and storing the rates everyday at 9am
- One cleaning the rates of the last month every day

Multiple choices here:

- Instead of storing the rates with a TTL of one months, I decided to do a task to clean them with a time parameter.
I have no strong opinion about what's best.
- I store the rates in Posgres directly in JSON format. Faster to do than having one column per rate but the validation
is weaker. Maybe using elasticsearch would have been better. Again, I just did something fast.

The tests are unit and a bit of integration, not enough time for end-2-end.

# Installing redis

- sudo apt-get install redis-server

or

- brew install redis

# Installing postgres

- sudo apt-get install postgresql postgresql-contrib

or

- brew install postgresql

Create a database for your user and edit tasks/config.py with the right database URL.
Then you can initialize it with dbinit.py (python dbinit.py)

# Starting Postgres locally

pg_ctl -D /usr/local/var/postgres start


# Creating your virtual environment

- virtualenv env -p python3
- source env/bin/activate
- pip install -r requrements.txt

The version I used is actually Python 3.7.

# Run the tests

- python -m pytest tests/


# Run the application

To run the application, use the commands in commands.sh:

- Start redis server: redis-server
- Source your virtualenv (source env/bin/activate)
- Start the workers: celery -A celery_worker worker -l info
- Start the beat: celery -A celery_worker beat -l info


# Deploy and monitoring in production:

I did 2 different config classes (tasks/config.py) one for development and one for production.
Based on those, I would:

- First set up a log system with files (eg: 'usio_development.log' and 'usio_production.log')
for each environment with rotation (using 'logging.handlers.RotatingFileHandler', see example in config.py) and then
monitor the files.

- Then, a smtp server handling to reveive email notifications when errors. ('logging.handlers.SMTPHandler', see
example in config.py)

- To differentiate production and development I would use an environment variable.

- Finally, deployment scripts (one for dev, one for prod) on the servers: pulling the source and running the app.
The workers and beat would be deamonized on the servers.

- Potentially dockerize the app with more time.
