'''
The EventManager is responsible primarily
for computing the rows of the observed_events MOOCdb
table. It also performs an extra duty which is to
compute the duration information for an Edx
event by taking the difference of timestamps
from the user's most recent previous event.

Some event types are explicitly intended to be
ignored for this duration computation.
'''


class EventManager(object):
    IGNORE = [
        'page_close', 'problem_check', 'problem_check_fail', 'problem_graded',
        'save_problem_check', 'i4x_problem_problem_check',
        'save_problem_success', 'problem_save', 'i4x_problem_problem_save',
        'save_problem_check_fail', 'reset_problem', 'reset_problem_fail',
        'problem_reset', 'save_problem_fail'
    ]

    def __init__(self, moocdb=None):
        self.staged_events = {}
        if moocdb:
            self.observed_events = moocdb.csv_writers['observed_events']

    def stage_event(self, event):
        user = event['anon_screen_name']

        # Page close gives no information on the user's location
        # *after* the event occured. Therefore, it is ignored.
        if event.data.get('event_type', None) in self.IGNORE:
            return None

        if user in self.staged_events.keys():
            ending_event = self.staged_events[user]
            end_time = event.data['time']

            # Compute event duration
            ending_event.set_duration(end_time)

            # Stage new event
            self.staged_events[user] = event

            # Return ending event, ready for insertion
            return ending_event
        else:
            self.staged_events[user] = event
            return None

    def store_event(self, event):
        event_to_store = self.stage_event(event)

        if event_to_store:
            self.observed_events.store(event_to_store.get_observed_event_row())

    def serialize(self):
        for event in self.staged_events.values():
            self.observed_events.store(event.get_observed_event_row())
