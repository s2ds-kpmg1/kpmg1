__author__ = 'elenagr'

import os
import time
import MySQLdb as mdb
from gensim import corpora
import enron
import create_dic as dic
import argparse
import stemming as stem
import enron


class MyCorpus(object):
    def __iter__(self):
        try:
            connection = mdb.connect('localhost', 'kpmg1', 's2ds', 'enron')
            cur = connection.cursor()
            cur.execute("select id from emails order by id desc limit 1;")
            res = cur.fetchall()
            size = [int(col) for row in res for col in row]
            for i in range(1,size[0]):
                command="""'emails','text','id = {0}'""".format(i)
                text = enron.queryDb(command)[0][0]
                text_stem = stem.stemmingString(text, id)
                yield dictionary.doc2bow(text_stem, allow_update=False)
        finally:
            connection.close()

def main():

    outfile = open('corpus.txt', 'w')

    print "Customizing dictionary..."

    dictionary=dic.customizeDic(10)

    connection = mdb.connect('localhost', 'kpmg1', 's2ds', 'enron')
    cur = connection.cursor()

    # In our case the IDs are ordered by entry. Otherwise you could do:
    # cur.execute("SELECT COUNT(*) FROM emails;")
    # The last ID number gives us the number of rows of the table.
    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    size = [int(col) for row in res for col in row]

    print "Creating corpus..."

    corpus=MyCorpus()

    outfile.write("{0}".format(corpus))
    corpora.mmcorpus.MmCorpus.serialize('corpus.mm', corpus)

    connection.close()

if __name__ == '__main__':
    main()
