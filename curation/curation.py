'''
Author : Sebastien Boyer
Pre-processing database before feature extraction
'''
from __future__ import print_function

import submissions_curation as sub
import observed_events as obv


def curate(db_name, username, password, db_host, db_port):
    print("Curating the submissions table...")
    sub.curate_submissions(db_name, username, password, db_host, db_port)
    print("Done")

    print("Curating observed_events table...")
    # minimum duration for observed_events table:

    min_time = 10  #minutes
    obv.curate_observed_events(db_name, username, password, db_host, db_port,
                               min_time)
    print("Done")
