__author__ = 'elenagr'

import os
import re
import math
import time
import MySQLdb as mdb
import specialwords as words
import scrubbing as scrub
from gensim import corpora
import stemming_tmp as stemming
import gensim
import nltk
import enron
from string import digits

def stemmingListofStrings(texts):

#    texts=[text for text,id in textsid]
#    ids=[id for text,id in textsid]

    stem=nltk.stem.snowball.EnglishStemmer()

    stop_words = enron.getCustomStopwords()
 #   textsid=[re.sub('[!@#$<>.,;:?!-\(\)/"\'\[\]]', '', text) for text in [text for text,id in textsid]]
    texts=[re.sub('[!@#$<>.,;:?!-\(\)/"\'\[\]]', '', text) for text in texts]
    texts=[text.translate(None, digits) for text in texts]

    if os.path.exists("word_replace_dic.txt"):
        os.remove("word_replace_dic.txt")

    texts=[words.abbreviations(text.lower(),"dic_enron.csv",id) for text in texts]

    if os.path.exists("ngrams_found.txt"):
         os.remove("ngrams_found.txt")


    texts=[words.ngramsText(text.lower(),3,"bigrams.txt","trigrams.txt",id) for text in texts]
    texts_token=[scrub.tokenizeString(text,lower=True,tokenizer="punktword") for text in texts]
    texts_token=[[x for x in text_token if x not in stop_words and len(x) > 1] for text_token in texts_token]

    texts_stem=[[stem.stem(word) for word in text_token] for text_token in texts_token]

    return texts_stem

def stemmingString(text,id):
    stem=nltk.stem.snowball.EnglishStemmer()

    stop_words = enron.getCustomStopwords()
    text=re.sub('[!-@#$<>.,;:?!-\(\)/"\'\[\]]', '', text)
    text=text.translate(None, digits)

    if os.path.exists("word_replace_dic.txt"):
        os.remove("word_replace_dic.txt")

    text=words.abbreviations(text.lower(),"dic_enron.csv",id)

    if os.path.exists("ngrams_found.txt"):
         os.remove("ngrams_found.txt")

    text=words.ngramsText(text.lower(),3,"bigrams.txt","trigrams.txt",id)
    text_token=scrub.tokenizeString(text,lower=True,tokenizer="punktword")
    text_token=[x for x in text_token if x not in stop_words and len(x) > 1]

    text_stem=[stem.stem(word) for word in text_token]

    return text_stem

def main():

    start_code = time.time()


    # Open the connection to the DB
    connection = mdb.connect('localhost', 'kpmg1', 's2ds','enron')
    cur=connection.cursor()

    # In our case the IDs are ordered by entry. Otherwise you could do:
    #  cur.execute("SELECT COUNT(*) FROM emails;")
    # The last ID number gives us the number of rows of the table.
    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    size=[int(col) for row in res for col in row]

    texts=[]
    ids=[]

    # We query the emails in the sample and store them in a list
    for id in range(1,3):
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp=cur.fetchall()
        print tmp[0][0]
        texts.append(tmp[0][0])
        ids.append(id)

    texts_id=zip(texts, ids)


    texts_stem=stemmingListofStrings(texts)

    print texts_stem

    dictionary=corpora.Dictionary(texts_stem)
    #
    for id in range(11,int(math.floor(size[0]*0.01))):
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp=cur.fetchall()
        print tmp[0][0]
        text_stem=stemmingString(tmp[0][0],id)
        mytext = dictionary.doc2bow(text_stem,allow_update=True)
        print mytext

    print dictionary
    dictionary.save_as_text("dictionary_words", sort_by_word=True)
    dictionary.save_as_text("dictionary_freq", sort_by_word=False)

    end_code = time.time()
    #
    codetime = end_code - start_code

    print 'Total time to create dictionary: {0} sec'.format(codetime)


if __name__ == '__main__':
    main()
