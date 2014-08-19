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

    dictionary=dic.customizeDic(10)



    print dictionary

if __name__ == '__main__':
    main()
