'''
Author : Sebastien Boyer (sebboyer@mit.edu)
Date : Feb 2016

Performs transformation from intermediary csv
to curated MySQL database in MOOCdb format
'''
from __future__ import print_function

import sys
import os
import time
from subprocess import check_output, Popen, PIPE

# qpipe modules
import extractor
from clickevents import ClickEventsManager
from eventformatter import EventFormatter
from resources import ResourceManager
from eventmanager import EventManager
from submissions import SubmissionManager
from helperclasses import CurationHelper
from moocdb import MOOCdb


def process_events(cfg_csv_path, cfg_csv_parsing, cfg_open_edx_spec, timestamp_format):
    print('****** Processing events *******')

    events_processing_duration = time.time()

    # MOOCdb storage interface
    moocdb = MOOCdb(cfg_csv_path['moocdb_csv_dir'])

    # Instanciating the piping architecture
    event_formatter = EventFormatter(moocdb, TIMESTAMP_FORMAT=timestamp_format)
    resource_manager = ResourceManager(moocdb, HIERARCHY_ROOT='https://')
    event_manager = EventManager(moocdb)
    submission_manager = SubmissionManager(moocdb)
    curation_helper = CurationHelper(cfg_csv_path['moocdb_csv_dir'])
    clickevents_manager = ClickEventsManager(moocdb)

    print("Processing %s" % cfg_csv_path['edx_track_event_path'])
    extract = extractor.CSVExtractor(cfg_csv_path, cfg_csv_parsing)

    num_rows = int(
        check_output(["wc", "-l", cfg_csv_path['edx_track_event_path']]).split(" ")[0])
    event_count = 0

    for raw_event in extract:
        event_count += 1
        if event_count % 500 == 0:
            progress = 'Progress: %0.4f%%' % (100.0 * float(event_count) /
                                                    float(num_rows))
            # A print statement is not used here because
            # a newline is automatically appended on each print, whereas
            # we want to use the CR character to move the terminal
            # pointer back to the beginning of the same line.
            print(progress)
            sys.stdout.write("\033[F")

        # Skip events explicitly not handled by qpipe
        if event_formatter.pass_filter(raw_event) is False:
            continue

        event = event_formatter.polish(raw_event)

        resource_id = resource_manager.create_resource(event)

        event.set_data_attr('resource_id', resource_id)
        submission_manager.update_submission_tables(event)
        curation_helper.record_curation_hints(event)
        clickevents_manager.record(event, cfg_open_edx_spec)
        event_manager.store_event(event)

    print('* All events processed')
    print('* Writing CSV output to : %s' % cfg_csv_path['moocdb_csv_dir'])

    event_formatter.serialize()
    event_manager.serialize()
    resource_manager.serialize(pretty_print_to=cfg_csv_path['resource_hierarchy_path'])
    submission_manager.serialize(pretty_print_to=cfg_csv_path['problem_hierarchy_path'])
    curation_helper.serialize()

    print('* Writing resource hierarchy to : %s' % cfg_csv_path['resource_hierarchy_path'])
    print('* Writing problem hierarchy to : %s' % cfg_csv_path['problem_hierarchy_path'])

    metadata_file_path = os.path.join(cfg_csv_path['moocdb_csv_dir'], 'metadata.csv')
    try:
        os.remove(metadata_file_path)
        print('* Removed old metadata file at %s' % metadata_file_path)
    except OSError:
        pass
    print('* Writing metadata row to : %s' % metadata_file_path)

    try:
        with open(metadata_file_path, 'w') as metafile:
            process = Popen(['git', 'describe', '--always'], stdout=PIPE)
            commit_hash, err = process.communicate()
            commit_hash = commit_hash.rstrip() if err is None else ''
            events_processing_duration = (
                int(time.time() - events_processing_duration)) / 60  # minutes
            metafile.write('%s,%s\n' %
                           (commit_hash, events_processing_duration))
    except OSError:
        pass
    moocdb.close()
