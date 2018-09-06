# This file is an example of what not to do.

# We should put this in an actual editable config file with configparser.
# I promise you, I know how to do this, but testing config on command line
# utilities is an astonishing pain and you probably don't want me to waste
# my time doing this, so I'm just going to stick them as app constants in
# this file here.

from appdirs import *
import os

# We're going to use appdirs here to make sure we have
# platform-safe data and log locations. In real life
# this would be configurable

# App details for application directories
APP_NAME = "fixercise"
APP_AUTHOR = "RikkHill"

# We will persist our data to this directory.
# In the mythical production version of this tool
# this would be configurable and we could put it anywhere
DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# We will want to log things to this location
LOG_DIR = user_log_dir(APP_NAME, APP_AUTHOR)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

FIXER_API_URL = "http://data.fixer.io/api"

# YOU SHOULD NEVER EVER DO THIS!
# You should never put secrets in your source code. It is bad and wrong.
# This should live in a proper config file or an envvar or something.
# I am fighting every natural impulse to put this here, but the constraints
# on this exercise compel me to do so.
FIXER_API_KEY = "285d26ee80459b0963164dd3c3872562"
