from __future__ import print_function

import os
import re
from subprocess import call

import mysql.connector
import sqlparse

# Returns True if any of the regex match the specified field
# False otherwise.


def match_regex(regexes, field, dictionary):
    for regex in regexes:
        r = re.compile(regex)
        if r.search(str(dictionary[field])):
            return True
    return False


def create_mysql(cfg_mysql, cfg_data_file, cfg_mysql_script_path):
    print('****** Create and Curate MySQL db from csv files *******')
    print('Creating MySQL Database : %s' % cfg_mysql['database'])
    # Create the .sql script for DB creation
    filename = cfg_mysql_script_path['qpipe_create_db_path']
    to_be_replaced = ['DB_NAME']
    replace_by = [cfg_mysql['database']]
    replaced_script = replaceWordsInFile(filename, to_be_replaced, replace_by)
    create_name = "create_to_mysqlDB_%s.sql" % cfg_data_file['course_folder']
    create_script = open(create_name, "w")
    create_script.write(replaced_script)
    create_script.close()
    shell_cmd = "mysql -h%s -P%d -u%s --password=\'%s\' < %s" % (
        cfg_mysql['host'], cfg_mysql['port'], cfg_mysql['user'],
        cfg_mysql['password'], create_name)
    call(shell_cmd, shell=True)
    os.remove(create_name)


def fill_mysql(cfg_mysql, cfg_csv_path, cfg_data_file, mysql_script):
    print('Filling MYSQL Database : %s with csv files data for %s' %
          (cfg_mysql['database'], cfg_data_file['course_folder']))

    # Create the .sql script for DB creation
    filename = mysql_script
    to_be_replaced = ['MOOCDB_DIR', 'DB_NAME']
    replace_by = [cfg_csv_path['moocdb_csv_dir'], cfg_mysql['database']]
    replaced_script = replaceWordsInFile(filename, to_be_replaced, replace_by)
    copy_name = "copy_to_mysqlDB_%s.sql" % cfg_data_file['course_folder']
    copy_script = open(copy_name, "w")
    copy_script.write(replaced_script)
    copy_script.close()
    shell_cmd = "mysql -h%s -P%d -u%s --password=\'%s\' --local-infile < %s" % (
        cfg_mysql['host'], cfg_mysql['port'], cfg_mysql['user'],
        cfg_mysql['password'], copy_name)
    call(shell_cmd, shell=True)
    os.remove(copy_name)


def replaceWordsInFile(filename, to_be_replaced, replace_by):
    txt = open(filename, 'r').read()
    if len(to_be_replaced) != len(replace_by):
        print('Error: sizes must be the same')
        exit(1)
    else:
        for i in range(0, len(to_be_replaced)):
            txt = re.sub(re.escape(to_be_replaced[i]), replace_by[i], txt)
    return txt


def executeSQL(connection, command, parent_conn=None):
    ''' command is a sequence of SQL commands
        separated by ";" and possibly "\n"
        connection is a MySQLdb connection
        returns the output from the last command
        in the sequence
    '''
    commands = command.split("\n")
    # remove comments and whitespace
    commands = [x for x in commands if x.lstrip()[0:2] != '--']
    commands = [re.sub('\r', '', x) for x in commands if x.lstrip() != '\r']
    command = ' '.join(commands)

    statements = sqlparse.split(command)

    for statement in statements:
        cur = connection.cursor()
        # make this sure actually does something
        if sqlparse.parse(statement):
            print("executing SQL statement")
            cur.execute(statement)
        cur.close()
    connection.commit()

    if parent_conn:
        parent_conn.send(True)
    return True
