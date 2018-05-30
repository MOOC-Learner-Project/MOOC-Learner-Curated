import helperclasses
import util
import genformatting
import specformatting
import inheritloc
import updateloc
import events


class EventFormatter(object):
    '''
    The Eventformatter class is responsible for
    cleaning up input data from a raw event before
    using it to initialize an Event class.
    '''

    def __init__(self, moocdb, TIMESTAMP_FORMAT):
        self.engaged_users = helperclasses.EngagedUsers()

        self.urls = helperclasses.DictionaryTable(moocdb, 'urls')
        self.agents = helperclasses.DictionaryTable(moocdb, 'agent')
        self.os = helperclasses.DictionaryTable(moocdb, 'os')

        self.pass_filter_regexes = ["sequential", "page_close"]

        genformatting.TIMESTAMP_FORMAT = TIMESTAMP_FORMAT

        self.general_formatting_functions = [
            genformatting.set_agent_os, genformatting.format_url,
            genformatting.parse_timestamp, genformatting.parse_problem_id,
            genformatting.parse_video_id, genformatting.parse_question_location
        ]

        # A list of tuples instead of a dictionary is used here because
        # the ordering of rules can matter.

        # An ordered dictionary cannot be used here to avoid looping
        # as the event type is not equal to the regex necessarily and
        # hence the event type cannot be used as a lookup key.
        self.specific_formatting_rules = [
            ('seq_', specformatting.format_seq),
            ('i4x:/', specformatting.format_i4x),
            ('^/[^:]+', specformatting.format_url_change)
        ]

        self.inherit_location_rules = [
            ('^$', inheritloc.no_url),
            ('courseware/[^/]+/[^/]+', inheritloc.inherit_seqnum)
        ]

        self.update_location_rules = [
            ('page_close', updateloc.close_previous_page),
            ('seq_', updateloc.update_seq), ('.*', updateloc.simple_update)
        ]

        self.instanciate_event_rules = [
            ('problem|showanswer', events.ProblemInteraction),
            ('video|transcript|fullscreen', events.VideoInteraction),
            ('book', events.PdfInteraction), (
                'oe_|combinedopenended|rubric_select|grading',
                events.OpenResponseAssessment), ('seq_', events.Navigational),
            ('.*', events.Event)
        ]

    def pass_filter(self, raw_event):
        '''
        Returns True if the event should be processed further
        '''
        return not util.match_regex(self.pass_filter_regexes, "event_type",
                                    raw_event)

    def do_generic_formatting(self, raw_event):
        '''
        Apply selected genformatting functions
        '''
        for func in self.general_formatting_functions:
            func(raw_event)

    def get_specific_formatting_func(self, raw_event):
        '''
        Determine the appropriate specific formatting function for the
        raw event. Returns a function(raw_event) is a corresponding one is found.
        Otherwise returns None.
        '''
        for (regex, func) in self.specific_formatting_rules:
            if util.match_regex([regex], "event_type", raw_event):
                return func

    def do_specific_formatting(self, raw_event):
        '''
        Apply a specific formatting function if the event type matches a defined regex.
        '''
        func = self.get_specific_formatting_func(raw_event)
        if func is not None:
            func(raw_event)

    def get_inherit_location_func(self, raw_event):
        '''
        Determine the appropriate inherit location function for the
        raw event. Returns a function(raw_event) if a corresponding one is found.
        Otherwise returns None.
        '''
        for (regex, func) in self.inherit_location_rules:
            if util.match_regex([regex], "page", raw_event):
                return func

    def inherit_location(self, raw_event):
        '''
        Try to inherit location when page field matches a defined regex
        '''
        current_location = self.engaged_users.get_location(
            raw_event['anon_screen_name'])

        if current_location:
            if not str(current_location[0]):
                return

            time_gap = (raw_event['time'] - current_location[1]).seconds

            if time_gap < 3600:
                raw_event['current_location'] = current_location
                func = self.get_inherit_location_func(raw_event)
                if func is not None:
                    func(raw_event)

    def get_update_location_func(self, raw_event):
        '''
        Determine the appropriate update location function for the
        raw event. Returns a function(raw_event) if a corresponding one is found.
        Otherwise returns None.
        '''
        for (regex, func) in self.update_location_rules:
            if util.match_regex([regex], "event_type", raw_event):
                return func

    def update_location(self, raw_event):
        '''
        Updates the user's current location when the event type matches a defined regex
        '''
        new_location = None
        func = self.get_update_location_func(raw_event)
        if func is not None:
            new_location = func(raw_event)

        if new_location:
            self.engaged_users.update_location(raw_event['anon_screen_name'],
                                               new_location, raw_event['time'])
        else:
            self.engaged_users.remove_user(raw_event['anon_screen_name'])

    def get_instanciate_event_func(self, raw_event):
        '''
        Determine the appropriate instanciate event function for the
        raw event. Returns a function(raw_event) if a corresponding one is found.
        Otherwise returns None.
        '''
        for (regex, func) in self.instanciate_event_rules:
            if util.match_regex([regex], "event_type", raw_event):
                return func

    def instanciate_event(self, raw_event):
        '''
        Instanciates an Event subclass from the now formatted raw_event when the event type
        matches a defined regex
        '''
        func = self.get_instanciate_event_func(raw_event)
        if func is not None:
            return func(raw_event)

    def record_event_metadata(self, raw_event):
        '''
        Event metadata is not to be confused with the moocdb metadata
        '''
        raw_event['url_id'] = self.urls.insert(str(raw_event['page']))
        raw_event['os'] = self.os.insert(raw_event['os'])
        raw_event['agent'] = self.agents.insert(raw_event['agent'])

    def polish(self, raw_event):
        '''
        Apply all the event polishing functions (when applicable).
        '''
        self.do_generic_formatting(raw_event)
        self.do_specific_formatting(raw_event)
        self.inherit_location(raw_event)
        self.update_location(raw_event)
        self.record_event_metadata(raw_event)
        return self.instanciate_event(raw_event)

    def serialize(self):
        '''
        Write out the moocdb urls, agents, and os tables.
        '''
        self.urls.serialize()
        self.agents.serialize()
        self.os.serialize()
