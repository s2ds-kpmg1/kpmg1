#!/usr/bin/env python

#from __future__ import division, with_statement
import sys, re, os, fileinput, glob
import numpy as np
import pprint as pp

from optparse import OptionParser, OptionValueError

def prepare_pattern(option, opt, value, parser):
    if value.count('@') != 2 or value.find('@@') != -1:
        raise OptionValueError(
            'The pattern needs exactly two separated @ symbols\n')
    pat = value.replace('@','([-+.e\d]*)')
    setattr(parser.values, option.dest, pat)

parser = OptionParser(usage='Usage: %prog [options] DIR [DIR ...]')
parser.add_option("-p", "--pattern", action='callback', type='string',
                  dest='PATTERN',
                  help="The match pattern to extract X and Y values "
                  "from the filename for plotting. Use '@' for the numbers. "
                  "(default = no plotting)",default=None,
                  callback=prepare_pattern)


opts, dirnames = parser.parse_args()


# File name should be '.'+[1-9]{1,2,3,4}, check this

# Write a bash script which goes through all the folders and calls this Python script

def scrapeText(filename):
    "Extract the text."
    file=open(filename,'r')
    text=file.read()
    words=text.split()
    # Come up with a dictionary with words with no value (a, the, on, in, it, etc) and remove them here, or define a separate function for this
    # Use the package Scrapy to reduce text encoding formats to ASCII
    # Insert variable type recognition?
    wordfreq={}
    for word in words:
        if word in wordfreq:
            wordfreq[word]+=1
        else:
            wordfreq[word]=1
    wordprobvector={}
    corpus_size=len(words)
    for word in wordfreq:
        wordprobvector[word]=float(wordfreq[word])/corpus_size
    def sort_function(a, b):
        if a[1] > b[1]:
           return -1
        elif a[1] < b[1]:
            return 1

    wordfrqvec = []
    for word, prob in wordfreq.items():
         wordfrqvec.append((word,prob))
        
    sortedwordfrqvec=sorted(wordfrqvec, key=lambda prob: prob[1], reverse=True)

    return sortedwordfrqvec
    #result=wordfrqvec.sort(sort_function)

    #return wordfreq

    #return result[:2]

# Scrub the text to remove punctuation marks and non-words (e.g. text separators: '------------------------'


# Write a stemming function here (remove suffixes from words etc) to correctly count occurrence of meaning (s, ing, ive, er)
# Include exceptions (do not remove 'er' from 'Manchester')
# Stemming should be done BEFORE finding the mode words and determining the keywords
# Lemmatization? So that 'better' and 'good' are related
# Special cases for abbreviations and acronyms


# Train on Wordnet?


filelist=sorted(os.listdir(os.getcwd()))
for i in filelist:
    if "test_email" in i and "~" not in i and "#" not in i:
        result=scrapeText(i)
        pp.pprint(result)
