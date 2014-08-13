#!/usr/env/python

"""Functions we might find useful"""

import MySQLdb as mdb


def deleteTable(cur, tablename):

    cur.execute("""DROP TABLE IF EXISTS {0}""".format(tablename))
    return

def deleteDB(cur, dbname):

    cur.execute("""DROP DATABASE IF EXISTS {0}""".format(dbname))
    return

def connectDB(db):

    connection = mdb.connect('localhost', 'kpmg1', 's2ds', db)
    cursor=connection.cursor()

    return (connection,cursor)
