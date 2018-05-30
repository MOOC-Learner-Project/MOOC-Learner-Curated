'''Click events related processing.
'''
from __future__ import print_function


class ClickEventsManager(object):
    '''
    Handles recording click event data into the proper
    moocdb table.
    '''
    CLICK_EVENT_TYPES = [
        'play_video', 'load_video', 'pause_video', 'stop_video',
        'seek_video', 'speed_change_video', 'hide_transcript', 'show_transcript',
        'video_hide_cc_menu', 'video_show_cc_menu'
    ]

    def __init__(self, moocdb):
        self.writer = moocdb.csv_writers['click_events']

    def record(self, event, cfg_open_edx_spec):
        '''
        Record the click event in the corresponding moocdb table if it matches
        one of the click event types.
        '''

        if event['event_type'] not in self.CLICK_EVENT_TYPES:
            return

        # The Click Event Table video_id is the event formatted video_id (see ModuleURI).
        # This needs to be grabbed from the raw_event data because the Event type converts
        # to a string before returning an accessed item.
        # The original video_id can be accessed as event['video_id']
        try:
            click_event_row = {
                'observed_event_id': event['_id'],
                'course_id': event['course_display_name'],
                'user_id': event['anon_screen_name'],
                'video_id': event.get_video_id()[cfg_open_edx_spec['video_id_spec']](),
                'observed_event_timestamp': event['time'],
                'observed_event_type': event['event_type'],
                'url': event.data['page'].url,
                'code': event.get_video_code(),
                'video_current_time': event['video_current_time'],
                'video_new_time': event['video_new_time'],
                'video_old_time': event['video_old_time'],
                'video_new_speed': event['video_new_speed'],
                'video_old_speed': event['video_old_speed']
            }
            self.writer.store(click_event_row)
        except KeyError as err:
            print("KeyError using key %s" % err)
            print("Event data is %s" % event.data)
