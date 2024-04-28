# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore
import numpy as np
import string
import math
#in Scikit-Learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_kernels

import modules.Speechify as speechify


tokenize = lambda doc: doc.lower().split(" ")

def sklearnCosineSimilaritySimple(corpus, vec, sentence):
	if not isinstance(corpus, list):
		return float(0)
	if len(corpus)<1:
		return float(0)
	
	#corpus=speechify.sentSegmenter(text, asString=False, posTags=False)
	#candidate_list = ['orange', 'banana', 'apple1', 'pineapple']
	#target = 'apple'
	###vec = CountVectorizer(analyzer='char')
	###vec.fit(corpus)
	cosineValue = pairwise_kernels(vec.transform([sentence]), vec.transform(corpus), metric='cosine')
	cosineValue = cosineValue.astype(type('float', (float,), {}))
	#cosineValue = np.asarray(cosineValue, dtype=np.float)
	#print(cosineValue[0])
	
	cosCount 		= float(0)
	corpusListCount = len(corpus)
	if corpusListCount == 0:
		return float(0.0)
	
	for v in cosineValue:
		for vv in v:
			#print(type(vv))
			#print(vv)
			cosCount = cosCount + vv
	
	return float(format(cosCount/corpusListCount, '.7f'))

def sklearnCosineSimilarity(text, sentence):
	if not isinstance(text, str):
		return float(0)
	if len(text)<200:
		return float(0)
	
	corpus=speechify.sentSegmenter(text, asString=False, posTags=False)
	#candidate_list = ['orange', 'banana', 'apple1', 'pineapple']
	#target = 'apple'
	vec = CountVectorizer(analyzer='char')
	vec.fit(corpus)
	cosineValue = pairwise_kernels(vec.transform([sentence]), vec.transform(corpus), metric='cosine')
	cosineValue = cosineValue.astype(type('float', (float,), {}))
	#cosineValue = np.asarray(cosineValue, dtype=np.float)
	#print(cosineValue[0])
	
	cosCount 		= float(0)
	corpusListCount = len(corpus)
	if corpusListCount == 0:
		return float(0.0)
	
	for v in cosineValue:
		for vv in v:
			#print(type(vv))
			#print(vv)
			cosCount = cosCount + vv
	
	return float(format(cosCount/corpusListCount, '.7f'))

def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)

def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)

def sublinear_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log(count)

def augmented_term_frequency(term, tokenized_document):
    max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
    return (0.5 + ((0.5 * term_frequency(term, tokenized_document))/max_count))

def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude
	
def calcCosineSimilarity(doc1, doc2):
	all_documents = [doc1, doc2]
	
	sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize)
	sklearn_representation = sklearn_tfidf.fit_transform(all_documents)
	#tfidf_representation = tfidf(all_documents)
	
	skl_tfidf_comparisons = []
	for count_0, doc_0 in enumerate(sklearn_representation.toarray()):
		for count_1, doc_1 in enumerate(sklearn_representation.toarray()):
			#skl_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
			skl_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
			#return cosine_similarity(doc_0, doc_1)
	
	for x in zip(sorted(skl_tfidf_comparisons, reverse = True)):
		#print("Doc 0:", doc1)
		#print("Doc 1:", doc2)
		print(x)
		print()
		
	return skl_tfidf_comparisons

def getMaxCosineSimilarity(corpusList, text):
	#sents 	= sentSegmenter(corpus, asString=False, posTags=False)
	#res 		= []
	corpusListCount = len(corpusList)
	cosCount 		= 0
	
	if corpusListCount == 0:
		return float(0.0)
	
	for s in corpusList:
		cosSim 		= spacyCosineSimilarity(s, text)
		cosCount 	= cosCount + cosSim
		#res.append([s, cosSim])
		#res.append(cosSim)
		#d = sorted(res, reverse=True, key=lambda x: x[0])
		#d = sorted(res)
		#if len(res) >= 1:
		#	return d[0]
		#	
	return float(format(cosCount/corpusListCount, '.7f'))
	#return 0

def spacyCosineSimilarity(doc1, doc2):
	if not isinstance(doc1, str):
		return False
	if not isinstance(doc2, str):
		return False
	
	v1 = doSpeechify(doc1)
	v2 = doSpeechify(doc2)
	return v1.similarity(v2)


"""
def sklearnCosineSimilarity(text, sentence):
	corpus=speechify.sentSegmenter(text, asString=True, posTags=False)
	corpusFin=[]
	count=0
	for c in corpus:
		corpusFin.append((count, c))
		count=count+1
		
	tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words='english')
	tfidf_matrix =  tf.fit_transform(corpusFin)
	
	for index, score in find_similar(tfidf_matrix, 1):
		print(score, corpusFin[index])
	   
	X = tf.fit_transform([sentence] + corpus) # now X will have 3 rows
	print(cosine(X[0].toarray(), X[1].toarray())) # cosine between s and 1st sentence)
	
def find_similar(tfidf_matrix, index, top_n = 5):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]

"""
