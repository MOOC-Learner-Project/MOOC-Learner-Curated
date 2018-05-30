CREATE_SCRIPT_DICT = {
    'video_axis': '''CREATE TABLE IF NOT EXISTS video_axis (
video_id varchar(255) NOT NULL,
course_id varchar(255),
name varchar(255),
video_length INT,
youtube_id varchar(255),
index_chapter SMALLINT,
index_video SMALLINT,
category varchar(31),
chapter_name varchar(255),
PRIMARY KEY (video_id)
);''',
    'video_stats': '''CREATE TABLE IF NOT EXISTS video_stats (
video_id varchar(255) NOT NULL,
name varchar(255),
videos_viewed INT,
videos_watched INT,
index_chapter SMALLINT,
index_video SMALLINT,
chapter_name varchar(255),
PRIMARY KEY (video_id)
);''',
    'video_stats_day': '''CREATE TABLE IF NOT EXISTS video_stats_day (
user_id varchar(255) NOT NULL,
video_id varchar(255) NOT NULL,
_date DATE,
position FLOAT,
PRIMARY KEY (user_id, video_id, _date)
);''',
    'pc_day_totals': '''CREATE TABLE IF NOT EXISTS pc_day_totals (
user_id varchar(255) NOT NULL,
ndays_act INT,
nevents INT,
nvideo INT,
ntranscript INT,
nseek_video INT,
npause_video INT,
PRIMARY KEY (user_id)
);''',
    'person_course_day': '''CREATE TABLE IF NOT EXISTS person_course_day (
user_id varchar(255) NOT NULL,
_date DATE NOT NULL,
nvideo INT,
nseek_video INT,
nvideos_viewed INT,
nvideos_watched_sec FLOAT,
PRIMARY KEY (user_id, _date)
);''',
    'person_course_video_watched': '''CREATE TABLE IF NOT EXISTS person_course_video_watched (
original_user_id varchar(255) NOT NULL,
course_id varchar(255),
n_unique_videos_watched INT,
fract_total_videos_watched FLOAT,
viewed BOOLEAN,
certified BOOLEAN,
verified BOOLEAN,
PRIMARY KEY (original_user_id)
);''',
    'stats_activity_by_day': '''CREATE TABLE IF NOT EXISTS stats_activity_by_day (
_date DATE NOT NULL,
nevents INT,
nvideo INT,
ntranscript INT,
nseek_video INT,
npause_video INT,
PRIMARY KEY (_date)
);''',
    'stats_overall': '''CREATE TABLE IF NOT EXISTS stats_overall (
course_id varchar(255) NOT NULL,
registered_sum INT,
nregistered_active INT,
n_unregistered INT,
viewed_sum INT,
explored_sum INT,
certified_sum INT,
n_male INT,
n_female INT,
n_verified_id INT,
verified_viewed INT,
verified_explored INT,
verified_certified INT,
verified_n_male INT,
verified_n_female INT,
nplay_video_sum INT,
nchapters_avg FLOAT,
ndays_act_sum INT,
nevents_sum INT,
nforum_posts_sum INT,
min_start_time TIMESTAMP,
max_last_event TIMESTAMP,
max_nchapters INT,
nforum_votes_sum INT,
nforum_endorsed_sum INT,
nforum_threads_sum INT,
nforum_commments_sum INT,
nforum_pinned_sum INT,
nprogcheck_avg FLOAT,
verified_nprogcheck FLOAT,
nshow_answer_sum INT,
nseq_goto_sum INT,
npause_video_sum INT,
avg_of_avg_dt FLOAT,
avg_of_sum_dt FLOAT,
n_have_ip INT,
n_missing_cc INT,
PRIMARY KEY (course_id)
);''',
    'time_on_task': '''CREATE TABLE IF NOT EXISTS time_on_task (
user_id varchar(255) NOT NULL,
_date DATE NOT NULL,
total_time_5 FLOAT,
total_time_30 FLOAT,
total_video_time_5 FLOAT,
total_video_time_30 FLOAT,
serial_video_time_30 FLOAT,
PRIMARY KEY (user_id, _date)
);''',
    'time_on_task_totals': '''CREATE TABLE IF NOT EXISTS time_on_task_totals (
user_id varchar(255) NOT NULL,
total_time_5 FLOAT,
total_time_30 FLOAT,
total_video_time_5 FLOAT,
total_video_time_30 FLOAT,
serial_video_time_30 FLOAT,
PRIMARY KEY (user_id)
);''',
    'user_info_combo': '''CREATE TABLE IF NOT EXISTS user_info_combo (
user_id varchar(255) NOT NULL,
orignial_user_id varchar(255) NOT NULL,
last_login TIMESTAMP,
date_joined TIMESTAMP,
enrollment_course_id varchar(255),
enrollment_created TIMESTAMP,
enrollment_is_active BOOLEAN,
enrollment_mode varchar(31),
PRIMARY KEY (user_id),
INDEX (user_id, orignial_user_id)
);'''

}


def IMPORT_SCRIPT_DICT(table):
    return '''LOAD DATA local INFILE 'MOOCDB_DIR/%s.csv'
IGNORE INTO TABLE %s
FIELDS TERMINATED BY ',' ENCLOSED BY '"';''' % (table, table)
