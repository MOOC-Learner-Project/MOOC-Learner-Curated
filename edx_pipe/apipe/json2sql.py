#!/usr/bin/env python
import argparse
import datetime
import os
import re
import socket
import sys
import time

from json_to_relation.edxTrackLogJSONParser import EdXTrackLogJSONParser
from json_to_relation.input_source import InURI
from json_to_relation.json_to_relation import JSONToRelation
from json_to_relation.output_disposition import OutputDisposition, OutputFile

# Transforms a single .json OpenEdX tracking log file to
# relational tables. See argparse below for options.
def buildOutputFileName(inFilePath, destDir):
    '''
    Given the full path to a .json tracking log file, a destination
    directory where results of a transform to relational tables will
    go, generate a new .sql filename that will be used by the transform.

    @param inFilePath: full path to .json file
    @type inFilePath: String
    @param destDir: full path to destination directory
    @type destDir: String
    @return: a full filename with a .sql extension, derived from the input file name
    @rtype: String
    '''
    return os.path.join(destDir, os.path.basename(inFilePath) + '.sql')

# Convert the OpenEdX tracking log to SQL files
# See command line help further below for the meaning of
# each argument.
def convert(inFilePath, destDir, targetFormat, dropTables = False):
    # Output file is name of input file with the
    # .json extension replaced by .sql
    outFullPath = buildOutputFileName(inFilePath, destDir)

    # Log file will go to <destDir>/../TransformLogs, the file being named j2s_<inputFileName>.log:
    logDir = os.path.join(destDir, '..', 'TransformLogs')
    if not os.access(logDir, os.W_OK):
        try:
            os.makedirs(logDir)
        except OSError:
            # Log dir already exists:
            pass

    logFile = os.path.join(logDir, 'j2s_%s.log' % os.path.basename(inFilePath))

    # Create an instance of JSONToRelation, taking input from the given file:
    # and pumping output to the given output path:
    if targetFormat == 'csv':
        outputFormat = OutputDisposition.OutputFormat.CSV
    elif targetFormat == 'sql_dump':
        outputFormat = OutputDisposition.OutputFormat.SQL_INSERT_STATEMENTS
    else:
        outputFormat = OutputDisposition.OutputFormat.SQL_INSERTS_AND_CSV

    outSQLFile = OutputFile(outFullPath, outputFormat, options='wb') # overwrite any existing sql file
    jsonConverter = JSONToRelation(InURI(inFilePath),
                                   outSQLFile,
                                   mainTableName='EdxTrackEvent',
                                   logFile=logFile,
                                   progressEvery = 10000
                                   )
    try:
        jsonConverter.setParser(EdXTrackLogJSONParser(jsonConverter, 
                                                      'EdxTrackEvent', 
                                                      replaceTables=dropTables, 
                                                      dbName='Edx',
                                                      progressEvery = 10000
                                                  ))
    except Exception as e:
        with open(logFile, 'w') as fd:
            fd.write("In json2sql: could not create EdXTrackLogJSONParser: %s" % `e`)
        # Try to delete the .sql file that was created when 
        # the OutputFile instance was made in the JSONToRelation
        # instantiation statement above:
        try:
            outSQLFile.remove();
        except Exception as e:
            pass
        sys.exit(1)
        
    jsonConverter.convert()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='json2sql.py')
    parser.add_argument('-x', '--expungeTables',
                        help='DROP all tables in database before beginning transform',
                        dest='dropTables',
                        action='store_true',
                        default=False)
    parser.add_argument('-t', '--targetFormat',
                        help='Output one CSV file per table, a dump file as would be created my mysqldump, or both. Default: sql_dump',
                        dest='targetFormat',
                        default='sql_dump',
                        choices = ['csv', 'sql_dump', 'sql_dump_and_csv'])
    parser.add_argument('destDir',
                        help='file path for the destination .sql/csv file(s)')
    parser.add_argument('inFilePath',
                        help='json file path to be converted to sql/csv.')

    args = parser.parse_args()
    convert(args.inFilePath, args.destDir, args.targetFormat, args.dropTables)
