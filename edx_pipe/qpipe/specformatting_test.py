#!/usr/bin/env python
'''Tester for specformatting functions
'''
import unittest
import specformatting

from helperclasses import ModuleURI, CourseURL


class SpecFormattingTest(unittest.TestCase):
    '''Tester for specformatting functions
    '''

    def test_format_i4x(self):
        '''Simple test coverage for format_i4x function. Should
        not override an already existing module field in a raw_event.
        '''

        # First check that an existing module field has not been overwritten.
        raw_event = {
            'event_type':
            '/courses/MITx/6.002x/2013_Spring/modx/i4x://MITx/6.002x/problem/H9P3_Designing_a_Shock_Absorber/problem_check',
            'module':
            'do not override me!'
        }
        specformatting.format_i4x(raw_event)
        self.assertEqual('i4x_problem_problem_check', raw_event['event_type'])
        self.assertEqual('do not override me!', raw_event['module'])

        # Now check that a missing module field has been instantiated.
        raw_event = {
            'event_type':
            '/courses/MITx/6.002x/2013_Spring/modx/i4x://MITx/6.002x/problem/H9P3_Designing_a_Shock_Absorber/problem_check'
        }

        module = ModuleURI(raw_event['event_type'])
        specformatting.format_i4x(raw_event)
        self.assertEqual('i4x_problem_problem_check', raw_event['event_type'])
        self.assertEqual(module, raw_event['module'])

    def test_format_url_change(self):
        '''Simple test coverage for format_url_change function. Since format_url_change
        partially acts as a wrapper around instantiating a CourseURL, the accuracy
        of the instantiation is left to the CourseURL tests.
        '''
        raw_event = {
            'event_type':
            '/courses/MITx/2.01x/2013_Spring/discussion/threads/519396f592634c1000000036/delete'
        }
        url = CourseURL(CourseURL.DEFAULT_DOMAIN + raw_event['event_type'])
        specformatting.format_url_change(raw_event)
        self.assertEqual(url, raw_event['page'])
        self.assertEqual('url_change', raw_event['event_type'])

    def test_format_seq(self):
        '''Simple test coverage for format_seq function. On an empty goto_dest field
        the raw event should be left unmodified. Since format_seq is partially a
        wrapper around the set_seq function in CourseURL the accuracy of the
        set_seq function is left to the CouresURL tests.
        '''
        url = CourseURL(
            'https://edx.org/MITx/6.002x/2013_Spring/courseware/c340d2/ff5b301/'
        )

        # First check that a raw event is properly left unmodified on
        # an empty goto_dest field.
        raw_event = {'event_type': 'seq_goto', 'goto_dest': '', 'page': url}
        raw_event_copy = raw_event.copy()
        specformatting.format_seq(raw_event)
        self.assertEqual(raw_event, raw_event_copy)

        # Now check for seq formatting.
        raw_event = {'event_type': 'seq_goto', 'goto_dest': '3', 'page': url}
        url_answer = CourseURL(
            'https://edx.org/MITx/6.002x/2013_Spring/courseware/c340d2/ff5b301/'
        )
        url_answer.set_seq(raw_event['goto_dest'])
        raw_event_answer = raw_event.copy()
        raw_event_answer['page'] = url_answer

        specformatting.format_seq(raw_event)
        self.assertEqual(raw_event_answer, raw_event)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(SpecFormattingTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
