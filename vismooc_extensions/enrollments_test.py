#!/usr/bin/env python
'''Tester for vismooc extensions enrollments module
'''
import unittest
import enrollments


class EnrollmentsTest(unittest.TestCase):
    '''
    Tester for the vismooc extensions enrollments module
    '''

    def test_get_csv_fields(self):
        '''
        Simple check that the csv fields are consistent with the ones
        set when the tests were written.
        '''
        self.assertEqual(
            ['_id', 'user_id', 'course_id', 'timestamp', 'action'],
            enrollments.get_csv_fields())

    def test_id_mapping(self):
        '''
        Simple check that the _id field in the vismooc
        enrollments schema is mapped to correctly.
        '''
        row = {'id': 'abc'}
        self.assertEqual('abc',
                         enrollments.get_csv_field_to_func_map()['_id'](row))

    def test_user_id_mapping(self):
        '''
        Simple check that the user_id field in the vismooc
        enrollments schema is mapped to correctly.
        '''
        row = {'user_id': 'bac'}
        self.assertEqual(
            'bac', enrollments.get_csv_field_to_func_map()['user_id'](row))

    def test_course_id_mapping(self):
        '''
        Simple check that the course_id field in the vismooc
        enrollments schema is mapped to correctly.
        '''
        row = {'course_id': 'cba'}
        self.assertEqual(
            'cba', enrollments.get_csv_field_to_func_map()['course_id'](row))

    def test_timestamp_mapping(self):
        '''
        Simple check that the timestamp field in the vismooc
        enrollments schema is mapped to correctly.
        '''
        row = {'created': '2014-04-10 16:22:04'}
        self.assertEqual(
            '2014-04-10 16:22:04',
            enrollments.get_csv_field_to_func_map()['timestamp'](row))

    def test_action_mapping(self):
        '''
        Simple check that the action field in the vismooc
        enrollments schema is mapped to correctly.
        '''
        row = {'is_active': '1'}
        self.assertEqual(
            1, enrollments.get_csv_field_to_func_map()['action'](row))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EnrollmentsTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
