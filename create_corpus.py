__author__ = 'elenagr'

import os
import time
import MySQLdb as mdb
from gensim import corpora, models, matutils
from time import time
import create_dic as dic
import argparse
import stemming as stem
import numpy as np
import tfidf
import kmeans_analysis as Mykmeans

class MyCorpus(object):
     def __init__(self, dict_name,size=None):
        self.dict_name = dict_name
        self.dictionary=corpora.Dictionary.load_from_text(dict_name)
        self.connection = mdb.connect('localhost', 'kpmg1', 's2ds', 'enron')
        self.cur = self.connection.cursor()
        if size == None:
            self.cur.execute("select id from emails order by id desc limit 1;")
            res = self.cur.fetchall()
            tmp = [int(col) for row in res for col in row]
            self.size=tmp[0]
        else:
            self.size = size

     def __iter__(self):
        try:
            for id in range(1,self.size):
                self.cur.execute(" select text from emails where id = {0} ".format(id))
                tmp = self.cur.fetchall()
                text_stem = stem.stemmingString(tmp[0][0], id, stopwords=False)
                yield self.dictionary.doc2bow(text_stem, allow_update=False)
        finally:
            self.connection.close()


parser = argparse.ArgumentParser(description="Generating a corpus")
parser.add_argument("--stopwords", help="Add stopwords",default=False, action='store_true')
parser.add_argument("--minfreq", help="Don't consider words whose frequency in the dictionary is below minfreq",
                    default=0,required = False, type=int)
parser.add_argument('--maxfreq', help = "Don't consider words whose frequency in the dictionary is over maxfreq",
                    default=300000,required = False, type=int)
parser.add_argument("--all", help="Create corpus using the whole set of emails",default=False, action='store_true')
parser.add_argument('--emails', help = 'Number of emails used to build the corpus',
                    default=None,required = False, type=int)
parser.add_argument("--tfidf", help="Apply tf-idf to the corpus",default=False, action='store_true')
parser.add_argument("--npy", help="Save corpus as a numpy array to be read by sci-kit learn",
                    default=False, action='store_true')
parser.add_argument("--bin", help="Save corpus as a binary file to be read by anybody",
                    default=False, action='store_true')

def main():

    args = parser.parse_args()
    min=args.minfreq
    max=args.maxfreq
    Nemails=args.emails
    stopws=args.stopwords

    if args.all:
        filename="corpus_min{0}_stopwds{1}_all.mm".format(min,stopws)
    else:
        filename="corpus_min{0}_stopwds{1}_{2}emails.mm".format(min,stopws,Nemails)

    t0=time()

    print "Customizing dictionary..."
    dictionaryname="new_dic_"+filename.split(".")[0]

    dic.customizeDic(dictionaryname,min,max,stopwords=stopws)

    dictionaryname=dictionaryname+"_freq.txt"

    print "Creating corpus..."

    dict=corpora.Dictionary.load_from_text(dictionaryname)
    features=len(dict)
    # Create corpus
    corpus=MyCorpus(dictionaryname,size=Nemails)
    # Save corpus to a mm file
    corpora.mmcorpus.MmCorpus.serialize(filename, corpus)
    print "Corpus created in {0} secs".format(time()-t0)

    if args.tfidf:
        print "Applying tf-idf to the corpus"
        corpus=tfidf.tfidfCorpus(filename)
        filename=filename.split(".")[0]+'_tfidf.'+filename.split(".")[1]

    if args.npy:
        print "Saving corpus as a numpy array"
        Mykmeans.npmatrixCorpus(filename,features)

    if args.bin:
        print "Saving corpus as a binary file"
        filename=filename.split(".")[0]+".npy"
        Mykmeans.binaryMatrix(filename)

    t1=time()-t0

    print "Dictionary used to create the corpus: {0}".format(dictionaryname)
    print 'Total time to create corpus: {0} sec'.format(t1)

    return corpus

if __name__ == '__main__':
    main()
