#!/usr/bin/env python
'''
Miscellaneous utilities used by several modules.
Some of these methods are obviously wrappers but these are
intended to be used to unify file I/O across the modules.
'''

import csv
import datetime
import json
import sys

JSON_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
CSV_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
EPOCH_START = datetime.datetime(1970, 1, 1)


def load_json(path):
    '''
    Load JSON file and return corresponding object.
    '''
    json_file = open(path).read()
    return json.loads(json_file)


def get_delimiter(filepath):
    '''
    Checks the file extension to determine
    the delimiter that should be used for a filepath.
    '.sql' files return a tab character
    anything else returns a comma character.
    '''
    if filepath.endswith('.sql'):
        return '\t'
    else:
        return ','


def get_id(entry):
    '''
    Returns a unique id for an entry in a vismooc table.
    '''
    # TODO was there no other non-cryptographic hash function? (We can leave it and open an issue about fixing it if we
    # are waiting for answer from VisMOOC)
    return hash(str(entry)) % (sys.maxsize + 1)


def load_table_and_write_simple_csv(input_path, output_path, fields,
                                    field_to_func_map):
    '''
    Write a simple vismooc_extension csv table that sources the Edx data
    from only a single input file.

    This serves largely as a wrapper around write_simple_csv but handles loading
    in a table file (.sql or .csv) on disk.
    '''
    with open(input_path, 'r') as input_file:
        reader = csv.DictReader(
            input_file, delimiter=get_delimiter(input_path))
        write_simple_csv(reader, output_path, fields, field_to_func_map)


def write_simple_csv(input_iterable, output_path, fields, field_to_func_map):
    '''
    Write a simple vismooc_extension csv table that sources data
    from only the input iterable.

    input_iterable should be an iterable where each item is a dictionary object
    (or has a __getitem__ method).
    output_path should be the absolute path to the output .csv file
    fields should be a list of strings containing the fields of the output .csv file
    field_to_func_map should be a map of an output field to a function that takes
    a single argument. This argument should be of the same type as the items
    contained in the input_iterable argument.
    '''
    output_file = open(output_path, 'w')
    writer = csv.DictWriter(
        output_file,
        delimiter=',',
        fieldnames=fields,
        quotechar='"',
        escapechar='\\',
        lineterminator='\n')

    for item in input_iterable:
        writer.writerow({
            field: field_to_func_map[field](item).encode('utf-8')
            if isinstance(field_to_func_map[field](item), unicode)
            else field_to_func_map[field](item)
            for field in fields})
    output_file.close()
