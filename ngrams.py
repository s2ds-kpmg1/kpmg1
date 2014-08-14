__author__ = 'elenagr'

"""

This file contains 3 functions:
best_ngrams(words, top_n, min_freq)
ngramsText(text,n,file1,file2=None)
ngramsFinder(text,min_freq,num_col,word_len)

"""
import logging
import re
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures

import gensim
from gensim.parsing.preprocessing import STOPWORDS

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

def best_ngrams(words, top_n, min_freq):

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

    # Write collocations to two files to be read by the preprocess program
    f1 = open('bigrams.txt', 'w')
    f1.writelines(["{0}\n".format(item)  for item in bigrams])
    f1.close()

    f2 = open('trigrams.txt', 'w')
    f2.writelines(["{0}\n".format(item)  for item in trigrams])
    f2.close()

    pat_gram2 = re.compile('(%s)' % '|'.join(bigrams), re.UNICODE)
    pat_gram3 = re.compile('(%s)' % '|'.join(trigrams), re.UNICODE)

    return pat_gram2, pat_gram3

def ngramsText(text,n,file1,file2=None):
    """
    This function takes a raw text and joins the trigrams and/or bigrams stored in file1(bigrams)
    and file2(trigrams) using underscores. In this way the tokenizer will consider them a single token.
    The argument n controls if only bigrams are to be found or also trigrams are expected.
    It returns the processed text.

    """
    print text
    if n == 3:

        print "Reading trigrams..."
        with open(file2) as f1:
            trigrams = f1.readlines()
            trigrams=[t.strip('\n') for t in trigrams]
            print trigrams
        for item in trigrams:
            itemst=str(item).lower()
            text=re.sub(itemst,itemst.replace(' ','_'), text.lower())
            print text

    if n == 2 or n == 3:

        print "Reading bigrams..."
        with open(file1) as f1:
            bigrams = f1.readlines()
            bigrams=[b.strip('\n') for b in bigrams]

            print bigrams
        for item in bigrams:
            itemst=str(item).lower()
            if n == 3:
                text=re.sub(itemst,itemst.replace(' ','_'), text.lower())
            elif n == 2:
                text=re.sub(itemst,itemst.replace(' ','_'), text.lower())
        print text

    else:
        print "Please insert the correct argument:\n 2 for bigrams \n 3 for bigrams and trigrams\n"

    return text

def ngramsFinder(text,min_freq,num_col,word_len):
    """
     This function takes a text, looks for the best n-grams,
     and returns a new text where the n-grams have been replaced by
     single token joined by '_'. In addition it generates two files with the
     results (bigrams.txt and trigrams.txt)

    """


    # Additional stopwords found in the results
    add_stopwords=['http','https','www','com','href','nbsp','arial','helvetica',
                   'font','verdana','sans','serif','fri','sat','font','bgcolor','ffffff',
                   'tel','fax','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']

    # Tokenize the text eliminating non alphanumeric characters, stopwords and also words of length <= 3
    tokens=[word for word in gensim.utils.tokenize(text, lower=True)
                if word not in STOPWORDS and len(word) > word_len if word not in add_stopwords]

    # Find the collocations in our text based on the frequency they appear.
    # Here is where all the magic happens :-)
    bigrams, trigrams=best_ngrams(tokens, top_n=num_col, min_freq=min_freq)

    #  re.sub is a function of the regular expressions library (re) which returns a string obtained
    #  by looking for 'pattern' in 'string' and replace it by 'repl'.
    # re.sub(pattern, repl, string, count=0, flags=0)
    # lambda is used in python to create anonymous functions. The equivalence is:
    # def function(N): return f(N)  -->  lambda N: f(N)

    tmp=re.sub(trigrams, lambda match: match.group(0).replace(u' ', u'_'), text.lower())
    newtext=re.sub(bigrams, lambda match: match.group(0).replace(u' ', u'_'), tmp)

    return newtext
