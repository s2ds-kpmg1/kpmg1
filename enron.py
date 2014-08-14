#!/usr/env/python

"""Functions we might find useful"""

import MySQLdb as mdb

def querySample(N):
    con, cur=connectDB("enron")

    # We generate a random sample of the entries.
    sample=random.sample(range(size[0]),int(math.floor(size[0]*N)))
    texts=[]

    # We query the emails in the sample and store them in a list
    for id in sample:
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp=cur.fetchall()
        texts.append(tmp[0][0])

    con.close()

    return texts


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
