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


class MyCorpus():
    def __iter__(self):
        try:
            print "Customizing dictionary..."
            dictionary=dic.customizeDic(10,30000)
            connection = mdb.connect('localhost', 'kpmg1', 's2ds', 'enron')
            cur = connection.cursor()
            cur.execute("select id from emails order by id desc limit 1;")
            res = cur.fetchall()
            size = [int(col) for row in res for col in row]
            for id in range(1,size[0]):
                #print id
                cur.execute(" select text from emails where id = {0} ".format(id))
                tmp = cur.fetchall()
                text_stem = stem.stemmingString(tmp[0][0], id)
                yield dictionary.doc2bow(text_stem, allow_update=False)
        finally:
            connection.close()

def main():

    outfile = open('corpus.txt', 'w')

    print "Creating corpus..."

    corpus=MyCorpus()

    corpora.mmcorpus.MmCorpus.serialize('corpus.mm', corpus)

    return corpus

if __name__ == '__main__':
    main()
