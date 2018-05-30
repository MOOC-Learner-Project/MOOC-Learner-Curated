#!/usr/bin/env python
'''
vismooc extensions module to extract the 
grades data from the Edx certificates file.
'''


def get_csv_fields():
    '''
    Return the csv fields for the grades table.
    '''
    return ['_id', 'user_id', 'course_id', 'timestamp', 'grade']


def get_csv_field_to_func_map():
    '''
    Returns a map of the grades output csv field to
    a function that takes a single argument which is a row (dict object).

    Most of the functions will simply pull the desired value striaght out
    of the dict argument but this design is chosen to provide flexibility
    in performing post-processing on the values contained in the dict
    argument should the schema mappings change, while still separating
    the boilerplate work of dumping the final values out to a csv. The
    boilerplate work is left to util.write_simple_csv.
    '''
    return {
        '_id': lambda row: row['id'],
        'user_id': lambda row: row['user_id'],
        'course_id': lambda row: row['course_id'],
        'timestamp': lambda row: row['created_date'],
        'grade': lambda row: row['grade']
    }
