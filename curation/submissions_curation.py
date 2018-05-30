"""
Created: 5/24/2015 by Ben Schreck

Curates submissions (and indirectly assessments)
"""
from __future__ import print_function

import datetime as dt
from sql_functions import block_sql_command, open_SQL_connection

BLOCK_SIZE = 50


def curate_submissions(db_name, username, password, host, port):
    conn = open_SQL_connection(db_name, username, password, host, port)
    cursor = conn.cursor()

    # If the validity column does not exist, create it.
    check_validity_query = 'SHOW COLUMNS FROM `%s`.submissions WHERE FIELD=\'validity\'' % db_name
    cursor.execute(check_validity_query)
    validity_column_exists = len(cursor.fetchall()) == 1
    if not validity_column_exists:
        print(
            "No validity column found in %s's submission table so it will be created."
            % db_name)
        add_validity = '''ALTER TABLE `%s`.submissions ADD validity int(1)''' % db_name
        cursor.execute(add_validity)
        conn.commit()

    # A first pass submissions invalidation is performed here
    # in batches of queries to prevent the lock wait timeout exceeded
    # error that can occur from a single, long update query being performed
    # on too large a number of rows.
    # Ideally the batches should be in number of entries but that is not
    # support by mysql so batching over timestamp ranges
    # is done instead.

    min_timestamp_query = '''
    SELECT MIN(submission_timestamp) FROM `%s`.submissions
    ''' % (db_name)
    cursor.execute(min_timestamp_query)
    min_timestamp = cursor.fetchall()[0][0]

    max_timestamp_query = '''
    SELECT MAX(submission_timestamp) FROM `%s`.submissions
    ''' % (db_name)
    cursor.execute(max_timestamp_query)
    max_timestamp = cursor.fetchall()[0][0]

    def datetime_range(start, end, step):
        # step specifies a number of days
        while start <= end:
            yield start
            start += dt.timedelta(step, 0)

    invalidate_submissions_first_pass_query = '''
    UPDATE `%s`.submissions
    SET validity = 0
    WHERE submission_timestamp >= DATE('%s')
    AND submission_timestamp <= DATE('%s')
    AND submission_attempt_number < 0
    OR submission_is_submitted != 1
    '''

    interval = 90
    for offset in datetime_range(min_timestamp, max_timestamp, interval):
        if offset is None:
            return
        print("First pass invalidation over %s to %s" %
              (offset, offset + dt.timedelta(interval, 0)))
        cursor.execute(invalidate_submissions_first_pass_query %
                       (db_name, offset, offset + dt.timedelta(interval, 0)))
        conn.commit()

    potential_submissions_query = '''
    SELECT  s.submission_id,
            s.user_id,
            s.problem_id,
            s.submission_timestamp,
            s.submission_answer,
            s.submission_attempt_number,
            s.submission_is_submitted,
            a.assessment_grade

    FROM `%s`.submissions AS s
    LEFT JOIN `%s`.assessments AS a
    ON s.submission_id = a.submission_id
    WHERE s.submission_attempt_number > -1
    AND   s.submission_is_submitted = 1
    ORDER BY s.user_id,
             s.problem_id,
             s.submission_attempt_number,
             s.submission_timestamp
             ASC
    ''' % (db_name, db_name)
    cursor.execute(potential_submissions_query)
    data = cursor.fetchall()
    cursor.close()

    print("Now determining validity of all submissions...")
    cursor = conn.cursor()
    valid_submissions = {
    }  # A mapping of user_id -> problem_id -> tuple of submission entries
    # of the form (submission_id, answer, attempt_number, grade, timestamp)
    invalid_submissions = []  # A list of submission_id

    for i in range(0, len(data)):
        submission_id, user_id, problem_id, timestamp, \
        answer, attempt_number, _, grade = data[i]

        if user_id in valid_submissions:
            if problem_id in valid_submissions[user_id]:
                subs = valid_submissions[user_id][problem_id]
                current_is_valid = True

                # If there is a correct answer already
                # don't include our current submission
                for sub in subs:
                    current_is_valid = current_is_valid and sub[3] != 1

                # If the current submission has the same answer as the previous one,
                # don't include it.
                if subs[-1][1] == answer:
                    current_is_valid = False

                # If the current submission is a duplicate, don't include it
                # duplicate means user_id, problem_id, timestamps are identical.
                for sub in subs:
                    current_is_valid = current_is_valid and sub[4] != timestamp

                if current_is_valid:
                    valid_submissions[user_id][problem_id].append(
                        (submission_id, answer, attempt_number, grade,
                         timestamp))
                else:
                    invalid_submissions.append(submission_id)
            else:
                valid_submissions[user_id][problem_id] = [(
                    submission_id, answer, attempt_number, grade, timestamp)]
        else:
            valid_submissions[user_id] = {
                problem_id: [(submission_id, answer, attempt_number, grade,
                              timestamp)]
            }

    # Modify invalid submissions in sql
    modify_invalids = '''
        UPDATE submissions
        SET validity = 0
        WHERE submission_id in (%s)'''
    block_sql_command(conn, cursor, modify_invalids, invalid_submissions,
                      BLOCK_SIZE)

    cursor.close()
    cursor = conn.cursor()

    # Modify valid submissions in sql
    valid_submission_ids = []
    for user_id in valid_submissions:
        for problem_id in valid_submissions[user_id]:
            for sub in valid_submissions[user_id][problem_id]:
                valid_submission_ids.append(sub[0])

    modify_valids = '''
        UPDATE submissions
        SET validity = 1
        WHERE submission_id in (%s)
    '''
    block_sql_command(conn, cursor, modify_valids, valid_submission_ids,
                      BLOCK_SIZE)

    cursor.close()
    conn.close()
