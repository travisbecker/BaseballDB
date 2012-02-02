#!/usr/bin/env python

"""
BaseballDB.py

Read in baseball data text files and import
into database.

Usage: python BaseballDB.py [-v] [-d data_file_path]

        where

        -v: Turn on verbose output.

        -d data_file_path: Define location of input
            data files, overriding default (../data).

        -h: Print help.

2011-07-05, Travis Becker
"""

import re
import sys
import string
import pyodbc

# Read in configuration data.
from BaseballDB_config import *

# Turn off verbose output by default.
verbose_output = False

# The util directory contains useful support utilities.
if __name__ == '__main__':
    sys.path.insert(0, DIRS['util'])
else:
    sys.path.insert(0, os.path.join(os.path.split(__file__)[0], DIRS['util']))
from BaseballDB_util import *

# The engine directory contains the main import and export routines.
if __name__ == '__main__':
    sys.path.insert(0, DIRS['engine'])
else:
    sys.path.insert(0, os.path.join(os.path.split(__file__)[0], DIRS['engine']))

def PrintHelp():
    """
    Print a help message.
    """
    print
    print 'BaseballDB.py'
    print
    print 'Usage: python BaseballDB.py [-v] [-d data_file_path] [-h]'
    print
    print '        where'
    print
    print '        -v: Turn on verbose output.'
    print
    print '        -d data_file_path: Define location of input'
    print '            data files, overriding default (../data).'
    print
    print '        -h: Print help.'
    print
    
def ProcessCommandLine():
    """
    Process command-line arguments.
    """
    
    if len(sys.argv) > 1:
        # Some paramaters have additional arguments, so need
        # to use a while loop, in case we need to jump to the
        # next argument, rather than a for loop.
        current_arg = 1
        while current_arg < len(sys.argv):
            if sys.argv[current_arg] == '-h':
                PrintHelp()
                sys.exit()
            elif sys.argv[current_arg] == '-v':
                verbose_output = True
            elif sys.argv[current_arg] == '-d':
                current_arg += 1
                DIRS['data'] = sys.argv[current_arg]

                # Redefine FILES to reflect the new data location.
                FILES[PEOPLE]     = [DIRS['data'] + os.sep + BASE_PEOPLE_FILENAME]
                FILES[BALLPARKS]  = [DIRS['data'] + os.sep + BASE_BALLPARKS_FILENAME]
                FILES[FRANCHISES] = [DIRS['data'] + os.sep + BASE_FRANCHISES_FILENAME]
                GAMELOG_FILENAME_PATTERN = '%s%s%s' % (DIRS['data'], os.sep, BASE_GAMELOG_FILENAME_PATTERN)
                FILES[GAMELOGS]  = glob.glob(GAMELOG_FILENAME_PATTERN)
            current_arg += 1
    
def PrintConfigData():
    """
    Print out a summary of the configuration data.
    """
    print 'Baseball Database'
    print
    print 'Defined directories:'
    PrintDict(DIRS, 'DIRS')
    print
    print 'Defined files:'
    PrintDict(FILES, 'FILES')
    print
    print 'Defined data types:'
    print DATA_TYPES
    print
    for i in DATA_TYPES:
        print 'Using %s for %s.' % (FILES[i], i)
    print
    
def main():
    ProcessCommandLine()
    PrintConfigData()

    # Connect to database
    cnxn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb)};Dbq=BaseballDB.mdb")
    cursor = cnxn.cursor()

    # Import the data files.
    for i in DATA_TYPES:
        # Make sure the table exists.
        try:
            cursor.execute("SELECT * from " + i)
        except:
            # Need to create the table.
            print 'Attempting to create table ' + i
            table_create_string = 'CREATE TABLE ' + i + '('
            table_create_list = []
            for j in DATA_FIELDS[i]:
                data_field_supertype = j.GetFieldSupertype()
                if   data_field_supertype == 'string' :
                    db_field_type = 'TEXT'
                elif data_field_supertype == 'numeric':
                    db_field_type = 'NUMBER'
                elif data_field_supertype == 'date'   :
                    db_field_type = 'DATE'
                else:
                    print 'WARNING: Invalid field type for %s.%s.' % \
                          (i, j.GetFieldName())
                table_create_list += [j.GetFieldName() + ' ' + db_field_type]
            table_create_string += string.join(table_create_list, ',') + ')'
            print table_create_string
            #try:
            cursor.execute(table_create_string)
            cnxn.commit()
            #except:
            #    print 'Unable to create table ' + i

        # Testing: delete the data in the table to start from scratch.
        cursor.execute("delete * from " + i)
        cnxn.commit()
        
        # The data type might have more than one file.
        for j in FILES[i]:
            try:
                print GetTimeStamp(), 'Opening %s for \'%s\' data.' % (j, i)
                file_obj = OpenDataFile(j)
                for line in file_obj:
                    line = line.strip() # Remove newline character at end.
                    line = string.replace(line, "'", "")
                    line_dict = {}
                    import_fields = string.split(line, ',')
                    if len(import_fields) != len(DATA_FIELDS[i]) - 1:
                        print '%s Line format wrong: %s' % (GetTimeStamp(), line)
                    else:
                        for j in range(len(import_fields)):
                            # Replace an empty string with database null character.
                            use_value = import_fields[j]
                            if not import_fields[j]:
                                use_value = DATABASE_NULL

                            # Some data files use double quotes to surround
                            # fields. Remove them if they exist.
                            quoted = re.match(r"^\"(.*)\"$", use_value)
                            if quoted:
                                use_value = quoted.group(1)

                            # If the imported field is numeric, convert to integer.
                            # (Assume no floating point fields are needed in this program.)
                            if DATA_FIELDS[i][j].IsFieldNumeric():
                                if import_fields[j]:
                                    use_value = int(use_value)
                                else:
                                    use_value = 0
                            if DATA_FIELDS[i][j].GetFieldSupertype() == 'date':
                                if not import_fields[j]:
                                    use_value = '1/1/1900'

                            # Special case. In the game log files, the game
                            # date is given by 'YYYYMMDD'. Need to convert this
                            # to 'MM/DD/YYYY'.
                            if i == 'game_logs':
                                if DATA_FIELDS[i][j].GetFieldName() == 'GameDate':
                                    use_value = str(use_value[4:6]) + '/' + \
                                                str(use_value[6:8]) + '/' + \
                                                str(use_value[0:4])

                            line_dict[DATA_FIELDS[i][j].GetFieldName()] = use_value
                        line_record = DatabaseRecord(line_dict, i)
                        line_record.data['DateAdded'] = GetDate()
                        print GetTimeStamp(), 'Importing', line_record.PrintSummary()

                        # Export to database.
                        table_insert_string = 'INSERT INTO ' + i + ' VALUES ('
                        table_insert_list = []
                        for k in DATA_FIELDS[i]:
                            data_field_supertype = k.GetFieldSupertype()
                            if   data_field_supertype == 'string' :
                                table_insert_list += ["'" + line_record.data[k.GetFieldName()] + "'"]
                            elif data_field_supertype == 'numeric':
                                table_insert_list += [str(line_record.data[k.GetFieldName()])]
                            elif data_field_supertype == 'date'   :
                                table_insert_list += ["'" + line_record.data[k.GetFieldName()] + "'"]
                            else:
                                print 'WARNING: Invalid field type for %s.%s.' % \
                                    (i, j.GetFieldName())
                        table_insert_string += string.join(table_insert_list, ',') + ')'
                        print GetTimeStamp(), 'Exporting to database'
                        cursor.execute(table_insert_string)
                        cnxn.commit()

                file_obj.close()
            except IOError:
                print 'unable to open'

                    
                    
        # To connect to Microsoft Access 2003-07 database:
        #cnxn = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb)};Dbq=<database.mdb>")
        #cursor = cnxn.cursor()
        #cursor.execute("create table Table1 (name text, hits number, debut date)")
        #cnxn.commit
        #cursor.execute("insert into Table1 values ('Hank Aaron', 3500, '4/25/1951')")
        #cursor.execute("select name from Table1")
        #rows = cursor.fetchall()
        #rows
        #cursor.execute("create table Table2 (
        #cnxn.close()
    cnxn.close()
        
if __name__ == '__main__':
    main()
