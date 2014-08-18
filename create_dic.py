__author__ = 'elenagr'

import os
import re
import time
import MySQLdb as mdb
import specialwords as words
import scrubbing as scrub
from gensim import corpora
import nltk
import enron
from string import digits
import argparse
from collections import Counter

parser = argparse.ArgumentParser(description="Generating a dictionary of stopwords")
parser.add_argument('-N', '--Ndic', help = 'Number of texts considered for initial dictionary',
                    required = True, type=int)
parser.add_argument('-dic', '--initialize', help='initialize dictionary', default=False, action='store_true')
parser.add_argument('--append', help='append word mapping to existing file', default=False,
                    action='store_true')

def stemmingListofStrings(textsid):
    """
    This function takes a list of tuples (id,text) and returns the text after cleaning, tokenizer and stemming
    :param textsid: list of tuples with raw text (id,text)
    :return: returns the stemmed text as a list of tuples (id,stem_text)
    """

    texts = [text for id, text in textsid]
    ids = [id for id, text in textsid]

    # Initialize the stemmer snowball
    stem = nltk.stem.snowball.EnglishStemmer()

    #Initialize the stop words
    stop_words = enron.getCustomStopwords()

    # Clean the text eliminating symbols and numbers
    texts = [re.sub(r'[\w\.-]+@+[\w\.-]+]','', text)  for text in texts ]
    texts = [text.translate(None, digits) for text in texts]
    texts = [re.sub(r'(.)\1{2}', r'', text) for text in texts]
    texts = [re.sub('[\^~+=!-*@#$<>.,;:?|!\-\(\)/"\'\[\]]', '', text.replace('\\','')) for text in texts]
    texts = [re.sub(r"[0-9,a-z]*enroncom\b",'',text.lower())for text in texts]
    texts = [re.sub(r"[0-9,a-z]*houect\b",'',text.lower()) for text in texts]
    texts = [re.sub(r"[0-9,a-z]*ectect\b",'',text.lower()) for text in texts]
    texts = [re.sub(r"[0-9,a-z]*houeese\b",'',text.lower()) for text in texts]
    texts = [re.sub(r"[0-9,a-z]*hotmailcom\b",'',text.lower()) for text in texts]
    texts = [re.sub(r"[0-9,a-z]*enronenron[0-9,a-z]*",'',text) for text in texts]
    texts = [re.sub(r"http[0-9,a-z]*com",'',text) for text in texts]
    texts = [re.sub('requestrequest','request',text) for text in texts]
    texts = [re.sub(r"[0-9,a-z]*developmentenron_develop[0-9,a-z]*",'',text.lower()) for text in texts]
    texts = [re.sub(r"[0-9,a-z]*_communicationsenron_0-9,a-z]*",'',text.lower()) for text in texts]
    texts = [re.sub(r"[0-9,a-z]*html\b",'',text.lower()) for text in texts]

    textsid = zip(ids, texts)

    # Replace any found term in the dictionary by its abbreviation
    texts = [words.abbreviations(text.lower(), "dic_enron.csv", id) for id, text in textsid]

    textsid = zip(ids, texts)

    # Joins any ngrams found in the given files
    texts = [words.ngramsText(text.lower(), 3, "bigrams.txt", "trigrams.txt", id) for id, text in textsid]

    # Tokenize the texts and eliminates stopwords and all words with length < 2
    texts_token = [scrub.tokenizeString(text, lower=True, tokenizer="punktword") for text in texts]
    texts_token = [[x for x in text_token if x not in stop_words and len(x) > 1] for text_token in texts_token]

    # Apply stemming
    texts_stem = [[stem.stem(word) for word in text_token] for text_token in texts_token]

    textsid = zip(ids, texts_stem)

    return textsid


def stemmingString(text, id):
    """
    This function takes a text and an id and returns the text after cleaning, tokenizer and stemming
    :param text: raw text
    :param id: id of the text
    :return: returns the stemmed text
    """

    # Initialize the stemmer snowball
    stem = nltk.stem.snowball.EnglishStemmer()

    #Initialize the stop words
    stop_words = enron.getCustomStopwords()

    # Clean the text eliminating symbols and numbers
    text = text.translate(None, digits)
    # Remove all characters repeated more than twice in a row
    text = re.sub(r'(.)\1{2}', r'', text)
    text = re.sub('[\^~+=!-*@#$<>.,;:?!|\-\(\)/"\'\[\]]', '', text.replace('\\',''))
    text = re.sub(r"[0-9,a-z]*enroncom\b",'',text.lower())
    text = re.sub(r"[0-9,a-z]*houect\b",'',text.lower())
    text = re.sub(r"[0-9,a-z]*ectect\b",'',text.lower())
    text = re.sub(r"[0-9,a-z]*hotmailcom\b",'',text.lower())
    text = re.sub(r"[0-9,a-z]*html\b",'',text.lower())
    text = re.sub(r"[0-9,a-z]*enronenron[0-9,a-z]*",'',text.lower())
    text = re.sub(r"http[0-9,a-z]*com",'',text.lower())
    text = re.sub(r"[0-9,a-z]*com",'',text.lower())
    text = re.sub('requestrequest','request',text.lower())
    text = re.sub(r"[0-9,a-z]*houeese\b",'',text.lower())
    text = re.sub(r"[0-9,a-z]*developmentenron_develop[0-9,a-z]*",'',text.lower())
    text = re.sub(r"[0-9,a-z]*_communicationsenron_0-9,a-z]*",'',text.lower())

    # Replace any found term in the dictionary by its abbreviation
    text = words.abbreviations(text.lower(), "dic_enron.csv", id)

    # Joins any ngrams found in the given files
    text = words.ngramsText(text.lower(), 3, "bigrams.txt", "trigrams.txt", id)

    # Tokenize the texts and eliminates stopwords and all words with length < 2
    text_token = scrub.tokenizeString(text, lower=True, tokenizer="punktword")
    text_token = [x for x in text_token if x not in stop_words and len(x) > 1]

    # Apply stemming
    text_stem = [stem.stem(word) for word in text_token]

    return text_stem


def initializeDic(N):
    """
    This function initialize the dictionary in case there is no any previously saved in disk
    :param N: number of emails to build it (recommended 3)
    :return: returns the dictionary
    """

    print "Initializing dictionary with the first {0} emails \n".format(N)

    # Open the connection to the DB
    connection = mdb.connect('localhost', 'kpmg1', 's2ds', 'enron')
    cur = connection.cursor()

    texts = []
    ids = []

    # Query emails for given ids
    for id in range(1, N):
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp = cur.fetchall()
        texts.append(tmp[0][0])
        ids.append(id)

    texts_id = zip(ids, texts)

    # Apply stemming to the given text
    texts_stem = stemmingListofStrings(texts_id)
    texts_stem = [text for id, text in texts_stem]

    # Builds a dictionary based on the words found in the given texts
    dictionary = corpora.Dictionary(texts_stem)

    return dictionary


def main():
    """
    This function generates a dictionary (map id<-> word) based on the texts saved in the enron database
    In the file dictionary_freq.txt one can see the word id, the word and the number of emails where that
    particular word appear
    There are two dictionary, one in alphabetic order (dictionary_word.txt) and another one ordered by frequency
    (dictionary_freq.txt)
    It also produces a file map_words.txt with the email id and all the words that appear in each of them.
    A complementary file map_freqs.txt contains the frequency for each of the words of the previous file.

    :return:
    """
    # Read arguments:
    args = parser.parse_args()
    N=args.Ndic

    start_code = time.time()

    # Remove files which will be generated within this function to avoid appending to an existing file unless
    # there is an argument which explicitly requires append to existing file
    if (args.append == False):
        if os.path.exists("word_replace_dic.txt"):
            os.remove("word_replace_dic.txt")
        if os.path.exists("ngrams_found.txt"):
            os.remove("ngrams_found.txt")
        if os.path.exists("map_freqs.txt"):
            os.remove("map_freqs.txt")
        if os.path.exists("map_words.txt"):
            os.remove("map_words.txt")

    # Open the connection to the DB
    connection = mdb.connect('localhost', 'kpmg1', 's2ds', 'enron')
    cur = connection.cursor()

    # In our case the IDs are ordered by entry. Otherwise you could do:
    # cur.execute("SELECT COUNT(*) FROM emails;")
    # The last ID number gives us the number of rows of the table.
    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    size = [int(col) for row in res for col in row]

    # Initialize the dictionary or reads it from file

    if (args.initialize == True):
        dictionary = initializeDic(N)
    else:
        dictionary = corpora.Dictionary.load_from_text("dictionary_words.txt")

    outfrqs = open('map_freqs.txt', 'a+')
    outids = open('map_words.txt', 'a+')

    # Here we go: construct the dictionary and the word-frequency mapping for each email
    for id in range(1, size[0]):
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp = cur.fetchall()
        text_stem = stemmingString(tmp[0][0], id)
        # We don't want to count twice the emails already consider in the dictionary. We set the
        # update to false for the emails used to build the dictionary
        if id <= N:
            mytext = dictionary.doc2bow(text_stem, allow_update=False)
        #For the rest we update our dictionary with each new emails
        else:
            mytext = dictionary.doc2bow(text_stem, allow_update=True)

        # Save to file the words and their frequency for each new text
        outids.writelines("{0}; {1}\n".format(id, [idw for idw, frq in mytext]))
        outfrqs.writelines("{0}; {1}\n".format(id, [frq for idw, frq in mytext]))

        # Save dictionary once in a while to make sure we don't loose everything if some error ocurrs
        if id % 100 == 0 or id == (size[0]-1):
            dictionary.save_as_text("dictionary_words.txt", sort_by_word=True)
            dictionary.save_as_text("dictionary_freq.txt", sort_by_word=False)
            print 'Dictionary saved until id = {0}'.format(id)

    end_code = time.time()

    codetime = end_code - start_code

    print 'Total time to create dictionary: {0} sec'.format(codetime)


if __name__ == '__main__':
    main()
