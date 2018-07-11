# Python Exercise

High level requirements:

- Use the http://fixer.io/ API to ingest currency rates.
- Have the ingest & store procedure run daily at 9:00AM.
- Ingest and store rates for all days *except* weekends.
- Ensure the system holds at least the last month of rates information.

Technical requrements:

- Write code as you normally would write for deployment to a production environment.
- Use Python version 3.6+.
- Provide instructions on how to install and run the application.
- Document (in a text/markdown file) how you could go about deploying & monitoring the application.
- If you ran out of time on any of the high level requirements, write down which you specifically did not yet implement.

Try to spend no more than 4 hours on the exercise. Submit a pull request with your code or send it directly via email.


## Solution

This is a simple solution which is using `crontab` to executa simple Python script which collects the exchange rates
data from Fixer and inserts it into the database. The database used is SQLite, but it is trivial to adapt it to any
other database supported by `sqlalchemy`.

This is a quick and dirty solution which respects all the requirements, although in production it would probably be
better to use a more robust system such as Apache Airflow or similar. Also, the script is not parameterised, so any
changes need to be done in the code. If there is no data in the database, it will read the rates for the last 30 days.

### Deployment

To deploy the script, first make sure that the requirements are installed:

    $ sudo pip3 install -r requirements.txt

Then, copy `rates.py` anywhere on a Unix-based system and make sure that it is executable. Finally, add the
following job definition to `crontab`, with the actual path to the script's location:

    00 09 * * * /path/to/rates.py
