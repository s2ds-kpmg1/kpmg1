#!/usr/env/python

"""Functions we might find useful"""

import MySQLdb as mdb


def deleteTable(cur, tablename):

	"""Delete a table when you are connected to the database"""

    cur.execute("""DROP TABLE IF EXISTS {0}""".format(tablename))
    return

def deleteDB(cur, dbname):

	"""Delete a database when you are connected to it"""

    cur.execute("""DROP DATABASE IF EXISTS {0}""".format(dbname))
    return

def connectDB(db):

	"""Connect to a database with the following credentials"""

    connection = mdb.connect('localhost', 'kpmg1', 's2ds', db)
    cursor=connection.cursor()

    return (connection,cursor)
