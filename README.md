# Python Exercise

## Usage
Docker has been used for development and deployment to a production environment can be done in two ways:
- traditional, run on a server with a cron job to run the script every weekday at 9:00 AM
- serverless with either aws lambda functions or GCP cloud functions, using triggers initialize the script at 9:00 AM
    - currently the app is only intended to be run on AWS

### Development
- To run the app in development run the following commands in the same directory as the docker-compose.yml file:
    - docker-compose up -d
    - docker-compose run app alembic upgrade head
    - docker-compose run app python main.py
- For further development and running unit tests:
    - docker-compose run app nosetests


### Production deployments
- see https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html for details on handlers and lambda functions
- run `docker-compose run app pip install -r /src/requirements.txt -t /src`
    - this will install dependencies into the root level directory, the contents of the src directory should then be zipped up
- using the AWS console or cli set the environment variables appropriately:
    -   FIXER_API_KEY
    -   FIXER_URL
    -   DATABASE_URL
- provision a postgres (or other SQL) database on your chosen platform
- run alembic migrations against the db, this may require provisioning an EC2 instance and checking out the code to run. the important command to run against the db is:
    -   `alembing upgrade head`
- create the lambda function, in this case using the aws cli:
    - ```aws lambda create-function \
        --region region \
        --function-name stor_fixer_data \
        --zip-file fileb://deployment-package.zip \
        --role arn:aws:iam::account-id:role/lambda_basic_execution  \
        --handler main.handler \
        --runtime python3.6 \
        --timeout 60 \
        --memory-size 512```
- the cron expression:
    - `aws events put-rule --schedule-expression "cron(0 9 * * MON-FRI *)" --name MyRule1`
    - set this as a trigger for the lambda function using the aws console or whatever method you are most familiar with



