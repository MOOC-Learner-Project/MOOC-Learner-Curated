#!/usr/bin/env python
'''Tester for vismooc extensions users module
'''
import hashlib
import unittest

import users


class UsersTest(unittest.TestCase):
    '''
    Tester for the vismooc extensions users module
    '''

    def test_get_csv_fields(self):
        '''
        Simple check that the csv fields are consistent with the ones
        set when the tests were written.
        '''
        self.assertEqual([
            '_id', 'original_id', 'username', 'name', 'language', 'location',
            'birth_date', 'education_level', 'bio', 'gender', 'country'
        ], users.get_csv_fields())

    def test_id_mapping(self):
        '''
        Simple check that the _id field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'id': 'abc'}
        self.assertEqual('abc',
                         users.get_profile_field_to_func_map()['_id'](row))

    def test_original_id_mapping(self):
        '''
        Simple check that the original_id field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'id': 'bac'}
        self.assertEqual(
            'bac', users.get_user_field_to_func_map()['original_id'](row))

    def test_username_mapping(self):
        '''
        Simple check that the username field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'username': 'cba'}
        self.assertEqual(
            hashlib.new('ripemd160', 'cba').hexdigest(),
            users.get_user_field_to_func_map()['username'](row))

    def test_name_mapping(self):
        '''
        Simple check that the name field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'name': 'John Doe'}
        self.assertEqual(
            hashlib.new('ripemd160', 'John Doe').hexdigest(),
            users.get_profile_field_to_func_map()['name'](row))

    def test_language_mapping(self):
        '''
        Simple check that the language field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'language': 'en'}
        self.assertEqual(
            'en', users.get_profile_field_to_func_map()['language'](row))

    def test_location_mapping(self):
        '''
        Simple check that the location field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'location': 'USA'}
        self.assertEqual(
            'USA', users.get_profile_field_to_func_map()['location'](row))

    def test_birth_date_mapping(self):
        '''
        Simple check that the birth_date field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'year_of_birth': '1984'}
        self.assertEqual(
            '1984', users.get_profile_field_to_func_map()['birth_date'](row))

    def test_education_level_mapping(self):
        '''
        Simple check that the education_level field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'level_of_education': 'p_oth'}
        self.assertEqual(
            'p_oth',
            users.get_profile_field_to_func_map()['education_level'](row))

    def test_bio_mapping(self):
        '''
        Simple check that the bio field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'goals': 'My goal is to finish my thesis and graduate on time.'}
        self.assertEqual(
            'My goal is to finish my thesis and graduate on time.',
            users.get_profile_field_to_func_map()['bio'](row))

    def test_gender_mapping(self):
        '''
        Simple check that the gender field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'gender': 'm'}
        self.assertEqual('m',
                         users.get_profile_field_to_func_map()['gender'](row))

    def test_country_mapping(self):
        '''
        Simple check that the country field in the vismooc
        users schema is mapped to correctly.
        '''
        row = {'country': 'South Korea'}
        self.assertEqual('South Korea',
                         users.get_profile_field_to_func_map()['country'](row))

    def test_clean_profile_file_data(self):
        '''
        Simple check to ensure that the troublesome byte sequences
        that can be found in Edx profile data are replaced appropriately.
        Namely, there should be no instances of '\r\\n'.
        '''
        problem_string = 'arbitrarystring\r\\noops!\r\\nhelp'
        self.assertEqual('arbitrarystring\\noops!\\nhelp',
                         users.clean_profile_file_data(problem_string))


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(UsersTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
