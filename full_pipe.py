#!/usr/bin/env python
"""
This is the complete moocdb moocdb/MOOC-Learner-Curated, translation followed by curation and vismooc extensions.
After configuration, run in the command line using:
python full_pipe.py
"""

from __future__ import print_function

import sys

from config import config
from curation.curation import curate
from edx_pipe.edx_pipe import run_folder_setup, write_full_pipe_log, run_apipe
from edx_pipe.qpipe import qpipe, util as qpipe_util
from vismooc_extensions.vismooc_extensions import process_vismooc
from newmitx_extensions.newmitx_extensions import process_newmitx


def run_edx():
    """
    edx pipe
    """
    cfg_csv_path = cfg.get_csv_path()
    cfg_data_file = cfg.get_data_file()
    cfg_mysql_script_path = cfg.get_mysql_script_path()
    cfg_open_edx_spec = cfg.get_open_edx_spec()
    cfg_csv_parsing = cfg.get_csv_parsing()

    if cfg.get_or_query_pipeline("folder_setup"):
        run_folder_setup(cfg_csv_path, cfg_data_file)

    write_full_pipe_log(cfg_data_file)

    if cfg.get_or_query_pipeline("apipe"):
        print ("(WARNING: This will remove all files in the intermediary_csv folder)")
        run_apipe(cfg_csv_path, cfg_data_file)

    if cfg.get_or_query_pipeline("qpipe"):

        if cfg.get_or_query_pipeline("qpipe:qpipe_process_events"):
            qpipe.process_events(cfg_csv_path, cfg_csv_parsing, cfg_open_edx_spec,
                                 timestamp_format=cfg_csv_parsing['timestamp_format'])

        if cfg.get_or_query_pipeline("qpipe:qpipe_create_db"):
            qpipe_util.create_mysql(cfg_mysql, cfg_data_file, cfg_mysql_script_path)

        if cfg.get_or_query_pipeline("qpipe:qpipe_populate_db"):
            qpipe_util.fill_mysql(cfg_mysql, cfg_csv_path, cfg_data_file,
                                  mysql_script=cfg_mysql_script_path['qpipe_copy_db_path'])


def run_curation():
    """
    curation pipe
    """
    if cfg.get_or_query_pipeline('curation'):
        print("Curating MySQL MOOCdb %s" % (cfg_mysql['database']))
        curate(
            db_name=cfg_mysql['database'],
            username=cfg_mysql['user'],
            password=cfg_mysql['password'],
            db_host=cfg_mysql['host'],
            db_port=cfg_mysql['port'])


def run_vismooc():
    """
    vismooc_extensions pipe
    """
    cfg_csv_path = cfg.get_csv_path()
    cfg_data_file = cfg.get_data_file()
    cfg_mysql_script_path = cfg.get_mysql_script_path()

    if cfg.get_or_query_pipeline('vismooc_extensions'):
        if cfg.get_or_query_pipeline('vismooc_extensions:vismooc_process'):
            process_vismooc(cfg_csv_path, cfg_data_file)

        if cfg.get_or_query_pipeline('vismooc_extensions:vismooc_populate'):
            qpipe_util.fill_mysql(cfg_mysql, cfg_csv_path, cfg_data_file,
                                  mysql_script=cfg_mysql_script_path['vismooc_extensions_import_path'])


def run_newmitx():
    """
    newmitx_extensions pipe
    """
    cfg_csv_path = cfg.get_csv_path()
    cfg_data_file = cfg.get_data_file()
    cfg_mysql_script_path = cfg.get_mysql_script_path()

    if cfg.get_or_query_pipeline('newmitx_extensions'):
        if cfg.get_or_query_pipeline('newmitx_extensions:newmitx_process'):
            process_newmitx(cfg_csv_path, cfg_data_file, cfg_mysql_script_path)

        if cfg.get_or_query_pipeline('newmitx_extensions:newmitx_populate'):
            qpipe_util.fill_mysql(cfg_mysql, cfg_csv_path, cfg_data_file,
                                  mysql_script=cfg_mysql_script_path['newmitx_extensions_import_path'])


def main():
    '''
    Main function handler for full pipe.
    This is a wrapper around edx_pipe, curation, and vismooc_extensions.
    '''
    run_edx()
    run_curation()
    run_vismooc()
    run_newmitx()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        cfg = config.ConfigParser()
    else:
        cfg = config.ConfigParser(sys.argv[1])
    if not cfg.is_valid():
        sys.exit("Config file is invalid.")
    cfg_mysql = cfg.get_or_query_mysql()

    main()
