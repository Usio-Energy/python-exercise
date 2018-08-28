# Python Exercise

**Introduction**

This app has been written using Python 3.6 and Django 2.1

This app uses RabbitMQ with celery to schedule the exchange rate collection at 9am every weekday, 
and sqlite to store the retrieved data.

An additional REST method has been supplied to collect data from legacy time periods, as has another
method for displaying the stored data.   

**Installation**

This app requires Docker, and Docker compose. It can be started as follows:

```bash
docker-compose build
docker-compose up -d
```

**Usage**

While running, this app will attempt to collect exchange rate data from Fixer.io at 9am every weekday, 
for that specific date

To see the exchange rates stored against a specific date, you can use the following REST method:
```bash
curl -X GET --header 'Accept: application/json' 'http://localhost/api/entries/2018-08-28/'
```

When you first run this app, the DB will contain no entries until 9am the next day when the scheduled 
task runs. To populate the DB with some data, you can use the below method, which ingests exchange 
rates between two given dates:
```bash
# ingest exchange rates from 2016/08/26 to the present day
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json'  -d '{ \ 
   "start_date": "2018-08-26" \ 
 }' 'http://localhost/api/entries/update_legacy'
 
 # ingest exchange rates between 2018/08/21 and 2018/08/28
 curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ \ 
   "start_date": "2018-08-21", \ 
   "end_date": "2018-08-28" \ 
 }' 'http://localhost/api/entries/update_legacy'
```

*Note that the above method returns an empty response. To see the data ingested, use the first method
to retrieve exchange rates for a specific day*
 
**Swagger**

As a convenience, a swagger view has been provided as a means of visualizing, documenting and testing 
the two REST methods. This view is available at http://localhost/api/docs/#/

**Deployment**

As this app has already been dockerized, it is fairly straightforward to run in production. However,
there are a few changes that would need to be made:

- The Django settings file would need to have private values (e.g. secret key, rabbitmq credentials) 
  written to environmental variables
- The celery service is currently running in dev mode - this would need changing
- The uWSGI permissions are currently too permissive to run in a live environment
- CORS config in nginx is a bit too open at present
- RabbitMQ credentials are currently set to their default values

**Monitoring**

All of the python processes in this app are controlled by supervisord. For production, it can be 
potentially integrated with the ELK stack for monitoring