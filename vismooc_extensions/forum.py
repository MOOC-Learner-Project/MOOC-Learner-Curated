#!/usr/bin/env python
'''
vismooc extensions module to extract the forum
data from the forum.mongo file.
'''
import datetime
import json
import dateutil.parser
import util

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def write_forum_csv(edx_forum_path, output_path):
    '''
    Write the forum csv out to the given output_path,
    according to the forum.mongo file.

    This serves largely as a wrapper around write_simple_csv but handles
    loading the forum.mongo file from disk.
    '''
    with open(edx_forum_path, 'r') as edx_forum_file:
        json_strings = edx_forum_file.read().splitlines()
        forum_entries = [json.loads(s) for s in json_strings]
        util.write_simple_csv(forum_entries, output_path,
                              get_csv_fields(), get_csv_field_to_func_map())


def get_csv_fields():
    '''
    Return the csv fields for the forum table.
    '''
    return [
        '_id', 'original_id', 'course_id', 'author_id', 'created_at',
        'updated_at', 'body', 'type', 'title', 'thread_type',
        'comment_thread_id', 'parent_id'
    ]


def get_csv_field_to_func_map():
    '''
    Returns a map of an output csv field to a function that takes a single
    argument which is a user row (dict object).

    Most of the functions will simply pull the desired value striaght out
    of the dict argument but this design is chosen to provide flexibility
    in performing post-processing on the values contained in the dict
    argument should the schema mappings change, while still separating
    the boilerplate work of dumping the final values out to a csv. The
    boilerplate work is left to util.write_simple_csv.
    '''
    return {
        '_id': lambda forum_entry: util.get_id(forum_entry),
        'original_id': lambda forum_entry: forum_entry['_id']['$oid'],
        'course_id': lambda forum_entry: forum_entry['course_id'],
        'author_id': lambda forum_entry: forum_entry['author_id'],
        'created_at': get_created_at_date,
        'updated_at': get_updated_at_date,
        # body fields can contain unicode not encodable by ascii,
        # so it must be encoded to utf-8 to avoid a UnicodeEncodeError.
        'body': lambda forum_entry: forum_entry['body'].encode('utf-8'),
        'type': lambda forum_entry: forum_entry['_type'],
        'title': get_title,
        'thread_type': get_thread_type,
        'comment_thread_id': get_comment_thread_id,
        'parent_id': get_parent_id
    }


def get_created_at_date(forum_entry):
    '''
    Returns the forum entry created_at date in unix time as an int.
    Embedded in the created_at field,
    $date is a unix timestamp given in milliseconds OR an ISO8601 timestamp.
    '''
    if isinstance(forum_entry['created_at']['$date'], int):
        return datetime.datetime.fromtimestamp(
            long(forum_entry['created_at']['$date']) /
            1000).strftime(DATETIME_FORMAT)

    return dateutil.parser.parse(
        forum_entry['created_at']['$date']).strftime(DATETIME_FORMAT)


def get_updated_at_date(forum_entry):
    '''
    Returns the forum entry updated_at date as a string formatted by DATETIME_FORMAT.
    Embedded in the updated_at field,
    $date is a unix timestamp given in millseconds OR an ISO8601 timestamp.
    '''
    if isinstance(forum_entry['updated_at']['$date'], int):
        return datetime.datetime.fromtimestamp(
            long(forum_entry['updated_at']['$date']) /
            1000).strftime(DATETIME_FORMAT)

    return dateutil.parser.parse(
        forum_entry['updated_at']['$date']).strftime(DATETIME_FORMAT)


def get_title(forum_entry):
    '''
    Returns the forum entry title if the forum entry is of type 'CommentThread'.
    Otherwise it returns an empty string.

    If for some reason the title field still cannot be found an empty string is
    returned instead.

    title fields can contain unicode not encodable by ascii,
    so it must be encoded to utf-8 to avoid a UnicodeEncodeError.
    '''
    if forum_entry['_type'] == 'CommentThread':
        if 'title' in forum_entry:
            return forum_entry['title'].encode('utf-8')
    return ''


def get_thread_type(forum_entry):
    '''
    Returns the forum entry thread_type if the forum entry is of type 'CommentThread'.
    Otherwise it returns an empty string.

    thread_type was added in 4 Sep 2014 old Edx course data will not have this field.
    In this scenario an empty string is returned.
    '''
    if forum_entry['_type'] == 'CommentThread':
        if 'thread_type' in forum_entry:
            return forum_entry['thread_type']
    return ''


def get_comment_thread_id(forum_entry):
    '''
    Returns the forum entry comment_thread_id if the forum entry is of type 'Comment'.
    Otherwise it returns an empty string.

    If for some reason the comment_thread_id field still cannot be found an empty string
    is returned instead.
    '''
    if forum_entry['_type'] == 'Comment':
        if 'comment_thread_id' in forum_entry:
            return forum_entry['comment_thread_id']['$oid']
    return ''


def get_parent_id(forum_entry):
    '''
    Returns the forum entry parent_id if the forum entry is of type 'Comment' and is
    a reply to another forum entry of type 'Comment'.
    Otherwise it returns an empty string.
    '''
    if forum_entry['_type'] == 'Comment':
        if 'parent_id' in forum_entry:
            return forum_entry['parent_id']['$oid']
    return ''
