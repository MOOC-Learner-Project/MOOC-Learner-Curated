#!/usr/bin/env python
'''
vismooc extensions module to extract the courses data
from the Edx course_structure json file.
'''
import csv
import datetime
import re

import util

COURSE_ENTRY_KEY_REGEX = re.compile(
    'i4x://(?P<org>[^/]*)/(?P<course>[^/]*)/course/(?P<run>[^/]*)')


def write_courses_csv(dictionary, output_path):
    '''
    Write the courses csv out to output_path,
    according to the dictionary representing the loaded
    {org}-{course}-{run}-course_structure-{site}-analytics.json file
    '''
    if not contains_course(dictionary):
        raise ValueError('loaded json file is missing a course entry')

    course_entry_key = get_course_entry_key(dictionary)
    course_entry = dictionary[course_entry_key]
    output_file = open(output_path, 'w')
    writer = csv.DictWriter(
        output_file,
        delimiter=',',
        fieldnames=get_csv_fields(),
        quotechar='"',
        escapechar='\\',
        lineterminator='\n')

    writer.writerow({
        '_id': str(util.get_id(course_entry)),
        'original_id': get_original_id(dictionary),
        'name': get_name(course_entry),
        'year': get_year(course_entry),
        'org': get_org(course_entry_key),
        'instructor': get_instructor(),
        'description': get_description(),
        'start_date': get_start_date(course_entry),
        'end_date': get_end_date(course_entry),
        'course_url': get_course_url(),
        'image_url': get_image_url()
    })
    output_file.close()


def get_csv_fields():
    '''
    Return the csv fields for the courses table.
    '''
    return [
        '_id', 'original_id', 'name', 'year', 'org', 'instructor',
        'description', 'start_date', 'end_date', 'course_url', 'image_url'
    ]


def contains_course(dictionary):
    '''
    dictionary should be a dictionary object representing the loaded course_structure json file.
    Returns whether or not the dictionary object has
    a (key, entry) pair where entry['category'] is 'course'.
    '''
    for (_, entry) in dictionary.iteritems():
        if 'category' not in entry:
            continue
        if entry['category'] == 'course':
            return True
    return False


def get_course_entry_key(dictionary):
    '''
    dictionary should be a dictionary object representing the loaded course_structure json file.
    Returns the key corresponding to the entry in the dictionary
    with the 'category' -> 'course' mapping. Returns None if no such
    key exists.
    '''
    for (key, entry) in dictionary.iteritems():
        if 'category' not in entry:
            continue
        if entry['category'] == 'course':
            return key
    return None


def get_original_id(dictionary):
    '''
    dictionary should be a dictionary object representing the loaded course_structure json file.
    Returns the original_id value according to the vismooc schema
    The original_id is of the form {org}/{course}/{run}.

    Returns an empty string if it cannot be found.
    '''
    course_entry_key = get_course_entry_key(dictionary)
    if course_entry_key is None:
        return ''
    match = COURSE_ENTRY_KEY_REGEX.search(course_entry_key)
    if match is None:
        return course_entry_key
    return '%s/%s/%s' % (match.group('org'), match.group('course'),
                         match.group('run'))


def get_name(course_entry):
    '''
    course_entry should be a dictionary object representing the entry
    with the 'catetgory' -> 'course' mapping.
    Returns the course name value according to the vismooc schema
    Returns an empty string if it cannot be found.
    '''
    if 'metadata' not in course_entry:
        return ''
    if 'display_name' not in course_entry['metadata']:
        return ''
    return course_entry['metadata']['display_name']


def get_year(course_entry):
    '''
    Returns the course start year as a string in the format YYYY_Q%d_R%d
    according to the start date.
    '''
    return '%d_Q%d_R%d' % (datetime.datetime.strptime(
        course_entry['metadata']['start'], util.JSON_TIMESTAMP_FORMAT).year, 0,
                           0)


def get_org(course_entry_key):
    '''
    course_entry_key is a string of the format i4x:://{org}/{course}/course/{run}.
    Returns the org value according to the vismooc schema
    Returns an empty string if it cannot be found.
    '''
    match = COURSE_ENTRY_KEY_REGEX.search(course_entry_key)
    if match is None:
        return ''
    return match.group('org')


def get_instructor():
    '''
    get_instructor should return an empty string until further
    clarification from the vismooc team.
    '''
    return ''


def get_description():
    '''
    get_description should return an empty string until further
    clarification from the vismooc team.
    '''
    return ''


def get_course_url():
    '''
    get_course_url should return an empty string until further
    clarification from the vismooc team.
    '''
    return ''


def get_image_url():
    '''
    get_image_url should return an empty string until further
    clarification from the vismooc team.
    '''
    return ''


def get_start_date(course_entry):
    '''
    Returns the course start date as a datetime string.
    '''
    return course_entry['metadata']['start']


def get_end_date(course_entry):
    '''
    Returns the course end date as a datetime string.
    '''
    return course_entry['metadata']['end']
