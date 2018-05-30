#!/usr/bin/env python
'''Tester for vismooc extensions forum module
'''

import unittest
import forum


class ForumTest(unittest.TestCase):
    '''
    Tester for the vismooc extensions forum module
    '''

    def test_get_csv_fields(self):
        '''
        Simple check that the csv fields are consistent with the ones
        set when the tests were written.
        '''
        self.assertEqual([
            '_id', 'original_id', 'course_id', 'author_id', 'created_at',
            'updated_at', 'body', 'type', 'title', 'thread_type',
            'comment_thread_id', 'parent_id'
        ], forum.get_csv_fields())

    def test_original_id_mapping(self):
        '''
        Simple check that the original_id field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'_id': {'$oid': 'abc'}}
        self.assertEqual('abc',
                         forum.get_csv_field_to_func_map()['original_id'](row))

    def test_course_id_mapping(self):
        '''
        Simple check that the course_id field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'course_id': 'Edx/5.01x/2T2199'}
        self.assertEqual('Edx/5.01x/2T2199',
                         forum.get_csv_field_to_func_map()['course_id'](row))

    def test_author_id_mapping(self):
        '''
        Simple check that the author_id field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'author_id': '235235'}
        self.assertEqual('235235',
                         forum.get_csv_field_to_func_map()['author_id'](row))

    def test_created_at_mapping(self):
        '''
        Simple check that the created_at field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'created_at': {'$date': 1387483835043}}
        self.assertEqual('2013-12-19 15:10:35',
                         forum.get_csv_field_to_func_map()['created_at'](row))

        # Apparently there can also be ISO8601 formatted timestamps
        row = {'created_at': {'$date': '2015-12-30T01:03:14.523Z'}}
        self.assertEqual('2015-12-30 01:03:14',
                         forum.get_csv_field_to_func_map()['created_at'](row))

    def test_updated_at_mapping(self):
        '''
        Simple check that the updated_at field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'updated_at': {'$date': 1387487272772}}
        self.assertEqual('2013-12-19 16:07:52',
                         forum.get_csv_field_to_func_map()['updated_at'](row))

        # Apparently there can also be ISO8601 formatted timestamps
        row = {'updated_at': {'$date': '2015-12-30T01:03:14.523Z'}}
        self.assertEqual('2015-12-30 01:03:14',
                         forum.get_csv_field_to_func_map()['updated_at'](row))

    def test_body_mapping(self):
        '''
        Simple check that the body field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'body': u'simple body of text'}
        self.assertEqual('simple body of text',
                         forum.get_csv_field_to_func_map()['body'](row))
        row = {'body': u'now with some tricky unicodei\xb4m'}
        self.assertEqual('now with some tricky unicodei\xc2\xb4m',
                         forum.get_csv_field_to_func_map()['body'](row))

    def test_type_mapping(self):
        '''
        Simple check that the type field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'_type': 'Comment'}
        self.assertEqual('Comment',
                         forum.get_csv_field_to_func_map()['type'](row))

    def test_title_mapping(self):
        '''
        Simple check that the title field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'_type': 'CommentThread'}
        self.assertEqual('', forum.get_csv_field_to_func_map()['title'](row))
        row = {'_type': 'CommentThread', 'title': 'simple title'}
        self.assertEqual('simple title',
                         forum.get_csv_field_to_func_map()['title'](row))
        row = {
            '_type': 'CommentThread',
            'title': u'title with tricky \xb4 unicode'
        }
        self.assertEqual('title with tricky \xc2\xb4 unicode',
                         forum.get_csv_field_to_func_map()['title'](row))

    def test_thread_type_mapping(self):
        '''
        Simple check that the thread_type field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'_type': 'Comment'}
        self.assertEqual('',
                         forum.get_csv_field_to_func_map()['thread_type'](row))
        row = {'_type': 'CommentThread'}
        self.assertEqual('',
                         forum.get_csv_field_to_func_map()['thread_type'](row))
        row = {'_type': 'CommentThread', 'thread_type': 'question'}
        self.assertEqual('question',
                         forum.get_csv_field_to_func_map()['thread_type'](row))
        row = {'_type': 'CommentThread', 'thread_type': 'discussion'}
        self.assertEqual('discussion',
                         forum.get_csv_field_to_func_map()['thread_type'](row))

    def test_comment_thread_id_mapping(self):
        '''
        Simple check that the comment_thread_id field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'_type': 'Comment'}
        self.assertEqual(
            '', forum.get_csv_field_to_func_map()['comment_thread_id'](row))
        row = {'_type': 'CommentThread'}
        self.assertEqual(
            '', forum.get_csv_field_to_func_map()['comment_thread_id'](row))
        row = {
            '_type': 'Comment',
            'comment_thread_id': {
                '$oid': '526f149558b9a081bf000065'
            }
        }
        self.assertEqual(
            '526f149558b9a081bf000065',
            forum.get_csv_field_to_func_map()['comment_thread_id'](row))

    def test_parent_id_mapping(self):
        '''
        Simple check that the parent_id field in the vismooc
        forum schema is mapped to correctly.
        '''
        row = {'_type': 'Comment'}
        self.assertEqual('',
                         forum.get_csv_field_to_func_map()['parent_id'](row))
        row = {'_type': 'CommentThread'}
        self.assertEqual('',
                         forum.get_csv_field_to_func_map()['parent_id'](row))
        row = {
            '_type': 'Comment',
            'parent_id': {
                '$oid': '529a1abe6bfde39898000068'
            }
        }
        self.assertEqual('529a1abe6bfde39898000068',
                         forum.get_csv_field_to_func_map()['parent_id'](row))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(ForumTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
