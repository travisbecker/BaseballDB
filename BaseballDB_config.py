#!/usr/bin/env python

"""
BaseballDB_config.py

Set up configuration items for BaseballDB.py.

2011-07-05, Travis Becker
"""

import glob
import re
from BaseballDB_const import *
from BaseballDB_classes import *

# Connect each data type to an associated database field for Person.
PERSON_LAST_NAME    = DatabaseField('LastName', MEDIUM_TEXT_FIELD, 'imported', 'string')
PERSON_FIRST_NAME   = DatabaseField('FirstName', MEDIUM_TEXT_FIELD, 'imported', 'string')
PERSON_RETRO_ID     = DatabaseField('RetroID', 'VARCHAR(8)', 'imported', 'string')
PERSON_DEBUT        = DatabaseField('Debut', 'DATE', 'imported', 'date')
PERSON_DATE_ADDED   = DatabaseField('DateAdded', 'DATE', 'created', 'date')

# Connect each data type to an associated database field for Ballpark.
BALLPARK_PARKID     = DatabaseField('ID', 'VARCHAR(5)', 'imported', 'string')
BALLPARK_NAME       = DatabaseField('Name', LONG_TEXT_FIELD, 'imported', 'string')
BALLPARK_AKA        = DatabaseField('AKA', LONG_TEXT_FIELD, 'imported', 'string')
BALLPARK_CITY       = DatabaseField('City', MEDIUM_TEXT_FIELD, 'imported', 'string')
BALLPARK_STATE      = DatabaseField('State', 'VARCHAR(2)', 'imported', 'string')
BALLPARK_START      = DatabaseField('StartDate', 'DATE', 'imported', 'date')
BALLPARK_END        = DatabaseField('EndDate', 'DATE', 'imported', 'date')
BALLPARK_LEAGUE     = DatabaseField('League', 'VARCHAR(2)', 'imported', 'string')
BALLPARK_NOTES      = DatabaseField('Notes', LONG_TEXT_FIELD, 'imported', 'string')
BALLPARK_DATE_ADDED = DatabaseField('DateAdded', 'DATE', 'created', 'date')

# Connect each data type to an associated database field for Franchise.
FRANCHISE_ABBR       = DatabaseField('Abbr', 'VARCHAR(3)', 'imported', 'string')
FRANCHISE_LEAGUE     = DatabaseField('League', 'VARCHAR(2)', 'imported', 'string')
FRANCHISE_CITY       = DatabaseField('City', MEDIUM_TEXT_FIELD, 'imported', 'string')
FRANCHISE_NICKNAME   = DatabaseField('Nickname', MEDIUM_TEXT_FIELD, 'imported', 'string')
FRANCHISE_START_YEAR = DatabaseField('StartYear', 'INT', 'imported', 'numeric')
FRANCHISE_END_YEAR   = DatabaseField('EndYear', 'INT', 'imported', 'numeric')
FRANCHISE_DATE_ADDED = DatabaseField('DateAdded', 'DATE', 'created', 'date')

GAMELOG_FILENAME_PATTERN = '%s%s%s' % (DIRS['data'], os.sep, BASE_GAMELOG_FILENAME_PATTERN) # Allow for multiple files.

# FILES: Dictionary of files to be used.
FILES = {
    # People, ballpark and franchise files are static.
    # Define as lists since more than one file may be imported.
    # All except GAMELOGS should have a single entry.
    PEOPLE:     [DIRS['data'] + os.sep + BASE_PEOPLE_FILENAME],
    BALLPARKS:  [DIRS['data'] + os.sep + BASE_BALLPARKS_FILENAME],
    FRANCHISES: [DIRS['data'] + os.sep + BASE_FRANCHISES_FILENAME],
    GAMELOGS:   glob.glob(GAMELOG_FILENAME_PATTERN)
    }

# data_fields: Dictionary of tuples for each data type.
# This defines the order of the fields in the input data file.
DATA_FIELDS = {
    PEOPLE: (PERSON_LAST_NAME, PERSON_FIRST_NAME, PERSON_RETRO_ID,
             PERSON_DEBUT, PERSON_DATE_ADDED),
    BALLPARKS: (BALLPARK_PARKID, BALLPARK_NAME, BALLPARK_AKA,
                BALLPARK_CITY, BALLPARK_STATE, BALLPARK_START,
                BALLPARK_END, BALLPARK_LEAGUE, BALLPARK_NOTES,
                BALLPARK_DATE_ADDED),
    FRANCHISES: (FRANCHISE_ABBR, FRANCHISE_LEAGUE, FRANCHISE_CITY,
                 FRANCHISE_NICKNAME, FRANCHISE_START_YEAR,
                 FRANCHISE_END_YEAR, FRANCHISE_DATE_ADDED)
    }

# Create data_fields for GAMELOG.
team_parts = ('VisitingTeam', 'HomeTeam')
name_league_gameNumber = ('Name', 'League', 'GameNumber')
offensive_stats = ('AtBats', 'Hits', 'Doubles', 'Triples', 'HomeRuns',
                   'RBI', 'SacrificeHits', 'SacrificeFlies', 'HitByPitch',
                   'Walks', 'IntentionalWalks', 'Strikeouts', 'StolenBases',
                   'CaughtStealing', 'GroundedIntoDoublePlays',
                   'CatcherInterference', 'LeftOnBase')
pitching_stats = ('PitchersUsed', 'IndividualEarnedRuns', 'TeamEarnedRuns',
                  'WildPitches', 'Balks')
defensive_stats = ('Putouts', 'Assists', 'Errors', 'PassedBalls',
                   'DoublePlays', 'TriplePlays')
umpire_positions = ('HomePlateUmpire', '1BUmpire', '2BUmpire', '3BUmpire',
                    'LFUmpire', 'RFUmpire')
key_people_fields = ('WinningPitcher', 'LosingPitcher', 'SavingPitcher', 'GWRBIBatter')
id_and_name = ('ID', 'Name')
id_name_and_position = ('ID', 'Name', 'Position')

# Need to use a list rather than a tuple in order to add indivudal or multiple fields.
DATA_FIELDS[GAMELOGS] = [
    DatabaseField('GameDate', 'DATE', 'imported', 'date'),            # Field 1
    DatabaseField('GameNumber', 'VARCHAR(1)', 'imported', 'numeric'), # Field 2
    DatabaseField('DayOfWeek', 'VARCHAR(3)', 'imported', 'string')    # Field 3
    ]
# Fields 4-9: Team name, league and game number for visiting and home team.
# Can't do "for i in team_parts for j in name_league_gameNumber" since mixing string and numeric.
#DATA_FIELDS[GAMELOGS] += [
#    DatabaseField(i+j, SHORT_TEXT_FIELD, 'imported', 'string') \
#    for i in team_parts for j in name_league_gameNumber
#    ]
DATA_FIELDS[GAMELOGS] += [
    DatabaseField(team_parts[0] + name_league_gameNumber[0], SHORT_TEXT_FIELD, 'imported', 'string'), \
    DatabaseField(team_parts[0] + name_league_gameNumber[1], SHORT_TEXT_FIELD, 'imported', 'string'), \
    DatabaseField(team_parts[0] + name_league_gameNumber[2], 'INT', 'imported', 'numeric'), \
    DatabaseField(team_parts[1] + name_league_gameNumber[0], SHORT_TEXT_FIELD, 'imported', 'string'), \
    DatabaseField(team_parts[1] + name_league_gameNumber[1], SHORT_TEXT_FIELD, 'imported', 'string'), \
    DatabaseField(team_parts[1] + name_league_gameNumber[2], 'INT', 'imported', 'numeric')
    ]

# Fields 10 and 11: Visiting and home team score.
DATA_FIELDS[GAMELOGS] += [
    DatabaseField(i+'Score', 'INT', 'imported', 'numeric') \
    for i in team_parts
    ]

DATA_FIELDS[GAMELOGS] += [
    DatabaseField('GameLengthOuts', 'INT', 'imported', 'numeric'),          # Field 12
    DatabaseField('DayNight', 'VARCHAR(1)', 'imported', 'string'),          # Field 13
    DatabaseField('CompletionInfo', LONG_TEXT_FIELD, 'imported', 'string'), # Field 14
    DatabaseField('ForfeitInfo', 'VARCHAR(1)', 'imported', 'string'),       # Field 15
    DatabaseField('ProtestInfo', 'VARCHAR(1)', 'imported', 'string'),       # Field 16
    DatabaseField('ParkID', 'VARCHAR(5)', 'imported', 'string'),            # Field 17
    DatabaseField('Attendance', 'INT', 'imported', 'numeric'),              # Field 18
    DatabaseField('GameLengthMinutes', 'INT', 'imported', 'numeric')        # Field 19
    ]

# Fields 20 and 21: Line scores.
DATA_FIELDS[GAMELOGS] += [
    DatabaseField(i+'LineScore', LONG_TEXT_FIELD, 'imported', 'string') \
    for i in team_parts
    ]

# Fields 22-77: Visiting and Home team statistics.
DATA_FIELDS[GAMELOGS] += [
    DatabaseField(i+j, 'INT', 'imported', 'numeric') \
    for i in team_parts for j in offensive_stats + pitching_stats + defensive_stats
    ]

# Fields 78-89: Umpire info.
DATA_FIELDS[GAMELOGS] += [
    DatabaseField(i+j, MEDIUM_TEXT_FIELD, 'imported', 'string') \
    for i in umpire_positions for j in id_and_name
    ]

# Fields 90-93: Manager info.
DATA_FIELDS[GAMELOGS] += [
    DatabaseField(i+'Manager'+j, MEDIUM_TEXT_FIELD, 'imported', 'string') \
    for i in team_parts for j in id_and_name
    ]

# Fields 94-101: Key people info.
DATA_FIELDS[GAMELOGS] += [
    DatabaseField(i+j, MEDIUM_TEXT_FIELD, 'imported', 'string') \
    for i in key_people_fields for j in id_and_name
    ]

# Fields 102-105: Starting pitchers.
DATA_FIELDS[GAMELOGS] += [
    DatabaseField(i+'StartingPitcher'+j, MEDIUM_TEXT_FIELD, 'imported', 'string') \
    for i in team_parts for j in id_and_name
    ]

# Fields 106-159: Starting lineups.
DATA_FIELDS[GAMELOGS] += [
    DatabaseField(i+'Batter'+str(j)+k, MEDIUM_TEXT_FIELD, 'imported', 'string') \
    for i in team_parts for j in range(1,10) for k in id_name_and_position
    ]
    
# Go back and fix fields that are actually numeric (i.e., player position).
for i in range(106,160):
    if (re.search('TeamBatter\d+Position$', DATA_FIELDS[GAMELOGS][i-1].GetFieldName())):
        DATA_FIELDS[GAMELOGS][i-1].SetFieldSupertype('numeric')
        DATA_FIELDS[GAMELOGS][i-1].SetFieldType('INT')
        

DATA_FIELDS[GAMELOGS] += [
    DatabaseField('AdditionalInfo', LONG_TEXT_FIELD, 'imported', 'string'),     # Field 160
    DatabaseField('AcquisitionInfo', 'VARCHAR(1)', 'imported', 'string')        # Field 161
    ]

# Last field: Date added.
DATA_FIELDS[GAMELOGS] += [DatabaseField('DateAdded', 'DATE', 'created', 'date')]
