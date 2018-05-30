#!/usr/bin/env python
'''Tester for genformatting functions
'''
import datetime
import unittest
import genformatting


class GenFormattingTest(unittest.TestCase):
    '''Tester for genformatting functions
    '''

    def test_set_agent_os(self):
        '''Simple test to check that agent and os fields are set
        after formatting. The tests belonging to the parsing library
        are responsible for maintaining the accuracy of the parsed os
        and agent data.
        '''
        raw_event = {
            'agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22'
        }
        genformatting.set_agent_os(raw_event)
        self.assertEqual('Windows 7', raw_event['os'])
        self.assertEqual('Chrome 25.0.1364.97', raw_event['agent'])

    def test_format_url(self):
        '''Simple test of the format url function. Since
        it merely acts as a wrapper to instantiate a CourseURL
        object the accuracy of the instantiation is left to
        independent CourseURL tests.
        '''
        raw_event = {'page': 'https://www.edx.org/3/2/5'}
        genformatting.format_url(raw_event)
        self.assertEqual('https://www.edx.org/3/2/5/', raw_event['page'].url)

    def test_parse_timestamp(self):
        '''Simple test coverage of timestamp parser.
        '''

        test_datetimes = {
            '2013-09-11T13:25:44.876729+00:00':
            datetime.datetime(2013, 9, 11, 13, 25, 44, 876729),
            '2013-02-22T13:13:31.323646':
            datetime.datetime(2013, 2, 22, 13, 13, 31, 323646),
            '2013-04-15T12:59:10':
            datetime.datetime(2013, 4, 15, 12, 59, 10),
            '2013-04-16 02:35:54':
            datetime.datetime(2013, 4, 16, 2, 35, 54)
        }
        for timestamp_string, datetime_answer in test_datetimes.iteritems():
            raw_event = {'time': timestamp_string}
            genformatting.TIMESTAMP_FORMAT = ['%Y-%m-%dT%H:%M:%S.%f',
                                              '%Y-%m-%dT%H:%M:%S',
                                              '%Y-%m-%d %H:%M:%S']
            genformatting.parse_timestamp(raw_event)
            self.assertEqual(datetime_answer, raw_event['time'])

    def test_parse_problem_id(self):
        '''Simple test coverage of problem id parser. Note that
        the problem id can come from both the answer_identifier or
        problem_id fields of the raw event. parse_problem_id is a
        wrapper to instantiate a ModuleURI object so the accuracy
        of the instantiation is left to independent ModuleURI tests.
        '''
        answer_problem_id = 'i4x://MITx/6.002x/problem/H10P2_New_Impedances/10/1/'
        raw_event = {
            'answer_identifier':
            'i4x-MITx-6_002x-problem-H10P2_New_Impedances_10_1',
            'problem_id':
            ''
        }
        genformatting.parse_problem_id(raw_event)
        self.assertEqual(answer_problem_id, raw_event['module'].get_uri())

        raw_event = {
            'answer_identifier': '',
            'problem_id': 'i4x-MITx-6_002x-problem-H10P2_New_Impedances_10_1'
        }
        genformatting.parse_problem_id(raw_event)
        self.assertEqual(answer_problem_id, raw_event['module'].get_uri())

        raw_event = {
            'problem_id': 'i4x-MITx-6_002x-problem-H10P2_New_Impedances_10_1'
        }
        genformatting.parse_problem_id(raw_event)
        self.assertEqual(answer_problem_id, raw_event['module'].get_uri())

        raw_event = {
            'problem_id': ''
        }
        genformatting.parse_problem_id(raw_event)
        self.assertNotIn('module', raw_event.keys())

        raw_event = {
            'answer_identifier': '',
        }
        genformatting.parse_problem_id(raw_event)
        self.assertNotIn('module', raw_event.keys())

    def test_parse_video_id(self):
        '''Simple test coverage of problem id parser. Note that
        the video id can come from both the video_id or
        transcript_id fields of the raw event. parse_video_id is a
        wrapper to instantiate a ModuleURI object so the accuracy
        of the instantiation is left to independent ModuleURI tests.
        '''
        answer_video_id = 'i4x://MITx/6.002x/video/S23V15_Buffer_circuit/'
        raw_event = {
            'transcript_id': 'i4x-MITx-6_002x-video-S23V15_Buffer_circuit',
            'video_id': ''
        }
        genformatting.parse_video_id(raw_event)
        self.assertEqual(answer_video_id, raw_event['module'].get_uri())

        raw_event = {
            'transcript_id': '',
            'video_id': 'i4x-MITx-6_002x-video-S23V15_Buffer_circuit'
        }
        genformatting.parse_video_id(raw_event)
        self.assertEqual(answer_video_id, raw_event['module'].get_uri())

    def test_parse_question_location(self):
        '''Test coverage of the question location parser. This appears
        to override all other module instantiations if the field is non-empty.
        '''

        # First check that the raw_event module field is not overridden
        # when the question_location field is empty.
        raw_event = {'module': 'do not override me!', 'question_location': ''}
        genformatting.parse_question_location(raw_event)
        self.assertEqual('do not override me!', raw_event['module'])

        # Now check that the module field has been overridden when
        # the question_location field is not empty.
        raw_event = {
            'module':
            'override me!',
            'question_location':
            '/courses/MITx/6.002x/2013_Spring/modx/i4x://MITx/6.002x/problem/Op_Amps/problem_get'
        }
        genformatting.parse_question_location(raw_event)
        self.assertEqual('i4x://MITx/6.002x/problem/Op_Amps/',
                         raw_event['module'].get_uri())


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(GenFormattingTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
