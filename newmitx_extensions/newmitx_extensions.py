import fileinput
from process import loading, mapping, concatenating, saving, typedict
from map_dict import PRE_MAP_DICT, POST_MAP_DICT
from script_dict import CREATE_SCRIPT_DICT, IMPORT_SCRIPT_DICT

FILE_INPUT = {
    'video_axis': None,
    'video_stats': None,
    'video_stats_day': None,
    'pc_day_totals': None,
    'person_course_day': None,
    'person_course_video_watched': None,
    'stats_activity_by_day': None,
    'stats_overall': None,
    'time_on_task': None,
    'time_on_task_totals': None,
    'user_info_combo': None,
}

FILE_OUTPUT = {
    'video_axis': 'video_axis.csv',
    'video_stats': 'video_stats.csv',
    'video_stats_day': 'video_stats_day.csv',
    'pc_day_totals': 'pc_day_totals.csv',
    'person_course_day': 'person_course_day.csv',
    'person_course_video_watched': 'person_course_video_watched.csv',
    'stats_activity_by_day': 'stats_activity_by_day.csv',
    'stats_overall': 'stats_overall.csv',
    'time_on_task': 'time_on_task.csv',
    'time_on_task_totals': 'time_on_task_totals.csv',
    'user_info_combo': 'user_info_combo.csv',
}

OUTPUT_FIELDS = {
    'video_axis': [
        u'video_id',
        u'course_id',
        u'name',
        u'video_length',
        u'youtube_id',
        u'index_chapter',
        u'index_video',
        u'category',
        u'chapter_name',
    ],
    'video_stats': [
        u'video_id',
        u'name',
        u'videos_viewed',
        u'videos_watched',
        u'index_chapter',
        u'index_video',
        u'chapter_name',
    ],
    'video_stats_day': [
        u'user_id',
        u'video_id',
        u'date',
        u'position'
    ],
    'pc_day_totals': [
        u'user_id',
        u'ndays_act',
        u'nevents',
        u'nvideo',
        u'ntranscript',
        u'nseek_video',
        u'npause_video',
    ],
    'person_course_day': [
        u'user_id',
        u'date',
        u'nvideo',
        u'nseek_video',
        u'nvideos_viewed',
        u'nvideos_watched_sec'
    ],
    'person_course_video_watched': [
        u'original_user_id',
        u'course_id',
        u'n_unique_videos_watched',
        u'fract_total_videos_watched',
        u'viewed',
        u'certified',
        u'verified',
    ],
    'stats_activity_by_day': [
        u'date',
        u'nevents',
        u'nvideo',
        u'ntranscript',
        u'nseek_video',
        u'npause_video',
    ],
    'stats_overall': [
        u'course_id',
        u'registered_sum',
        u'nregistered_active',
        u'n_unregistered',
        u'viewed_sum',
        u'explored_sum',
        u'certified_sum',
        u'n_male',
        u'n_female',
        u'n_verified_id',
        u'verified_viewed',
        u'verified_explored',
        u'verified_certified',
        u'verified_n_male',
        u'verified_n_female',
        u'nplay_video_sum',
        u'nchapters_avg',
        u'ndays_act_sum',
        u'nevents_sum',
        u'nforum_posts_sum',
        u'min_start_time',
        u'max_last_event',
        u'max_nchapters',
        u'nforum_votes_sum',
        u'nforum_endorsed_sum',
        u'nforum_threads_sum',
        u'nforum_commments_sum',
        u'nforum_pinned_sum',
        u'nprogcheck_avg',
        u'verified_nprogcheck',
        u'nshow_answer_sum',
        u'nseq_goto_sum',
        u'npause_video_sum',
        u'avg_of_avg_dt',
        u'avg_of_sum_dt',
        u'n_have_ip',
        u'n_missing_cc',
    ],
    'time_on_task': [
        u'user_id',
        u'date',
        u'total_time_5',
        u'total_time_30',
        u'total_video_time_5',
        u'total_video_time_30',
        u'serial_video_time_30',
    ],
    'time_on_task_totals': [
        u'user_id',
        u'total_time_5',
        u'total_time_30',
        u'total_video_time_5',
        u'total_video_time_30',
        u'serial_video_time_30',
    ],
    'user_info_combo': [
        u'user_id',
        u'original_user_id',
        u'last_login',
        u'date_joined',
        u'enrollment_course_id',
        u'enrollment_created',
        u'enrollment_is_active',
        u'enrollment_mode',
    ]
}


def process_newmitx(cfg_csv_path, cfg_data_file, cfg_mysql_script_path):
    print('Output directory: %s' % cfg_csv_path['moocdb_csv_dir'])
    print('Generating %s csv for newmitx extensions' % cfg_data_file['course_folder'])
    global FILE_INPUT

    FILE_INPUT['video_axis'] = cfg_data_file['newmitx_file']['course_video_axis_file']
    FILE_INPUT['video_stats'] = cfg_data_file['newmitx_file']['course_video_stats_file']
    FILE_INPUT['video_stats_day'] = cfg_data_file['newmitx_file']['course_video_stats_day_file']
    FILE_INPUT['pc_day_totals'] = cfg_data_file['newmitx_file']['course_pc_day_totals_file']
    FILE_INPUT['person_course_day'] = cfg_data_file['newmitx_file']['course_person_course_day_file']
    FILE_INPUT['person_course_video_watched'] = cfg_data_file['newmitx_file']['course_person_course_video_watched_file']
    FILE_INPUT['stats_activity_by_day'] = cfg_data_file['newmitx_file']['course_stats_activity_by_day_file']
    FILE_INPUT['stats_overall'] = cfg_data_file['newmitx_file']['course_stats_overall_file']
    FILE_INPUT['time_on_task'] = cfg_data_file['newmitx_file']['course_time_on_task_file']
    FILE_INPUT['time_on_task_totals'] = cfg_data_file['newmitx_file']['course_time_on_task_totals_file']
    FILE_INPUT['user_info_combo'] = cfg_data_file['newmitx_file']['course_user_info_combo_file']

    for table in FILE_INPUT:
        if FILE_INPUT[table] is None:
            FILE_OUTPUT.pop(table, None)
            PRE_MAP_DICT.pop(table, None)
            POST_MAP_DICT.pop(table, None)
            OUTPUT_FIELDS.pop(table, None)

    FILE_INPUT = {table: FILE_INPUT[table]
                  for table in FILE_INPUT
                  if FILE_INPUT[table] is not None}

    with open(cfg_mysql_script_path['newmitx_extensions_import_path'], 'w') as script:
        script.write('''CREATE DATABASE IF NOT EXISTS DB_NAME;
USE DB_NAME;
SET @@global.local_infile = 1;
SET @original_sql_mode = @@SESSION.sql_mode;
SET SESSION sql_mode = '';\n\n''')
        for table in FILE_INPUT:
            script.write(CREATE_SCRIPT_DICT[table]+'\n\n')
            script.write(IMPORT_SCRIPT_DICT(table)+'\n\n')
        script.write('''SET SESSION sql_mode = @original_sql_mode;\n''')

    saving(cfg_csv_path['moocdb_csv_dir'],
           FILE_OUTPUT,
           concatenating(
               mapping(
                   concatenating(
                       mapping(
                           loading(
                               cfg_data_file['new_mitx_data_dir'],
                               FILE_INPUT
                           ),
                           PRE_MAP_DICT
                       )
                   ),
                   POST_MAP_DICT
               )
           ),
           OUTPUT_FIELDS
           )
    print("Reported missing field types: %s" % str(typedict))
    print("Total number of missing fiedls: %d" % sum(list(typedict.values())))