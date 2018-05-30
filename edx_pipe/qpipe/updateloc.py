'''
Functions for keeping track of updating locations.
'''
import copy

# Each rule has to return the new location of the user
# If the user is previously engaged, the 'current_location' field is available in raw_event
# So engagement should be checked with "'current_location' in raw_event.keys()"


def simple_update(raw_event):
    '''
    Simply returns the page field in the raw event.
    '''
    return raw_event['page']


def update_seq(raw_event):
    '''
    Returns a CourseURL copy from the page field
    with an update sequence number according to the
    goto_dest field
    '''
    url_copy = copy.copy(raw_event['page'])
    url_copy.set_seq(raw_event['goto_dest'])
    return url_copy


def close_previous_page(raw_event):
    '''
    Returns the current location after closing the
    previous page, if it can be determined.
    '''

    # If the user's previous location is not known,
    # page_close doesn't give further information,
    # so return None
    if 'current_location' not in raw_event.keys():
        return None

    current_location = raw_event['current_location'][0]
    closed_url = raw_event['page']

    string = closed_url.get_unit()
    if closed_url.get_sub_unit():
        string += closed_url.get_sub_unit()

    if string in str(current_location):
        return None
    else:
        return current_location
