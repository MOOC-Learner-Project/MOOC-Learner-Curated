'''Event classes and their variations.
'''
from __future__ import print_function

MAX_DURATION_MINUTES = 60
DEFAULT_DURATION_MINUTES = 2


class Event(object):
    '''
    Base event class which covers all the common event properties.
    '''

    def __init__(self, polished_event):
        self.data = polished_event
        self.duration = 0
        self.validity = 1

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data and \
                   self.duration == other.duration and \
                   self.validity == other.validity
        return False

    def __neq__(self, other):
        return not self.__eq__(other)

    def get_observed_event_row(self):
        '''
        Returns an array corresponding to a line in MOOCdb.observed_events.

        'event_type' and 'resource_id' fields are added, though not mentioned yet
        in MOOCdb specifications.

        Note that observed_event_id is *not* a unique identifier, since
        a user interaction may yield several rows in the intermediary DB.
        '''
        return {
            'observed_event_id': self['_id'],
            'user_id': self['anon_screen_name'],
            'url_id': self['resource_id'],
            'observed_event_timestamp': self['time'],
            'observed_event_duration': self.duration,
            'observed_event_ip': self['ip'],
            'observed_event_os': self['os'],
            'observed_event_agent': self['agent'],
            'observed_event_type': self['event_type'],
            'validity': self.validity
        }

    def __getitem__(self, key):
        '''
        Stringifies value for any found (key, value) pairs before
        returning it; otherwise returns None.
        '''
        item = self.data.get(key)
        if item is not None:
            return str(item)
        else:
            return None

    def set_data_attr(self, key, value):
        '''
        Only sets an attribute if value evaluates to True.
        '''
        if not value:
            return

        self.data[key] = value

    def get_uri(self):
        '''
        Attempts to reconstruct the URI that triggered the event. It is not
        possible to properly reconstruct the URI if there is missing or incorrect
        event data so an (obvious) substring replacement is made in this case.
        '''
        url = self['page'] if self['page'] else 'https://unknown/'
        module = self.data.get('module', '')
        if module:
            return url + module.get_relative_uri()
        else:
            return url

    def get_resource_display_name(self):
        '''
        Attempts to obtain the resource_display_name for the event. If no
        resource_display_field field is set then it tries to provide a name
        through the module field if it is set.
        '''
        name = self.data.get('resource_display_name', '')
        if not name:
            module = self.data.get('module')
            if module:
                name = module.get_name()
        return name

    def set_duration(self, end_time):
        '''
        Computes the duration of an event in minutes, by taking the difference
        between the event's timestamp and a given end time.
        '''
        self.duration = (end_time - self.data['time']).seconds / 60
        self.duration = self.duration if self.duration <= MAX_DURATION_MINUTES \
            else DEFAULT_DURATION_MINUTES


class VideoInteraction(Event):
    '''
    Corresponds to the 'Video Interaction Event' type in [edXdocs]
    VideoInteraction class is instanciated from the following raw_events :

    play_video
    stop_video
    pause_video
    seek_video
    load_video
    speed_change_video
    fullscreen
    not_fullscreen
    hide_transcript
    show_transcript
    video_hide_cc_menu
    video_show_cc_menu
    '''

    def __init__(self, polished_event):
        super(VideoInteraction, self).__init__(polished_event)

    def get_video_code(self):
        '''
        Attempts to return the video_code if it is set.
        If video_code is set then it returns the corresponding value.
        Otherwise it is assumed transcript_code is set and returns
        the corresponding value there.
        '''
        if self['video_code']:
            return self['video_code']
        else:
            return self['transcript_code']

    def get_video_id(self):
        '''
        Return a dict of functions to get the correct video_id for different
        specifications of open edx.
        :return: a dict of functions to get the correct video_id
        '''
        return {
            'MITx': self.data['module'].get_uri,
            'HKUSTx': lambda: self.data['video_id']
        }

    def get_uri(self):
        '''
        Attempts to reconstruct the URI pointing to the video that
        triggered the event.
        '''
        uri = super(VideoInteraction, self).get_uri()
        video_code = self.get_video_code()
        try:
            return uri + '_' + video_code
        except TypeError as err:
            print('TypeError: %s' % err)
            return ''


class PdfInteraction(Event):
    '''
    Corresponds to the 'PDF Interaction Event Types' in [readthedocs]
    Instanciated from the following raw event types:
      - book
    '''

    def __init__(self, polished_event):
        super(PdfInteraction, self).__init__(polished_event)
        self.set_page(self['goto_dest'])

    def set_page(self, page):
        url = self.data['page']
        url.set_page(page)

    def get_page(self):
        url = self.data['page']
        return url.get_page()


class ProblemInteraction(Event):
    '''
    Corresponds to the 'Problem Interaction Event Types' in [edXdocs].
    This event class is used to generate the rows of the Submission mode
    tables in MOOCdb (submissions, assessments, problems)

    ProblemInteraction events are instanciated from the following event types:

    - problem_check (Server)
      '[edXdocs] The server fires problem_check events when a problem is successfully checked'
    - problem_check (Browser)
      '[edXdocs] A browser fires problem_check events when a user wants to check a problem.'
    - problem_check_fail (Server)
      '[edXdocs] The server fires problem_check_fail events when a
                 problem cannot be checked successfully.'
    - problem_reset (Browser)
      '[edXdocs] Events fire when a user resets a problem
    - reset_problem (Server)
      '[edXdocs] Fires when a problem has been reset successfully'
    - problem_save (Browser)
    - problem_show (Browser)
    - showanswer (Server)
      '[edXdocs] Server-side event which displays the answer to a problem'
    - save_problem_fail (Server)
    - save_problem_success (Server)
    - problem_graded
    - i4x_problem_input_ajax
    - i4x_problem_problem_check
    - i4x_problem_problem_get
    - i4x_problem_problem_reset
    - i4x_problem_problem_save
    - i4x_problem_problem_show

    [edXdocs] : edx.readthedocs.org/projects/devdata/en/latest/
                internal_data_formats/tracking_logs.html
    '''

    # Different codes for the submission status
    # 0 : Answer is saved
    # 1 : Answer is submitted
    # 2 : Failure
    # 3 : Reset
    IS_SUBMITTED = {
        'problem_check': 1,
        'problem_check_fail': 2,
        'problem_graded': 1,
        'i4x_problem_problem_check': 1,
        'save_problem_check': 1,
        'save_problem_success': 0,
        'problem_save': 0,
        'i4x_problem_problem_save': 0,
        'save_problem_check_fail': 2,
        'reset_problem': 3,
        'reset_problem_fail': 2,
        'problem_reset': 3,
        'save_problem_fail': 2
    }

    # Events that are used to populate assessment table
    # (These are all associated to automatic assessments)
    ASSESSMENT_EVENTS = {'save_problem_check', 'problem_check'}

    # incomplete is not a correctness value that is documented
    # on the edx tracking log documentation, but it has been found
    # in tracking log files. It is treated differently from incorrect.
    GRADE_DICT = {'incorrect': 0, 'correct': 1, 'incomplete': -1}

    def __init__(self, raw_event):
        super(ProblemInteraction, self).__init__(raw_event)
        self.validity = 1

    def get_success(self):
        '''
        Server problem_check events come with a 'success' field indicating
        wether the answer checked is correct.
        If the 'success' field is absent, we can fallback on CorrectMap.correctness
        '''
        correctness = self.data.get('correctness', None)
        if not correctness:
            return None

        try:
            return self.GRADE_DICT[correctness]
        except KeyError:
            print('event id: %s with unknown correctness value: %s' %
                  (self['_id'], correctness))

    def get_is_submitted(self):
        '''
        Deduce from the event_type wether an answer is being
        submitted or just saved.
        '''
        return self.IS_SUBMITTED.get(self['event_type'], -1)

    def get_submission_row(self):
        '''
        Returns an array corresponding to a row in MOOCdb.submissions
        Note that 'submission_id' is absent : it will be generated by
        the SubmissionManager instance.
        '''

        try:
            n_attempts = int(self['attempts'])
        except ValueError as e:
            print("events.get_submission_row ValueError: {}".format(e))
            n_attempts = -1

        is_submitted = int(self.get_is_submitted())
        if n_attempts < 0 or is_submitted < 1:
            self.validity = 0

        return {
            'submission_id': self['_id'],
            'user_id': self['anon_screen_name'],
            'problem_id': self['problem_id'],
            'submission_timestamp': self['time'],
            'submission_attempt_number': self['attempts'],
            'submission_ip': self['ip'],
            'submission_os': self['os'],
            'submission_agent': self['agent'],
            'submission_answer': self['answer'],
            'submission_is_submitted': self.get_is_submitted(),
            'validity': self.validity
        }

    def get_assessment_row(self):
        '''
        Returns an array corresponding to a row in MOOCdb.assessments.
        'assessment_id' (primary key) and 'submission_id' (foreign key)
        will be generated by SubmissionManager instance.

        Since each event records an answer to a specific question,
        the grade is usually binary : either 'correct' or 'incorrect'
        ('incomplete' is treated as separate from 'incorrect')
        '''
        return {
            'assessment_grader_id': 'automatic',
            'assessment_timestamp': self['time'],
            'assessment_grade': self.get_success(),
            'submission_id': self['_id'],
            'assessment_id': self['_id']
        }


class OpenResponseAssessment(Event):
    '''
    Corresponds to the 'Open Response Assessment Event Types' in [edXdocs]
    Instanciated from the following raw event types :

    - oe_hide_question (Browser)
    - oe_show_question (Browser)
      '[readthedocs] Fires when the user hides or redisplays a combined open-ended problem.'

    - rubric_select (Browser)

    - i4x_combinedopenended_<action> (Server)

    - peer_grading_<action> (Browser)
    - staff_grading_<action> (Browser)
    - i4x_peergrading_<action> (Server)
    '''

    def __init__(self, raw_event):
        super(OpenResponseAssessment, self).__init__(raw_event)

    def get_is_submitted(self):
        '''
        No support yet for open response submissions so
        always return -1.
        '''
        return -1

    def get_success(self):
        '''
        No support yet for open response success
        always return None.
        '''
        return None


class Navigational(Event):
    '''
    Corresponds to the 'Navigational Event Types' in [readthedocs]
    Instanciated from events :
    - seq_goto
    - seq_prev
    - seq_next
    '''

    def __init__(self, raw_event):
        super(Navigational, self).__init__(raw_event)
        self.sequence_id = raw_event['sequence_id']
        self.goto_dest = raw_event['goto_dest']
        self.goto_from = raw_event['goto_from']

    def get_uri(self):
        '''
        Returns the URI for navigational events.
        The module relative path should not be appended for these events.
        '''
        return self['page']
