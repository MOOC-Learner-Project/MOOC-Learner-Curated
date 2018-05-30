CREATE DATABASE IF NOT EXISTS DB_NAME;
USE DB_NAME;
SET @@global.local_infile = 1;

CREATE TABLE IF NOT EXISTS courses (
    _id varchar(255) NOT NULL,
    original_id varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    year varchar(255) NOT NULL,
    org varchar(255) NOT NULL,
    instructor varchar(255) NOT NULL,
    description varchar(255) NOT NULL,
    start_date datetime NOT NULL,
    end_date datetime NOT NULL,
    course_url varchar(2083) NOT NULL,
    image_url varchar(2083) NOT NULL,
    PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS course_video (
    _id varchar(255) NOT NULL,
    course_id varchar(255) NOT NULL,
    video_id varchar(255) NOT NULL,
    PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS videos (
    _id varchar(255) NOT NULL,
    original_id varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    section varchar(255) NOT NULL,
    description varchar(255) NOT NULL,
    url varchar(255) NOT NULL,
    PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS enrollments (
    _id varchar(255) NOT NULL,
    user_id varchar(11) NOT NULL,
    course_id varchar(255) NOT NULL,
    timestamp datetime NOT NULL,
    action TINYINT NOT NULL,
    PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS forum (
    _id varchar(255) NOT NULL,
    original_id varchar(255) NOT NULL,
    course_id varchar(255) NOT NULL,
    author_id varchar(255) NOT NULL,
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    body LONGTEXT NOT NULL,
    type varchar(255) NOT NULL,
    title MEDIUMTEXT NOT NULL,
    thread_type varchar(255) NOT NULL,
    comment_thread_id varchar(255) NOT NULL,
    parent_id varchar(255) NOT NULL,
    PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS grades (
    _id varchar(255) NOT NULL,
    user_id varchar(11) NOT NULL,
    course_id varchar(255) NOT NULL,
    timestamp datetime NOT NULL,
    grade varchar(5) NOT NULL,
    PRIMARY KEY (_id)
);

CREATE TABLE IF NOT EXISTS users (
    _id varchar(255) NOT NULL,
    original_id varchar(11) NOT NULL,
    username varchar(30) NOT NULL,
    name varchar(255) NOT NULL,
    language varchar(255) NOT NULL,
    location varchar(255) NOT NULL,
    birth_date varchar(11) NOT NULL,
    education_level varchar(6) NOT NULL,
    bio LONGTEXT NOT NULL,
    gender varchar(6) NOT NULL,
    country varchar(2) NOT NULL,
    PRIMARY KEY (_id)
);


LOAD DATA local INFILE 'MOOCDB_DIR/courses.csv'
IGNORE INTO TABLE courses
FIELDS TERMINATED BY ',' ENCLOSED BY '"';

LOAD DATA local INFILE 'MOOCDB_DIR/course_video.csv'
IGNORE INTO TABLE course_video
FIELDS TERMINATED BY ',' ENCLOSED BY '"';

LOAD DATA local INFILE 'MOOCDB_DIR/videos.csv'
IGNORE INTO TABLE videos
FIELDS TERMINATED BY ',' ENCLOSED BY '"';

LOAD DATA local INFILE 'MOOCDB_DIR/enrollments.csv'
IGNORE INTO TABLE enrollments
FIELDS TERMINATED BY ',' ENCLOSED BY '"';

LOAD DATA local INFILE 'MOOCDB_DIR/forum.csv'
IGNORE INTO TABLE forum
FIELDS TERMINATED BY ',' ENCLOSED BY '"';

LOAD DATA local INFILE 'MOOCDB_DIR/grades.csv'
IGNORE INTO TABLE grades
FIELDS TERMINATED BY ',' ENCLOSED BY '"';

LOAD DATA local INFILE 'MOOCDB_DIR/users.csv'
IGNORE INTO TABLE users
FIELDS TERMINATED BY ',' ENCLOSED BY '"';
