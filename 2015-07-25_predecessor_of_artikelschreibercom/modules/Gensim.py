# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore

import uuid
import string
import numpy as np
import gensim
import nltk
import os, sys, logging, re
from gensim import corpora, models, similarities
from gensim.models import word2vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import word2vec
from gensim.models import doc2vec
from gensim.models.ldamulticore import LdaMulticore
#import spacy# pip3 install --upgrade spacy
#from spacy.en import English
#from spacy.de import German
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem.snowball import SnowballStemmer

import modules.Wordify as wordify
import modules.TextGenify as genify
import modules.Speechify as speechify
import modules.Sentify as sentify
#import modules.Servify as servify
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

# kommt später in config datei rein
minSpeechIndexValue		= float(0.85)	# ab 0.84 kommt gutes Textmaterial ## 0.853


# https://github.com/cemoody/lda2vec

# TESTEN: https://nbviewer.jupyter.org/github/rare-technologies/gensim/blob/develop/docs/notebooks/atmodel_tutorial.ipynb

#pip3 install stop-words
from stop_words import get_stop_words
stopwordsDE = get_stop_words('de')

# load nltk's English stopwords as variable called 'stopwords'
stopwords 	= nltk.corpus.stopwords.words('german')
# load nltk's SnowballStemmer as variabled 'stemmer'
stemmer 	= SnowballStemmer("german")

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Load the punkt tokenizer
tokenizer 			= nltk.data.load('tokenizers/punkt/german.pickle')
# https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-2-word-vectors

nlp_allowed 		= [u"NN",u"NNP",u"NNPS",u"PROPN",u"NOUN",u"NE", u"NNE"]
#ruby_script	= "/home/buz/buzzgreator/modules/sentence_tokenizer.rb"

debug				= False
max_gensim_results 	= 25

def topicModeling(text):
	import modules.Sentify as sentify
	import modules.Speechify as speechify
	#print(type(text))
	#print(len(text))
	
	if len(text) < 150:
		return float(0.0)
	
	words	= []
	texts 	= []
	#text1 	= wordify.encodeToUTF8Adv(text) #wordify.encodeToLatin1(text)
	#print(len(text1))
	#text2 	= speechify.sentSegmenter(text1, asString=False, posTags=False)
	text2 	= speechify.sentSegmenterSimple(text, asString=False)
	#textDoc2Bow="\n".join(text2)
	#print(text2)
	#print(type(text2))
	#exit
	#print(type(text2))
	#print(len(text2))
	
	# list for tokenized documents in loop
	#words 		= [w for w in text2 if not w in stopwords or not w in stopwordsDE]
	for w in text2:
		a=w.split()
		for t in a:
			if t.lower() in stopwords:
				continue
			if t.lower() in stopwordsDE:
				continue
			if t in stopwords:
				continue
			if t in stopwordsDE:
				continue
			if len(t)<3:
				continue
			if not t.isalnum():
				continue
			#if not sentify.isNotBlacklisted(t):
			#	continue
			
			tv1=wordify.encodeToUTF8(t)
			words.append(tv1)
	
	#words = list(words)
	#print(words)
	#exit(1)
	"""
	for a in words:
		print(wordify.encodeToLatin1(a))
	
	exit(1)
	exit(1)
	"""
	
	# stem tokens
	#stemmed_tokens = [stemmer.stem(i.lower()) for i in words]
	#stemmed_tokens = [stemmer.stem(i) for i in words]
	# add tokens to list
	#for a in stemmed_tokens:
	#	print(a)
	#	#texts.append(a.split(" "))
	#	texts.append(a)
	
	# Number of trainings epochs
	num_epochs = 1
	# Number of topics to show
	num_topics_my=55
	# Number of threads to run in parallel
	num_workers=18
	# Context window size
	minimum_probability_my=0.65#0.55
	
	#for a in words:
	#	ua = wordify.encodeToUTF8(a)
	#	texts.append(ua.split())
	# texts -> encodeToUTF8
	
	texts=words
	# turn our tokenized documents into a id <-> term dictionary
	dictionary	= corpora.Dictionary([words])
	
	#convert the dictionary to a bag of words corpus for reference
	corpus 		= [dictionary.doc2bow(t) for t in [words]]
	
	if debug:
		print("gensim.topicModeling(): Start MultiCore Topic Modelling")
	ldamodel 	= gensim.models.ldamulticore.LdaMulticore(corpus, num_topics=num_topics_my, id2word=dictionary, chunksize=30000, passes=num_epochs, workers=num_workers)
	b 			= ldamodel.get_document_topics(corpus, minimum_probability=minimum_probability_my, per_word_topics=False)
	
	count 		= 0
	c 			= set()
	for ele in b:
		for e in ele:
			c.add(e)
	
	resultSet 	= set()
	resultList 	= []
	d 			= sorted(c, reverse=True, key=lambda x: x[1])
	
	if debug:
		print("gensim.topicModeling(): Parsing Results of Topic Modelling")
	for e in d:
		document_id = e[0]
		f 			= ldamodel.show_topic(document_id, topn=15)
		#print(f)
		for f_e in f:
			word 	= wordify.encodeToUTF8Adv(f_e[0])
			#print(wordify.encodeToLatin1(word))
			#calc 		= f_e[1]
			#print(wordify.encodeToLatin1(word_pos))
			#t			= word_pos.split("::")
			#word 		= t[0]
			#pos_tag 	= t[1]
			
			if len(resultList) >= max_gensim_results:
				#print("gensim.topicModeling():", resultList)
				return resultList
			
			if word not in resultSet:
				resultList.append(word)
				resultSet.add(word)
	if debug:
		print("gensim.topicModeling():", resultList)
	return resultList

#def gensimWord2Vec(documents, word, nounOnly):
def gensimWord2Vec(documents, word):
	if len(documents) < 65:
		return []
	
	#print(documents)
	#exit(1)
	"""
	#documents 		= documents.encode('utf-8', "ignore")
	#documents 		= str(documents.decode('latin-1', "ignore"))
	pid 		= os.getpid()
	pid 		= str(pid)
	storePath 	= "/tmp/buzzgreator.word2vec."+pid+".bin"
	#sentences 	= review_to_sentences(documents, tokenizer)
	###sentences 	= create_wordlist(documents)
	"""
	#t_sent 		= speechify.sentSegmenter(documents, asString=False, posTags=False)
	t_sent 		= speechify.sentSegmenterSimple(documents, asString=False)
	sentences 	= []
	stops 		= set(stopwords)
	
	for w in t_sent:
		a=w.split()
		s=[]
		for t in a:
			if t.lower() in stopwords:
				continue
			if t.lower() in stopwordsDE:
				continue
			if t in stopwords:
				continue
			if t in stopwordsDE:
				continue
			if len(t)<3:
				continue
			if not t.isalnum():
				continue
			#if not sentify.isNotBlacklisted(t):
			#	continue
			s.append(t)
		if len(s) > 0:
			words = [w for w in s if not w in stops]
			sentences.append(words)
	
	
	#print("Gensim:", sentences)
	#exit(1)
	
	"""
	for s in t_sent:
		l = s.split()
		words = [w for w in l if not w in stops]
		sentences.append(words)
	"""
	
	"""
	if word in documents:
		print("Found")
		return True
	"""
	# https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/models/word2vec.py#L389
	# Number of trainings epochs
	num_epochs = 1
	# Word vector dimensionality
	num_features=800
	# Minimum word count - min_count = ignore all words with total frequency lower than this.
	min_word_count=1
	# Number of threads to run in parallel
	num_workers=9
	# Context window size
	context=1#5
	# Downsample setting for frequent words
	downsampling=1e-3
    # Initialize and train the model (this will take some time)
	
	if debug:
		print("Training Word2Vec model...")
	
	#model = gensim.models.Word2Vec(sentences, workers=num_workers, size=num_features, min_count= min_word_count, window=context, sample=downsampling, iter=num_epochs, sg=1)
	
	model = gensim.models.Word2Vec(workers=num_workers, size=num_features, min_count=min_word_count, window=context, iter=num_epochs, alpha=0.005)
	model.sort_vocab()
	model.build_vocab(sentences)
	
	try:
		for epoch in range(num_epochs):
			model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
			model.alpha -= 0.0002  # decrease the learning rate
			
		#model.sort_vocab()
		#model.build_vocab(sentences)
		model.init_sims(replace=True)# can only read from, but no more training -> less memory
		#model.save(storePath)
	except Exception as strerror:
			#print("Unexpected error:", sys.exc_info()[0])
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			tel = {'hit':0,'content':""}
			resultList.append(tel)
			return resultList
	
	if debug:
		print("gensimWord2Vec(documents, word): ", len(documents))
		print("gensimWord2Vec(sentences): ", len(sentences))
		print("gensimWord2Vec(Vocabulary Length): ", len(model.wv.vocab))
		print("gensimWord2Vec(word): ", word)
	
	resultSet	 = set()
	resultList	 = []
	
	try: 
		#new_doc_vec = model.infer_vector(word)
		# funzt nicht: sims = model.most_similar(positive=[new_doc_vec], topn=30
		sims = model.most_similar(positive=word.split(),topn=5000)
		#sims = model.most_similar(positive=word,topn=5000)
		for i, val in enumerate(sims):
			if len(resultList) >= max_gensim_results:
				return resultList
			
			simWord = sims[i][0]
			simValue = sims[i][1]
			#if sims[i][0] not in resultSet and sims[i][0].isalpha() and sentify.isGoodCasing(sims[i][0]):
			if simWord not in resultSet:
				print("Gensim.Word2Vec():", simWord)
				tel = {'hit':simValue,'content':simWord}
				resultList.append(tel)
				resultSet.add(simWord)
				"""
				toks1 	= speechify.doSpeechify(simWord)
				#if nounOnly == 1:
				for word in toks1:
					#print(word.text,word.pos_)
					if (word.pos_ in nlp_allowed):
					#if sentify.isSentenceStructureAdvanced(simWord) and sentify.isNotBlacklisted(simWord) and sentify.isLongEnoughSentence(simWord, dynamic=True) and sentify.isNotDublicateString(simWord) and sentify.sentify.isGoodCasing(simWord) and word.pos_ in nlp_allowed:
						#print("Word2Vec Score ->",simValue,"|| Wort ->",simWord,"|| POS ->",word.pos_);
						resultSet.add(simWord)
						#resultList.append([simValue,simWord])
						tel = {'hit':simValue,'content':simWord}
						resultList.append(tel)
						#resultList.append([sims[i][1],sims[i][0]+"::NOUN"])
					#else:
					#	resultSet.add(sims[i][0])
					#	#resultList.append([sims[i][1],sims[i][0]])
					#	resultList.append([sims[i][1],sims[i][0]+"::OTHER"])
				"""
		#resultList = sorted(resultList, reverse=True, key=lambda x: x[0])
		return resultList
	except KeyError:
		tel = {'hit':0,'content':""}
		resultList.append(tel)
		return resultList

def flattenDoc2VecList(doc2VecList):
	p=[]
	for a in doc2VecList:
		simValue	= float(a[0])
		sentSample 	= str(a[1])
		p.append(sentSample)
	return p

def doc2VecPlainList(resultList, simValueOption):
	s=set()
	l=list()
	for e in resultList:
		#print("lenght e:", len(e))
		#print("simValueOption:", simValueOption)
		markov_sample 	= str(e[1])
		simValue	 	= float(e[simValueOption])
		#print("doc2VecPlainList() - markov_sample:", markov_sample)
		#print("simValue:", simValue)
		if markov_sample not in s and simValue >= minSpeechIndexValue:
			#print("doc2VecPlainList() - markov_sample (GOOD):", simValue, " -> ",markov_sample)
			#markov_sample=wordify.encodeToLatin1(markov_sample)
			l.append(markov_sample)
		s.add(markov_sample)
	
	"""
	if len(l)==0:
		s=set()
		for e in resultList:
			markov_sample 	= str(e[1])
			simValue	 	= float(e[simValueOption])
			print("simValue:", simValue)
			if markov_sample not in s:
				l.append(markov_sample)
			s.add(markov_sample)
	"""
	return l

def gensimDoc2Vec(documents, word, advanced=False):	
	import modules.TextGenify as genify
	
	if len(documents) < 65:
		return []
	"""
	#documents 		= documents.encode('utf-8', "ignore")
	#documents 		= str(documents.decode('latin-1', "ignore"))
	pid 			= os.getpid()
	pid 			= str(pid)
	storePath 		= "/tmp/buzzgreator.doc2vec."+pid+".bin"
	"""
	
	lSent 			= []
	lGoodSentences 	= dict()
	#sentences 		= review_to_sentences(documents, tokenizer)
	sentences 		= sentence_tokenizer(documents)
	raw_sentences 	= sentences
	#raw_sentences 	= nltk.sent_tokenize(documents.strip())
	#raw_sentences 	= tokenizer.tokenize(documents.strip())
	#raw_sentences1 	= tokenizer.tokenize(documents.strip())
	
	count 			= 0
	for a1 in sentences:
		x 			= uuid.uuid4() # https://pymotw.com/2/uuid/
		t_string 	= str(x)
		labelSent 	= gensim.models.doc2vec.LabeledSentence(a1, [t_string])
		lSent.append(labelSent)
		#lSentDebug.append([count,a1,t_string])
		#original lGoodSentences.update({t_string:raw_sentences[count]})
		#lGoodSentences.update({t_string:raw_sentences[count]+count+a1})
		lGoodSentences.update({t_string:raw_sentences[count]})
		count 		= count + 1
	
	sentences_gSim = lSent
	
	# Number of trainings epochs
	num_epochs = 1
	# Word vector dimensionality
	num_features=400
	# Minimum word count
	min_word_count=1
	# Number of threads to run in parallel
	num_workers=9
	# Context window size
	context=5
	# Downsample setting for frequent words
	downsampling=1e-3
    # Initialize and train the model (this will take some time)
	
	if debug:
		print("Training Doc2Vec model...")
	
	model = gensim.models.Doc2Vec(workers=num_workers, size=num_features, min_count=min_word_count, window=context, sample=downsampling, dm=1, dbow_words=1, alpha=0.005, iter=num_epochs)
	
	model.sort_vocab()
	model.build_vocab(sentences_gSim)
	
	try:
		for epoch in range(num_epochs):
			model.train(sentences_gSim, epochs=model.iter, total_examples=model.corpus_count)
			model.alpha -= 0.0002  # decrease the learning rate
		
		model.init_sims(replace=True)# can only read from, but no more training -> less memory
	except Exception as strerror:
			#print("Unexpected error:", sys.exc_info()[0])
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			tel = {'hit':0,'content':""}
			resultList.append(tel)
			return resultList
			
	#model.save(storePath)
	
	"""
	model.sort_vocab()
	model.build_vocab(sentences_gSim)
	model.init_sims(replace=True)# can only read from, but no more training -> less memory
	model.save(storePath)
	"""
	if debug:
		print("gensimDoc2Vec(documents, word): ", len(documents))
		print("gensimDoc2Vec(sentences): ", len(sentences))
		print("gensimDoc2Vec(Vocabulary Length): ", len(model.wv.vocab))
		print("gensimDoc2Vec(word): ", word)
	
	resultSet 		= set()
	resultList	 	= []
	
	try:
		#funzt: sims = model.similar_by_word(word,topn=20)
		new_doc_vec = model.infer_vector(word)
		sims = model.docvecs.most_similar(positive=[new_doc_vec], topn=5000)
		
		###new_doc_vec = model.infer_vector(word)
		###sims = model.docvecs.most_similar(positive=[word], topn=25)
		for i, val in enumerate(sims):
			if len(resultList) >= max_gensim_results:
				return resultList
			
			simWord = sims[i][0]
			simValue = sims[i][1]
			t_sentence = str(lGoodSentences[simWord])
			
			if advanced is True and not genify.matchMainKeyword(t_sentence, word):
				continue
			
			if t_sentence and t_sentence not in resultSet and sentify.isGoodSentence(t_sentence):
				#print("Doc2Vec Score ->",sims[i][1],"|| Hash ID ->",sims[i][0], "|| Satz ->", t_sentence);
				#resultSet.add(t_sentenceSave)
				#t_sentenceSave = speechify.splitOnLowerUppercase(t_sentence)
				#if (sentify.isGoodSentenceStart(t_sentence) and sentify.isSentenceStructureAdvanced(t_sentence) and sentify.isNotBlacklisted(t_sentence) and sentify.isLongEnoughSentence(t_sentence, dynamic=True) and sentify.isNotDublicateString(t_sentence) and sentify.isGoodCasing(t_sentence) and sentify.isGoodSpecialCharsSimple(t_sentence, 3) ) or sentify.isGoodSentence(t_sentence):
				#if sentify.isGoodSentence(t_sentence):
				tel = {'hit':simValue,'content':t_sentence}
				resultList.append(tel)
				resultSet.add(t_sentence)
		#resultList = sorted(resultList, reverse=True, key=lambda x: x[0])
		return resultList
	except KeyError:
		1
	tel = {'hit':0,'content':""}
	resultList.append(tel)
	return resultList

def CalcBleuScore(corpus, markov):
	#BLEUscore = nltk.translate.bleu_score.sentence_bleu([corpus], markov)
	BLEUscore = nltk.translate.bleu_score.sentence_bleu([markov], corpus)
	return BLEUscore

def sentence_tokenizer(review):
	#print("sent_preview:", review)
	t_string = speechify.sentSegmenter(review, asString=True, posTags=False)
	#print("sent_tokenize:", t_string)
	return t_string.split("\n")

# Define a function to split a review into parsed sentences
def review_to_sentences( review, tokenizer, remove_stopwords=False ):
    # Function to split a review into parsed sentences. Returns a 
    # list of sentences, where each sentence is a list of words
    #
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    # raw_sentences = tokenizer.tokenize(review.strip())
    # raw_sentences = nltk.sent_tokenize(review.strip())
    raw_sentences = sentence_tokenizer(review.strip())
	# 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call review_to_wordlist to get a list of words
            sentences.append( create_wordlist( raw_sentence, remove_stopwords ))
    #
    # Return the list of sentences (each sentence is a list of words,
    # so this returns a list of lists
    return sentences

def create_wordlist(review, remove_stopwords=True):
    #review = review.encode('utf-8', "ignore")
    #review = review.encode('latin-1', "ignore")

    # Function to convert a document to a sequence of words,
    # optionally removing stop words.  Returns a list of words.
    #
    # 1. Remove HTML
    # review_text = BeautifulSoup(review, "lxml").get_text()
    #  
    # 2. Remove non-letters
    # review_text = re.sub("[^a-zA-Z0-9]"," ", review)
    #
    # 3. Convert words to lower case and split them
    words = review.lower().split()
    #words = review_text.lower().split()
    #words = review.split() # Spacy.IO needs case sensetive data
    ######23.1.2017 words = nltk.word_tokenize(review)
    #
    # 4. Optionally remove stop words (false by default)
    if remove_stopwords:
        stops = set(stopwords)
        words = [w for w in words if not w in stops]
    #
    # 5. Return a list of words
    return(words)
	
def topicModelingv1(text):
	import modules.Sentify as sentify
	
	if len(text) < 65:
		return []
	
	texts 		= []
	text1 		= wordify.encodeToUTF8Adv(text) #wordify.encodeToLatin1(text)
	#print(len(text1))
	text2 		= speechify.sentSegmenter(text1, asString=False, posTags=True)
	textDoc2Bow="\n".join(text2)
	#print(text2)
	#print(type(text2))
	#exit
	
	# list for tokenized documents in loop
	words 		= [w for w in text2 if not w in stopwords or not w in stopwordsDE]
	
	# stem tokens
	#stemmed_tokens = [stemmer.stem(i.lower()) for i in words]
	#stemmed_tokens = [stemmer.stem(i) for i in words]
	# add tokens to list
	#for a in stemmed_tokens:
	#	print(a)
	#	#texts.append(a.split(" "))
	#	texts.append(a)
	
	# Number of trainings epochs
	num_epochs = 1
	# Number of topics to show
	num_topics_my=35
	# Number of threads to run in parallel
	num_workers=9
	# Context window size
	minimum_probability_my=0.45
	
	for a in words:
		ua = wordify.encodeToUTF8(a)
		texts.append(ua.split())
	# texts -> encodeToUTF8
	
	# turn our tokenized documents into a id <-> term dictionary
	dictionary	= corpora.Dictionary([textDoc2Bow.split()] )
	
	#convert the dictionary to a bag of words corpus for reference
	corpus 		= [dictionary.doc2bow(t) for t in texts]
	
	if debug:
		print("gensim.topicModeling(): Start MultiCore Topic Modelling")
	ldamodel 	= gensim.models.ldamulticore.LdaMulticore(corpus, num_topics=num_topics_my, id2word=dictionary, chunksize=30000, passes=num_epochs, workers=num_workers)
	b 			= ldamodel.get_document_topics(corpus, minimum_probability=minimum_probability_my, per_word_topics=False)
	
	count 		= 0
	c 			= set()
	for ele in b:
		for e in ele:
			c.add(e)
	
	resultSet 	= set()
	resultList 	= []
	d 			= sorted(c, reverse=True, key=lambda x: x[1])
	
	if debug:
		print("gensim.topicModeling(): Parsing Results of Topic Modelling")
	for e in d:
		
		document_id = e[0]
		f 			= ldamodel.show_topic(document_id, topn=5)
		#print(f)
		for f_e in f:
			word_pos 	= f_e[0]
			calc 		= f_e[1]
			print(wordify.encodeToLatin1(word_pos))
			t			= word_pos.split("::")
			word 		= t[0]
			pos_tag 	= t[1]
			
			if len(resultList) >= max_gensim_results:
				return resultList
			
			if pos_tag.upper() in nlp_allowed and word not in resultSet:
				resultList.append(word)
				resultSet.add(word)
	
	return resultList