import re
import MySQLdb
import MySQLdb.cursors as cursors
import sqlparse


def open_SQL_connection(db_name, username, password, host, port):
    return MySQLdb.connect(
        host=host,
        port=port,
        user=username,
        passwd=password,
        db=db_name,
        cursorclass=cursors.SSCursor)


def executeSQL(connection, command, parent_conn=None):
    ''' command is a sequence of SQL commands
        separated by ";" and possibly "\n"
        connection is a MySQLdb connection
        returns the output from the last command
        in the sequence
    '''
    #This is somewhat a duplication of the function found in qpipe/util.py
    #but this is kept separate to avoid an awkward import dependency

    #split commands by \n
    commands = command.split("\n")
    #remove comments and whitespace"
    commands = [x for x in commands if x.lstrip()[0:2] != '--']
    commands = [re.sub('\r', '', x) for x in commands if x.lstrip() != '\r']
    command = ' '.join(commands)

    statements = sqlparse.split(command)
    for statement in statements:
        cur = connection.cursor()
        #make sure actually does something
        if sqlparse.parse(statement):
            print "executing SQL statement"
            cur.execute(statement)
        cur.close()
    connection.commit()
    if parent_conn:
        parent_conn.send(True)
    return True


def block_sql_command(conn, cursor, command, data, block_size):
    last_block = False
    current_offset = 0
    while not last_block:
        if current_offset + block_size < len(data):
            block = data[current_offset:current_offset + block_size]
        else:
            block = data[current_offset:]
            last_block = True
        if block:
            data_str = str(block)[1:-1]
            grounded_command = command % (data_str)
            cursor.execute(grounded_command)
            conn.commit()
            current_offset += block_size
