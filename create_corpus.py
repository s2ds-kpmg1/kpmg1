__author__ = 'elenagr'

import os
import time
import MySQLdb as mdb
from gensim import corpora
import enron
import create_dic as dic
import argparse
import stemming as stem


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

    corpus=[]

    print "Creating corpus..."

    for id in range(1, 101):
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp = cur.fetchall()
        text_stem = stem.stemmingString(tmp[0][0], id)
        corpus.append(dictionary.doc2bow(text_stem, allow_update=False))
        print id

    corpora.mmcorpus.MmCorpus.serialize('test.mm', corpus)
    mm = corpora.mmcorpus.MmCorpus('test.mm')
    dictionary.id2token("4300")
    print(mm[20])
    # print (corpus)
    outfile.write("{0}".format(corpus))

if __name__ == '__main__':
    main()
