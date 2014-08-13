__author__ = 'elenagr'

import argparse
import math
import random
import MySQLdb as mdb
import nltk
from nltk import word_tokenize
import gensim
from gensim.parsing.preprocessing import STOPWORDS

parser = argparse.ArgumentParser(description="Generating a dictionary of stopwords")
parser.add_argument("--sample",help="Size of sample in percentage", dest="sample",required=True,type=float)

def main():
    args = parser.parse_args()
    N = args.sample

    # Open the connection to the DB
    connection = mdb.connect('localhost', 'kpmg1', 's2ds','enron')
    cur=connection.cursor()


    # In our case the IDs are ordered by entry. Otherwise you could do: cur.execute("SELECT COUNT(*) FROM emails;")
    # The last ID number gives us the number of rows of the table.
    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    size=[int(col) for row in res for col in row]
    print type(size[0])
    print type(N)

    # We generate a random sample of the entries.
    sample=random.sample(range(size[0]),int(math.floor(size[0]*N)))

    texts=[]

    for id in sample:
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp=cur.fetchall()
        texts.append(tmp[0][0])

    raw=" ".join(texts)

    tokens=[word for word in gensim.utils.tokenize(raw, lower=True)
                if word not in STOPWORDS and len(word) > 1]

    text = nltk.Text(tokens)
    coll=text.collocations()

    # Close all cursors
    connection.close()
    # Close all databases
    return


if __name__ == "__main__":
    main()

