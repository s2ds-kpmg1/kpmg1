#!/usr/env/python

"""We can use the getattr() function to test a whole range of functions/set-ups/combinations
in one place"""

import gensim
import nltk
from nltk.corpus import stopwords
import mdb
import enron

def main():

	stopwords = stopwords.words('english')
	
	
	
	# NB this is just rough code while I have the ideas. It's not tested or anything
	
	token_packages = [
						'nltk.tokenize.WordPunctTokenizer',
						'nltk.tokenize.PunktWordTokenizer', 
						'gensim.utils'
						]
	
	token_func = ['tokenize', 
					'tokenize', 
					'tokenize']
	
	
	stem_packages = ['nltk.stem.snowball.EnglishStemmer', 
						'nltk.stem.snowball.PorterStemmer', 
						'nltk.stem.lancaster.LancasterStemmer',
						'nltk.stem.WordNetLemmatizer', 
						'gensim.utils']
	
	stem_func = ['stem', 'stem', 'stem', 'lemmatize',
		'lemmatize']
	

	text = enron.querySample(0.001)

	text = text.lower()
	
	token_args = [(text),(text), (text)]
	token_kwargs = [{}, {}, {}]
	
	stem_kwargs = [{}, {}, {}, {}, {}]
	
	#loop over each version
	
	for (tpackage, tfunc, targ, tkwarg) in zip(token_packages,token_func, token_args, token_kwargs):
	
		for (spackage, sfunc, skwarg) in zip(stem_packages, stem_packages, stem_kwargs):
	
			output = 'testing_{0}.{1}_{2}.{3}.txt'.format(tpackage,tfunc, spackage,sfunc)
	
			outfile = open(output, 'w')
	
			tokenizerFunction = getattr(tpackage, tfunc)
			text_token = tokenizerFunction(*token_args, **token_kwargs)
	
			stemFunction = getattr(spackage, sfunc)
	
			if spackage == 'gensim.utils':
	
				text_stem  = stemFunction(*(text_token),**stem_kwargs))
	
			elif spackage == nltk.stem.WordNetLemmatizer
	
				wnl = WordNetLemmatizer
				stemFunction_new = wnl
				text_stem = [stemFunction_new(*(word),**stem_kwargs) for word in text_token]
	
			else:
	
				text_stem = [stemFunction(*(word), **stem_kwargs) for word in text_token]
	
	
			text_stem = [x for x in text_stem if x not in stopwords]
	
	
			output.write(text_stem)
	
			output.close()


if __main___ == main:
	main()


