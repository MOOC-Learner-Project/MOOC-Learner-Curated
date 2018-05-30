#!/usr/bin/env python
'''Tester for updateloc functions
'''

import unittest

from helperclasses import CourseURL
from updateloc import simple_update, update_seq, close_previous_page


class UpdateLocTest(unittest.TestCase):
    '''Tester for the updateloc functions
    '''

    def test_simple_update(self):
        '''Simple coverage test for the simple_update function.
        '''
        event = {
            'page':
            CourseURL(
                'https://edx.org/courses/Medicine/SciWrite/run/courseware/00000/87510/'
            )
        }

        self.assertEqual(
            CourseURL(
                'https://edx.org/courses/Medicine/SciWrite/run/courseware/00000/87510/'
            ), simple_update(event))

    def test_update_seq(self):
        '''Simple coverage test for the update_seqnum function.
        '''
        event = {
            'page':
            CourseURL(
                'https://edx.org/courses/Medicine/SciWrite/run/courseware/00000/87510/'
            ),
            'event_type':
            'seq_goto',
            'goto_dest':
            '3',
        }
        self.assertEqual(
            CourseURL(
                'https://edx.org/courses/Medicine/SciWrite/run/courseware/00000/87510/3/'
            ), update_seq(event))

    def test_close_previous_page(self):
        '''Simple coverage test for the close_previous_page function.
        '''

        event_page_equal_current_location = {
            'page':
            CourseURL(
                'https://edx.org/courses/Medicine/SciWrite/run/courseware/87510/'
            ),
            'event_type':
            'page_close',
            'current_location': (CourseURL(
                'https://edx.org/courses/Medicine/SciWrite/run/courseware/87510/'
            ), '')
        }
        self.assertEqual(
            None, close_previous_page(event_page_equal_current_location))

        event_page_notequal_current_location = {
            'page':
            CourseURL(
                'https://edx.org/courses/Medicine/SciWrite/run/courseware/87510/3/2/'
            ),
            'event_type':
            'page_close',
            'current_location': (CourseURL(
                'https://edx.org/courses/Medicine/SciWrite/run/courseware/87510/'
            ), '')
        }
        self.assertEqual(
            CourseURL(
                'https://edx.org/courses/Medicine/SciWrite/run/courseware/87510/'
            ), close_previous_page(event_page_notequal_current_location))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(UpdateLocTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
