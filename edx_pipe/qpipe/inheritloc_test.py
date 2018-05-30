#!/usr/bin/env python
'''Tester for inheritloc functions
'''

import unittest

from helperclasses import CourseURL
from inheritloc import no_url, inherit_seqnum


class InheritLocTest(unittest.TestCase):
    '''Tester for the inheritloc functions
    '''

    def test_no_url_no_inheritance(self):
        '''Test the no_url function with an event that
        should not inherit a url.
        '''
        event = {
            'current_location':
            (CourseURL('http://a/b/'), '2013-11-10 06:43:41'),
            'time': '2013-12-10 06:44:00',
            'page': ''
        }
        expected_event = {
            'current_location':
            (CourseURL('http://a/b/'), '2013-11-10 06:43:41'),
            'time': '2013-12-10 06:44:00',
            'page': '',
            'inherited': ''
        }

        no_url(event)
        self.assertEqual(expected_event, event)

    def test_no_url_yes_inheritance(self):
        '''Test the no_url function with an event that
        should inherit a url.
        '''
        event = {
            'current_location': (CourseURL(
                'https://edx.edu/courses/Medicine/SciWrite/run/courseware/c340d5/ff5b3/3/'
            ), '2013-11-10 06:43:41'),
            'time':
            '2013-12-10 06:44:00',
            'page':
            ''
        }
        expected_event = {
            'current_location': (CourseURL(
                'https://edx.edu/courses/Medicine/SciWrite/run/courseware/c340d5/ff5b3/3/'
            ), '2013-11-10 06:43:41'),
            'time':
            '2013-12-10 06:44:00',
            'page':
            CourseURL(
                'https://edx.edu/courses/Medicine/SciWrite/run/courseware/c340d5/ff5b3/3/'
            ),
            'inherited':
            'url'
        }

        no_url(event)
        self.assertEqual(expected_event, event)

    def test_inherit_seqnum(self):
        '''Test the inherit_seqnum function with an event
        that should inherit a sequence number.
        '''
        event = {
            'current_location': (CourseURL(
                'https://edx.edu/courses/Medicine/SciWrite/run/courseware/c340d5/ff5b3/3/'
            ), '2013-11-10 06:43:41'),
            'page':
            CourseURL(
                'https://edx.edu/courses/Medicine/SciWrite/run/courseware/c340d5/ff5b3/'
            )
        }
        expected_event = {
            'current_location': (CourseURL(
                'https://edx.edu/courses/Medicine/SciWrite/run/courseware/c340d5/ff5b3/3/'
            ), '2013-11-10 06:43:41'),
            'page':
            CourseURL(
                'https://edx.edu/courses/Medicine/SciWrite/run/courseware/c340d5/ff5b3/'
            ),
            'inherited':
            'seqnum'
        }
        expected_event['page'].set_seq(3)
        inherit_seqnum(event)
        self.assertEqual(expected_event, event)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(InheritLocTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
