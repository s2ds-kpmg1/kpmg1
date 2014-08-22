#/usr/env/python

"""Code to perform the TF-IDF reweighting of the corpus"""

from gensim import corpora, models
import time
import argparse

parser = argparse.ArgumentParser(description="Generating a corpus")
parser.add_argument("--file", help="Name of the corpus in mm format",
                    default="corpus.mm",required = False, type=str)
def main():

    args = parser.parse_args()
    corpusname=args.file

    start_time = time.time()

    # Load the raw count (TF) corpus
    corpus = corpora.MmCorpus(corpusname)

    # Define a model (which is the gensim name for a transformation) based on this corpus which performs the TFIDF transformation/calculation
    tfidf = models.TfidfModel(corpus)

    # Apply it to the input corpus
    new_corpus = tfidf[corpus]

    outname=corpusname.split(".")[0]+'_tfidf.'+corpusname.split(".")[1]
    # Save the new corpus
    corpora.mmcorpus.MmCorpus.serialize(outname, new_corpus)

    # This command displays the corpus. Or run a print loop over the elements of the corpus. For debugging purposes.
    #print(list(new_corpus))

    end_time=time.time()
    time_taken = end_time - start_time

    print 'Time taken to perform TF-IDF reweighting: {0}'.format(time_taken)


if __name__ == '__main__':
    main()
