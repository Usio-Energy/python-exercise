# Python Exercise

## High level requirements:

- Use the http://fixer.io/ API to ingest currency rates.
- Have the ingest & store procedure run daily at 9:00AM.
- Ingest and store rates for all days *except* weekends.
- Ensure the system holds at least the last month of rates information.

## Technical requirements:

- Write code as you normally would write for deployment to a production environment.
- Use Python version 3.6+.
- Provide instructions on how to install and run the application.
- Document (in a text/markdown file) how you could go about deploying & monitoring the application.
- If you ran out of time on any of the high level requirements, write down which you specifically did not yet implement.

Try to spend no more than 4 hours on the exercise. Submit a pull request with your code or send it directly via email.

## Solution

This solution is a first phase - POC or prototype.

My aim is to have a working and testable version complete that can be built and iterated on at later stages of
development if necessary.

My initial decisions for design are as follows:

 - use docker to run the application in because:
   - can be deployed to AWS using the ECS service very easily
   - portable, both google and azure have container services
   - can be run on any server or VM that supports docker

 - use a PostgresSQL database to store the data in because:
   - persistent data storage
   - probably will already have an available DB service running
   - I read in job spec that postgres is in use
   - can store JSON as blob

 - write a simple Python script which retrieves and stores the JSON data into SQL fields


## Build and run

This has been developed built and run on a mac - all commands should run fine on any
*nix system though. I have not run or tested on Windows.

First you must have a valid value for API_KEY set in your env vars - to do this get a
valid api key from http://fixer.io/ and then set it with

    export API_KEY <your api key>

As the whole thing runs in docker you must have docker/docker-compose installed on your
system. Please consult the official documentation on how to do this.

Once you have docker installed you can navigate to the root folder (this folder) and
simply run the following:

    docker-compose build
    docker-compose up

Don't forget to tear it down after with

    docker-compose down

This will collect the daily rates and store them persistently in the database.
You can check this by manually connecting to the database with and interface pointing at
localhost:5432 with username postgres and password postgrespass.

I use psql which will connect as such

    export PGPASSWORD=postgrespass
    psql -h localhost -U postgres

NOTE that there is no task scheduling built into this part of the program. This is
because this is more properly part of the deployment and probably should not be done
within the code. Please see section below.


## Deployment

There is no specified requirement for deployment but I understand from the job spec that
AWS in in use. As such I would likely use amazon ECS to deploy the app as a docker image.

Using amazon ECS build in scheduler provided by amazon, within the task definition. This
task definition can be automated using CloudFormation, but I have not done this here due
to limited time.

An alternative could be using something like EBS which also has allows you to automate
scheduled running for the app - again the infrastructure can be written in CloudFormation.
