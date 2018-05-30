# /usr/bin/env python
import sys
import os
import argparse

# The purpose of this script is to attempt to reformat the
# VisMOOC elearning-data folder file tree into the
# MOOC-Learner-Curated folder file tree automatically

# One can specify the path to the elearning-data
# folder and it will finally rename the folder to 'data'

# The default path is './elearning-data/'

EVENT_FILE_OLD = '-clickstream.log'
EVENT_FILE_NEW = '___tracking_log.json'
DATABASE_FILE = {'structure': '-course_structure-prod-analytics.json',
                 'certificate': '-certificates_generatedcertificate-prod-analytics.sql',
                 'enrollment': '-student_courseenrollment-prod-analytics.sql',
                 'user': '-auth_user-prod-analytics.sql',
                 'profile': '-auth_userprofile-prod-analytics.sql',
                 'forum': '-prod.mongo'}

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Reformat the VisMOOC elearning-data folder file tree into the '
                                     'MOOC-Learner-Curated folder file tree automatically.')
    parser.add_argument('-r', action='store_true', default=False, dest='is_rev', help='reversely reformatting')
    parser.add_argument("-p", action="store", default='', dest='path', help='path to data folder')
    is_rev = parser.parse_args().is_rev
    path = parser.parse_args().path
    if path == '':
        path = './data/' if is_rev else './elearning-data/'
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        sys.exit('Directory does not exist.')

    courses = next(os.walk(path))[1]
    if not courses:
        sys.exit('No course found')

    for course in courses:
        course_path = os.path.join(path, course)
        content = next(os.walk(course_path))[1]
        if is_rev and 'log_data' not in content or (not is_rev and ('databaseData' not in content or 'eventData' not in content)):
            print('Course directory {} is not complete'.format(course))
            continue

        if is_rev:
            log_path = os.path.abspath(os.path.join(course_path, "log_data/"))
            files = [f for f in os.listdir(log_path)]
            event_flag = False
            for event_file in files:
                if event_file.endswith(EVENT_FILE_NEW):
                    os.rename(os.path.join(log_path, event_file),
                              os.path.join(log_path, event_file[:event_file.index(EVENT_FILE_NEW)] + EVENT_FILE_OLD))
                    event_flag = True
            if not event_flag:
                print('No event log found under course %s' % course)
            event_path = os.path.abspath(os.path.join(course_path, "eventData/"))
            os.rename(log_path, event_path)

            database_path = os.path.abspath(os.path.join(course_path, "databaseData/"))
            if not os.path.isdir(os.path.join(course_path, 'extras/')):
                os.makedirs(database_path)
            else:
                os.rename(os.path.join(course_path, 'extras'), database_path)
            database_file_list = []
            database_name_list = []
            for database_name in DATABASE_FILE:
                database_suffix = DATABASE_FILE[database_name]
                for database_file in files:
                    if database_file.endswith(database_suffix):
                        database_name_list.append(database_name)
                        database_file_list.append(database_file)
                        continue
            if not database_name_list == list(DATABASE_FILE.keys()):
                print('Database logs under course %s not complete' % course)
                print('The following database files are missing: ' + str(set(DATABASE_FILE.keys()) - set(database_name_list)))
            for database_file in database_file_list:
                os.rename(os.path.join(event_path, database_file),
                          os.path.join(database_path, database_file))

        else:
            event_path = os.path.abspath(os.path.join(course_path, "eventData/"))
            event_files = [f for f in os.listdir(event_path)]
            event_flag = False
            for event_file in event_files:
                if event_file.endswith(EVENT_FILE_OLD):
                    os.rename(os.path.join(event_path, event_file),
                              os.path.join(event_path, event_file[:event_file.index(EVENT_FILE_OLD)] + EVENT_FILE_NEW))
                    event_flag = True
            if not event_flag:
                print('No event log found under course %s' % course)
            log_path = os.path.abspath(os.path.join(course_path, "log_data/"))
            os.rename(event_path, log_path)

            database_path = os.path.abspath(os.path.join(course_path, "databaseData/"))
            database_files = [f for f in os.listdir(database_path)]
            database_file_list = []
            database_name_list = []
            for database_name in DATABASE_FILE:
                database_suffix = DATABASE_FILE[database_name]
                for database_file in database_files:
                    if database_file.endswith(database_suffix):
                        database_name_list.append(database_name)
                        database_file_list.append(database_file)
                        continue
            if not database_name_list == list(DATABASE_FILE.keys()):
                print('Database logs under course %s not complete' % course)
                print('The following database files are missing: ' + str(set(DATABASE_FILE.keys()) - set(database_name_list)))
            for database_file in database_file_list:
                os.rename(os.path.join(database_path, database_file),
                          os.path.join(log_path, database_file))
            os.rename(database_path, os.path.join(course_path, 'extras'))

    parent_path = os.path.abspath(os.path.join(path, ".."))
    if is_rev:
        os.rename(os.path.join(parent_path, 'data'), os.path.join(parent_path, 'elearning-data'))
        path = os.path.abspath(os.path.join(parent_path, "elearning-data/"))
    else:
        os.rename(os.path.join(parent_path, 'elearning-data'), os.path.join(parent_path, 'data'))
        path = os.path.abspath(os.path.join(parent_path, "data/"))
    print('Done')
