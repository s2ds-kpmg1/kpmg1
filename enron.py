#!/usr/env/python

"""Functions we might find useful"""

import MySQLdb as mdb
from nltk.corpus import stopwords
import random
import math

def getCustomStopwords(filename='add_stopwords.txt'):

    """Returns the full list, plus our new list of stopwords"""

    stopwords = stopwords.words('english')

    with open(filename, 'r') as f:

        new = f.readlines()

    new = [unicode(n.strip()) for n in new]

    updated = stopwords + new

    return updated

def addToStopwords(word, filename = 'add_stopwords.txt'):

    """Add single word to stopwords file"""

    with open(filename, 'a') as f:
        f.write(unicode(word+'\n'))

    return



def querySample(N):
    con, cur=connectDB("enron")

    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    size=[int(col) for row in res for col in row]

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
