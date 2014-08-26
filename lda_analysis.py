#!/usr/env/python

import logging, gensim
import pdb
import random
import re
import argparse

parser = argparse.ArgumentParser(description = 'Applying LDA to a corpus')
parser.add_argument('-d', '--dictionary', help = 'Dictionary file', required = True, type = str)
parser.add_argument('-c', '--corpus', help='Corpus file', required = True, type = str)
parser.add_argument('-t', '--topics', help = 'Number of topics', required = True, type = int)
parser.add_argument('-l', '--logfile', help = 'Logfile', default='gensim.lda.log')

def lda_testing(dictionary_array, corpus_array, topic_array, logfile='gensim.lda_testing.log', 
    eval_every=20, chunksize=10000, passes=2):

    """Function to test LDA on a variety of corpora with their corresponding dictionaries over a number of topics"""

    logging.basicConfig(filename=logfile, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    for dictionary,corpus in zip(dictionary_array, corpus_array):

        id2word = gensim.corpora.Dictionary.load_from_text(dictionary)

        mm = gensim.corpora.MmCorpus(corpus)

        logging.info('Using dictionary {0}'.format(dictionary))
        logging.info('Loaded corpus {0}'.corpus)

        print 'Using dictionary {0}'.format(dictionary)
        print 'Using corpus {0}'.format(corpus)

        for ntop in topic_array:

            logging.info('Using topic number {0}'.format(ntop))
            print 'Using topic number {0}'.format(ntop)

            lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=ntop, 
                eval_every=eval_every, chunksize=chunksize, passes=passes)

    return

    
def main():

    """Will run gensim.LDA on a dictionary, corpus and set number of topics.  To run over a range
    of these checkout the lda_testing() function"""
    
    args = parser.parse_args()

    id2word = gensim.corpora.Dictionary.load_from_text(args.dictionary)

    topics = args.topics

    logging.basicConfig(filename=args.logfile, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    mm = gensim.corpora.MmCorpus(corp)

    print (corp)
    print(mm)

    logging.info("Using corpus {0}".format(corp))
    logging.info("Using topic number {0}".format(ntop))
    print 'Running topic {0}'.format(ntop)

    #This is the pure gensim version. It uses variational Bayes
    lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=topics, eval_every=20, chunksize=10000, passes=5)
  
    

    
if __name__ == "__main__":

    main()