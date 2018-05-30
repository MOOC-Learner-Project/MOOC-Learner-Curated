from __future__ import print_function

import csv
import pandas as pd


class CSVExtractor(object):
    """
    Loads data from CSV export of the Stanford datastage tables
    """
    # TODO How can we sure these field names are synchronized with the Stanford datastage format
    ANSWER_FIELDNAMES = ['answer_id', 'problem_id', 'answer', 'course_id']
    CORRECT_MAP_FIELDNAMES = [
        'correct_map_id', 'answer_identifier', 'correctness', 'npoints', 'msg',
        'hint', 'hintmode', 'queustate'
    ]
    EDX_TRACK_EVENT_FIELDNAMES = [
        '_id', 'event_id', 'agent', 'event_source', 'event_type', 'ip', 'page',
        'session', 'time', 'anon_screen_name', 'downtime_for', 'student_id',
        'instructor_id', 'course_id', 'course_display_name',
        'resource_display_name', 'organization', 'sequence_id', 'goto_from',
        'goto_dest', 'problem_id', 'problem_choice', 'question_location',
        'submission_id', 'attempts', 'long_answer', 'student_file',
        'can_upload_file', 'feedback', 'feedback_response_selected',
        'transcript_id', 'transcript_code', 'rubric_selection',
        'rubric_category', 'video_id', 'video_code', 'video_current_time',
        'video_speed', 'video_old_time', 'video_new_time', 'video_seek_type',
        'video_new_speed', 'video_old_speed', 'book_interaction_type',
        'success', 'answer_id', 'hint', 'hintmode', 'msg', 'npoints',
        'queuestate', 'orig_score', 'new_score', 'orig_total', 'new_total',
        'event_name', 'group_user', 'group_action', 'position',
        'badly_formatted', 'correctMap_fk', 'answer_fk', 'state_fk',
        'load_info_fk'
    ]

    def __init__(self, cfg_csv_path, cfg_csv_parsing):
        # Create a CSV reader for the EdxTrackEvent table
        events = open(cfg_csv_path['edx_track_event_path'])
        self.edx_track_event = csv.DictReader(
            events,
            fieldnames=self.EDX_TRACK_EVENT_FIELDNAMES,
            delimiter=',',
            quotechar=cfg_csv_parsing['quotechar'],
            escapechar=cfg_csv_parsing['escapechar'])
        try:
            pass
        except IOError as e:
            print('Unable to open EdxTrackEvent file : %s' %
                  cfg_csv_path['edx_track_event_path'])
            exit(1)

        # Load Answer and CorrectMap tables into pandas DataFrames,
        # indexed by the table's primary key.
        try:
            self.answer = pd.read_csv(
                cfg_csv_path['answer_path'],
                delimiter=',',
                quotechar=cfg_csv_parsing['quotechar'],
                escapechar=cfg_csv_parsing['escapechar'],
                index_col=0,
                names=self.ANSWER_FIELDNAMES,
                dtype='string')
            self.correct_map = pd.read_csv(
                cfg_csv_path['correct_map_path'],
                delimiter=',',
                quotechar=cfg_csv_parsing['quotechar'],
                escapechar=cfg_csv_parsing['escapechar'],
                index_col=0,
                names=self.CORRECT_MAP_FIELDNAMES,
                dtype='string')
        except Exception as e:
            print('Pandas is unable to load CSV due to error: %s' % str(e))
            exit(1)

    def __iter__(self):
        return self

    def next(self):
        event = self.edx_track_event.next()

        # Map information contained in datastage tables outside the Edx track event table
        # to the corresponding entries in the Edx track event table.
        # See get_foreign_values.
        self.get_foreign_values(event, 'answer_fk', ['answer'], self.answer)
        self.get_foreign_values(event, 'correctMap_fk',
                                ['answer_identifier', 'correctness'],
                                self.correct_map)
        return event

    def get_foreign_values(self, event, fkey_name, fval_names, dataframe):
        '''
        This method adds to the EdxTrackEvent row the relevant
        fields fetched from a foreign table.
        It performs the analog of a SQL join with fk_dict on foreign_key_name.

        In case of conflict (foreign field holding same information and having
        same name as local field), the local value is kept if non empty and
        overridden otherwise.

        foreign_key: value of the foreign key on which the join is performed
        fk_dict: dictionary mapping foreign keys to foreign values
        '''
        fkey = event.get(fkey_name, None)

        if fkey:
            try:
                frow = dataframe.loc[fkey]
                for name in fval_names:
                    # pandas uses nan as its default null value, which causes problems
                    # later when other functions interpret it as a non-null value.
                    # Thus the event field is only set on non-null values.
                    if not pd.isnull(frow.loc[name]):
                        event[name] = frow.loc[name]
            except Exception as e:
                print('Broken foreign key: %s\n Error: %s' % (fkey, str(e)))
        else:
            # If the foreign key is missing, set all foreign fields to ''
            for name in fval_names:
                event[name] = ''
