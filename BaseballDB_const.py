#!/usr/bin/env python

"""
BaseballDB_const.py

Universal constants for Baseball Database.

2011-07-18, Travis Becker
"""

import os

ALLOWED_FIELD_SOURCE = ( 'imported', 'created' )
ALLOWED_FIELD_SUPERTYPE = ( 'string', 'numeric', 'date', 'primary_key' )
SHORT_TEXT_FIELD = 'VARCHAR(10)'
MEDIUM_TEXT_FIELD = 'VARCHAR(20)'
LONG_TEXT_FIELD = 'VARCHAR(40)'
DATABASE_NULL = 'NULL'

# DIRS: Dictionary of directories to be used.
DIRS = {'main': '.' }
# Reference remaining directories relative to 'main'.
DIRS = {
    # Note that 'data' may be redefined later via a command-line parameter.
    'data': DIRS['main'] + os.sep + 'data',
    'util': DIRS['main'] + os.sep + 'util',
    'engine': DIRS['main'] + os.sep + 'engine'
    }

# Strings defining basic types of data files to import.
PEOPLE     = 'people'
BALLPARKS  = 'ballparks'
FRANCHISES = 'franchises'
GAMELOGS   = 'game_logs'

# data_types: Tuple of types of data that will be imported.
DATA_TYPES = (PEOPLE, BALLPARKS, FRANCHISES, GAMELOGS)

# Base file names.
BASE_PEOPLE_FILENAME     = 'RetroID_data.txt'
BASE_BALLPARKS_FILENAME  = 'ballparks_data.txt'
BASE_FRANCHISES_FILENAME = 'franchise_data.txt'
BASE_GAMELOG_FILENAME_PATTERN = 'GL[0-9][0-9][0-9][0-9].TXT'

### Database configuration parameters.
# Local database (easier for testing).
LOCAL_DB_CONFIG = {
    'driver': '{Microsoft Access Driver (*.mdb)}',
    'file'  : 'BaseballDB.mdb'
    }
DB_CONNECT_STRING = "\"DRIVER=" + LOCAL_DB_CONFIG['driver'] + \
                    ";DBQ=" + LOCAL_DB_CONFIG['file'] + "\""

# Remote database (eventual home).
REMOTE_DB_CONNECT_STRING = "DSN=BaseballDB"
