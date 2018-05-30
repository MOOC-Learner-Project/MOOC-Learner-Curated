CREATE DATABASE IF NOT EXISTS DB_NAME;
USE DB_NAME;
SET @@global.local_infile = 1;
SET @original_sql_mode = @@SESSION.sql_mode;
SET SESSION sql_mode = '';

SET SESSION sql_mode = @original_sql_mode;
