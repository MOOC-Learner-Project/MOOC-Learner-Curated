#!/usr/bin/env python
'''Tester for vismooc extensions videos module
'''
import unittest

import videos


class CourseVideoTest(unittest.TestCase):
    '''
    Tester for the vismooc extensions videos module
    This tests the course_video maps.
    '''

    def setUp(self):
        '''
        Sets up the course_structure dictionary needed.
        '''
        self.video_id = 'i4x://org/course/video/f50cc021e7b84729b53aabf23017cd13'
        self.course_structure = {
            'i4x://org/edxcourse/course/run': {
                'category': 'course'
            },
            self.video_id: {
                'category': 'video'
            }
        }

    def test_get_csv_fields(self):
        '''
        Simple check that the csv fields are consistent with the ones
        set when the tests were written.
        '''
        self.assertEqual(['_id', 'course_id', 'video_id'],
                         videos.get_course_video_csv_fields())

    def test_id_mapping(self):
        '''
        Simple check that the _id field in the vismooc
        course_video schema is mapped to correctly.
        '''
        self.assertEqual('4176302298990310613',
                         videos.get_course_video_csv_field_to_func_map(
                             self.course_structure)['_id'](self.video_id))

    def test_course_id_mapping(self):
        '''
        Simple check that the courseId field in the vismooc
        course_video schema is mapped to correctly.
        '''
        self.assertEqual(
            'org/edxcourse/run',
            videos.get_course_video_csv_field_to_func_map(
                self.course_structure)['course_id'](self.video_id))

    def test_video_id_mapping(self):
        '''
        Simple check that the videoId field in the vismooc
        course_video schema is mapped to correctly.
        '''
        self.assertEqual(self.video_id,
                         videos.get_course_video_csv_field_to_func_map(
                             self.course_structure)['video_id'](self.video_id))


class VideosTest(unittest.TestCase):
    '''
    Tester for the vismooc extensions videos module
    This tests the videos maps.
    '''

    def setUp(self):
        '''
        Sets up the course_structure dictionary needed.
        '''
        self.video_id_zero = 'i4x://org/course/video/2229d6d6ffbbacf5ad9edea51ff54b4b'
        self.video_id_one = 'i4x://org/course/video/f50cc021e7b84729b53aabf23017cd13'
        self.course_structure = {
            'i4x://org/edxcourse/course/run': {
                'category':
                'course',
                'children': [
                    'i4x://org/course/chapter/e7b8471204b84885a4797f517715722a',
                    'i4x://org/course/chapter/a88924285729a589902cda2842e3a84b'
                ],
                'metadata': {
                    'display_name': 'course zero'
                }
            },
            'i4x://org/course/chapter/e7b8471204b84885a4797f517715722a': {
                'category':
                'chapter',
                'children': [
                    'i4x://org/course/sequential/0fcf98abc23b42fda43b393485f3ef2a'
                ],
                'metadata': {
                    'display_name': 'chapter zero'
                }
            },
            'i4x://org/course/chapter/a88924285729a589902cda2842e3a84b': {
                'category':
                'chapter',
                'children': [
                    'i4x://org/course/sequential/11ba0a5f3efb40c3b1ff57546168f517',
                    'i4x://org/course/sequential/55abcb2199f9465e88424ece4177d108'
                ],
                'metadata': {
                    'display_name': 'chapter one'
                }
            },
            'i4x://org/course/sequential/0fcf98abc23b42fda43b393485f3ef2a': {
                'category':
                'sequential',
                'children':
                ['i4x://org/course/vertical/cbc46e7903b046e18f1c21dd48fda412'],
                'metadata': {
                    'display_name': 'sequential zero'
                }
            },
            'i4x://org/course/sequential/11ba0a5f3efb40c3b1ff57546168f517': {
                'category':
                'sequential',
                'children':
                ['i4x://org/course/vertical/54e1628c7b4e4c7ab23651d883b60217'],
                'metadata': {
                    'display_name': 'sequential one'
                }
            },
            'i4x://org/course/sequential/55abcb2199f9465e88424ece4177d108': {
                'category':
                'sequential',
                'children': [
                    'i4x://org/course/vertical/bb089e1b1a224255809597c1823901a9',
                    'i4x://org/course/vertical/b986d9bfb11443ab123e0c72259f9bcb'
                ],
                'metadata': {
                    'display_name': 'sequential two'
                }
            },
            'i4x://org/course/vertical/cbc46e7903b046e18f1c21dd48fda412': {
                'category': 'vertical',
                'children': [self.video_id_zero],
                'metadata': {
                    'display_name': 'vertical zero'
                }
            },
            'i4x://org/course/vertical/54e1628c7b4e4c7ab23651d883b60217': {
                'category':
                'vertical',
                'children':
                ['i4x://org/course/problem/4b9026e2aaef13f79e436a5161145b43'],
                'metadata': {
                    'display_name': 'vertical one'
                }
            },
            'i4x://org/course/vertical/b986d9bfb11443ab123e0c72259f9bcb': {
                'category':
                'vertical',
                'children':
                ['i4x://org/course/html/bac9fc959c6340abf41512c14f62ae76'],
                'metadata': {
                    'display_name': 'vertical two'
                }
            },
            'i4x://org/course/vertical/bb089e1b1a224255809597c1823901a9': {
                'category':
                'vertical',
                'children': [
                    'i4x://org/course/html/bef1b3c555124374a703420e2159d986',
                    self.video_id_one
                ],
                'metadata': {
                    'display_name': 'vertical three'
                }
            },
            self.video_id_zero: {
                'category': 'video',
                'children': [],
                'metadata': {
                    'display_name': 'video zero',
                    'html5_sources': []
                }
            },
            self.video_id_one: {
                'category': 'video',
                'children': [],
                'metadata': {
                    'display_name':
                    'video one',
                    'html5_sources':
                    ['http://edx.org/edX/edxcourse/download/course video.mp4']
                }
            },
            'i4x://org/course/problem/4b9026e2aaef13f79e436a5161145b43': {
                'category': 'problem',
                'children': [],
                'metadata': {
                    'display_name': 'problem zero'
                }
            },
            'i4x://org/course/html/bac9fc959c6340abf41512c14f62ae76': {
                'category': 'html',
                'children': [],
                'metadata': {
                    'display_name': 'html zero'
                }
            },
            'i4x://org/course/html/bef1b3c555124374a703420e2159d986': {
                'category': 'html',
                'children': [],
                'metadata': {
                    'display_name': 'html one'
                }
            }
        }

    def test_get_csv_fields(self):
        '''
        Simple check that the csv fields are consistent with the ones
        set when the tests were written.
        '''
        self.assertEqual(
            ['_id', 'original_id', 'name', 'section', 'description', 'url'],
            videos.get_videos_csv_fields())

    def test_id_mapping(self):
        '''
        Simple check that the _id field in the vismooc
        videos schema is mapped to correctly.
        '''
        self.assertEqual('4176302298990310613',
                         videos.get_videos_csv_field_to_func_map(
                             self.course_structure)['_id'](self.video_id_one))
        self.assertEqual('7353585395721519839',
                         videos.get_videos_csv_field_to_func_map(
                             self.course_structure)['_id'](self.video_id_zero))

    def test_original_id_mapping(self):
        '''
        Simple check that the originalId field in the vismooc
        videos schema is mapped to correctly.
        '''
        self.assertEqual(
            self.video_id_one,
            videos.get_videos_csv_field_to_func_map(
                self.course_structure)['original_id'](self.video_id_one))
        self.assertEqual(
            self.video_id_zero,
            videos.get_videos_csv_field_to_func_map(
                self.course_structure)['original_id'](self.video_id_zero))

    def test_name_mapping(self):
        '''
        Simple check that the name field in the vismooc
        videos schema is mapped to correctly.
        '''
        self.assertEqual('video one',
                         videos.get_videos_csv_field_to_func_map(
                             self.course_structure)['name'](self.video_id_one))
        self.assertEqual(
            'video zero',
            videos.get_videos_csv_field_to_func_map(
                self.course_structure)['name'](self.video_id_zero))

    def test_section_mapping(self):
        '''
        Simple check that the section field in the vismooc
        videos schema is mapped to correctly.

        This is the test in particular that requires the fairly large
        course structure object because the section field has to be determined
        through iteration of the course structure tree from the course block
        (i.e. the root node).
        '''
        self.assertEqual(
            '1>>chapter one>>1>>sequential two>>0>>vertical three>>1>>video one>>',
            videos.get_videos_csv_field_to_func_map(
                self.course_structure)['section'](self.video_id_one))
        self.assertEqual(
            '0>>chapter zero>>0>>sequential zero>>0>>vertical zero>>0>>video zero>>',
            videos.get_videos_csv_field_to_func_map(
                self.course_structure)['section'](self.video_id_zero))

    def test_description_mapping(self):
        '''
        Simple check that the description field in the vismooc
        videos schema is mapped to correctly.

        description should map to an empty string until further
        clarification from the vismooc team.
        TODO
        '''
        self.assertEqual(
            '',
            videos.get_videos_csv_field_to_func_map(
                self.course_structure)['description'](self.video_id_one))

    def test_url_mapping(self):
        '''
        Simple check that the url field in the vismooc
        videos schema is mapped to correctly.
        '''
        self.assertEqual(
            'http://edx.org/edX/edxcourse/download/course video.mp4',
            videos.get_videos_csv_field_to_func_map(
                self.course_structure)['url'](self.video_id_one))
        self.assertEqual('',
                         videos.get_videos_csv_field_to_func_map(
                             self.course_structure)['url'](self.video_id_zero))

    def test_get_video_id_set(self):
        '''
        Simple check that the the generation of the video id set
        given a course structure json object is computed correctly.
        '''
        answer_set = set([
            'i4x://org/course/video/f50cc021e7b84729b53aabf23017cd13',
            'i4x://org/course/video/2229d6d6ffbbacf5ad9edea51ff54b4b'
        ])
        self.assertEqual(answer_set,
                         videos.get_video_id_set(self.course_structure))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(CourseVideoTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(VideosTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
