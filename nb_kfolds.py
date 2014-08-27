#!/usr/env/python

import numpy as np
from sklearn.naive_bayes import MultinomialNB
import argparse
from sklearn import cross_validation
import pdb


parser = argparse.ArgumentParser(description='K-fold Testing using Naive Bayes on a model')
parser.add_argument('-c', '--corpus', help = 'A numpy file for the corpus (including .npy)', required = True, type = str)
parser.add_argument('-l', '--labels', help = 'A file containing a list of labels for each document in the corpus', required = True, type = str)
parser.add_argument('-k', '--kfold', help='Number of kfolds', default = 10, type=int)

def main():

    args = parser.parse_args()

    y = np.genfromtxt(args.labels, unpack = True, dtype=None)

    X = np.load(args.corpus)

    #you must transpose X!
    X = X.transpose()

    clf = MultinomialNB()
   # clf.fit(X,y)

    n_elements = len(y)
    nfolds = args.kfold

    kf = cross_validation.KFold(n_elements, n_folds=nfolds)

    score = np.zeros(nfolds)

    for idx, (train, test) in enumerate(kf):

        print 'Running k-fold {0}'.format(idx+1)

        xtrain, ytrain = X[train], y[train]
        xtest, ytest = X[test], y[test]

        clf.fit(xtrain, ytrain)

        score[idx] = clf.score(xtest,ytest)

    for idx,sc in enumerate(score): print '{0}\t{1}'.format(idx+1, sc)
    print 'Mean score: {0}'.format(np.mean(score))






if __name__=='__main__':

    main()
