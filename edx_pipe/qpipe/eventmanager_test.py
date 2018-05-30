#!/usr/bin/env python
'''Tester for EventManager classes
'''

import unittest

import eventmanager
from events import Event
import genformatting


class EventManagerTest(unittest.TestCase):
    '''Tester for the EventManager class
    '''

    def test_stage_event(self):
        '''Simple coverage test to check that event staging is correct.
        In particular, check that the duration calculation is as expected.
        '''
        manager = eventmanager.EventManager()
        raw_events = [{
            '_id': '1',
            'anon_screen_name': 'A',
            'time': '2013-11-10 06:00:00'
        }, {
            '_id': '2',
            'anon_screen_name': 'B',
            'time': '2013-11-10 06:00:00'
        }, {
            '_id': '3',
            'anon_screen_name': 'A',
            'time': '2013-11-10 06:05:00'
        }, {
            '_id': '4',
            'anon_screen_name': 'B',
            'time': '2013-11-10 06:10:00'
        }, {
            '_id': '5',
            'anon_screen_name': 'A',
            'time': '2013-11-10 06:10:00'
        }]

        expected_answers = {
            '1': {
                'anon_screen_name': 'A',
                'duration': '5'
            },
            '2': {
                'anon_screen_name': 'B',
                'duration': '10'
            },
            '3': {
                'anon_screen_name': 'A',
                'duration': '5'
            }
        }

        for raw_event in raw_events:
            genformatting.TIMESTAMP_FORMAT = ['%Y-%m-%dT%H:%M:%S.%f',
                                              '%Y-%m-%dT%H:%M:%S',
                                              '%Y-%m-%d %H:%M:%S']
            genformatting.parse_timestamp(raw_event)
            event = Event(raw_event)
            ending_event = manager.stage_event(event)
            if ending_event:
                self.assertEqual(
                    expected_answers[ending_event['_id']]['anon_screen_name'],
                    ending_event['anon_screen_name'])
                self.assertEqual(
                    expected_answers[ending_event['_id']]['duration'],
                    str(ending_event.duration))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EventManagerTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
