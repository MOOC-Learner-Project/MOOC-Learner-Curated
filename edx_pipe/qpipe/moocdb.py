'''The MOOCdb final schema that is used to generate corresponding csv files to
be imported into mysql is represented by the MOOCdb class.
'''
import csv
import os


class MOOCdb(object):
    '''Provides an interface to store data into a MOOCdb instance.
    The serialization may be MySQL or CSV'''
    # TODO: Determine a way to ensure this is consistent with the mysql creation / copy scripts
    # IMPORTANT: primary key should be the first specified for each table
    TABLES = {
        'observed_events': [
            'observed_event_id', 'user_id', 'url_id',
            'observed_event_timestamp', 'observed_event_duration',
            'observed_event_ip', 'observed_event_os', 'observed_event_agent',
            'observed_event_type', 'validity'
        ],
        'resources': [
            'resource_id', 'resource_name', 'resource_uri', 'resource_type_id',
            'resource_parent_id', 'resource_child_number',
            'resource_relevant_week', 'resource_release_timestamp'
        ],
        'resources_urls': ['resources_urls_id', 'resource_id', 'url_id'],
        'urls': ['url_id', 'url'],
        'resource_types':
        ['resource_type_id', 'resource_type_content', 'resource_type_medium'],
        'problems': [
            'problem_id', 'problem_name', 'problem_parent_id',
            'problem_child_number', 'problem_type_id',
            'problem_release_timestamp'
            'problem_soft_deadline', 'problem_hard_deadline',
            'problem_max_submission', 'problem_max_duration', 'problem_weight',
            'resource_id', 'problem_week'
        ],
        'submissions': [
            'submission_id', 'user_id', 'problem_id', 'submission_timestamp',
            'submission_attempt_number', 'submission_answer',
            'submission_is_submitted', 'submission_ip', 'submission_os',
            'submission_agent', 'validity'
        ],
        'assessments': [
            'assessment_id', 'submission_id', 'assessment_feedback',
            'assessment_grade', 'assessment_grade_with_penalty',
            'assessment_grader_id', 'assessment_timestamp'
        ],
        # problem_types appears tserializeo only be relevant for the coursera pipe
        'problem_types': ['problem_type_id', 'problem_type_name'],
        'os': ['os_id', 'os_name'],
        'agent': ['agent_id', 'agent_name'],
        'click_events': [
            'observed_event_id', 'course_id', 'user_id', 'video_id',
            'observed_event_timestamp', 'observed_event_type', 'url', 'code',
            'video_current_time', 'video_new_time', 'video_old_time',
            'video_new_speed', 'video_old_speed'
        ],
    }

    def __init__(self, moocdb_dir=''):
        self.csv_writers = {}
        self.create_csv_writers(moocdb_dir)

    def close(self):
        '''Closes all the contained CSVWriter objects to ensure data is flushed to disk.
        '''
        for _, csv_writer in self.csv_writers.iteritems():
            csv_writer.close()

    def create_csv_writers(self, moocdb_dir):
        '''Creates all the CSVWriter objects responsible for each moocdb table's corresponding
        csv file.
        '''
        for table_name in self.TABLES:
            self.csv_writers[table_name] = CSVWriter(
                os.path.join(moocdb_dir, table_name + '.csv'),
                self.TABLES[table_name])


class CSVWriter(object):
    '''This is a wrapper around csv.DictWriter that bundles the output file
    with a csv.DictWriter object together.
    '''

    def __init__(self, output_file, fields, escape='\\'):
        try:
            self.output = open(output_file, 'w')
            self.writer = csv.DictWriter(
                self.output,
                delimiter=',',
                fieldnames=fields,
                quotechar='"',
                escapechar=escape,
                lineterminator='\n')

        except IOError:
            print('[%s] Could not open file %s' %
                  (self.__class__.__name__, output_file))
            return

    def store(self, row):
        '''Writes row to open csv.DictWriter.
        '''
        self.writer.writerow(row)

    def close(self):
        '''Closes the open output file to ensure data is flushed to disk.
        '''
        self.output.close()
