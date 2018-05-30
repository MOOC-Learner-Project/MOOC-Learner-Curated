#!/usr/bin/env python
'''
This is the parser of YAML configuration file.

Parse the YAML config file and store all configuration variables as constants.
'''
import yaml
import os
import sys
import getpass


class ConfigParser(object):
    '''
    Handles parsing and processing the config YAML file and
    act as an interface for other modules to read config information.
    '''

    # Legal structure of cfg dict
    CONFIG_STRUCTURE = {
        "pipeline": {
            "query": None,
            "folder_setup": None,
            "apipe": None,
            "qpipe": {
                "qpipe_create_db": None,
                "qpipe_populate_db": None,
                "qpipe_process_events": None
            },
            "curation": None,
            "vismooc_extensions": {
                "vismooc_populate": None,
                "vismooc_process": None
            },
            "newmitx_extensions": {
                "newmitx_populate": None,
                "newmitx_process": None,
            },
        },
        "csv_path": {
            "edx_track_event_name": None,
            "problem_hierarchy_name": None,
            "answer_name": None,
            "correct_map_name": None,
            "resource_hierarchy_name": None,
            "moocdb_csv_dir": None,
            "intermediary_csv_dir": None
        },
        "mysql_script_path": {
            "apipe_folder": None,
            "qpipe_copy_db_script": None,
            "vismooc_extensions_folder": None,
            "newmitx_extensions_folder": None,
            "qpipe_create_db_script": None,
            "qpipe_folder": None,
            "edx_pipe_folder": None,
            "MLC_dir": None,
            "vismooc_extensions_import_script": None,
            "newmitx_extensions_import_script": None,
            "curation_folder": None
        },
        "csv_parsing": {
            "quotechar": None,
            "escapechar": None,
            "timestamp_format": None
        },
        "data_file": {
            "log_data_folder": None,
            "data_dir": None,
            "vismooc_data_folder": None,
            "new_mitx_data_folder": None,
            "course_folder": None,
            "log_file": None,
            "vismooc_file": {
                "course_profile_file": None,
                "course_certificates_file": None,
                "course_forum_file": None,
                "course_structure_file": None,
                "course_enrollment_file": None,
                "course_user_file": None,
            },
            "newmitx_file": {
                "course_video_axis_file": None,
                "course_video_stats_file": None,
                "course_video_stats_day_file": None,
                "course_pc_day_totals_file": None,
                'course_person_course_day_file': None,
                "course_person_course_video_watched_file": None,
                "course_stats_activity_by_day_file": None,
                "course_stats_overall_file": None,
                "course_time_on_task_file": None,
                "course_time_on_task_totals_file": None,
                "course_user_info_combo_file": None,
            },
        },
        "open_edx_spec": {
            "video_id_spec": None
        },
        "mysql": {
            "query_database": None,
            "database": None,
            "host": None,
            "query_password": None,
            "password": None,
            "query_user": None,
            "user": None,
            "port": None
        }
    }

    pipeline_MESSAGE = {
        'folder_setup': '###### Step 1: Do you want to create folder environment for log transformation?',
        'apipe': '###### Step 2: Do you want to translate the log file into csv?',
        'qpipe': '###### Step 3: Do you want to enter qpipe?',
        'qpipe_process_events': '## Step 3.1: Do you want to pipeline events?',
        'qpipe_create_db': '## Step 3.2: Do you want to create MYSQL database?',
        'qpipe_populate_db': '## Step 3.3: Do you want to populate the MYSQL database?',
        'curation': '###### Step 4: Do you want to enter curation?',
        'vismooc_extensions': '###### Step 5: Do you want to enter vismooc extensions?',
        'vismooc_process': '## Step 5.1: Do you want to generate vismooc extensions csv?',
        'vismooc_populate': '## Step 5.2: Do you want to populate vismooc extensions into moocdb?',
        'newmitx_extensions': '###### Step 6: Do you want to enter newmitx extensions?',
        'newmitx_process': '## Step 6.1: Do you want to generate newmitx extensions csv?',
        'newmitx_populate': '## Step 6.2: Do you want to populate newmitx extensions into moocdb?'
    }

    def __init__(self, path='./config/config.yml'):
        # Parse YAML file and check validity
        self.cfg = yaml.safe_load(open(path))
        self.validity = self.check()
        if self.validity:
            self.pre_process()

    def check(self):
        # Check whether the structure of cfg is valid
        return self.dict_structure(self.cfg) == self.CONFIG_STRUCTURE

    def dict_structure(self, d):
        # Extract out the structure of dict cfg to
        # compare with the legal structure
        if isinstance(d, dict):
            return {k: self.dict_structure(d[k]) for k in d}
        else:
            # Replace all non-dict values with None.
            return None

    def is_valid(self):
        return self.validity

    def pre_process(self):
        # pre-process the fundamental dirs
        self.cfg['data_file']['data_dir'] = os.path.abspath(
            self.cfg['data_file']['data_dir']
        )
        self.cfg['mysql_script_path']['MLC_dir'] = os.path.abspath(
            self.cfg['mysql_script_path']['MLC_dir']
        )

        # pre-process course path
        self.cfg['data_file']['course_dir'] = os.path.join(
            self.cfg['data_file']['data_dir'],
            self.cfg['data_file']['course_folder'] + '/'
        )
        self.cfg['data_file']['log_data_dir'] = os.path.join(
            self.cfg['data_file']['course_dir'],
            self.cfg['data_file']['log_data_folder'] + '/'
        )
        self.cfg['data_file']['vismooc_data_dir'] = os.path.join(
            self.cfg['data_file']['course_dir'],
            self.cfg['data_file']['log_data_folder'] + '/',
            self.cfg['data_file']['vismooc_data_folder'] + '/'
        )
        self.cfg['data_file']['new_mitx_data_dir'] = os.path.join(
            self.cfg['data_file']['course_dir'],
            self.cfg['data_file']['log_data_folder'] + '/',
            self.cfg['data_file']['new_mitx_data_folder'] + '/'
        )

        # pre-process intermediary CSV paths
        sql_file_prefix = self.cfg['data_file']['log_file'] + '.sql_'
        self.cfg['csv_path']['intermediary_csv_dir'] = os.path.join(
            self.cfg['data_file']['data_dir'],
            self.cfg['data_file']['course_folder'],
            self.cfg['csv_path']['intermediary_csv_dir'] + '/'
        )
        self.cfg['csv_path']['edx_track_event_path'] = os.path.join(
            self.cfg['csv_path']['intermediary_csv_dir'],
            sql_file_prefix + self.cfg['csv_path']['edx_track_event_name'],
        )
        self.cfg['csv_path']['correct_map_path'] = os.path.join(
            self.cfg['csv_path']['intermediary_csv_dir'],
            sql_file_prefix + self.cfg['csv_path']['correct_map_name'],
        )
        self.cfg['csv_path']['answer_path'] = os.path.join(
            self.cfg['csv_path']['intermediary_csv_dir'],
            sql_file_prefix + self.cfg['csv_path']['answer_name'],
        )

        # pre-process moocdb CSV paths
        self.cfg['csv_path']['moocdb_csv_dir'] = os.path.join(
            self.cfg['data_file']['data_dir'],
            self.cfg['data_file']['course_folder'],
            self.cfg['csv_path']['moocdb_csv_dir'] + '/'
        )
        self.cfg['csv_path']['resource_hierarchy_path'] = os.path.join(
            self.cfg['csv_path']['moocdb_csv_dir'],
            self.cfg['csv_path']['resource_hierarchy_name'],
        )
        self.cfg['csv_path']['problem_hierarchy_path'] = os.path.join(
            self.cfg['csv_path']['moocdb_csv_dir'],
            self.cfg['csv_path']['problem_hierarchy_name'],
        )

        # pre-process MySQL script paths
        self.cfg['mysql_script_path']['qpipe_create_db_path'] = os.path.join(
            self.cfg['mysql_script_path']['MLC_dir'],
            self.cfg['mysql_script_path']['edx_pipe_folder'] + '/',
            self.cfg['mysql_script_path']['qpipe_folder'] + '/',
            self.cfg['mysql_script_path']['qpipe_create_db_script']
        )
        self.cfg['mysql_script_path']['qpipe_copy_db_path'] = os.path.join(
            self.cfg['mysql_script_path']['MLC_dir'],
            self.cfg['mysql_script_path']['edx_pipe_folder'] + '/',
            self.cfg['mysql_script_path']['qpipe_folder'] + '/',
            self.cfg['mysql_script_path']['qpipe_copy_db_script']
        )
        self.cfg['mysql_script_path']['vismooc_extensions_import_path'] = os.path.join(
            self.cfg['mysql_script_path']['MLC_dir'],
            self.cfg['mysql_script_path']['vismooc_extensions_folder'] + '/',
            self.cfg['mysql_script_path']['vismooc_extensions_import_script']
        )
        self.cfg['mysql_script_path']['newmitx_extensions_import_path'] = os.path.join(
            self.cfg['mysql_script_path']['MLC_dir'],
            self.cfg['mysql_script_path']['newmitx_extensions_folder'] + '/',
            self.cfg['mysql_script_path']['newmitx_extensions_import_script']
        )

    def get_csv_path(self):
        return self.cfg['csv_path']

    def get_mysql_script_path(self):
        return self.cfg['mysql_script_path']

    def get_csv_parsing(self):
        return self.cfg['csv_parsing']

    def get_data_file(self):
        return self.cfg['data_file']

    def get_open_edx_spec(self):
        return self.cfg['open_edx_spec']

    def get_or_query_mysql(self):
        cfg_mysql = self.cfg['mysql']
        if cfg_mysql['query_user']:
            cfg_mysql['user'] = raw_input('Enter your username for MySQL: ')
        if cfg_mysql['query_password']:
            cfg_mysql['password'] = getpass.getpass('Enter corresponding password of user %s: ' % cfg_mysql['user'])
        if cfg_mysql['query_database']:
            cfg_mysql['database'] = raw_input('Enter the database name: ')
        credential_list = [
            'host',
            'port',
            'user',
            'password',
            'database'
        ]
        return {k: cfg_mysql[k] for k in credential_list if k in cfg_mysql}

    def get_or_query_pipeline(self, pipeline_name, default='y'):
        '''
        Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        '''
        valid = {"yes": True, "y": True, "no": False, "n": False}
        prompt = " (default: %s) [y/n] " % default
        query = self.cfg['pipeline']['query']
        try:
            if not query:
                if len(pipeline_name.split(':')) == 1:
                    is_queued = self.cfg['pipeline'][pipeline_name]
                else:
                    is_queued = self.cfg['pipeline'][pipeline_name.split(':')[0]][pipeline_name.split(':')[1]]
                if isinstance(is_queued, dict):
                    is_queued = any(list(is_queued.values()))
                if is_queued:
                    # Transform query to instruction
                    message = self.pipeline_MESSAGE[pipeline_name.rsplit(':', 1)[-1]][:-1] + '.'
                    message = ''.join([message.rsplit('Do you want to ', -1)[0],
                                       message.rsplit('Do you want to ', -1)[-1][0].capitalize() +
                                       message.rsplit('Do you want to ', -1)[-1][1:]])
                    print(message)
                return is_queued
            else:
                while True:
                    sys.stdout.write(self.pipeline_MESSAGE[pipeline_name.rsplit(':', 1)[-1]]
                                     + prompt)
                    choice = raw_input().lower()
                    if default is not None and choice == '':
                        return valid[default]
                    elif choice in valid:
                        return valid[choice]
                    else:
                        sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
        except KeyError as e:
            print ('Unrecognized pipeline name. Error message: %s' % str(e))
