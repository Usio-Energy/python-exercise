# Install locally

Prereq - docker & docker compose. https://docs.docker.com/install/
```
docker-compose build
docker-compose up db
```

Once the database is created
```
docker-compose up
docker-compose run --rm web django-admin createsuperuser
```

To run the test locally:
```
docker-compose run --rm web django-admin test python_exercice.currency
```