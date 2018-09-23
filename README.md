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

# Solution

The presented solution took me a bit more of the 4 hours specified, mainly because I spent a lot of time trying to provide a
database solution that did not required the use of docker. I desisted trying to get a postgres instance running on my machine
and went for an implementation of a piclke file based storage. The storage handler is pandas as it whould have been easy to push 
the same data into a database given an engine. 

The installation of the application only requires a git pull from the repository where the code is stored.
In addition will be required to have up to date the dependent libraries in requirements.txt
Also an API key has to be provided, to do so a `secrets.py` containig text `api_key = YOUR_API_KEY` has to be
created in the main directory of the exercise.

Please note that to obtain a complete month worth of data a premium API has to be purchased from fixer.io.

To run the tests the following should be introduced in the comand line:

`pytest PATH_TO_EXERCISE/python-exercise/test/test_set.py`
    
To deploy the application I whould set up a database implementation of the storage, that has not been the
solution provided to this excercise due to the overhead work that whould have taken.
    
When deploying I would set an scheduler in the server that the app runs, to do so run the following core in a unix comand line:

`0 9 * * * PATH_TO_EXERCISE/python-exercise/__main__.py`
    
To monitor the app, I would check that the increments of data are as expected in regular intervals. In addition I woul
d check the correctness of the data calling to the storage every now and then.

Regarding te high level requirements all four of them have been achieved with some points worth noticing:
- A file storage solution is not the prefered one but an acceptable compromise for the sake of the exercise
- The collection of data is using the most efficeint methods available although the `timeseries` capabilities of fixer.io have to be adquired.
- The collected data is stored in a tidy format to ease the analysis and remove unnecesary metadata
- The selection of weekdays is done when tidying the data
- When saving the data a check on completion is perform and the handler collects the missing data if needed

In addition some test have been implemented testing the tree main steps of this excersise:
- Checking that the calls are sucessfull
- Testing that the data is clean and tidy
- Testing that there is no deletion of data when saving


