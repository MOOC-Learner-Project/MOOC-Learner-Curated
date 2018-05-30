#!/usr/bin/env python
'''Tester for SubmissionManager
'''

import unittest
import submissions
import moocdb
import events


class SubmissionManagerTest(unittest.TestCase):
    '''Tester for the EventManager class
    '''

    def test_update_submissions_tables(self):
        '''Simple coverage test 
        
        TODO currently tests only checks that no errors are thrown
        TODO test problem insertion in hierarchy
        '''
        _moocdb = moocdb.MOOCdb()
        manager = submissions.SubmissionManager(_moocdb)
        raw_event = {}

        event = events.OpenResponseAssessment(raw_event)
        table_update = manager.update_submission_tables(event)
        self.assertIsNone(table_update)
        self.assertEquals(0, len(event.data))

        event = events.Event({'problem_id': 'something'})
        table_update = manager.update_submission_tables(event)
        self.assertIsNone(table_update)
        self.assertEquals(event.data['problem_id'], 'something')


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(SubmissionManagerTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
