#!/usr/env/python

from gensim.models.lsimodel import LsiModel
from gensim.models.lsimodel import stochastic_svd
import time, argparse, shutil, os
from gensim import corpora
import pprint as pp
#import logging
from operator import itemgetter
import cPickle as pickle


#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Performs Latent Semantic Analysis on an input corpus.')
parser.add_argument("--corpus","-c",help="Input name of corpus file (MM file type)",default=None, required=True, type=str)
parser.add_argument("--dict","-d",help="Input name of dictionary file",default=None, required=True, type=str)
parser.add_argument("--ntopics","-nt",help="Input desired number of topics",default=10, required=True, type=int)
parser.add_argument("--query","-q",help="Input document for similarity query against topics found",default=None, required=True, type=int)
parser.add_argument("--nwords","-nw",help="Input desired number of words to show per topic",default=10, required=False, type=int)


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

#if len(args.query)!=1:
#print corpus[args.query]
queryresult = lsi[corpus[args.query]]
sortedqueryresult = sorted(list(queryresult), key=lambda query: abs(query[1]), reverse=True)
#screenqueryresult = sorted(list(queryresult), key=itemgetter(1))

#screenoutput = lsi.print_topics(num_topics=10, num_words=1)
#output = lsi.print_topics(num_topics=10, num_words=10)
#print "\nResult:"
#pp.pprint(screenoutput)
#lsi.save('lsi_result.txt')


corpustopics=lsi.show_topics(num_words=args.ntopics, log=True, formatted=False)
screencorpustopics=lsi.show_topics(num_words=args.nwords, log=False, formatted=True)

print "\nCorpus top five topics: (full set of topics printed to file)"
pp.pprint(screencorpustopics[:5])
# Use this to show all the words within e.g. the first topic, not just the top 10 words
#pp.pprint(corpustopics[:1])
print "\nSimilarity of document number {0} in corpus with corpus topics:".format(args.query)
pp.pprint(sortedqueryresult)
#pp.pprint(sortedqueryresult[:10])

rootdir=os.getcwd()
foldername='lsi_output'
folderpath=os.path.join(rootdir,foldername)
if (os.path.exists(folderpath)==True):
    shutil.rmtree(folderpath)
    os.makedirs(folderpath)
else:
    os.makedirs(folderpath)

os.chdir(folderpath)

lsimodelfile=(str(args.corpus).replace('.mm',''))+'_lsi.model'
lsi.save(lsimodelfile)
#filename1= (str(args.corpus).replace('.mm',''))+'_lsi_topics.txt'
filename1= (str(args.corpus).replace('.mm',''))+'_lsi_topics.pkl'
filename2= (str(args.corpus).replace('.mm',''))+('_item_{0}_classification.txt'.format(args.query))

with open(filename1,'wb') as output:
    pickle.dump(corpustopics, output)
# f = open(filename1,'w')
# f.seek(0)
# f.write(str(corpustopics))
# f.close()
f = open(filename2,'w')
f.seek(0)
f.write(str(queryresult))
f.close()

os.chdir(rootdir)

end_time=time.time()
runtime=end_time-start_time
print "\nRuntime: {0} seconds\n".format(runtime)
