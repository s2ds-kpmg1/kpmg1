#!/usr/env/python

import logging, gensim, bz2
import pdb
import random
    
    
def main():
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    # load id->word mapping (the dictionary), one of the results of step 2 above
    id2word = gensim.corpora.Dictionary.load_from_text('dictionary_words.txt')
    # load corpus iterator
    mm = gensim.corpora.MmCorpus('corpus.mm')
    # mm = gensim.corpora.MmCorpus(bz2.BZ2File('wiki_en_tfidf.mm.bz2')) # use this if you compressed the TFIDF output
    
    print(mm)

    #we can split the corpus to test the samples with a hold-out technique

    cp = list(mm)
    random.shuffle(cp)

    cp_size = int(len(cp)*0.8)
    cp_train = cp[0:p]
    cp_test = cp[p:]


    
    #This is the pure gensim version. It uses variational Bayes
    #lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=100, update_every=1, chunksize=5000, passes=5)
    
    pdb.set_trace()
    
    #This is the same set-up but run through the MALLET code instead which uses Gibbs sampling
    lda_mallet = gensim.models.mallet('/Users/emma/mallet/bin/mallet', corpus=mm, id2word=id2word, num_topics=100, update_every=1, chunksize=5000, passes=5)

    
if __name__ == "__main__":

    main()