#!/usr/env/python

import numpy as np
from sklearn.naive_bayes import MultinomialNB
import argparse
from sklearn import cross_validation
import pdb
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
import matplotlib.pyplot as plt

from gensim import corpora, matutils



parser = argparse.ArgumentParser(description='K-fold Testing using Naive Bayes on a model')
parser.add_argument('-c', '--corpus', help = 'The corpus file in MM format. It will be translated into a sparse scipy matrix.', required = True, type = str)
parser.add_argument('-l', '--labels', help = 'A file containing a list of labels for each document in the corpus', required = True, type = str)
parser.add_argument('-k', '--kfold', help='Number of kfolds', default = 10, type=int)
parser.add_argument('-t', '--topics', help='Number of topics in model', required = True, type=int)

def main():

    args = parser.parse_args()

    y = np.genfromtxt(args.labels, unpack = True, dtype=None)

    corpus_file = args.corpus

    new_corpus = corpora.mmcorpus.MmCorpus(corpus_file)
    X = matutils.corpus2csc(new_corpus, new_corpus.num_terms, num_docs=new_corpus.num_docs)
        
    X = X.transpose()

    clf2 = MultinomialNB()
   # clf.fit(X,y)

    n_elements = len(y)
    nfolds = args.kfold

    classes = [x for x in range(args.topics)]

    #ybin = label_binarize(y, classes=classes)

    kf = cross_validation.KFold(n_elements, n_folds=nfolds)
    #kf = cross_validation.StratifiedKFold(y, n_folds=nfolds)

    score = np.zeros(nfolds)

    tpr_list = [{} for i in xrange(nfolds)]
    fpr_list = [{} for i in xrange(nfolds)]
    roc_list = [{} for i in xrange(nfolds)]

    classes = [x for x in xrange(args.topics)]

    for idx, (train, test) in enumerate(kf):

        print 'Running k-fold {0}'.format(idx+1)

        xtrain, ytrain = X[train], y[train]
        xtest, ytest = X[test], y[test]
        
        clf2.fit(xtrain, ytrain)
        score[idx] = clf2.score(xtest,ytest)
        y_score = clf2.predict(xtest)   #different for NB or SVC


    #fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    #roc_auc[i] = auc(fpr[i], tpr[i])

       
        for cls in classes:

            fpr_list[idx][cls], tpr_list[idx][cls], threshold = roc_curve(ytest[ytest==cls], y_score[ytest==cls], pos_label=cls)
            
            roc_list[idx][cls] = auc(fpr_list[idx][cls], tpr_list[idx][cls])
            

        #do micro averaging over all classes

        fpr_list[idx]["micro"], tpr_list[idx]["micro"], _ = roc_curve(ytest.ravel(), y_score.ravel())
        roc_list[idx]["micro"] = auc(fpr_list[idx]["micro"], tpr_list[idx]["micro"])


        #make ROC curve for each class in this fold

        # Plot ROC curve
        plt.figure(idx)
        plt.plot(fpr_list[idx]["micro"], tpr_list[idx]["micro"],
                 label='micro-average ROC curve (area = {0:0.2f})'
                       ''.format(roc_list[idx]["micro"]))
        for cls in classes:
            plt.plot(fpr_list[idx][cls], tpr_list[idx][cls], label='ROC curve of class {0} (area = {1:0.2f})'
                                           ''.format(cls, roc_list[idx][cls]))

        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve for k-fold {0}'.format(idx))
        plt.legend(loc="lower right")
        plt.show()



    #for idx,sc in enumerate(score): print '{0}\t{1}'.format(idx+1, sc)
    #print 'Mean score: {0}'.format(np.mean(score))






if __name__=='__main__':

    main()
