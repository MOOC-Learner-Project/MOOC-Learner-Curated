#!/usr/bin/env python
'''
Tester for ClickEventsManager
'''
import os
import tempfile
import unittest

from events import Event, VideoInteraction
from helperclasses import CourseURL, ModuleURI
from moocdb import MOOCdb
from clickevents import ClickEventsManager


class ClickEventsManagerTest(unittest.TestCase):
    '''
    Tester for ClickEventsManager
    '''

    def test_play_video_MITx_csv_output(self):
        '''Tests click_events.csv output for the play_video event.
        '''
        event = VideoInteraction({
            '_id':
                'a',
            'anon_screen_name':
                'play_anonymous',
            'course_display_name':
                'org/course/run',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2013-08-13 19:47:47.451372',
            'event_type':
                'play_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/play/video'),
            'video_code':
                'abcd1234',
            'video_current_time':
                '0',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_load_video_MITx_csv_output(self):
        '''Tests click_events.csv output for the load_video event.
        '''
        event = VideoInteraction({
            '_id':
                'b',
            'anon_screen_name':
                'load_anonymous',
            'course_display_name':
                'org/course/run',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2013-08-13 19:03:04',
            'event_type':
                'load_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/load/video'),
            'video_code':
                'bcde2345',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_pause_video_MITx_csv_output(self):
        '''Tests click_events.csv output for the pause_video event.
        '''
        event = VideoInteraction({
            '_id':
                'c',
            'anon_screen_name':
                'pause_anonymous',
            'course_display_name':
                'org/course/run',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2013-08-11 11:03:47',
            'event_type':
                'pause_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/pause/video'),
            'video_code':
                'cdef3456',
            'video_current_time':
                '21.055',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_stop_video_MITx_csv_output(self):
        '''Tests click_events.csv output for the stop_video event.
        '''
        event = VideoInteraction({
            '_id':
                'd',
            'anon_screen_name':
                'stop_anonymous',
            'course_display_name':
                'org/course/run',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2013-06-13 07:03:04',
            'event_type':
                'stop_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/stop/video'),
            'video_code':
                'defg4567',
            'video_current_time':
                '133.812',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_seek_video_MITx_csv_output(self):
        '''Tests click_events.csv output for the seek_video event.
        '''
        event = VideoInteraction({
            '_id':
                'h',
            'anon_screen_name':
                'seek_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2013-12-02 18:44:40',
            'event_type':
                'seek_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/seek/video'),
            'video_code':
                'hijk8901',
            'video_current_time':
                '',
            'video_new_time':
                '330',
            'video_old_time':
                '293.24',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_speed_change_video_MITx_csv_output(self):
        '''Tests click_events.csv output for the speed_change_video event.
        '''
        event = VideoInteraction({
            '_id':
                'g',
            'anon_screen_name':
                'speed_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2013-11-06 18:45:25',
            'event_type':
                'speed_change_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/speed/change/video'),
            'video_code':
                'ghij7890',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '2',
            'video_old_speed':
                '1',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_hide_transcript_MITx_csv_output(self):
        '''Tests click_events.csv output for the hide_transcript event.
        '''
        event = VideoInteraction({
            '_id':
                'e',
            'anon_screen_name':
                'hide_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2014-06-09 01:16:48',
            'event_type':
                'hide_transcript',
            'page':
                CourseURL('https://www.edx.org/courses/0/hide/transcript'),
            'video_code':
                'efgh5678',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_show_transcript_MITx_csv_output(self):
        '''Tests click_events.csv output for the show_transcript event.
        '''
        event = VideoInteraction({
            '_id':
                'f',
            'anon_screen_name':
                'show_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2013-11-06 18:45:25',
            'event_type':
                'show_transcript',
            'page':
                CourseURL('https://www.edx.org/courses/0/show/transcript'),
            'video_code':
                'fghi6789',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_video_hide_cc_menu_MITx_csv_output(self):
        '''Tests click_events.csv output for the video_hide_cc_menu event.
        '''
        event = VideoInteraction({
            '_id':
                'f',
            'anon_screen_name':
                'show_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2013-11-06 18:45:25',
            'event_type':
                'video_hide_cc_menu',
            'page':
                CourseURL('https://www.edx.org/courses/0/show/transcript'),
            'video_code':
                'fghi6789',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_video_show_cc_menu_MITx_csv_output(self):
        '''Tests click_events.csv output for the video_show_cc_menu event.
        '''
        event = VideoInteraction({
            '_id':
                'f',
            'anon_screen_name':
                'show_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI('i4x://play/video/uri'),
            'time':
                '2013-11-06 18:45:25',
            'event_type':
                'video_show_cc_menu',
            'page':
                CourseURL('https://www.edx.org/courses/0/show/transcript'),
            'video_code':
                'fghi6789',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'MITx')

    def test_play_video_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the play_video event.
        '''
        event = VideoInteraction({
            '_id':
                'a',
            'anon_screen_name':
                'play_anonymous',
            'course_display_name':
                'org/course/run',
            'module':
                ModuleURI(''),
            'time':
                '2013-08-13 19:47:47.451372',
            'event_type':
                'play_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/play/video'),
            'video_code':
                'abcd1234',
            'video_current_time':
                '0',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                'i4x-HKUSTx-COMP102x-video-a6a52021a087402fafa1bb717406b326',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def test_load_video_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the load_video event.
        '''
        event = VideoInteraction({
            '_id':
                'b',
            'anon_screen_name':
                'load_anonymous',
            'course_display_name':
                'org/course/run',
            'module':
                ModuleURI(''),
            'time':
                '2013-08-13 19:03:04',
            'event_type':
                'load_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/load/video'),
            'video_code':
                'bcde2345',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                'i4x-HKUSTx-COMP102x-video-2680e14cba5e43f488d9c9fc73e25cb9',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def test_pause_video_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the pause_video event.
        '''
        event = VideoInteraction({
            '_id':
                'c',
            'anon_screen_name':
                'pause_anonymous',
            'course_display_name':
                'org/course/run',
            'module':
                ModuleURI(''),
            'time':
                '2013-08-11 11:03:47',
            'event_type':
                'pause_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/pause/video'),
            'video_code':
                'cdef3456',
            'video_current_time':
                '21.055',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                'i4x-HKUSTx-COMP102x-video-04229dc8688948f0a98d18e2d1815282',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def test_stop_video_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the stop_video event.
        '''
        event = VideoInteraction({
            '_id':
                'd',
            'anon_screen_name':
                'stop_anonymous',
            'course_display_name':
                'org/course/run',
            'module':
                ModuleURI(''),
            'time':
                '2013-06-13 07:03:04',
            'event_type':
                'stop_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/stop/video'),
            'video_code':
                'defg4567',
            'video_current_time':
                '133.812',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                'i4x-HKUSTx-COMP102x-video-d86629a449b04f60bc822939efc0e832',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def test_seek_video_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the seek_video event.
        '''
        event = VideoInteraction({
            '_id':
                'h',
            'anon_screen_name':
                'seek_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI(''),
            'time':
                '2013-12-02 18:44:40',
            'event_type':
                'seek_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/seek/video'),
            'video_code':
                'hijk8901',
            'video_current_time':
                '',
            'video_new_time':
                '330',
            'video_old_time':
                '293.24',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                'i4x-HKUSTx-COMP102x-video-b3f8a32d52374496afc421e07e0aaf89',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def test_speed_change_video_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the speed_change_video event.
        '''
        event = VideoInteraction({
            '_id':
                'g',
            'anon_screen_name':
                'speed_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI(''),
            'time':
                '2013-11-06 18:45:25',
            'event_type':
                'speed_change_video',
            'page':
                CourseURL('https://www.edx.org/courses/0/speed/change/video'),
            'video_code':
                'ghij7890',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '2',
            'video_old_speed':
                '1',
            'video_id':
                '09e004c72f114843a7d50d32b723a741',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def test_hide_transcript_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the hide_transcript event.
        '''
        event = VideoInteraction({
            '_id':
                'e',
            'anon_screen_name':
                'hide_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI(''),
            'time':
                '2014-06-09 01:16:48',
            'event_type':
                'hide_transcript',
            'page':
                CourseURL('https://www.edx.org/courses/0/hide/transcript'),
            'video_code':
                'efgh5678',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                'ff00eb135e2d44fbb3d545fe12cd157e',
            'transcript_id':
                'ff00eb135e2d44fbb3d545fe12cd157e'
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def test_show_transcript_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the show_transcript event.
        '''
        event = VideoInteraction({
            '_id':
                'f',
            'anon_screen_name':
                'show_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI(''),
            'time':
                '2013-11-06 18:45:25',
            'event_type':
                'show_transcript',
            'page':
                CourseURL('https://www.edx.org/courses/0/show/transcript'),
            'video_code':
                'fghi6789',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                'b3f8a32d52374496afc421e07e0aaf89',
            'transcript_id':
                'b3f8a32d52374496afc421e07e0aaf89'
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def test_video_hide_cc_menu_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the video_hide_cc_menu event.
        '''
        event = VideoInteraction({
            '_id':
                'f',
            'anon_screen_name':
                'show_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI(''),
            'time':
                '2013-11-06 18:45:25',
            'event_type':
                'video_hide_cc_menu',
            'page':
                CourseURL('https://www.edx.org/courses/0/show/transcript'),
            'video_code':
                'fghi6789',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                '4dbe0f48a74547bb9d2ce3736e58c3ed',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def test_video_show_cc_menu_HKUSTx_csv_output(self):
        '''Tests click_events.csv output for the video_show_cc_menu event.
        '''
        event = VideoInteraction({
            '_id':
                'f',
            'anon_screen_name':
                'show_anonymous',
            'course_display_name':
                'course-v1:HKUSTx+EBA101x+3T2016',
            'module':
                ModuleURI(''),
            'time':
                '2013-11-06 18:45:25',
            'event_type':
                'video_show_cc_menu',
            'page':
                CourseURL('https://www.edx.org/courses/0/show/transcript'),
            'video_code':
                'fghi6789',
            'video_current_time':
                '',
            'video_new_time':
                '',
            'video_old_time':
                '',
            'video_new_speed':
                '',
            'video_old_speed':
                '',
            'video_id':
                'c636c61da1bd4951a1e76c9fb2ae4e96',
            'transcript_id':
                ''
        })
        self.check_equal_click_event(event, 'HKUSTx')

    def check_equal_click_event(self, event, specification):
        '''This is only used as a helper function within actual tests
        to assert event equivalence with a click event from a click_events.csv file.
        '''
        moocdb = MOOCdb(tempfile.gettempdir())
        click_events_manager = ClickEventsManager(moocdb)
        click_events_manager.record(event, {'video_id_spec': specification})
        moocdb.close()

        with open(os.path.join(tempfile.gettempdir(), 'click_events.csv'),
                  'r') as click_events_file:
            lines = click_events_file.read().splitlines()
            self.assertEqual(1, len(lines))
            for line in lines:
                self.assertEqual(
                    line.count(','), 12,
                    "Mismatched number of fields in line: %s" % line)
                (observed_event_id, course_id, user_id, video_id,
                 observed_event_timestamp, observed_event_type, url, code,
                 video_current_time, video_new_time, video_old_time,
                 video_new_speed, video_old_speed) = line.split(',')
                event_from_file = VideoInteraction({
                    '_id':
                        observed_event_id,
                    'anon_screen_name':
                        user_id,
                    'course_display_name':
                        course_id,
                    'module':
                        ModuleURI(video_id) if specification == 'MITx' else ModuleURI(''),
                    'time':
                        observed_event_timestamp,
                    'event_type':
                        observed_event_type,
                    'page':
                        CourseURL(url),
                    'video_code':
                        code,
                    'video_current_time':
                        video_current_time,
                    'video_new_time':
                        video_new_time,
                    'video_old_time':
                        video_old_time,
                    'video_new_speed':
                        video_new_speed,
                    'video_old_speed':
                        video_old_speed,
                    'video_id':
                        video_id if specification == 'HKUSTx'
                        else '',
                    'transcript_id':
                        video_id if specification == 'HKUSTx'
                                    and (observed_event_type == 'hide_transcript'
                                         or observed_event_type == 'show_transcript')
                        else ''
                })
                self.assertEqual(event, event_from_file)

        for name in moocdb.TABLES:
            os.remove(os.path.join(tempfile.gettempdir(), '%s.csv' % name))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(ClickEventsManagerTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
