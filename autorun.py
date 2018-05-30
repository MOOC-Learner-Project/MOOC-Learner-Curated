# /usr/bin/env python
import sys
import os
import argparse
import subprocess
import tempfile
import getpass
import yaml

# The purpose of this script is to recognize the MLC data file trees
# and/or (serving as an entry-point) to config and run MLC automatically
# to populate the event data of all courses into a common database (or several databases).
# TODO: Extend MLC and MLQ autorun to work with multiple databases.

MOOCDB_CONFIG_SUB_STRUCTURE = {
    "MOOCdb": {
        "database": None,
        "work_dir": None,
        "MLC_folder": None
    },
    "mysql": {
        "host": None,
        "password": None,
        "port": None,
        "user": None
    },
    "full_pipeline": {
        "MLC": None
    },
    "MLC_pipeline": {
        "apipe": None,
        "qpipe": {
            "qpipe_create_db": None,
            "qpipe_process_events": None,
            "qpipe_populate_db": None
        },
        "folder_setup": None,
        "curation": None,
        "vismooc_extensions": {
            "vismooc_process": None,
            "vismooc_populate": None
        },
        "newmitx_extensions": {
            "newmitx_process": None,
            "newmitx_populate": None
        },
    },
    "data_file": {
        "course_name_prefix": None,
        "data_dir": None,
        "log_file": None,
        "vismooc_file": {
            "course_forum_file": None,
            "course_structure_file": None,
            "course_certificates_file": None,
            "course_enrollment_file": None,
            "course_profile_file": None,
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
}

DEFAULT_DATA_FILE_SUFFIX = {'log_file': 'log_data.json',
                            'vismooc_file': {
                                'course_structure_file': 'course_structure-prod-analytics.json',
                                'course_certificates_file': 'certificates_generatedcertificate-prod-analytics.sql',
                                'course_enrollment_file': 'student_courseenrollment-prod-analytics.sql',
                                'course_user_file': 'auth_user-prod-analytics.sql',
                                'course_profile_file': 'auth_userprofile-prod-analytics.sql',
                                'course_forum_file': 'prod.mongo',
                            },
                            'newmitx_file': {
                                'course_video_axis_file': 'video_axis.json',
                                'course_video_stats_file': 'video_stats.json',
                                "course_video_stats_day_file": 'video_stats_day.json',
                                "course_pc_day_totals_file": 'pc_day_totals.json',
                                'course_person_course_day_file': 'person_course_day.json',
                                "course_person_course_video_watched_file": 'person_course_video_watched.json',
                                "course_stats_activity_by_day_file": 'stats_activity_by_day.json',
                                "course_stats_overall_file": 'stats_overall.json',
                                "course_time_on_task_file": 'time_on_task.json',
                                "course_time_on_task_totals_file": 'time_on_task_totals.json',
                                "course_user_info_combo_file": 'user_info_combo.json',
                            },
}

DEFAULT_PIPELINE = {
    "apipe": True,
    "qpipe": {
        "qpipe_create_db": True,
        "qpipe_process_events": True,
        "qpipe_populate_db": True
    },
    "query": False,
    "curation": True,
    "folder_setup": True,
    "vismooc_extensions": {
        "vismooc_process": False,
        "vismooc_populate": False
    },
    "newmitx_extensions": {
        "newmitx_process": False,
        "newmitx_populate": False
    },
}

MLC_CONFIG_TEMPLATE = {
    "open_edx_spec": {
        "video_id_spec": None
    },
    "mysql": {
        "query_user": False,
        "database": None,
        "query_password": False,
        "host": "localhost",
        "user": None,
        "query_database": False,
        "password": None,
        "port": None
    },
    "data_file": {
        "data_dir": None,
        "log_data_folder": "log_data",
        "vismooc_data_folder": "vismooc",
        "new_mitx_data_folder": "newmitx",
    },
    "csv_path": {
        "edx_track_event_name": "EdxTrackEventTable.csv",
        "moocdb_csv_dir": "moocdb_csv",
        "correct_map_name": "CorrectMapTable.csv",
        "resource_hierarchy_name": "resource_hierarchy.org",
        "problem_hierarchy_name": "problem_hierarchy.org",
        "intermediary_csv_dir": "intermediary_csv",
        "answer_name": "AnswerTable.csv"
    },
    "mysql_script_path": {
        "apipe_folder": "apipe",
        "qpipe_copy_db_script": "copy_to_mysqlDB.sql",
        "vismooc_extensions_folder": "vismooc_extensions",
        "newmitx_extensions_folder": "newmitx_extensions",
        "qpipe_create_db_script": "create_mysqlDB.sql",
        "qpipe_folder": "qpipe",
        "edx_pipe_folder": "edx_pipe",
        "MLC_dir": None,
        "vismooc_extensions_import_script": "import_vismooc_to_moocdb.sql",
        "newmitx_extensions_import_script": "import_newmitx_to_moocdb.sql",
        "curation_folder": "curation"
    },
    "csv_parsing": {
        "quotechar": "'",
        "escapechar": "\\",
        "timestamp_format": [
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f %Z"
        ]
    }
}


class FileNotComplete(Exception):
    pass


def dict_structure(d):
    # Extract out the structure of dict cfg to
    # compare with the legal structure
    if isinstance(d, dict):
        return {k: dict_structure(d[k]) for k in d}
    else:
        # Replace all non-dict values with None.
        return None


def db_config_check(sup_dict, sub_dict):
    return all(item in dict_structure(sup_dict).items()
               if not isinstance(item[1], dict)
               else db_config_check(sup_dict[item[0]], sub_dict[item[0]])
               for item in dict_structure(sub_dict).items())


def autorun():
    # Parse arguments
    parser = argparse.ArgumentParser('Recognize the MOOC-Learner-Curated data file tree then auto-config and run'
                                     'MLC automatically to populate the VisMOOC tables into one common database.')
    parser.add_argument('-c', action="store", default=None, dest='db_config_path',
                        help='path to MOOCdb config file')
    parser.add_argument('-x', action='store_true', default=False,
                        dest='is_select', help='manually select a subset of course to analyze')
    parser.add_argument("-s", action="store", default='../data/', dest='data_path',
                        help='path to data folder, default: folder data next to MLC')
    parser.add_argument("-t", action="store", default='.', dest='MLC_path', help='path to MLC, default: current folder')
    db_config_path = parser.parse_args().db_config_path

    # MOOCdb config
    if not db_config_path:
        is_select = parser.parse_args().is_select
        data_path = parser.parse_args().data_path
        MLC_path = parser.parse_args().MLC_path
        data_file_suffix = DEFAULT_DATA_FILE_SUFFIX
        MLC_CONFIG_TEMPLATE['mysql']['host'] = 'localhost'
        MLC_CONFIG_TEMPLATE['mysql']['port'] = 3306
        MLC_CONFIG_TEMPLATE['mysql']['user'] = raw_input('Enter your username for MySQL: ')
        MLC_CONFIG_TEMPLATE['mysql']['password'] = getpass.getpass('Enter corresponding password: ')
        MLC_CONFIG_TEMPLATE['mysql']['database'] = raw_input('Enter the database name: ')
        MLC_CONFIG_TEMPLATE['open_edx_spec']['video_id_spec'] = 'HKUSTx'
        MLC_CONFIG_TEMPLATE['pipeline'] = DEFAULT_PIPELINE
        db_cfg = {}
    else:
        db_config_path = os.path.abspath(db_config_path)
        if not os.path.isfile(db_config_path):
            sys.exit('Specified MOOCdb config file does not exist.')
        db_cfg = yaml.safe_load(open(db_config_path))
        if not db_config_check(db_cfg, MOOCDB_CONFIG_SUB_STRUCTURE):
            sys.exit('MOOCdb config file is invalid.')
        # Exit with code 0 if not queued
        if not db_cfg['full_pipeline']['MLC']:
            print('MLC is not queued, container exited.')
            exit(0)
        is_select = False
        data_path = db_cfg['data_file']['data_dir']
        MLC_path = os.path.join(
            db_cfg['MOOCdb']['work_dir'],
            db_cfg['MOOCdb']['MLC_folder'] + '/'
        )
        data_file_suffix = {
            k: db_cfg['data_file'][k]
            for k in db_cfg['data_file'] if k.endswith('_file')
        }
        # Docker bridge mode, code to git the host ip
        # MLC_CONFIG_TEMPLATE['mysql']['host'] = \
        # subprocess.check_output("route -n | awk \'/UG[ \t]/{print $2}\'", shell=True).strip()
        MLC_CONFIG_TEMPLATE['mysql']['host'] = db_cfg['mysql']['host']
        MLC_CONFIG_TEMPLATE['mysql']['port'] = db_cfg['mysql']['port']
        MLC_CONFIG_TEMPLATE['mysql']['user'] = db_cfg['mysql']['user']
        MLC_CONFIG_TEMPLATE['mysql']['password'] = db_cfg['mysql']['password']
        MLC_CONFIG_TEMPLATE['mysql']['database'] = db_cfg['MOOCdb']['database']
        MLC_CONFIG_TEMPLATE['open_edx_spec']['video_id_spec'] = \
            db_cfg['open_edx_spec']['video_id_spec']
        MLC_CONFIG_TEMPLATE['pipeline'] = db_cfg['MLC_pipeline']

    # Check data and MLC paths
    data_path = os.path.abspath(data_path)
    MLC_path = os.path.abspath(MLC_path)
    if not os.path.isdir(data_path):
        sys.exit('Data directory does not exist.')
    if not os.path.isdir(MLC_path):
        sys.exit('MLC directory does not exist.')

    # Retrieve course list and check the data file tree
    courses = next(os.walk(data_path))[1]
    if db_config_path and db_cfg['data_file']['course_name_prefix']:
        courses = [course for course in courses if course.startswith(db_cfg['data_file']['course_name_prefix'])]
    if not courses:
        sys.exit('No course found')
    courses_file = {}
    valid_courses = []
    for course in courses:
        try:
            course_path = os.path.join(data_path, course)
            content = next(os.walk(course_path))[1]
            log_path = os.path.abspath(os.path.join(course_path, "log_data/"))
            if not os.path.isdir(log_path):
                print('Course directory <%s> is not complete. Removed from course list.' % course)
                print('log_data folder is missing')
                print('')
                raise FileNotComplete
            # Search for data files
            data_file_dict = {}
            # Search for the tracking log file first
            data_files = [f for f in os.listdir(log_path)]
            for data_file in data_files:
                if data_file.endswith(data_file_suffix['log_file']):
                    data_file_dict['log_file'] = data_file
            # Searching for the extension data files
            for extension_name in data_file_suffix:
                if extension_name == 'log_file':
                    continue
                extension_name = extension_name[:-5]
                extension_pipe = extension_name + "_extensions"
                if extension_pipe not in MLC_CONFIG_TEMPLATE['pipeline']:
                    print('Unrecognized extension pipe %s.' % extension_name)
                    exit(0)
                if ((isinstance(MLC_CONFIG_TEMPLATE['pipeline'][extension_pipe], dict)
                     and
                         any(list(MLC_CONFIG_TEMPLATE['pipeline'][extension_pipe].values())))
                    or
                        (isinstance(MLC_CONFIG_TEMPLATE['pipeline'][extension_pipe], bool)
                         and
                             MLC_CONFIG_TEMPLATE['pipeline'][extension_pipe])):
                    extension_path = os.path.abspath(os.path.join(log_path, extension_name + "/"))
                    if not os.path.isdir(extension_path):
                        print('Course directory <%s> is not complete. Removed from course list.' % course)
                        print('extension file folder %s is missing' % extension_name)
                        print('')
                        raise FileNotComplete
                    extension_files = [f for f in os.listdir(extension_path)]
                    data_file_dict[extension_name + "_file"] = {}
                    for extension_file_name in data_file_suffix[extension_name + "_file"]:
                        extension_file_suffix = data_file_suffix[extension_name + "_file"][extension_file_name]
                        if extension_file_suffix is None:
                            data_file_dict[extension_name + "_file"][extension_file_name] = None
                            continue
                        for extension_file in extension_files:
                            if extension_file.endswith(extension_file_suffix):
                                data_file_dict[extension_name + "_file"][extension_file_name] = extension_file
                                continue
                    if not dict_structure(data_file_dict[extension_name + "_file"]) \
                            == dict_structure(data_file_suffix[extension_name + "_file"]):
                        print('Course directory <%s> is not complete. Removed from course list.' % course)
                        print('The following database files are missing: ' +
                              str(list(set(data_file_suffix[extension_name + "_file"]) -
                                       set(data_file_dict[extension_name + "_file"]))))
                        print('')
                        raise FileNotComplete
        except FileNotComplete:
            continue
        # Fill unnecessary and missing extension files in data_file_dict by nulls:
        for extension_name in data_file_suffix:
            if extension_name == 'log_file':
                continue
            extension_name = extension_name[:-5]
            if (extension_name + "_file") not in data_file_dict:
                data_file_dict[extension_name + "_file"] = {}
            for extension_file_name in data_file_suffix[extension_name + "_file"]:
                if extension_file_name not in data_file_dict[extension_name + "_file"]:
                    data_file_dict[extension_name + "_file"][extension_file_name] = None
        valid_courses.append(course)
        courses_file[course] = data_file_dict
    courses = valid_courses
    if not courses:
        sys.exit('No valid course found')

    # Check the MLC folder
    MLC_files = [f for f in os.listdir(MLC_path)]
    if 'full_pipe.py' not in MLC_files:
        sys.exit("MLC directory is not complete.")
    MLC_exec = os.path.join(MLC_path, 'full_pipe.py')

    # Select the subset of course to analyze if is_select
    if is_select:
        print("Find the following courses:")
        for n, course in enumerate(courses):
            print("[%d]: <%s>" % (n, course))
        id_dict = dict(enumerate(courses))
        while True:
            try:
                selected_courses = raw_input("Please indicate the selected courses "
                                             "by entering their ids, and split them by commas:")
                selected_courses = list(set(selected_courses.split(',')))
                selected_courses = map(int, selected_courses)
                selected_courses = [id_dict[x] for x in selected_courses]
                if selected_courses:
                    break
            except (ValueError, SyntaxError, NameError) as e:
                print("Invalid id found, error message: %s. Please re-enter." % str(e))
            except KeyError as e:
                print("Invalid id <%s> found. Please re-enter." % str(e))
        courses = selected_courses
        courses_file = {k: courses_file[k] for k in courses if k in courses_file.keys()}
    print("Selected courses: %s" % str(courses))

    # Finally set the two paths after check
    if db_config_path:
        MLC_CONFIG_TEMPLATE['pipeline']['query'] = False
    MLC_CONFIG_TEMPLATE['data_file']['data_dir'] = data_path
    MLC_CONFIG_TEMPLATE['mysql_script_path']['MLC_dir'] = MLC_path

    # Run MLC as subprocess
    for course in courses:
        print("Running MLC on course %s" % course)
        config_dict = MLC_CONFIG_TEMPLATE
        config_dict['data_file']['course_folder'] = course
        for data_file_name in courses_file[course]:
            config_dict['data_file'][data_file_name] = courses_file[course][data_file_name]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml') as config_file:
            yaml.dump(config_dict, config_file, default_flow_style=False)
            p = subprocess.Popen(sys.executable + ' -u ' + MLC_exec + ' ' + config_file.name,
                                 shell=True, stderr=subprocess.PIPE, bufsize=1)
            print("Process pid: %d" % p.pid)
            with p.stderr:
                for line in iter(p.stderr.readline, ''):
                    print(line)
            p.wait()


if __name__ == "__main__":
    autorun()
