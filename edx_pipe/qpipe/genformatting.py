from __future__ import print_function

import httpagentparser
import helperclasses
import datetime
import re

# A place holder of timestamp format passing from config file
TIMESTAMP_FORMAT = []

def set_agent_os(raw_event):
    """ Parses the HTTP Agent header taken from the 'agent' field 
    of raw event, and sets 'agent' and 'os' fields."""
    os_and_agent = httpagentparser.simple_detect(raw_event['agent'])
    raw_event['os'] = os_and_agent[0]
    raw_event['agent'] = os_and_agent[1]


def format_url(raw_event):
    """ Instanciates a CourseURL object from the 'page' field """
    raw_event['page'] = helperclasses.CourseURL(raw_event['page'])


def parse_timestamp(raw_event):
    # Remove possible offset information
    # 2013-09-11T13:25:44.876729+00:00
    # 2013-09-11T13:25:44.876729
    timestamp = re.sub('\+.*$', '', raw_event['time'])

    for timestamp_format in TIMESTAMP_FORMAT:
        try:
            # Parse timestamp
            raw_event['time'] = datetime.datetime.strptime(timestamp,
                                                           timestamp_format)
            return

        except ValueError:
            # Attempt to parse with other timestamp format
            pass

    # If we got here that means we were unable to parse the timestamp correctly
    print(
        'ERROR: Could not parse event_id %s timestamp: %s using formats %s. '
        'Try adding a new timestamp format to in the configuration file.'
        % (raw_event['_id'], timestamp, TIMESTAMP_FORMAT))


def parse_problem_id(raw_event):
    '''Gives a consistent URI formatting to problem IDs.
    Example :
        i4x-MITx-6_002x-problem-H10P2_New_Impedances_10_1
      becomes:
        i4x://MITx/6.002x/problem/H10P2_New_Impedances/10/1/
    
    That way, URL hierarchy and problem hierarchy can be handled 
    similarly.
    '''

    if raw_event.get('answer_identifier', ''):
        problem_id = raw_event['answer_identifier']
    elif raw_event.get('problem_id', ''):
        problem_id = raw_event['problem_id']
    else:
        return
            
    raw_event['module'] = helperclasses.ModuleURI(problem_id)


def parse_video_id(raw_event):
    '''
    Video ID can either be found in 'video_id' or 
    'transcript_id' fields.
    '''
    if raw_event['video_id']:
        video_id = raw_event['video_id']
    elif raw_event['transcript_id']:
        video_id = raw_event['transcript_id']
    else:
        return
    raw_event['module'] = helperclasses.ModuleURI(video_id)


def parse_question_location(raw_event):
    if raw_event['question_location']:
        raw_event['module'] = helperclasses.ModuleURI(
            raw_event['question_location'])
