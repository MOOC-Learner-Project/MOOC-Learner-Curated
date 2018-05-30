#!/usr/bin/env python
'''Tester for the EventFormatter class
'''

import unittest
import tempfile
import os
from eventformatter import EventFormatter
from moocdb import MOOCdb
import events
import specformatting
import inheritloc
import updateloc


class EventFormatterTest(unittest.TestCase):
    '''Tester for the EventFormatter class.
    '''

    def setUp(self):
        self.moocdb = MOOCdb(tempfile.gettempdir())
        timestamp_format = ['%Y-%m-%dT%H:%M:%S.%f',
                            '%Y-%m-%dT%H:%M:%S',
                            '%Y-%m-%d %H:%M:%S']
        self.eventformatter = EventFormatter(self.moocdb,
                                             TIMESTAMP_FORMAT=timestamp_format)

    def tearDown(self):
        self.moocdb.close()
        for name in self.moocdb.TABLES:
            os.remove(os.path.join(tempfile.gettempdir(), '%s.csv' % name))

    def test_pass_filter(self):
        '''Full coverage test for the pass_filter method.
        '''
        for event_type in self.eventformatter.pass_filter_regexes:
            self.assertEqual(False,
                             self.eventformatter.pass_filter({
                                 'event_type':
                                 event_type
                             }))

    '''
    do_generic_formatting and do_specific_formatting are just wrappers
    for methods in genformatting.py and specformatting.py which have their
    own respective test harnesses. However, testing that the correct specific
    formatting function is delegated to a particular event type is important.
    '''

    def test_get_specific_formatting_func_seq(self):
        '''Test the Course Navigation Events are delegated
        to the appropriate specific formatting function.
        '''
        for event_type in ['seq_goto', 'seq_next', 'seq_prev']:
            raw_event = {'event_type': event_type}
            self.assertEqual(
                specformatting.format_seq,
                self.eventformatter.get_specific_formatting_func(raw_event))

    def test_get_specific_formatting_func_i4x(self):
        '''Test the i4x events are delegated
        to the appropriate specific formatting function.
        '''
        i4x_event_types = [
            '/courses/org/course/run/modx/i4x://org/course/problem/E0_12/problem_reset',
            '/courses/org/course/run/xqueue/127929/i4x://org/course/problem/E0_7/score_update',
            '/courses/org/course/run/submission_history/abcd/i4x://org/course/problem/Q1_2_2'
            '/courses/org/course/run/jump_to/i4x://org/course/discussion/discussion_09a58a8b612c'
        ]
        for event_type in i4x_event_types:
            raw_event = {'event_type': event_type}
            self.assertEqual(
                specformatting.format_i4x,
                self.eventformatter.get_specific_formatting_func(raw_event))

    def test_get_specific_formatting_func_url(self):
        '''Test the URL change events are delegated
        to the appropriate specific formatting function.
        '''
        url_event_types = [
            '/courses/org/course/run/xblock/i4x:;_;_org;_course;_problem;_R6_2/handler/xmodule_handler/problem_check',
        ]
        for event_type in url_event_types:
            raw_event = {'event_type': event_type}
            self.assertEqual(
                specformatting.format_url_change,
                self.eventformatter.get_specific_formatting_func(raw_event))

    '''
    inherit_location is partially a wrapper for methods in inheritloc.py which has its own
    test harness. However, testing that the correct inherit location function is delegated
    to a particular event type is important.
    '''

    def test_get_inherit_location_func(self):
        '''Test that events are delegated to the appropriate
        inherit location functions.
        '''
        raw_event = {'page': ''}
        self.assertEqual(
            inheritloc.no_url,
            self.eventformatter.get_inherit_location_func(raw_event))

        courseware_pages = [
            '/courses/org/course/run/courseware/4_ThingB_IV/Problemset4/hw4_1_1b_patched.png',
            '/courses/org/course/run/courseware/4_ThingB_IV/Problemset4/006f.png',
            '/courses/org/course/run/courseware/2_ThingA_II/2_Recitation/005d.png',
        ]
        for page in courseware_pages:
            raw_event = {'page': page}
            self.assertEqual(
                inheritloc.inherit_seqnum,
                self.eventformatter.get_inherit_location_func(raw_event))

    '''
    update_location is partially a wrapper for methods in updateloc.py which has its own
    test harness. However, testing that the correct update location function is delegated
    to a particular event type is important.
    '''

    def test_get_update_location_func(self):
        '''Test that events are delegated to the appropriate
        update location functions.
        '''
        raw_event = {'event_type': 'page_close'}
        self.assertEqual(
            updateloc.close_previous_page,
            self.eventformatter.get_update_location_func(raw_event))

        for event_type in ['seq_goto', 'seq_next', 'seq_prev']:
            raw_event = {'event_type': event_type}
            self.assertEqual(
                updateloc.update_seq,
                self.eventformatter.get_update_location_func(raw_event))

        raw_event = {'event_type': 'anything_else'}
        self.assertEqual(
            updateloc.simple_update,
            self.eventformatter.get_update_location_func(raw_event))

    '''
    instanciate_event is partially a wrapper for class instanciation functions in events.py
    which has its own test harness. However, testing that the correct instanciation function
    is delegated to a particular event type is important.
    '''

    def test_get_instanciate_event_func_video_interaction(self):
        '''Test that VideoInteraction events are delegated to the appropriate
        instanciate event functions.
        '''

        video_interaction_event_types = [
            'play_video', 'stop_video', 'pause_video', 'seek_video',
            'load_video', 'speed_change_video', 'fullscreen', 'not_fullscreen',
            'hide_transcript', 'show_transcript', 'video_hide_cc_menu',
            'video_show_cc_menu'
        ]
        for event_type in video_interaction_event_types:
            raw_event = {'event_type': event_type}
            self.assertEqual(
                events.VideoInteraction,
                self.eventformatter.get_instanciate_event_func(raw_event))

    def test_get_instanciate_event_func_pdf_interaction(self):
        '''Test that PdfInteraction events are delegated to the appropriate
        instanciate event functions.
        '''

        pdf_interaction_event_types = ['book']
        for event_type in pdf_interaction_event_types:
            raw_event = {'event_type': event_type}
            self.assertEqual(
                events.PdfInteraction,
                self.eventformatter.get_instanciate_event_func(raw_event))

    def test_get_instanciate_event_func_problem_interaction(self):
        '''Test that ProblemInteraction events are delegated to the appropriate
        instanciate event functions.
        '''

        problem_interaction_event_types = [
            'problem_check', 'problem_check_fail', 'problem_reset',
            'reset_problem', 'problem_save', 'problem_show', 'showanswer',
            'save_problem_fail', 'save_problem_success', 'problem_graded',
            'i4x_problem_input_ajax', 'i4x_problem_problem_check',
            'i4x_problem_problem_get', 'i4x_problem_problem_reset',
            'i4x_problem_problem_save', 'i4x_problem_problem_show'
        ]
        for event_type in problem_interaction_event_types:
            raw_event = {'event_type': event_type}
            self.assertEqual(
                events.ProblemInteraction,
                self.eventformatter.get_instanciate_event_func(raw_event))

    def test_get_instanciate_event_func_open_response_assessment(self):
        '''Test that OpenResponseAssessment events are delegated to the appropriate
        instanciate event functions.
        '''

        open_response_assessment_event_types = [
            'oe_hide_question', 'oe_show_question', 'rubric_select',
            'i4x_combinedopenended_some_action', 'peer_grading_some_action',
            'staff_grading_some_action', 'i4x_peergrading_some_action'
        ]
        for event_type in open_response_assessment_event_types:
            raw_event = {'event_type': event_type}
            self.assertEqual(
                events.OpenResponseAssessment,
                self.eventformatter.get_instanciate_event_func(raw_event))

    def test_get_instanciate_event_func_navigational(self):
        '''Test that Navigational events are delegated to the appropriate
        instanciate event functions.
        '''

        navigational_event_types = ['seq_goto', 'seq_prev', 'seq_next']
        for event_type in navigational_event_types:
            raw_event = {'event_type': event_type}
            self.assertEqual(
                events.Navigational,
                self.eventformatter.get_instanciate_event_func(raw_event))

    def test_get_instanciate_event_func_generic(self):
        '''Test that other events without a specific handler are delegated
        to the appropriate instanciate event function. That is, all other
        events should be delegated to the Event base class.
        '''
        raw_event = {'event_type': 'generic_anything'}
        self.assertEqual(
            events.Event,
            self.eventformatter.get_instanciate_event_func(raw_event))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EventFormatterTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
