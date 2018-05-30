#!/usr/bin/env python
'''
vismooc extensions module to extract the videos and course_video data
from the Edx course_structure json file.
'''
import courses
import util

def write_video_csvs(dictionary, course_video_path, videos_path):
    '''
    Write the course_video and videos csvs out to course_video_path
    and videos_path respectively,
    according to the dictionary representing the loaded
    {org}-{course}-{run}-course_structure-{site}-analytics.json file.

    This serves largely as a wrapper around util.write_simple_csv
    '''
    video_id_set = get_video_id_set(dictionary)

    util.write_simple_csv(video_id_set, course_video_path,
                          get_course_video_csv_fields(),
                          get_course_video_csv_field_to_func_map(dictionary))
    util.write_simple_csv(video_id_set, videos_path,
                          get_videos_csv_fields(),
                          get_videos_csv_field_to_func_map(dictionary))


def get_course_video_csv_fields():
    '''
    Return the csv fields for the courses_video table.
    '''
    return ['_id', 'course_id', 'video_id']


def get_videos_csv_fields():
    '''
    Return the csv fields for the courses_video table.
    '''
    return ['_id', 'original_id', 'name', 'section', 'description', 'url']


def get_course_video_csv_field_to_func_map(dictionary):
    '''
    Returns a map of the course_video output csv field
    to a function that takes a single argument which is a string.

    Most of the functions will simply pull the desired value straight out
    of the dict argument but this design is chosen to provide flexibility
    in performing post-processing on the values contained in the dict
    argument should the schema mappings change, while still separating
    the boilerplate work of dumping the final values out to a csv. The
    boilerplate work is left to util.write_simple_csv.
    '''
    course_id = courses.get_original_id(dictionary)
    return {
        '_id': lambda video_id: str(util.get_id(video_id)),
        'course_id': lambda _: course_id,
        'video_id': lambda video_id: video_id
    }


def get_videos_csv_field_to_func_map(dictionary):
    '''
    Returns a map of the videos output csv field
    to a function that takes a single argument which is a string.

    Most of the functions will simply pull the desired value straight out
    of the dict argument but this design is chosen to provide flexibility
    in performing post-processing on the values contained in the dict
    argument should the schema mappings change, while still separating
    the boilerplate work of dumping the final values out to a csv. The
    boilerplate work is left to util.write_simple_csv.
    '''
    video_id_to_section_map = get_video_id_to_section_map(dictionary)
    return {
        '_id': lambda video_id: str(util.get_id(video_id)),
        'original_id': lambda video_id: video_id,
        'name':
        lambda video_id: dictionary[video_id]['metadata']['display_name'],
        'section': lambda video_id: video_id_to_section_map[video_id],
        'description': lambda _: '',
        'url': lambda video_id: get_url(dictionary, video_id)
    }


def get_url(dictionary, video_id):
    '''
    Returns the url corresponding to the video_id if it is available.
    Returns an empty string otherwise.
    '''
    html_sources = dictionary[video_id]['metadata']['html5_sources']
    if len(html_sources) > 0:
        return html_sources[0]
    return ''


def get_video_id_set(dictionary):
    '''
    Returns the set of all the video_ids in the course_structure
    dictionary argument.
    '''
    video_id_set = set()
    for (key, entry) in dictionary.iteritems():
        if entry['category'] == 'video':
            video_id_set.add(key)
    return video_id_set


def get_video_id_to_section_map(dictionary):
    '''
    Returns a map from a video_id to the section string.
    '''
    video_id_to_section = {}
    course_entry_key = courses.get_course_entry_key(dictionary)
    course_block = dictionary[course_entry_key]
    for (idx, val) in enumerate(course_block['children']):
        video_id_to_section.update(
            build_video_id_to_section_map(dictionary, val, '%d>>' % idx))
    return video_id_to_section


def build_video_id_to_section_map(dictionary, key, string):
    '''
    This is a helper function to build the video_id to section
    map for the videos table.
    '''
    video_id_to_section = {}
    block = dictionary[key]
    if 'metadata' not in block:
        return {}
    if 'display_name' not in block['metadata']:
        return {}
    display_name = block['metadata']['display_name']
    next_string = string + '%s>>' % display_name
    for (idx, val) in enumerate(block['children']):
        video_id_to_section.update(
            build_video_id_to_section_map(dictionary, val, next_string + '%d>>'
                                          % idx))
    if block['category'] == 'video':
        video_id_to_section[key] = next_string
    return video_id_to_section
