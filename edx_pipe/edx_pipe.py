#!/usr/bin/env python
'''
This is the edx to moocdb translation pipeline.
'''
from __future__ import print_function

import os
import subprocess
import sys
import time

from apipe import json2sql


def run_folder_setup(cfg_csv_path, cfg_data_file):
    '''
    Sets up the folder environment in the course folder for apipe and qpipe.
    '''
    print("********  Creating environment **********")

    cmd_queue = []

    # Create directories
    if os.path.isdir(cfg_data_file['log_data_dir']):
        print("log_data folder already exists! Didn't touch it.")
    else:
        cmd_queue.append(' '.join(['mkdir', cfg_data_file['log_data_dir']]))

    if os.path.isdir(cfg_csv_path['intermediary_csv_dir']):
        print("intermediary_csv folder already exists! Didn't touch it.")
    else:
        cmd_queue.append(' '.join(['mkdir', cfg_csv_path['intermediary_csv_dir']]))

    if os.path.isdir(cfg_csv_path['moocdb_csv_dir']):
        print("moocdb_csv folder already exists! Didn't touch it.")
    else:
        cmd_queue.append(' '.join(['mkdir', cfg_csv_path['moocdb_csv_dir']]))

    # Locate log files, move them into the data folder, and decompress if necessary.
    course_dir = cfg_data_file['course_dir']

    # The only required file for translation is the tracking_log.json file
    # Look for it or the gzip compressed version inside either the
    # course_dir or LOG_DATA_DIR. The end result should be a log file
    # located at LOG_DATA_DIR/<log file>
    found_log_file = False

    # First look for an uncompressed one in course_dir
    log_file_path = os.path.join(course_dir, cfg_data_file['log_file'])
    if os.path.isfile(log_file_path):
        cmd_queue.append(' '.join(['mv', log_file_path, cfg_data_file]))
        found_log_file = True

    # Try looking a compressed one in the course_dir
    if not found_log_file:
        log_file_path = os.path.join(course_dir, cfg_data_file['log_file'] + '.gz')
        if os.path.isfile(log_file_path):
            cmd_queue.append(' '.join(['gzip', '-d', log_file_path]))
            log_file_path = log_file_path[:-3]
            cmd_queue.append(' '.join(['mv', log_file_path, cfg_data_file['log_data_dir']]))
            found_log_file = True

    # Try looking for an uncompressed one in the LOG_DATA_DIR
    if not found_log_file:
        log_file_path = os.path.join(cfg_data_file['log_data_dir'], cfg_data_file['log_file'])
        if os.path.isfile(log_file_path):
            found_log_file = True

    # Try looking for a compressed one in the LOG_DATA_DIR
    if not found_log_file:
        log_file_path = os.path.join(cfg_data_file['log_data_dir'], cfg_data_file['log_file'] + '.gz')
        if os.path.isfile(log_file_path):
            cmd_queue.append(' '.join(['gzip', '-d', log_file_path]))
            found_log_file = True

    # If we still haven't found it then exit with error
    if not found_log_file:
        print(
            "Error: could not find required log file %s or %s.gz in directory %s or %s "
            "in course directory or log data folder" %
            (cfg_data_file['log_file'], cfg_data_file['log_file'], course_dir, cfg_data_file['log_data_dir']))
        sys.exit(1)

    # By now the log file will be located at LOG_DATA_DIR/<log file>
    print("Successfully located the log file")

    # Execute the batch of queued batch of commands to finalize folder preparation
    for cmd in cmd_queue:
        print("Executing cmd: %s" % cmd)
        subprocess.call(cmd, shell=True)


def run_apipe(cfg_csv_path, cfg_data_file):
    '''
    Searches for tracking log file post-environment setup and runs apipe on it.
    '''
    print("********  Clearing the intermediary_csv folder **********")
    cmd = "rm -f %s/*" % cfg_csv_path['intermediary_csv_dir']
    print("Executing cmd: %s\n" % cmd)
    subprocess.call(cmd, shell=True)

    print("********  Translating from json to csv **********")

    log_file_path = ''.join([cfg_data_file['log_data_dir'], cfg_data_file['log_file']])
    if os.path.isfile(log_file_path):
        print("Successfully located the tracking log file at %s" %
              log_file_path)
    else:
        print("Could not locate the tracking log file at %s" % log_file_path)
        sys.exit(1)

    time_elapsed = time.time()
    json2sql.convert(log_file_path, cfg_csv_path['intermediary_csv_dir'], 'csv')
    time_elapsed = time.time() - time_elapsed
    mins, secs = divmod(time_elapsed, 60)
    hours, mins = divmod(mins, 60)
    print("json to csv translation complete: took %dh%02dm%02ds" %
          (hours, mins, secs))


def write_full_pipe_log(cfg_data_file):
    '''
    Write git commit hash, status, remotes, and diff into a log if inside a git repo.
    If git is not install then it does nothing.
    '''
    try:
        if subprocess.call(
            ['git', 'status'], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE) == 0:
            log = open(
                os.path.join(cfg_data_file['data_dir'], cfg_data_file['course_folder'],
                             'full_pipe.log'), 'w')
            subprocess.call(['git', 'log', '-n 1'], stdout=log, stderr=log)
            subprocess.call(['git', 'status'], stdout=log, stderr=log)
            subprocess.call(['git', 'remote', '-v'], stdout=log, stderr=log)
            subprocess.call(['git', 'diff'], stdout=log, stderr=log)
            log.close()
    except OSError:
        return
