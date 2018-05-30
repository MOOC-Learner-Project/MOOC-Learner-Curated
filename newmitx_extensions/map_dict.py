from process import report
import hashlib

def UNIT_MAP_IDENTICAL(x):
    return x


def UNIT_MAP_CONVERT_BOOL_TO_TINYINT(x):
    if x:
        return 1
    else:
        return 0

def UNIT_MAP_HASH_USERNAME(x):
    oneHash = hashlib.new('ripemd160')
    oneHash.update(x)
    return oneHash.hexdigest()


PRE_MAP_DICT = {
    'video_axis': [
        (
            (2, 2),
            'video_axis',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'video_stats': [
        (
            (2, 2),
            'video_stats',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'video_stats_day': [
        (
            (0, 0),
            'video_stats_day',
            {
                u'video_id': u'video_id',
                u'date': u'date',
                u'position': u'position',
            }
        ),
        (
            (0, 1),
            'video_stats_day',
            {
                u'user_id': lambda d: UNIT_MAP_HASH_USERNAME(d[u'username'])
                if u'username' in d
                else report(d, u'username'),
            }
        )
    ],
    'pc_day_totals': [
        (
            (0, 0),
            'pc_day_totals',
            {
                u'ndays_act': u'ndays_act',
                u'nevents': u'nevents',
                u'nvideo': u'nvideo',
                u'ntranscript': u'ntranscript',
                u'nseek_video': u'nseek_video',
                u'npause_video': u'npause_video',
            }
        ),
        (
            (0, 1),
            'pc_day_totals',
            {
                u'user_id': lambda d: UNIT_MAP_HASH_USERNAME(d[u'username'])
                if u'username' in d
                else report(d, u'username'),
            }
        )
    ],
    'person_course_day': [
        (
            (0, 0),
            'person_course_day',
            {
                u'date': u'date',
                u'nvideo': u'nvideo',
                u'nseek_video': u'nseek_video',
                u'nvideos_viewed': u'nvideos_viewed',
                u'nvideos_watched_sec': u'nvideos_watched_sec',
            }
        ),
        (
            (0, 1),
            'person_course_day',
            {
                u'user_id': lambda d: UNIT_MAP_HASH_USERNAME(d[u'username'])
                if u'username' in d
                else report(d, u'username'),
            }
        )
    ],
    'person_course_video_watched': [
        (
            (0, 0),
            'person_course_video_watched',
            {
                u'original_user_id': u'user_id',
                u'course_id': u'course_id',
                u'n_unique_videos_watched': u'n_unique_videos_watched',
                u'fract_total_videos_watched': u'fract_total_videos_watched',
            }
        ),
        (
            (0, 1),
            'person_course_video_watched',
            {
                u'viewed': lambda d: UNIT_MAP_CONVERT_BOOL_TO_TINYINT(d[u'viewed'])
                if u'viewed' in d
                else report(d, u'viewed'),
                u'certified': lambda d: UNIT_MAP_CONVERT_BOOL_TO_TINYINT(d[u'certified'])
                if u'certified' in d
                else report(d, u'certified'),
                u'verified': lambda d: UNIT_MAP_CONVERT_BOOL_TO_TINYINT(d[u'verified'])
                if u'verified' in d
                else report(d, u'verified'),
            }
        )
    ],
    'stats_activity_by_day': [
        (
            (0, 0),
            'stats_activity_by_day',
            {
                u'date': u'date',
                u'nevents': u'nevents',
                u'nvideo': u'nvideo',
                u'ntranscript': u'ntranscript',
                u'nseek_video': u'nseek_video',
                u'npause_video': u'npause_video',
            }
        )
    ],
    'stats_overall': [
        (
            (2, 2),
            'stats_overall',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'time_on_task': [
        (
            (0, 0),
            'time_on_task',
            {
                u'date': u'date',
                u'total_time_5': u'total_time_5',
                u'total_time_30': u'total_time_30',
                u'total_video_time_5': u'total_video_time_5',
                u'total_video_time_30': u'total_video_time_30',
                u'serial_video_time_30': u'serial_video_time_30',
            }
        ),
        (
            (0, 1),
            'time_on_task',
            {
                u'user_id': lambda d: UNIT_MAP_HASH_USERNAME(d[u'username'])
                if u'username' in d
                else report(d, u'username'),
            }
        )
    ],
    'time_on_task_totals': [
        (
            (0, 0),
            'time_on_task_totals',
            {
                u'total_time_5': u'total_time_5',
                u'total_time_30': u'total_time_30',
                u'total_video_time_5': u'total_video_time_5',
                u'total_video_time_30': u'total_video_time_30',
                u'serial_video_time_30': u'serial_video_time_30',
            }
        ),
        (
            (0, 1),
            'time_on_task_totals',
            {
                u'user_id': lambda d: UNIT_MAP_HASH_USERNAME(d[u'username'])
                if u'username' in d
                else report(d, u'username'),
            }
        )
    ],
    'user_info_combo': [
        (
            (0, 0),
            'user_info_combo',
            {
                u'original_user_id': u'user_id',
                u'last_login': u'last_login',
                u'date_joined': u'date_joined',
                u'enrollment_course_id': u'enrollment_course_id',
                u'enrollment_created': u'enrollment_created',
                u'enrollment_is_active': u'enrollment_is_active',
                u'enrollment_mode': u'enrollment_mode',

            }
        ),
        (
            (0, 1),
            'user_info_combo',
            {
                u'user_id': lambda d: UNIT_MAP_HASH_USERNAME(d[u'username'])
                if u'username' in d
                else report(d, u'username'),
            }
        )
    ]
}

POST_MAP_DICT = {
    'video_axis': [
        (
            (2, 2),
            'video_axis',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'video_stats': [
        (
            (2, 2),
            'video_stats',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'video_stats_day': [
        (
            (2, 2),
            'video_stats_day',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'pc_day_totals': [
        (
            (2, 2),
            'pc_day_totals',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'person_course_day': [
        (
            (2, 2),
            'person_course_day',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'person_course_video_watched': [
        (
            (2, 2),
            'person_course_video_watched',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'stats_activity_by_day': [
        (
            (2, 2),
            'stats_activity_by_day',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'stats_overall': [
        (
            (2, 2),
            'stats_overall',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'time_on_task': [
        (
            (2, 2),
            'time_on_task',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'time_on_task_totals': [
        (
            (2, 2),
            'time_on_task_totals',
            UNIT_MAP_IDENTICAL,
        )
    ],
    'user_info_combo': [
        (
            (2, 2),
            'user_info_combo',
            UNIT_MAP_IDENTICAL,
        )
    ]
}