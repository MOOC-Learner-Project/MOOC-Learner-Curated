import os

import util as vismooc_util, courses, videos, grades, enrollments, users, forum


def process_vismooc(cfg_csv_path, cfg_data_file):
    print('Output directory: %s' % cfg_csv_path['moocdb_csv_dir'])
    print('Generating %s csv for vismooc extensions' % cfg_data_file['course_folder'])
    course_structure = vismooc_util.load_json(
        os.path.join(cfg_data_file['vismooc_data_dir'], cfg_data_file['vismooc_file']['course_structure_file']))
    courses_path = os.path.join(cfg_csv_path['moocdb_csv_dir'], 'courses.csv')
    courses.write_courses_csv(course_structure, courses_path)

    # The course_video and videos csvs are grouped because they
    # read from the same Edx course data files
    course_video_path = os.path.join(cfg_csv_path['moocdb_csv_dir'], 'course_video.csv')
    videos_path = os.path.join(cfg_csv_path['moocdb_csv_dir'], 'videos.csv')
    videos.write_video_csvs(course_structure, course_video_path, videos_path)

    certificate_path = os.path.join(cfg_data_file['vismooc_data_dir'],
                                    cfg_data_file['vismooc_file']['course_certificates_file'])
    grades_path = os.path.join(cfg_csv_path['moocdb_csv_dir'], 'grades.csv')
    vismooc_util.load_table_and_write_simple_csv(
        certificate_path, grades_path,
        grades.get_csv_fields(), grades.get_csv_field_to_func_map())

    course_enrollments_path = os.path.join(cfg_data_file['vismooc_data_dir'],
                                           cfg_data_file['vismooc_file']['course_enrollment_file'])
    enrollments_path = os.path.join(cfg_csv_path['moocdb_csv_dir'], 'enrollments.csv')
    vismooc_util.load_table_and_write_simple_csv(
        course_enrollments_path, enrollments_path,
        enrollments.get_csv_fields(),
        enrollments.get_csv_field_to_func_map())

    course_user_path = os.path.join(cfg_data_file['vismooc_data_dir'],
                                    cfg_data_file['vismooc_file']['course_user_file'])
    profile_path = os.path.join(cfg_data_file['vismooc_data_dir'],
                                cfg_data_file['vismooc_file']['course_profile_file'])
    users_path = os.path.join(cfg_csv_path['moocdb_csv_dir'], 'users.csv')
    users.write_users_csv(course_user_path, profile_path, users_path)

    edx_forum_path = os.path.join(os.path.join(cfg_data_file['vismooc_data_dir'],
                                               cfg_data_file['vismooc_file']['course_forum_file']))
    forum_path = os.path.join(cfg_csv_path['moocdb_csv_dir'], 'forum.csv')
    forum.write_forum_csv(edx_forum_path, forum_path)