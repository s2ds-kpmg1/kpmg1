__author__ = 'elenagr'

from sklearn.cluster import KMeans, MiniBatchKMeans
import numpy as np
from gensim import corpora, models, matutils
from time import time
import struct
import argparse
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer

def npmatrixCorpus(corpusname,features):
    t0=time()
    # Read corpus from file
    new_corpus = corpora.mmcorpus.MmCorpus(corpusname)
    docs=len(new_corpus)
    # Convert corpus to numpy array
    X=matutils.corpus2dense(new_corpus,features,num_docs=docs)

    # Save array to file
    outfile=corpusname.split(".")[0]+'.npy'
    np.save(outfile, X)
    print "numpy array saved in {0} sec".format(time()-t0)
    return X


def binaryMatrix(inputfile):

    outputfile = inputfile.split(".")[0]+".bin"
    t0=time()
    # Load from the file
    mat = np.load(inputfile)

    # Create a binary file
    binfile = file(outputfile, 'wb')
    # and write out two integers with the row and column dimension
    header = struct.pack('2I', mat.shape[0], mat.shape[1])
    binfile.write(header)
    # then loop over columns and write each
    for i in range(mat.shape[1]):
        data = struct.pack('%id' % mat.shape[0], *mat[:,i])
        binfile.write(data)
    binfile.close()
    print "Binary file saved in {0} secs".format(time()-t0)


parser = argparse.ArgumentParser(description="Applying k-means clustering")
parser.add_argument("--file", help="Name of the file stored: numpy array"
                    ,required = True, type=str)
parser.add_argument('--Nclusters', help = 'Number of clusters',
                    default=3,required = False, type=int)
parser.add_argument("--minibatch", help="Use MiniBatchKMeans",default=False, action='store_true')

def main():

    args = parser.parse_args()
    filename=args.file
    Nclusters=args.Nclusters
    t0 = time()

    print "Loading dictionary..."
    dictname="new_dic_min1_stopwdsTrue_freq.txt"
    dictionary=corpora.Dictionary.load_from_text(dictname)
    print "Loading corpus..."
    npyfile=filename+'.npy'
    npy=np.load(npyfile)

    print("n_features: %d, n_samples: %d" % npy.shape)
    if args.minibatch:
        km = MiniBatchKMeans(init='k-means++', n_clusters=Nclusters,n_init=10, verbose=True)
    else:
        km = KMeans(n_clusters=Nclusters, init='k-means++', max_iter=100, n_init=1,verbose=True)



    t0 = time()
    print "Fitting the data..."
    km.fit(npy)
    inertia=km.inertia_

    print("done in %0.3fs" % (time() - t0))
    t0 = time()
    # labels = mbkm.labels_

    # print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, k_means.labels_))
    # print("Completeness: %0.3f" % metrics.completeness_score(labels, k_means.labels_))
    # print("V-measure: %0.3f" % metrics.v_measure_score(labels, k_means.labels_))
    # print("Adjusted Rand-Index: %.3f"
    #   % metrics.adjusted_rand_score(labels, k_means.labels_))
    # print("Silhouette Coefficient: %0.3f"
    #   % metrics.silhouette_score(npy, labels, sample_size=1000))

    print("Top terms per cluster:")
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    for i in range(Nclusters):
        print("Cluster %d:" % i)
        for ind in order_centroids[i, :10]:
            print(' %s' % dictionary[ind])
        print()

    print()


    # if True:
    #     print("Top terms per cluster:")
        # order_centroids = k_means.cluster_centers_.argsort()[:, ::-1]
        # terms=terms[0]
        # for i in range(Nclusters):
        #     print("Cluster %d: \n" % i)
        #     for ind in order_centroids[i, :10]:
        #         print(' %s \n' % terms[ind])
        #         print()

    # t_batch = time() - t0
    # k_means_labels = mbkm.labels_
    k_means_cluster_centers = km.cluster_centers_
    # k_means_labels_unique = np.unique(k_means_labels)

    # print k_means_labels
    # print k_means_cluster_centers
    # print k_means_labels_unique


if __name__ == '__main__':
    main()
