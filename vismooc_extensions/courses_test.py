#!/usr/bin/env python
'''Tester for vismooc extensions courses module
'''
import unittest
import courses


class CoursesTest(unittest.TestCase):
    '''
    Tester for the vismooc extensions courses module
    '''

    def test_get_csv_fields(self):
        '''
        Simple check that the csv fields are consistent with the ones
        set when the tests were written.
        '''
        self.assertEqual([
            '_id', 'original_id', 'name', 'year', 'org', 'instructor',
            'description', 'start_date', 'end_date', 'course_url', 'image_url'
        ], courses.get_csv_fields())

    def test_contains_course(self):
        '''
        Simple coverage test for the contains_course method.
        The various values for the category field are sourced from
        https://edx.readthedocs.io/projects/devdata/en/latest/internal_data_formats/course_structure.html#course-data
        '''
        self.assertEqual(False, courses.contains_course({}))
        self.assertEqual(False, courses.contains_course({'key': {}}))
        self.assertEqual(False,
                         courses.contains_course({
                             'key': {
                                 'category': 'chapter'
                             }
                         }))
        self.assertEqual(False,
                         courses.contains_course({
                             'key': {
                                 'category': 'discussion'
                             }
                         }))
        self.assertEqual(False,
                         courses.contains_course({
                             'key': {
                                 'category': 'html'
                             }
                         }))
        self.assertEqual(False,
                         courses.contains_course({
                             'key': {
                                 'category': 'problem'
                             }
                         }))
        self.assertEqual(False,
                         courses.contains_course({
                             'key': {
                                 'category': 'sequential'
                             }
                         }))
        self.assertEqual(False,
                         courses.contains_course({
                             'key': {
                                 'category': 'vertical'
                             }
                         }))
        self.assertEqual(True,
                         courses.contains_course({
                             'key': {
                                 'category': 'course'
                             }
                         }))
        self.assertEqual(True,
                         courses.contains_course({
                             'key1': {
                                 'category': 'sequential'
                             },
                             'key2': {
                                 'category': 'course'
                             }
                         }))
        self.assertEqual(False,
                         courses.contains_course({
                             'key1': {
                                 'category': 'sequential'
                             },
                             'key2': {
                                 'category': 'discussion'
                             }
                         }))

    def test_get_course_entry_key(self):
        '''
        Simple coverage test for the get_course_key method.
        '''
        self.assertEqual('key2',
                         courses.get_course_entry_key({
                             'key1': {
                                 'category': 'sequential'
                             },
                             'key2': {
                                 'category': 'course'
                             }
                         }))
        self.assertEqual(None,
                         courses.get_course_entry_key({
                             'key1': {
                                 'category': 'sequential'
                             },
                             'key2': {
                                 'category': 'discussion'
                             }
                         }))

    def test_get_original_id(self):
        '''
        Simple coverage test for the get_original_id method.
        '''
        self.assertEqual('', courses.get_original_id({}))
        self.assertEqual('{org}/{course}/{run}',
                         courses.get_original_id({
                             'i4x://{org}/{course}/course/{run}': {
                                 'category': 'course'
                             }
                         }))

    def test_get_name(self):
        '''
        Simple coverage test for the get_name method.
        '''
        self.assertEqual('', courses.get_name({}))
        self.assertEqual('', courses.get_name({'metadata': {}}))
        self.assertEqual('Some human readable name for an edx course',
                         courses.get_name({
                             'metadata': {
                                 'display_name':
                                 'Some human readable name for an edx course'
                             }
                         }))

    def test_get_year(self):
        '''
        Simple coverage test for get_year method.
        '''
        course_entry = {
            'category': 'course',
            'metadata': {
                'start': '2014-06-17T22:00:00Z'
            }
        }
        self.assertEqual('2014_Q0_R0', courses.get_year(course_entry))

    def test_get_org(self):
        '''
        Simple coverage test for the get_original_id method.
        '''
        self.assertEqual('', courses.get_org('i4x://invalid'))
        self.assertEqual('{org}',
                         courses.get_org('i4x://{org}/{course}/course/{run}'))

    def test_get_instructor(self):
        '''
        Simple coverage test for the get_instructor method.
        get_description should return an empty string until further
        clarification from the vismooc team.
        TODO
        '''
        self.assertEqual('', courses.get_instructor())

    def test_get_description(self):
        '''
        Simple coverage test for the get_description method.
        get_description should return an empty string until further
        clarification from the vismooc team.
        TODO
        '''
        self.assertEqual('', courses.get_description())

    def test_get_course_url(self):
        '''
        Simple coverage test for the get_instructor method.
        get_course_url should return an empty string until further
        clarification from the vismooc team.
        TODO
        '''
        self.assertEqual('', courses.get_course_url())

    def test_get_image_url(self):
        '''
        Simple coverage test for the get_description method.
        get_image_url should return an empty string until further
        clarification from the vismooc team.
        TODO
        '''
        self.assertEqual('', courses.get_image_url())

    def test_get_start_date(self):
        '''
        Simple coverage test for get_start_date method.
        '''
        course_entry = {
            'category': 'course',
            'metadata': {
                'start': '2014-06-17T22:00:00Z'
            }
        }
        self.assertEqual('2014-06-17T22:00:00Z',
                         courses.get_start_date(course_entry))

    def test_get_end_date(self):
        '''
        Simple coverage test for end_start_date method.
        '''
        course_entry = {
            'category': 'course',
            'metadata': {
                'end': '2014-09-05T19:00:00Z'
            }
        }
        self.assertEqual('2014-09-05T19:00:00Z',
                         courses.get_end_date(course_entry))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(CoursesTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
