#!/usr/env/python

from gensim.models.lsimodel import LsiModel
from gensim.models.lsimodel import stochastic_svd
import time
from gensim import corpora
import argparse
import pprint as pp


parser = argparse.ArgumentParser(description='Performs Latent Semantic Analysis on an input corpus.')
parser.add_argument("--corpus","-c",help="Input name of corpus file (MM file type)",default=None, required=True, type=str)
parser.add_argument("--dict","-d",help="Input name of dictionary file",default=None, required=True, type=str)
parser.add_argument("--ntopics","-nt",help="Input desired number of topics",default=10, required=True, type=int)
#parser.add_argument("--nwords","-nw",help="Input desired number of words to show per topic",default=10, required=True, type=int)

args = parser.parse_args()


start_time=time.time()

print "\nLoading dictionary..."
dict = corpora.Dictionary.load_from_text(args.dict)
print(dict)
print "\nLoading corpus..."
corpus = corpora.MmCorpus(args.corpus)
print(corpus)

print "\nPerforming Latent Semantic Indexing..."
lsi = LsiModel(corpus=corpus, num_topics=args.ntopics, id2word=dict, distributed=False)

## This is the fancy stochastic (aka truncated) SVD, however it throws runtime memory errors for me (e.g. segmentation fault)
#lsi = stochastic_svd(corpus,rank=100,num_terms=args.ntopics)

screenoutput = lsi.print_topics(num_topics=10, num_words=1)
output = lsi.print_topics(num_topics=10, num_words=10)
print "\nResult:"
pp.pprint(screenoutput)
#lsi.save('lsi_result.txt')

f = open('lsi_result.txt','w')
f.seek(0)
f.write(str(output))
f.close()

end_time=time.time()
runtime=end_time-start_time
print "\nRuntime: {0} seconds\n".format(runtime)
