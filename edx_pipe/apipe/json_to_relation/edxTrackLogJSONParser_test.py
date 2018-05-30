#!/usr/bin/env python
'''Tester for EdX track log parser functions

Used for MOOC-Learner-Curation. Adapted from test/test_edxTrackLogJSONParser

TODO do not fragment tests...
'''
import datetime
import unittest
import edxTrackLogJSONParser
import json_to_relation
import input_source
import os
import output_disposition

class EdxTrackLogJSONParserTest(unittest.TestCase):
    '''Tester for EdX track log parser functions
    '''

    def setUp(self):
        
        super(EdxTrackLogJSONParserTest, self).setUp()
        self.currDir = os.path.dirname(__file__)
        self.stringSource = input_source.InURI(os.path.join(self.currDir ,"test/data/twoJSONRecords.json"))
    def test_extractCourseIDFromProblemXEvent(self):
        '''Test coverage of extracting course id from and event
        '''

        raw_event = {"success": "correct", "correct_map": {"i4x-Medicine-HRP258-problem-8dd11b4339884ab78bc844ce45847141_2_1": {"hint": "", "hintmode": "null",}}}
        fileConverter = \
        json_to_relation.JSONToRelation(self.stringSource,
                                        output_disposition.OutputFile(os.devnull,
                                                                      output_disposition.OutputDisposition.OutputFormat.CSV),
                                        mainTableName='Main' )
        edxParser = edxTrackLogJSONParser.EdXTrackLogJSONParser(fileConverter, 'Main', replaceTables=True, dbName='Edx', useDisplayNameCache=True)

        course_id = edxParser.extractCourseIDFromProblemXEvent(raw_event)
        expected_course_id = "Medicine-HRP258"
        self.assertEqual(expected_course_id, course_id)

        raw_event = {"success": "correct", "correct_map": {"8dd11b4339884ab78bc844ce45847141_2_1": {"hint": "", "hintmode": "null",}}}
        fileConverter = \
        json_to_relation.JSONToRelation(self.stringSource,
                                        output_disposition.OutputFile(os.devnull,
                                                                      output_disposition.OutputDisposition.OutputFormat.CSV),
                                        mainTableName='Main' )
        edxParser = edxTrackLogJSONParser.EdXTrackLogJSONParser(fileConverter, 'Main', replaceTables=True, dbName='Edx', useDisplayNameCache=True)

        course_id = edxParser.extractCourseIDFromProblemXEvent(raw_event)
        self.assertIsNone(course_id)

        raw_event = {
            
                "answers": {
                    "2096c93e320e463eadcced6bde30fa1b_2_1": "choice_0",
                    "2096c93e320e463eadcced6bde30fa1b_3_1": "choice_2",
                    "2096c93e320e463eadcced6bde30fa1b_4_1": "choice_2",
                    "2096c93e320e463eadcced6bde30fa1b_5_1": "choice_2",
                    "2096c93e320e463eadcced6bde30fa1b_6_1": "choice_2",
                    "2096c93e320e463eadcced6bde30fa1b_7_1": "choice_0"
                },
            "attempts": 1,
            "correct_map": {
                "2096c93e320e463eadcced6bde30fa1b_2_1": {
                    "answervariable": "null",
                    "correctness": "incorrect",
                    "hint": "",
                    "hintmode": "null",
                    "msg": "",
                    "npoints": "null",
                    "queuestate": "null"
                },
                "2096c93e320e463eadcced6bde30fa1b_3_1": {
                    "answervariable": "null",
                    "correctness": "correct",
                    "hint": "",
                    "hintmode": "null",
                    "msg": "",
                    "npoints": "null",
                    "queuestate": "null"
                },
                "2096c93e320e463eadcced6bde30fa1b_4_1": {
                    "answervariable": "null",
                    "correctness": "correct",
                    "hint": "",
                    "hintmode": "null",
                    "msg": "",
                    "npoints": "null",
                    "queuestate": "null"
                },
                "2096c93e320e463eadcced6bde30fa1b_5_1": {
                    "answervariable": "null",
                    "correctness": "correct",
                    "hint": "",
                    "hintmode": "null",
                    "msg": "",
                    "npoints": "null",
                    "queuestate": "null"
                },
                "2096c93e320e463eadcced6bde30fa1b_6_1": {
                    "answervariable": "null",
                    "correctness": "correct",
                    "hint": "",
                    "hintmode": "null",
                    "msg": "",
                    "npoints": "null",
                    "queuestate": "null"
                },
                "2096c93e320e463eadcced6bde30fa1b_7_1": {
                    "answervariable": "null",
                    "correctness": "incorrect",
                    "hint": "",
                    "hintmode": "null",
                    "msg": "",
                    "npoints": "null",
                    "queuestate": "null"
                }
            },
            "grade": 4,
            "max_grade": 6,
            "permutation": {
                "2096c93e320e463eadcced6bde30fa1b_2_1": [
                    "shuffle",
                    [
                        "choice_2",
                        "choice_1",
                        "choice_0"
                    ]
                ],
                "2096c93e320e463eadcced6bde30fa1b_4_1": [
                    "shuffle",
                    [
                        "choice_1",
                        "choice_0",
                        "choice_2"
                    ]
                ],
                "2096c93e320e463eadcced6bde30fa1b_5_1": [
                    "shuffle",
                    [
                        "choice_2",
                        "choice_0",
                        "choice_1"
                    ]
                ],
                "2096c93e320e463eadcced6bde30fa1b_6_1": [
                    "shuffle",
                    [
                        "choice_0",
                        "choice_2",
                        "choice_1"
                    ]
                ],
                "2096c93e320e463eadcced6bde30fa1b_7_1": [
                    "shuffle",
                    [
                        "choice_1",
                        "choice_2",
                        "choice_0"
                    ]
                ]
            },
            "problem_id": "block-v1:HKUSTx+EBA102x+1T2016+type@problem+block@2096c93e320e463eadcced6bde30fa1b",
            "state": {
                "correct_map": {},
                "done": "null",
                "input_state": {
                    "2096c93e320e463eadcced6bde30fa1b_2_1": {},
                    "2096c93e320e463eadcced6bde30fa1b_3_1": {},
                    "2096c93e320e463eadcced6bde30fa1b_4_1": {},
                    "2096c93e320e463eadcced6bde30fa1b_5_1": {},
                    "2096c93e320e463eadcced6bde30fa1b_6_1": {},
                    "2096c93e320e463eadcced6bde30fa1b_7_1": {}
                },
                "seed": 1,
                "student_answers": {}
            },
            "submission": {
                "2096c93e320e463eadcced6bde30fa1b_2_1": {
                    "answer": "emphasising a particular point in written text",
                    "correct": "false",
                    "input_type": "choicegroup",
                    "question": "1. Register can be defined as a language style used for _____.",
                    "response_type": "multiplechoiceresponse",
                    "variant": ""
                },
                "2096c93e320e463eadcced6bde30fa1b_3_1": {
                    "answer": "formal and specific",
                    "correct": "true",
                    "input_type": "choicegroup",
                    "question": "2. The register of business contracts tends to be _____.",
                    "response_type": "multiplechoiceresponse",
                    "variant": ""
                },
                "2096c93e320e463eadcced6bde30fa1b_4_1": {
                    "answer": "invalid; without legal force; not binding",
                    "correct": "true",
                    "input_type": "choicegroup",
                    "question": "3.The term \u201cnull and void\u201d means _____.",
                    "response_type": "multiplechoiceresponse",
                    "variant": ""
                },
                "2096c93e320e463eadcced6bde30fa1b_5_1": {
                    "answer": "important information to managers",
                    "correct": "true",
                    "input_type": "choicegroup",
                    "question": "4. Business reports are written to provide _____.",
                    "response_type": "multiplechoiceresponse",
                    "variant": ""
                },
                "2096c93e320e463eadcced6bde30fa1b_6_1": {
                    "answer": "personalize the writing so that it is more meaningful to the potential client",
                    "correct": "true",
                    "input_type": "choicegroup",
                    "question": "5.When writing a business proposal, you should ________.",
                    "response_type": "multiplechoiceresponse",
                    "variant": ""
                },
                "2096c93e320e463eadcced6bde30fa1b_7_1": {
                    "answer": "We must begin to socialize our employees into the work culture so that they internalize the core values of cost-reduction and high-quality that our company embraces.",
                    "correct": "false",
                    "input_type": "choicegroup",
                    "question": "6. Which excerpt is an appropriate register for a business proposal?",
                    "response_type": "multiplechoiceresponse",
                    "variant": ""
                }
            },
            "success": "incorrect"
        }
        edxParser = edxTrackLogJSONParser.EdXTrackLogJSONParser(fileConverter, 'Main', replaceTables=True, dbName='Edx', useDisplayNameCache=True)

        course_id = edxParser.extractCourseIDFromProblemXEvent(raw_event)
        self.assertIsNone(course_id)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(EdxTrackLogJSONParserTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
