#!/usr/env/python

import numpy as np
import argparse
from distutils.version import StrictVersion
import sys

parser = argparse.ArgumentParser(description='Get the top n topics. Plot histogram of all topics. NB requires Numpy 1.8+')
parser.add_argument('-f', '--filename', help = 'Filename containing the probability vectors for each document', required = True, type=str)
parser.add_argument('-n', '--number', help = 'Return the top n topics', required = True, type=int)
parser.add_argument('-p', '--plot', help = 'Plot histogram', action='store_true')

def main():

    numpy_version = np.__version__

    if StrictVersion('1.8.1') > StrictVersion(numpy_version):
        print """Your version of numpy is too old.  This code requires >= 1.8 
        but you have version {0}""".format(numpy_version)
        sys.exit()

    args = parser.parse_args()

    X = np.genfromtxt(args.filename, unpack = True)

    topics = np.shape(X)[0]

    score = []

    for t in range(topics):

        summation = np.sum(X[:][t])
        score.append(summation)

        print t, summation

    score = np.array(score)
    ind = np.argpartition(score, -args.number)[-args.number:]

    print 'Most important topics are: '
    print ind
    print 'with scores'
    print score[ind]



#Auto data sample:
#[54 71 21 18 57 47 49  3  2 24]

#Old output - alpha = 0.1
#In [7]: ind
#Out[7]: array([39, 62, 60, 49, 37, 31, 26, 13,  9,  0])

#In [8]: score[ind]
#Out[8]:
#array([  6054.25213735,  23005.53803987,   6188.53675998,  10624.11923656,
#         8552.07141789,   8780.46728334,  11576.84519712,  12077.38138667,
#         8206.77927727,  11312.8841365 ])

if __name__ == "__main__":
    main()
