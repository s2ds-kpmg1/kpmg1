__author__ = 'elenagr'

import logging
import re
import argparse
import math
import random
import MySQLdb as mdb

import nltk
from nltk import word_tokenize
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures

import gensim
from gensim.parsing.preprocessing import STOPWORDS

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

parser = argparse.ArgumentParser(description="Generating a dictionary of stopwords")
parser.add_argument("--sample",help="Size of sample in percentage", dest="sample",required=True,type=float)

def best_ngrams(words, top_n=1000, min_freq=100):

    """
    This function has been extracted from a tutorial given in Europython 2014 about
    topic modelling given by Radim Rehurek

    Extract `top_n` most salient collocations (bigrams and trigrams),
    from a stream of words. Ignore collocations with frequency
    lower than `min_freq`.

    This fnc uses NLTK for the collocation detection itself -- not very scalable!

    Return the detected ngrams as compiled regular expressions, for their faster
    detection later on.

    """
    tcf = TrigramCollocationFinder.from_words(words)
    tcf.apply_freq_filter(min_freq)
    trigrams = [' '.join(w) for w in tcf.nbest(TrigramAssocMeasures.chi_sq, top_n)]
    logging.info("%i trigrams found: %s..." % (len(trigrams), trigrams[:20]))

    bcf = tcf.bigram_finder()
    bcf.apply_freq_filter(min_freq)
    bigrams = [' '.join(w) for w in bcf.nbest(BigramAssocMeasures.pmi, top_n)]
    logging.info("%i bigrams found: %s..." % (len(bigrams), bigrams[:20]))

    pat_gram2 = re.compile('(%s)' % '|'.join(bigrams), re.UNICODE)
    pat_gram3 = re.compile('(%s)' % '|'.join(trigrams), re.UNICODE)

 #   print bigrams
 #   print trigrams

    return pat_gram2, pat_gram3

def main():
    args = parser.parse_args()
    N = args.sample

    # Open the connection to the DB
    connection = mdb.connect('localhost', 'kpmg1', 's2ds','enron')
    cur=connection.cursor()


    # In our case the IDs are ordered by entry. Otherwise you could do: cur.execute("SELECT COUNT(*) FROM emails;")
    # The last ID number gives us the number of rows of the table.
    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    size=[int(col) for row in res for col in row]


    # We generate a random sample of the entries.
    sample=random.sample(range(size[0]),int(math.floor(size[0]*N)))

    texts=[]

    for id in sample:
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp=cur.fetchall()
        texts.append(tmp[0][0])

    raw=" ".join(texts)

    new=['http','https','www','com']

    tokens=[word for word in gensim.utils.tokenize(raw, lower=True)
                if word not in STOPWORDS and len(word) > 3 if word not in new]
    #print tokens
    best_ngrams(tokens, top_n=1000, min_freq=500)

    text = nltk.Text(tokens)
    coll=text.collocations()

    # Close all cursors
    connection.close()
    # Close all databases
    return


if __name__ == "__main__":
    main()

