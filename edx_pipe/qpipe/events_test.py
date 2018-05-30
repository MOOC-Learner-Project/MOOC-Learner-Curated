#!/usr/bin/env python
'''Tester for Event classes
'''

import unittest
import datetime
import events
import genformatting
from helperclasses import CourseURL, ModuleURI


class EventTest(unittest.TestCase):
    '''Tester for the common Event class
    '''

    def test_get_observed_event_row(self):
        '''Simple coverage test to check that mapping of event rows
        to moocdb observed event fields are correct or up-to-date.
        '''
        raw_event = {
            '_id': 'a',
            'anon_screen_name': 'b',
            'resource_id': 'c',
            'time': '2013-08-13 19:47:47.451372',
            'ip': '127.0.0.1',
            'os': 'TempleOS',
            'agent': 'Netscape',
            'event_type': 'd'
        }
        event = events.Event(raw_event)
        observed_event_row = {
            'observed_event_id': raw_event['_id'],
            'user_id': raw_event['anon_screen_name'],
            'url_id': raw_event['resource_id'],
            'observed_event_timestamp': raw_event['time'],
            'observed_event_duration': 0,
            'observed_event_ip': raw_event['ip'],
            'observed_event_os': raw_event['os'],
            'observed_event_agent': raw_event['agent'],
            'observed_event_type': raw_event['event_type'],
            'validity': 1
        }
        self.assertEqual(observed_event_row, event.get_observed_event_row())

    def test_set_data_attr(self):
        '''Simple coverage test to check the field setter method works correctly.
        The setter function should ignore any false types.
        '''
        event = events.Event({})
        event.set_data_attr('key', 'value')
        self.assertEqual('value', event['key'])
        event.set_data_attr('key', False)
        self.assertEqual('value', event['key'])
        event.set_data_attr('key', '')
        self.assertEqual('value', event['key'])
        event.set_data_attr('key', None)
        self.assertEqual('value', event['key'])

    def test_get_uri(self):
        '''Simple coverage test to check the get_uri method works under the
        following scenarios:
        - No page field set and no module (ModuleURI) field set.
        - page field set but no module (ModuleURI) field set.
        - No page field set but module (ModuleURI) field set.
        - page field set and module (ModuleURI) field set.
        '''
        event = events.Event({})
        self.assertEqual('https://unknown/', event.get_uri())
        event.set_data_attr('page', 'https://edx.org/')
        self.assertEqual('https://edx.org/', event.get_uri())

        event = events.Event({})
        event.set_data_attr(
            'module',
            ModuleURI(
                '/courses/MITx/1.111x/2010_Spring/modx/i4x://MITx/1.111x/problem/a/problem_get'
            ))
        self.assertEqual('https://unknown/problem/a/', event.get_uri())
        event.set_data_attr('page', 'https://edx.org/')
        self.assertEqual('https://edx.org/problem/a/', event.get_uri())

    def test_get_resource_display_name(self):
        '''Simple coverage test to check the get_resource_name method works under
        the following scenarios:
        - No resource_display_name field set but module (ModuleURI) is set
        - resource_display_name field set and module (ModuleURI) is set
        '''
        event = events.Event({})
        event.set_data_attr(
            'module',
            ModuleURI(
                '/courses/MITx/2.111x/2010_Spring/modx/i4x://MITx/2.111x/problem/a/problem_get'
            ))
        self.assertEqual('a', event.get_resource_display_name())
        event.set_data_attr('resource_display_name', 'display_name')
        self.assertEqual('display_name', event.get_resource_display_name())

    def test_set_duration(self):
        '''Simple coverage test to check the set_duration works under the following
        scenarios:
        - end_time > event['time'] and (end_time - event['time']) < MAX_DURATION_MINUTES
        - end_time > event['time'] and (end_time - event['time']) = MAX_DURATION_MINTUES
        - end_time > event['time'] and (end_time - event['time']) > MAX_DURATION_MINUTES
        - end_time = event['time']
        '''
        raw_event = {'_id': 'a', 'time': '2013-08-13T19:47:47.451372'}
        genformatting.TIMESTAMP_FORMAT = ['%Y-%m-%dT%H:%M:%S.%f',
                                          '%Y-%m-%dT%H:%M:%S',
                                          '%Y-%m-%d %H:%M:%S']
        genformatting.parse_timestamp(raw_event)
        start_time = raw_event['time']
        event = events.Event(raw_event)

        end_time = start_time + datetime.timedelta(minutes=(max(
            0, events.MAX_DURATION_MINUTES - 5)))
        duration = (end_time - raw_event['time']).seconds / 60
        event.set_duration(end_time)
        self.assertEqual(duration, event.duration)

        end_time = start_time + datetime.timedelta(
            minutes=events.MAX_DURATION_MINUTES)
        event.set_duration(end_time)
        self.assertEqual(events.MAX_DURATION_MINUTES, event.duration)

        end_time = start_time + datetime.timedelta(
            minutes=events.MAX_DURATION_MINUTES + 5)
        event.set_duration(end_time)
        self.assertEqual(events.DEFAULT_DURATION_MINUTES, event.duration)

        event.set_duration(start_time)
        self.assertEqual(0, event.duration)

    def test_do_no_stringify_nonetype(self):
        '''Ensure that when a field is not set, an event __getitem__ call returns None.
        In the translation project there is code resembling the following:

        if event['unset_field']:
            <conditional body>

        However, old implementations of the base Event class would stringify
        any __getitem__ calls which resulted in behavior where an unset field
        would return the string "None", which consequently led to conditional
        code like the aforementioned snippet always executing.
        '''
        event = events.Event({})
        self.assertEqual(None, event['unset_field'])


class VideoInteractionTest(unittest.TestCase):
    '''Tester for the VideoInteraction subclass
    '''

    def test_get_video_code(self):
        '''Simple coverage test to check that the get_video_code method works
        under the following scenarios:
        - video_code field set but no transcript_code field set
        - video_code field set and transcript_code field set
        - No video_code field set but transcript_code field set
        '''
        event = events.VideoInteraction({'video_code': 'a'})
        self.assertEqual('a', event.get_video_code())

        event = events.VideoInteraction({
            'video_code': 'b',
            'transcript_code': 'c'
        })
        self.assertEqual('b', event.get_video_code())

        event = events.VideoInteraction({'transcript_code': 'd'})
        self.assertEqual('d', event.get_video_code())

    def test_get_uri(self):
        '''Simple coverage test to check that the overridden get_uri method
        works when the page, module (ModuleURI), and video_code fields
        are set approprirately.
        '''
        event = events.VideoInteraction({
            'page':
            'https://edx.org/',
            'module':
            ModuleURI(
                '/courses/MITx/3.111x/2009_Spring/modx/i4x://MITx/3.111x/video/What_is_MATLAB/'
            ),
            'video_code':
            'OEoXabPEzfa'
        })
        self.assertEqual('https://edx.org/video/What_is_MATLAB/_OEoXabPEzfa',
                         event.get_uri())


class PdfInteractionTest(unittest.TestCase):
    '''Tester for the PdfInteraction subclass
    '''

    def test_get_page(self):
        '''Simple coverage test to check the get_page method works
        when the page (CourseURL) field and goto_dest field are set'''
        event = events.PdfInteraction({
            'page':
            CourseURL('https://edx.org/book/2/3'),
            'goto_dest':
            2
        })
        self.assertEqual('2', event.get_page())

    def test_set_page(self):
        '''Simple coverage test to check that the set_page method
        works when the page (CourseURL) field and goto_dest field are set
        '''
        event = events.PdfInteraction({
            'page':
            CourseURL('https://edx.org/book/2/3'),
            'goto_dest':
            4
        })
        event.set_page(1)
        self.assertEqual('1', event.get_page())


class ProblemInteractionTest(unittest.TestCase):
    '''Tester for the ProblemInteraction subclass
    '''

    def test_get_success(self):
        '''Check complete coverage for all supported correctness values
        '''
        event = events.ProblemInteraction({})
        event.set_data_attr('correctness', 'incorrect')
        self.assertEqual(0, event.get_success())
        event.set_data_attr('correctness', 'correct')
        self.assertEqual(1, event.get_success())
        event.set_data_attr('correctness', 'incomplete')
        self.assertEqual(-1, event.get_success())

    def test_get_is_submitted(self):
        '''Check complete coverage for all supported event types mapping
        to submission statuses.
        '''
        event = events.ProblemInteraction({})
        event.set_data_attr('event_type', 'problem_check')
        self.assertEqual(1, event.get_is_submitted())
        event.set_data_attr('event_type', 'problem_check_fail')
        self.assertEqual(2, event.get_is_submitted())
        event.set_data_attr('event_type', 'problem_graded')
        self.assertEqual(1, event.get_is_submitted())
        event.set_data_attr('event_type', 'i4x_problem_problem_check')
        self.assertEqual(1, event.get_is_submitted())
        event.set_data_attr('event_type', 'save_problem_check')
        self.assertEqual(1, event.get_is_submitted())
        event.set_data_attr('event_type', 'save_problem_success')
        self.assertEqual(0, event.get_is_submitted())
        event.set_data_attr('event_type', 'problem_save')
        self.assertEqual(0, event.get_is_submitted())
        event.set_data_attr('event_type', 'i4x_problem_problem_save')
        self.assertEqual(0, event.get_is_submitted())
        event.set_data_attr('event_type', 'save_problem_check_fail')
        self.assertEqual(2, event.get_is_submitted())
        event.set_data_attr('event_type', 'reset_problem')
        self.assertEqual(3, event.get_is_submitted())
        event.set_data_attr('event_type', 'reset_problem_fail')
        self.assertEqual(2, event.get_is_submitted())
        event.set_data_attr('event_type', 'problem_reset')
        self.assertEqual(3, event.get_is_submitted())
        event.set_data_attr('event_type', 'save_problem_fail')
        self.assertEqual(2, event.get_is_submitted())

    def test_get_submission_row(self):
        '''Simple coverage test for the get_submission_row method
        '''
        raw_event = {
            '_id': 'a',
            'event_type': 'problem_check',
            'anon_screen_name': 'b',
            'problem_id': 'c',
            'time': '2013-08-13T19:47:47.451372',
            'attempts': '3',
            'ip': 'USA',
            'os': 'TempleOS',
            'agent': 'Netscape',
            'answer': 'd',
        }
        genformatting.TIMESTAMP_FORMAT = ['%Y-%m-%dT%H:%M:%S.%f',
                                          '%Y-%m-%dT%H:%M:%S',
                                          '%Y-%m-%d %H:%M:%S']
        genformatting.parse_timestamp(raw_event)
        event = events.ProblemInteraction(raw_event)
        submission_row = {
            'submission_id': 'a',
            'user_id': 'b',
            'problem_id': 'c',
            'submission_timestamp': '2013-08-13 19:47:47.451372',
            'submission_attempt_number': '3',
            'submission_ip': 'USA',
            'submission_os': 'TempleOS',
            'submission_agent': 'Netscape',
            'submission_answer': 'd',
            'submission_is_submitted': 1,
            'validity': 1
        }
        self.assertEqual(submission_row, event.get_submission_row())

        raw_event = {
            '_id': 'a',
            'event_type': 'problem_check',
            'anon_screen_name': 'b',
            'problem_id': 'c',
            'time': '2013-08-13T19:47:47.451372',
            'attempts': '',
            'ip': 'USA',
            'os': 'TempleOS',
            'agent': 'Netscape',
            'answer': 'd',
        }
        genformatting.TIMESTAMP_FORMAT = ['%Y-%m-%dT%H:%M:%S.%f',
                                          '%Y-%m-%dT%H:%M:%S',
                                          '%Y-%m-%d %H:%M:%S']
        genformatting.parse_timestamp(raw_event)
        event = events.ProblemInteraction(raw_event)
        submission_row = {
            'submission_id': 'a',
            'user_id': 'b',
            'problem_id': 'c',
            'submission_timestamp': '2013-08-13 19:47:47.451372',
            'submission_attempt_number': '',
            'submission_ip': 'USA',
            'submission_os': 'TempleOS',
            'submission_agent': 'Netscape',
            'submission_answer': 'd',
            'submission_is_submitted': 1,
            'validity': 0
        }
        self.assertEqual(submission_row, event.get_submission_row(), "{} != {}".format(submission_row, event.get_submission_row()))

    def test_get_assessment_row(self):
        '''Simple coverage test for the get_assessment_row method
        '''
        raw_event = {
            '_id': 'a',
            'time': '2013-08-13T19:47:47.451372',
            'correctness': 'correct'
        }
        genformatting.TIMESTAMP_FORMAT = ['%Y-%m-%dT%H:%M:%S.%f',
                                          '%Y-%m-%dT%H:%M:%S',
                                          '%Y-%m-%d %H:%M:%S']
        genformatting.parse_timestamp(raw_event)
        event = events.ProblemInteraction(raw_event)
        assessment_row = {
            'assessment_grader_id': 'automatic',
            'assessment_timestamp': '2013-08-13 19:47:47.451372',
            'assessment_grade': 1,
            'submission_id': 'a',
            'assessment_id': 'a'
        }
        self.assertEqual(assessment_row, event.get_assessment_row())


class OpenResponseAssessmentTest(unittest.TestCase):
    '''Tester for the OpenResponseAssessment subclass
    '''

    def test_get_is_submitted(self):
        '''Check that -1 is always returned for the get_is_submitted
        method as this is not yet supported for OpenResponseAssessment
        '''
        event = events.OpenResponseAssessment({})
        self.assertEqual(-1, event.get_is_submitted())


    def test_get_success(self):
        '''Check that None is always returned for the get_success
        method as this is not yet supported for OpenResponseAssessment
        '''
        event = events.OpenResponseAssessment({})
        self.assertIsNone(event.get_success())


class NavigationalTest(unittest.TestCase):
    '''Tester for the Navigational subclass
    '''

    def test_get_uri(self):
        '''Simple coverage test for the get_uri method.
        Relative pathing should not be appended for these events.
        '''
        raw_event = {
            'sequence_id': 'a',
            'goto_dest': 2,
            'goto_from': 3,
            'page': CourseURL('https://edx.org/')
        }
        event = events.Navigational(raw_event)
        self.assertEqual('https://edx.org/', event.get_uri())


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EventTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)

    SUITE = unittest.TestLoader().loadTestsFromTestCase(VideoInteractionTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)

    SUITE = unittest.TestLoader().loadTestsFromTestCase(PdfInteractionTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)

    SUITE = unittest.TestLoader().loadTestsFromTestCase(ProblemInteractionTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)

    SUITE = unittest.TestLoader().loadTestsFromTestCase(
        OpenResponseAssessmentTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)

    SUITE = unittest.TestLoader().loadTestsFromTestCase(NavigationalTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
