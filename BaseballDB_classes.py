#!/usr/bin/env python

"""
BaseballDB_classes.py

Class definitions for Baseball Database:
    DatabaseField
    DatabaseRecord

2011-07-18, Travis Becker
"""

import sys
from BaseballDB_const import *

### Class for database field definitions.
class DatabaseField():
    """
    Class for a database fields that contains information
    about setting up the field in a database table.

    field_name:   Name of the field
    field_type:   Data type of the field
    field_source: 'imported' (pulled directly from an input
            text file) or 'created' (created by the program).
    field_supertype: 'string' or 'numeric' to determine how to import the field.

    Initialization: DatabaseField(field_name, field_type, field_source)
    """

    def __init__(self, field_name='NoName',
                 field_type=LONG_TEXT_FIELD,
                 field_source='created',
                 field_supertype='string'):
        self.field_name   = field_name
        self.field_type   = field_type
        if field_source in ALLOWED_FIELD_SOURCE:
            self.field_source = field_source
        self.field_supertype = field_supertype

    def __str__(self):
        return '%s: %s (%s)' % (self.field_name, self.field_type,
                                self.field_source)

    def GetFieldName(self):
        return self.field_name

    def GetFieldType(self):
        return self.field_type

    def GetFieldSupertype(self):
        return self.field_supertype

    def IsFieldImported(self):
        return (self.field_source == 'imported')

    def IsFieldNumeric(self):
        return (self.field_supertype == 'numeric')
        
    def SetFieldType(self, newType):
    	  self.field_type = newType;
    	  
    def SetFieldSupertype(self, newSupertype):
    	  self.field_supertype = newSupertype;


### Class for records, both for import from text files and export to database.
class DatabaseRecord():
    def __init__(self, input_dict, record_type):
        self.record_type = record_type
        import copy
        self.data = copy.deepcopy(input_dict)

    def __str__(self):
        sys.path.insert(0, DIRS['util'])
        from BaseballDB_util import StringDict as StringDict
        return '%s\tRecord type: %s\n' % (StringDict(self.data, 'record'),
                                           self.record_type)

    def PrintOneLine(self):
        sys.path.insert(0, DIRS['util'])
        from BaseballDB_util import StringDictOneLine as StringDictOneLine
        return 'Record type: %s; data = %s' % (self.record_type, self.data)

    def PrintSummary(self):
        if self.record_type == 'people':
            return '%s %s (%s)' % (self.data['FirstName'], \
                                   self.data['LastName'], \
                                   self.data['RetroID'])
        elif self.record_type == 'ballparks':
            return '%s (%s)' % (self.data['Name'], \
                                self.data['ID'])
        elif self.record_type == 'franchises':
            return '%s %s (%s)' % (self.data['City'], \
                                   self.data['Nickname'], \
                                   self.data['Abbr'])
        elif self.record_type == 'game_logs':
            return '%s at %s on %s' % (self.data['VisitingTeamName'], \
                                       self.data['HomeTeamName'], \
                                       self.data['GameDate'])

    def __eq__(self, other):
        # Can't compare records of different types.
        if self.record_type != other.record_type:
            return_value = False
        else:
            """
            When comparing database records, only compare the 'imported' data.
            """
            for i in DATA_FIELDS[self.record_type]:
                if i.FieldImported():
                    print 'comparing field %s' % i.FieldName()
                    if self.data[i.FieldName()] != other.data[i.FieldName()]:
                        return_value = False

            # Wish I could do:
            # for i in [j in DATA_FIELDS[self.record_type] if j.FieldImported()]
            # But this gives an 'invalid syntax' error.

            return_value = True

        return return_value
