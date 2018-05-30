#!/usr/bin/env python
'''
vismooc extensions module to extract the users
data from the Edx user and profile files.
'''
import csv
import hashlib
import itertools
from StringIO import StringIO

import util


def write_users_csv(user_path, profile_path, output_path):
    '''
    Write the users vismooc_extension csv table.

    util.write_simple_csv cannot be used because that models a simple case of
    a single Edx input course file used to create a single vismooc extensions
    output table. The vismooc extensions users table pulls data from the Edx
    user file and the Edx profile file and hence a custom function must be written.
    Both the Edx user and profile file are expected to have the exact same number
    of rows. If they have different lengths then the processing stops once the file
    with the lower number of rows is exhausted.

    user_path should be the absolute path to a .csv or .sql Edx user file
    profile_path should be the absolute path to a .csv or .sql Edx profile file
    output_path should be the absolute path to the output .csv file
    '''
    user_map = get_user_field_to_func_map()
    profile_map = get_profile_field_to_func_map()

    output_file = open(output_path, 'w')
    writer = csv.DictWriter(
        output_file,
        delimiter=',',
        fieldnames=get_csv_fields(),
        quotechar='"',
        escapechar='\\',
        lineterminator='\n')

    profile_string = ''
    with open(profile_path) as raw_profile_file:
        profile_string = raw_profile_file.read()
    profile_file = StringIO(clean_profile_file_data(profile_string))

    with open(user_path) as user_file:
        user_reader = csv.DictReader(
            user_file, delimiter=util.get_delimiter(user_path))
        profile_reader = csv.DictReader(
            profile_file, delimiter=util.get_delimiter(profile_path))

        for user_row, profile_row in itertools.izip(user_reader,
                                                    profile_reader):
            output_row = {
                field: user_map[field](user_row)
                for field in user_map
            }
            output_row.update({
                field: profile_map[field](profile_row)
                for field in profile_map
            })
            output_row = {
                key: value if value != 'NULL' else ''
                for (key, value) in output_row.iteritems()
            }
            writer.writerow(output_row)
    profile_file.close()
    output_file.close()


def get_csv_fields():
    '''
    Return the csv fields for the users table.
    '''
    return [
        '_id', 'original_id', 'username', 'name', 'language', 'location',
        'birth_date', 'education_level', 'bio', 'gender', 'country'
    ]


def get_user_field_to_func_map():
    '''
    Returns a map of an output csv field to a function that takes a single
    argument which is a user row (dict object).

    Most of the functions will simply pull the desired value striaght out
    of the dict argument but this design is chosen to provide flexibility
    in performing post-processing on the values contained in the dict
    argument should the schema mappings change, while still separating
    the boilerplate work of dumping the final values out to a csv. The
    boilerplate work is left to write_users_csv.
    '''
    return {
        'original_id':
        lambda row: row['id'],
        'username':
        lambda row: hashlib.new('ripemd160', row['username']).hexdigest()
    }


def get_profile_field_to_func_map():
    '''
    Returns a map of an output csv field to a function that takes a single
    argument which is a profile row (dict object).

    Most of the functions will simply pull the desired value striaght out
    of the dict argument but this design is chosen to provide flexibility
    in performing post-processing on the values contained in the dict
    argument should the schema mappings change, while still separating
    the boilerplate work of dumping the final values out to a csv. The
    boilerplate work is left to write_users_csv.
    '''
    return {
        '_id': lambda row: row['id'],
        'name': lambda row: hashlib.new('ripemd160', row['name']).hexdigest(),
        'language': lambda row: row['language'],
        'location': lambda row: row['location'],
        'birth_date': lambda row: row['year_of_birth'],
        'education_level': lambda row: row['level_of_education'],
        'bio': lambda row: row['goals'],
        'gender': lambda row: row['gender'],
        'country': lambda row: row['country']
    }


def clean_profile_file_data(string):
    '''
    Finds troublesome byte sequences that are sometimes contained in the
    Edx profile and replaces them with safer equivalents to avoid tripping
    up csv.DictReader.

    For example, the byte sequence '\r\\n' can be found in fields such as
    'mailing_address' but it should not be left to interpretation as a
    newline by csv.DictReader because then the data row gets split
    into several data rows.

    string should be a regular Python string obtained by calling read() on
    an open Edx profile file.

    The following replacements are made:
    '\r\\n' -> '\\n'

    Returns a string with the troublesome byte sequences replaced with safer
    equivalents.
    '''
    return string.replace('\r\\n', '\\n')
