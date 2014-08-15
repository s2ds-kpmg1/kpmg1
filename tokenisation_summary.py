#!/usr/env/python

"""Examing the output from the csv files generated in the stemming_test.py
script and pull out the most common words and their frequency.  Also use
the dictionary to search for non-English words"""

import argparse
import glob
from collections import Counter
import os
import cPickle as pickle

parser = argparse.ArgumentParser(description='Run some tests on the output files from stemming_test.py')
parser.add_argument('directory', help='Directory where you are keeping the files', type = str)
parser.add_argument('-s', '--savepickle', help='Save some output in a pickle', action='store_true', default=False)

def main():

    args = parser.parse_args()

    print args

    #add trailing / if necessary

    if (args.directory[-1] != '/'): 
        args.directory = args.directory+'/'

    findcsv = glob.glob('{0}*.csv'.format(args.directory))

    print 'Found {0} files:'.format(len(findcsv))

    results_dict = [{'tokeniser':'', 'stemmer':'', 'tokens':0, 'unique':0, 'most_common':[], 'over_500':[]} for f in findcsv]

    for i,foundfile in enumerate(findcsv):

        with open(foundfile, 'r') as f:
            data = f.read()

        fname = os.path.splitext(os.path.basename(foundfile))[0].split('_')
        tokeniser = fname[1]
        stemmer = fname[2]

        data = data.strip('\r\n').split(',')



        data_unique = set(data)

        counter = Counter(data)

        most_common = counter.most_common()[0:50]

        all_common = dict((k,v) for k,v in counter.items() if v >=500)

        print '************************************'
        print 'Tokeniser: {0}'.format(tokeniser)
        print 'Stemmer: {0}'.format(stemmer)
        print 'Token number: {0}'.format(len(data))
        print 'Unique tokens: {0}'.format(len(data_unique))
        print '50 Most Common Words: '
        print most_common
        print 'All words > 500 frequency:'
        print all_common
        print ''

        results_dict[i]['tokeniser'] = tokeniser
        results_dict[i]['stemmer'] = stemmer
        results_dict[i]['tokens'] = len(data)
        results_dict[i]['unique'] = len(data_unique)
        results_dict[i]['most_common'] = most_common
        results_dict[i]['over_500'] = all_common


    print '************************************'

    if args.savepickle == True:
        with open('tokeniser_stats.pkl', 'wb') as output:
            pickle.dump(results_dict, output)
        print 'Written pickle {0}'.format('tokeniser_stats.pkl')
        



if __name__ == "__main__":
    main()