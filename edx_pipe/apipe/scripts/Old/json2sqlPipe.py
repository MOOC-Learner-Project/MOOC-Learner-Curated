#!/usr/bin/env python

import sys
import os

source_dir = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "../json_to_relation/")]
source_dir.extend(sys.path)
sys.path = source_dir

from json_to_relation import JSONToRelation
from output_disposition import OutputPipe, OutputDisposition
from input_source import InPipe
from edxTrackLogJSONParser import EdXTrackLogJSONParser

if __name__ == "__main__":

    # Create an instance of JSONToRelation, taking input from stdin,
    # and pumping output to stdout. Format output as SQL dump statements.
    jsonConverter = JSONToRelation(InPipe(),
                                   OutputPipe(OutputDisposition.OutputFormat.SQL_INSERT_STATEMENTS),
				   mainTableName='EdxTrackEvent',
				   logFile='/tmp/j2s.log'
                                   )
    jsonConverter.setParser(EdXTrackLogJSONParser(jsonConverter, 'EdxTrackEvent', replaceTables=True, dbName='test'
))
    jsonConverter.convert()
