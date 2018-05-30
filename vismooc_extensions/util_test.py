#!/usr/bin/env python
'''Tester for vismooc extensions utilities module
'''

import os
import tempfile
import unittest

import util


class UtilitiesTest(unittest.TestCase):
    '''
    Tester for the vismooc extensions utilities module
    '''
    def test_get_id(self):
        '''
        Simple check that ensures the hash function works and
        the hashed id is in legal format.
        '''
        course_entry = {
            'category': 'course',
            'field_a': 'value_1',
            'field_b': 'value_2'
        }
        course_entry_copy = course_entry.copy()
        self.assertEqual(
            util.get_id(course_entry), util.get_id(course_entry_copy))
        course_entry_copy['field_b'] = 'value_3'
        self.assertNotEqual(
            util.get_id(course_entry), util.get_id(course_entry_copy))
        self.assertEqual(
            '2538887322753988521', str(util.get_id(course_entry)))

    def test_write_sample_csv(self):
        '''
        Check that ensures the write_sample_csv function works and can
        handle ascii and unicode strings at the same time.
        '''
        input_iterable = {u'block-v1:HKUSTx+EBA101x+3T2016+type@video+block@f721c1c4a17f4491b27c14e20dd9e706'}
        output_path = os.path.join(tempfile.gettempdir(), 'util_test.csv')
        fields = ['_id', 'original_id', 'name', 'section', 'description', 'url']

        # NOTE Mock field to function map from `video.py::get_videos_csv_field_to_func_map`
        field_to_func_map = {
            '_id': lambda _: '4126901492853833867',
            'original_id': lambda _: u'block-v1:HKUSTx+EBA101x+3T2016+type@'
                                     u'video+block@f721c1c4a17f4491b27c14e20dd9e706',
            'name': lambda _: u'Part 1',
            'section': lambda _: u'2>>Week 1>>3>>1.3: Challenging English sounds>>1>>'
                                 u'Challenging English Sounds /\u026a/ and /i:/>>1>>Part 1>>',
            'description': lambda _: '',
            'url': lambda _: u'http://w02.hkvu.hk/edX/EBA101x/download/'
                             u'EBA101x_Wk01_1-3_V02_Challenging_English_Sounds_Part1_480p.mp4',
        }
        util.write_simple_csv(input_iterable, output_path, fields, field_to_func_map)
        with open(output_path, 'r') as f:
            self.assertEqual('4126901492853833867,block-v1:HKUSTx+EBA101x+3T2016+'
                             'type@video+block@f721c1c4a17f4491b27c14e20dd9e706,'
                             'Part 1,2>>Week 1>>3>>1.3: Challenging English sounds>>1>>'
                             'Challenging English Sounds /\xc9\xaa/ and /i:/>>1>>Part 1>>,'
                             ',http://w02.hkvu.hk/edX/EBA101x/download/'
                             'EBA101x_Wk01_1-3_V02_Challenging_English_Sounds_Part1_480p.mp4\n',
                             f.readline())

    def tearDown(self):
        try:
            os.remove('test_write_sample_csv.csv')
        except OSError:
            pass


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(UtilitiesTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
