use DB_NAME;
SET @@global.local_infile = 1;

LOAD DATA local INFILE  'MOOCDB_DIR/agent.csv'
INTO TABLE agent
FIELDS TERMINATED BY ',';

-- Copy answer data
-- LOAD DATA local INFILE 'COURSE_FOLDER_NAME/moocdb_csv/answer.csv'
-- INTO TABLE answer
-- FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/assessments.csv'
INTO TABLE assessments
FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/observed_events.csv'
INTO TABLE observed_events
FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/os.csv'
INTO TABLE os
FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/problem_types.csv'
INTO TABLE problem_types
FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/problems.csv'
INTO TABLE problems
FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/resource_types.csv'
INTO TABLE resource_types
FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/resources.csv'
INTO TABLE resources
FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/resources_urls.csv'
INTO TABLE resources_urls
FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/submissions.csv'
INTO TABLE submissions
FIELDS TERMINATED BY ',';

LOAD DATA local INFILE 'MOOCDB_DIR/urls.csv'
INTO TABLE urls
FIELDS TERMINATED BY ',';

-- click_events is handled differently to set nulls explicitly instead of empty strings.
-- This removes the burden on the python code to handle click_events differently from
-- the other moocdb tables.
LOAD DATA local INFILE 'MOOCDB_DIR/click_events.csv'
INTO TABLE click_events
FIELDS TERMINATED BY ','
(@v1, @v2, @v3, @v4, @v5, @v6, @v7, @v8, @v9, @v10, @v11, @v12, @v13)
SET
observed_event_id        = nullif(@v1, ''),
course_id                = nullif(@v2, ''),
user_id                  = nullif(@v3, ''),
video_id                 = nullif(@v4, ''),
observed_event_timestamp = nullif(@v5, ''),
observed_event_type      = nullif(@v6, ''),
url                      = nullif(@v7, ''),
code                     = nullif(@v8, ''),
video_current_time       = nullif(@v9, ''),
video_new_time           = nullif(@v10, ''),
video_old_time           = nullif(@v11, ''),
video_new_speed          = nullif(@v12, ''),
video_old_speed          = nullif(@v13, '')
;

LOAD DATA local INFILE 'MOOCDB_DIR/metadata.csv'
INTO TABLE metadata
FIELDS TERMINATED BY ',';
