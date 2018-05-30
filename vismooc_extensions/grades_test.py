#!/usr/bin/env python
'''Tester for vismooc extensions grades module
'''
import unittest

import grades


class GradesTest(unittest.TestCase):
    '''
    Tester for the vismooc extensions grades module
    '''

    def test_get_csv_fields(self):
        '''
        Simple check that the csv fields are consistent with the ones
        set when the tests were written.
        '''
        self.assertEqual(['_id', 'user_id', 'course_id', 'timestamp', 'grade'],
                         grades.get_csv_fields())

    def test_id_mapping(self):
        '''
        Simple check that the _id field in the vismooc
        grades schema is mapped to correctly.
        '''
        row = {'id': 'abc'}
        self.assertEqual('abc', grades.get_csv_field_to_func_map()['_id'](row))

    def test_user_id_mapping(self):
        '''
        Simple check that the user_id field in the vismooc
        grades schema is mapped to correctly.
        '''
        row = {'user_id': 'bac'}
        self.assertEqual('bac',
                         grades.get_csv_field_to_func_map()['user_id'](row))

    def test_course_id_mapping(self):
        '''
        Simple check that the course_id field in the vismooc
        grades schema is mapped to correctly.
        '''
        row = {'course_id': 'cba'}
        self.assertEqual('cba',
                         grades.get_csv_field_to_func_map()['course_id'](row))

    def test_timestamp_mapping(self):
        '''
        Simple check that the timestamp field in the vismooc
        grades schema is mapped to correctly.
        '''
        row = {'created_date': '2014-08-13 01:43:25'}
        self.assertEqual('2014-08-13 01:43:25',
                         grades.get_csv_field_to_func_map()['timestamp'](row))

    def test_grade_mapping(self):
        '''
        Simple check that the grade field in the vismooc
        grades schema is mapped to correctly.
        '''
        row = {'grade': '0.07'}
        self.assertEqual('0.07',
                         grades.get_csv_field_to_func_map()['grade'](row))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(GradesTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
