__author__ = 'elenagr'

import os
import time
import MySQLdb as mdb
from gensim import corpora
import enron
import create_dic as dic
import argparse
import stemming as stem


def main():

    mm = corpora.mmcorpus.MmCorpus('corpus.mm')


    # dictionary.id2token("4300")


if __name__ == '__main__':
    main()
