#!/usr/bin/env python

"""
BaseballDB_utils.py

Utility functions for Baseball Database.

2011-07-05, Travis Becker
"""

def PrintDict(mydict, name):
    """
    Print the contents of a dictionary to the screen.
    """
    print name, ' ='
    for i in mydict.keys():
        print '\t%s: %s' % (i, mydict[i])

def StringDict(mydict, name):
    """
    Return a string pretty printing the dictionary.
    """
    mystr = '%s =\n' % name
    for i in mydict.keys():
        mystr += '\t%s: %s\n' % (i, mydict[i])
    return mystr

def StringDictOneLine(mydict):
    """
    Return a string printing the dictionary on one line.
    """
    mystr = '{'
    mykeys = mydict.keys()
    for i in range(len(mykeys)):
        mystr += '%s: %s; ' % (mykeys[i], mydict[mykeys[i]])
    mystr += '%s: %s}' % (mykeys[i], mydict[mykeys[i]])

def GetTimeStamp():
    """
    Return a string containing the current time, for use in log files.
    """
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S GMT:', time.gmtime())

def GetDate():
    """
    Return a simple date string (no time value).
    """
    import time
    return time.strftime('%m/%d/%Y', time.gmtime())

def OpenDataFile(data_file):
    """
    Attempt to open a text data file for the given data type.
    """
    try:
        file_obj = open(data_file)
        return file_obj
    except IOError:
        raise IOError
        return None
