CREATE DATABASE IF NOT EXISTS DB_NAME;
USE DB_NAME;

-- All of these 12 tables are populated by CSV files
-- These table descriptions should be consistent with
-- moocdb.py::MOOCdb:TABLES
-- And also be consistent with corresponding event type
-- objects

CREATE TABLE IF NOT EXISTS submissions (
    submission_id              varchar(50)  NOT NULL,
    user_id                    varchar(50)  NOT NULL,
    problem_id                 int(11)      NOT NULL,
    submission_timestamp       datetime     NOT NULL,
    submission_attempt_number  int(11)      NULL,
    submission_answer          text         NULL,
    submission_is_submitted    int(2)       NOT NULL,
    submission_ip              varchar(50)  NULL,
    submission_os              int(11)      NULL,
    submission_agent           int(11)      NULL,
    validity                   int(1)       NULL,
    PRIMARY KEY (submission_id),
    KEY (user_id),
    KEY (problem_id)
);

CREATE TABLE IF NOT EXISTS agent (
    agent_id    int(11)      NOT NULL,
    agent_name  varchar(50)  NULL,
    PRIMARY KEY (agent_id)
);

CREATE TABLE IF NOT EXISTS assessments (
     assessment_id                  varchar(50)  NOT NULL,
     submission_id                  varchar(50)  NOT NULL,
     assessment_feedback            text         NULL,
     assessment_grade               double       NULL,
     assessment_grade_with_penalty  double       NULL,
     assessment_grader_id           varchar(50)  NULL,
     assessment_timestamp           datetime     NULL,
     PRIMARY KEY (assessment_id),
     KEY (assessment_grader_id),
     KEY (submission_id)
);

CREATE TABLE IF NOT EXISTS observed_events (
     observed_event_id         varchar(50)   NOT NULL,
     user_id                   varchar(50)   NOT NULL,
     url_id                    int(11)       NOT NULL,
     observed_event_timestamp  datetime      NOT NULL,
     observed_event_duration   int(11)       NULL,
     observed_event_ip         varchar(50)   NULL,
     observed_event_os         int(11)       NULL,
     observed_event_agent      int(11)       NULL,
     observed_event_type       varchar(255)  NULL,
     validity                  int(1)        NULL,
     PRIMARY KEY (observed_event_id),
     KEY (user_id),
     KEY (url_id)
);

CREATE TABLE IF NOT EXISTS os (
     os_id    int(11)      NOT NULL,
     os_name  varchar(50)  NULL,
     PRIMARY KEY (os_id)
);

CREATE TABLE IF NOT EXISTS problem_types (
     problem_type_id    varchar(50)  NOT NULL,
     problem_type_name  varchar(50)  NOT NULL,
     PRIMARY KEY (problem_type_id)
);

CREATE TABLE IF NOT EXISTS problems (
     problem_id                 int(11)       NOT NULL,
     problem_name               varchar(555)  NOT NULL,
     problem_parent_id          int(11)       NULL,
     problem_child_number       int(11)       NULL,
     problem_type_id            int(11)       NULL,
     problem_release_timestamp  datetime      NULL,
     problem_soft_deadline      datetime      NULL,
     problem_hard_deadline      datetime      NULL,
     problem_max_submission     int(11)       NULL,
     problem_max_duration       int(11)       NULL,
     problem_weight             int(11)       NULL,
     resource_id                int(11)       NULL,
     problem_week               int(11)       NULL,
     PRIMARY KEY (problem_id),
     KEY (problem_name),
     KEY (problem_parent_id),
     KEY (problem_type_id),
     KEY (resource_id)
);

CREATE TABLE IF NOT EXISTS resource_types (
     resource_type_id       int(11)      NOT NULL,
     resource_type_content  varchar(20)  NOT NULL,
     resource_type_medium   varchar(20)  NOT NULL,
     PRIMARY KEY (resource_type_id)
);

CREATE TABLE IF NOT EXISTS resources (
     resource_id                 int(11)       NOT NULL,
     resource_name               varchar(555)  NULL,
     resource_uri                varchar(555)  NOT NULL,
     resource_type_id            int(2)        NOT NULL,
     resource_parent_id          int(11)       NULL,
     resource_child_number       int(11)       NULL,
     resource_relevant_week      int(11)       NULL,
     resource_release_timestamp  datetime      NULL,
     PRIMARY KEY (resource_id),
     KEY (resource_uri),
     KEY (resource_type_id),
     KEY (resource_parent_id)
);

CREATE TABLE IF NOT EXISTS resources_urls (
     resources_urls_id  int(11)  NOT NULL,
     resource_id        int(11)  NOT NULL,
     url_id             int(11)  NOT NULL,
     PRIMARY KEY (resources_urls_id),
     KEY (resource_id),
     KEY (url_id)
);

CREATE TABLE IF NOT EXISTS urls (
     url_id  int(11)        NOT NULL,
     url     varchar(2083)  NULL,
     PRIMARY KEY (url_id)
);

-- This table is primarily for the VisMOOC team
-- It's a bit too Edx specific to be part of the core MOOCdb
-- schema frankly.
CREATE TABLE IF NOT EXISTS click_events (
     observed_event_id         varchar(50)                 NOT NULL,
     course_id                 varchar(50)                 NOT NULL,
     user_id                   varchar(50)                 NOT NULL,
     video_id                  varchar(2083)               NOT NULL,
     observed_event_timestamp  datetime                    NOT NULL,
     observed_event_type       varchar(255)                NOT NULL,
     url                       varchar(2083)               NOT NULL,
     code                      varchar(50)                 NOT NULL,
     video_current_time        float                       NULL,
     video_new_time            float                       NULL,
     video_old_time            float                       NULL,
     video_new_speed           float                       NULL,
     video_old_speed           float                       NULL,
     PRIMARY KEY (observed_event_id),
     KEY (user_id),
     KEY (video_id)
);

-- This is intended to be a one row entry containing metadata
-- for the full pipe execution
-- More specifically, the git describe of current HEAD of MLC repo
CREATE TABLE IF NOT EXISTS metadata(
    commit_hash                 varchar(50) NULL,
     -- duration measured in minutes
    events_processing_duration  int(255)    NULL,
    KEY (commit_hash)
);

-- This table is not populated with data
-- There is no insertion script corresponding
-- to this table in copy_to_mysqlDB.sql
CREATE TABLE IF NOT EXISTS answer (
    answer_id       int(11)  NOT NULL,
    answer_content  text     NULL,
    PRIMARY KEY (answer_id)
);
