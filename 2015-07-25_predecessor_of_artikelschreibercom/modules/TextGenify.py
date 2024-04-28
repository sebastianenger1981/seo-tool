# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore
import re
import sys
import math
import glob
import time
import shutil
import string
import signal, os
import hashlib
import markovify
import numpy as np
from multiprocessing.pool import Pool
from datetime import datetime as dTime

"""
import torch 
import torch.nn as nn
import numpy as np
from torch.autograd import Variable
from modules.pytorch_lib.data_utils import Dictionary, Corpus
"""

#import modules.Gensim as gSim
#import modules.Wordify as wordify
import modules.Speechify as speechify
#import modules.Servify as servify
import modules.Fileify as fileify

#import logging
#logger = logging.Logger(40)
debug=True
triesMarkov				= int(25)		# 75 # 15
max_overlap_ratioMarkov = 0.85 			# 77
max_overlap_totalMarkov	= int(9) 		# vorher war 9 -> 16
#markovState_size		= int(4)		# 24.3.2017: (3) -> 7 ging gut
minSpeechIndexValue		= float(0.84)	# ab 0.84 kommt gutes Textmaterial

cpu_pool				= int(20) 	# cpu threads
signal_timeout			= int(10)	#5
#MarkovResultList		= list()
markovpath				="/var/tmp/markov_bin/"

"""
# Hyper Parameters
embed_size 				= 64 # 128
hidden_size 			= 16 # 1024
num_layers 				= 3
num_epochs 				= 600
num_samples 			= 423  # number of words to be sampled
batch_size 				= 20
seq_length 				= 20
num_classes 			= 10
learning_rate 			= 2e-3 # 0.002
"""

"""
Later from multiprocessing import Process
"""

def getBestMarkovHits(markovList, corpus):
	import modules.CosineSimilarity as cosine
	import modules.Sentify as sentify
	from sklearn.feature_extraction.text import CountVectorizer
	vec = CountVectorizer(analyzer='char')
	
	if not isinstance(corpus, str):
		return False
	
	t_List=list()
	resultList=list()
	t_finalList={}
	t2_finalList=list()
	finalList=list()
	t_finalSet=set()
	t_finalListFin=list()
	
	if debug:
		print("TextGenify.cosine.sklearnCosineSimilaritySimple() Check started")
		
	# Cosine Similiarity zu jedem Markov Element berechnen
	#corpusV2=speechify.sentSegmenter(corpus, asString=False, posTags=False)
	corpusV2=speechify.sentSegmenterSimple(corpus, asString=False)
	try:
		vec.fit(corpusV2)
	except Exception as e:
		1
	else:
		for e in markovList:
			#speechIndex = cosine.sklearnCosineSimilarity(corpus, e)
			speechIndex = cosine.sklearnCosineSimilaritySimple(corpusV2, vec, e)
			t_List.append([speechIndex,e])
			"""
				todo: 	multiprocessing einbauen
						10=markovList[:10]
						r=pool.apply_async(cosine.sklearnCosineSimilaritySimple, (corpusV2, e, filesave))
						sklearnCosineSimilaritySimple speichert alle ergebnisse nach filesave
						hier dann filesave auslesen
			#if debug:
			#	1#print("TextGenify.cosine.sklearnCosineSimilaritySimple()", speechIndex, e)
			"""
		
		if debug:
			print("TextGenify.sorted() Check started")
			
		# Markov Cosine Liste nach Cosine Werten (größte zuerst) sortieren
		resultList = sorted(t_List, reverse=True, key=lambda x: x[0])
		
		# nur gute Markov Sätze durchlassen: sentify.isGoodSentence(mySentence)
		if debug:
			print("TextGenify.sorted() Count sorted Results:", len(resultList))
			print("TextGenify.sentify.isGoodSentence() Check started")
		
		for r in resultList:
			mySpeechIndex=float(r[0])
			mySentence=str(r[1])
			if mySpeechIndex >= minSpeechIndexValue:
				#if sentify.isGoodSentence(mySentence): # wird hier nicht benötigt
					#print("mySpeechIndex isGood:",mySpeechIndex) 
					#print("mySentence isGood:", mySentence)
					#t_finalList={""+mySentence+"":mySpeechIndex}
					#Hier eventell eine andere Datenstruktur als LIST nehmen -> set eventuell
				t_finalSet.add(mySentence)
				#t_finalListFin.append()
			#else:
			#	print("TextGenify.mySentence(): mySpeechIndex NOT good:", mySpeechIndex, mySentence)
			#	print()
		
		if debug:
			print("TextGenify.sorted() mySpeechIndex sorted Results:", len(t_finalSet))
		
		"""
		print(t_finalList)
		from operator import itemgetter
		# Gute Markov Satzliste sortieren
		for value, key in sorted(t_finalList.items(), itemgetter(1), True):
			print(key, value)
		
		exit(1)
		t2_finalList = sorted(t_finalList,key=lambda x: float(x))
		for f in t2_finalList:
			mySentence=str(f[1])
			finalList.append(mySentence)
		
		"""
		return list(t_finalSet)
	return list()

def textGeneration(corpus, MainKeyword, SubKeywords, maxresults):
	if not isinstance(corpus, str):
		return False
	
	if not os.path.exists(markovpath):
		os.makedirs(markovpath)
	else:
		shutil.rmtree(markovpath)
		os.makedirs(markovpath)
	
	multi 			= []
	MainKeyword		= MainKeyword.strip()
	SubKeywords		= SubKeywords.strip()
	#t_Corpus_List	= speechify.sentSegmenter(corpus, asString=False, posTags=False)
	t_Corpus_List	= speechify.sentSegmenterSimple(corpus, asString=False)
	t_Corpus		= "\n".join(t_Corpus_List)
	pool 			= Pool(processes=cpu_pool)
	
	#for i in range(cpu_pool):
	#for i in range(2,12):	# von markovState_size=2 bis markovState_size=9
	advanced=False
	for i in [2,3,4,5,6,7,8,9,10,11,12]: # von markovState_size=2 bis markovState_size=12
		result2 = pool.apply_async(generateMarkovTextSingle, (i, t_Corpus, MainKeyword, SubKeywords, maxresults, advanced))
		multi.append(result2)
		#advanced=True
		#result22 = pool.apply_async(generateMarkovTextSingle, (i, t_Corpus, MainKeyword, SubKeywords, maxresults, advanced))
		#multi.append(result22)
	"""
	result2 = pool.apply_async(generateMarkovTextSingle, (2, t_Corpus, MainKeyword, SubKeywords, maxresults, advanced))
	multi.append(result2)
	result2 = pool.apply_async(generateMarkovTextSingle, (3, t_Corpus, MainKeyword, SubKeywords, maxresults, advanced))
	multi.append(result2)
	result2 = pool.apply_async(generateMarkovTextSingle, (2, t_Corpus, MainKeyword, SubKeywords, maxresults, advanced))
	multi.append(result2)
	result2 = pool.apply_async(generateMarkovTextSingle, (4, t_Corpus, MainKeyword, SubKeywords, maxresults, advanced))
	multi.append(result2)
	"""
	if debug:
		print("genify.textGeneration(): Start Running ... with MainKeyword:'",MainKeyword,"' -> ",str(dTime.now()))
		print("genify.generateMarkovTextSingle(): Corpus lenght:", len(corpus))
		print("genify.generateMarkovTextSingle(): Creating Markov Database ...  -> ",str(dTime.now()))
		print("genify.generateMarkovTextSingle(): Markov Database Created ...  -> ",str(dTime.now()))
		print("genify.textGeneration(): Will start working with Multi Threading...")
		print("genify.textGeneration(): Starting "+str(signal_timeout)+" Seconds Text Generation Time Schedule ... "," -> ",str(dTime.now()))
		print()
	
	# kurz schlafen legen
	time.sleep(signal_timeout+1)
	for m in multi:
		w = m.get()
	pool.close()
	pool.join()
	
	MarkovResultReturnList=list()
	files = glob.glob(markovpath+"/*.bin")
	for file in files:
		#t_fname = os.path.basename(file)
		MarkovResultList=fileify.binaryRead(file)
		#MarkovResultReturnList.extend(MarkovResultList)
		#MarkovResultReturnList.append(MarkovResultList)
		MarkovResultReturnList+=MarkovResultList
	if debug:
		print("textgenify.lenght MarkovResultList:", len(MarkovResultReturnList))
	return MarkovResultReturnList

"""(tModel,t_Corpus, MainKeyword, SubKeywords, advanced)"""
def generateMarkovTextSingle(markovState_size, t_Corpus, MainKeyword, SubKeywords, maxresults, advanced):
	import modules.Sentify as sentify
	
	MarkovResultList= list()
	tModel 	= markovify.NewlineText(t_Corpus, state_size=markovState_size)
	#tModel 	= markovify.Text(t_Corpus, state_size=markovState_size)
	
	# Idee: TopicModell und Word2Vec von Wikipedia Artikel gegen die Markov Ketten vergleichen -> gute Ergebenisse bekommen Bonuspunkte
	workTimeframe = int(time.time()) + int(signal_timeout)# 3 sekunden spontanzeit
	while (maxresults > len(MarkovResultList)):
		c_Time = int(time.time())
		if (c_Time > workTimeframe):
			if debug:
				print("genify.generateMarkovTextSingle(): Markov Create Time OverflowError (markovState_size=",markovState_size,") -> ",advanced, " -> length:", len(MarkovResultList)," -> ",str(dTime.now()))
			sid = fileify.createShortid()
			fileify.binaryWrite(MarkovResultList, markovpath+sid+".bin")
			return True
		
		try:
			#print("genify.textGeneration(): Markov Chain Creating: START -> ",str(dTime.now()))
			if advanced is True:
				markov_sample = None
				MKtmp = MainKeyword.split()
				t_MK=MKtmp[:3]
				MK=" ".join(t_MK)
				if len(MKtmp) >= 1:
					markov_sample = tModel.make_sentence_with_start(beginning=MK, max_overlap_ratio=max_overlap_ratioMarkov)
					if not markov_sample or markov_sample is None:
						SKtmp = SubKeywords.split()
						t_SK=SKtmp[:3]
						SK=" ".join(t_SK)
						if len(SKtmp) >= 1:
							markov_sample = tModel.make_sentence_with_start(beginning=SK, max_overlap_ratio=max_overlap_ratioMarkov)
				if markov_sample is None:
					markov_sample = tModel.make_sentence(tries=triesMarkov, max_overlap_ratio=max_overlap_ratioMarkov)
			else:
				markov_sample = tModel.make_sentence(tries=triesMarkov, max_overlap_ratio=max_overlap_ratioMarkov)
			#print("genify.textGeneration(): Markov Chain Creating: FINISH -> ",str(dTime.now()))
		except Exception as strerror:
			#print("Unexpected error:", sys.exc_info()[0])
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			#print("Error while creating Markov Sample with: tModel.make_sentence():")
			1
		
		else:
			if markov_sample is not None and sentify.isGoodSentence(markov_sample):
				# if matchMainKeyword(markov_sample, MainKeyword):
				# if matchMainKeyword(markov_sample, SubKeywords):
				MarkovResultList.append(markov_sample)
	return True

def matchMainKeyword(markov, MainKeyword):
	if isinstance(markov, str) and isinstance(MainKeyword, str):
		if (not markov or not MainKeyword):
			return False
		
		if MainKeyword in markov or markov in MainKeyword:
			return True
			
		if MainKeyword.find(markov) != -1:
			return True
		if markov.find(MainKeyword) != -1:
			return True
		
		for char in string.punctuation:
			markov = markov.replace(char, '')
		
		tmpList 	= markov.lower().split()
		if MainKeyword.lower() in tmpList:
			return True
		
		m_List 		= markov.lower().split()
		k_List		= MainKeyword.lower().split()
		vListing 	= list(set(m_List) & set(k_List))
			
		if (len(vListing)>=1):
			return True
	
	return False

def createPhraseKeyword(markov, kw):
	if isinstance(markov, str) and isinstance(kw, str):
		if (not markov or not kw):
			return False
		
		for char in string.punctuation:
			markov = markov.replace(char, '')
		
		tmpList 	= markov.lower().split(" ")
		
		if type(kw) is str and kw.lower() in tmpList:
			return True
		elif type(kw) is list:
			KW1 = []
			for a in kw:
				KW1.append(a.strip().lower())
			
			vListing 	= list(set(tmpList) & set(KW1))
			
			if (len(vListing)>=1):
				return True
			else:
				return False
			
		else:
			return False
	return False

def createNounPhraseSubKeywords(markov, SubKeywords):
	if isinstance(markov, str) and isinstance(SubKeywords, str):
		#markov = u"Dieser Seitensprung ist kein Gerücht mehr"
		if (not markov or not SubKeywords):
			return False
		
		if SubKeywords.find(',') != -1:
			# keine Kommas im Satz erlauben
			subKW 	= SubKeywords.lower().strip().split(",")
		
		if SubKeywords.find(';') != -1:
			# keine Kommas im Satz erlauben
			subKW 	= SubKeywords.lower().strip().split(";")
		
		if SubKeywords.find('-') != -1:
			# keine Kommas im Satz erlauben
			subKW 	= SubKeywords.lower().strip().split("-")
		
		KW 	= []
		for a in subKW:
			KW.append(a.strip().lower())
		
		for char in string.punctuation:
			markov = markov.replace(char, '')
		
		tmpList 	= markov.lower().split(" ")
		vListing 	= list(set(tmpList) & set(KW))
		
		if (len(vListing)>=1):
			return True
		else:
			return False
	return False

def createGrammarBasedAdvanced(markov, AllowedList):
	if isinstance(markov, str):
		if (not markov or not AllowedList):
			return False
		
		#markov = "Sarah fährt mit dem Rad spazieren."
		posTagMarkov 	= []
		toks1 			= speechify.doSpeechify(markov)
		for token1 in toks1:
			posTagMarkov.append(token1.pos_)
		
		posTagMarkovString = " ".join(posTagMarkov)
		posTagMarkovString = posTagMarkovString.replace("PUNCT","")
		posTagMarkovString = posTagMarkovString.replace("SPACE","")
		posTagMarkovString = re.sub(r"\s+", '-', posTagMarkovString)
		
		# todo: zurückgeben, der Satz und später: zurückgeben des Teiles des Satzes der auf die POS Strukur genau gematcht wurde 
		count = 0
		for posEle in AllowedList:
			count = count + 1
			posEleString = posEle
			posEleString = posEleString.replace("PUNCT","")
			posEleString = posEleString.replace("SPACE","")
			posEleString = re.sub(r"\s+", '-', posEleString)
			#print("createGrammarBasedAdvanced")
			#print(count)
			
			#print("CORPUS POS TAGS:", posEleString)
			#print("MARKOV POS TAGS:", posTagMarkovString)
			#print("\tMARKOV:", markov)
			if posEleString in posTagMarkovString:
				return True
			else:
				return False
		return False
	return False

def createGrammarBased(markov, allowedRuleString):
	if isinstance(markov, str) and isinstance(allowedRuleString, str):
		if (not markov or not allowedRuleString):
			return False
		
		for char in string.punctuation:
			markov = markov.replace(char, '')
		
		#markov = "Sarah fährt mit dem Rad spazieren."
		posTagMarkov 	= []
		toks1 			= speechify.doSpeechify(markov)
		#pprint.pprint(markov)
		
		for token1 in toks1:
			posTagMarkov.append(token1.pos_)
			#pprint.pprint(token1.pos_)

		posTagMarkovString = ",".join(posTagMarkov).replace("PUNCT","")
		
		if allowedRuleString in posTagMarkovString:
			return True
		else:
			return False
	return False

def matchMainKeywordv1(markov, MainKeyword):
	if isinstance(markov, str) and isinstance(MainKeyword, str):
		if (not markov or not MainKeyword):
			return False
		
		if MainKeyword in markov:
			return True
			
		if MainKeyword.find(markov) != -1:
			return True
		
		if re.search(MainKeyword,markov):
			#print "Der Ausdruck hat gepasst"
			return True
		
		for char in string.punctuation:
			markov = markov.replace(char, '')
		
		tmpList 	= markov.lower().split()
		if MainKeyword.lower() in tmpList:
			return True
		
		m_List 		= markov.lower().split()
		k_List		= MainKeyword.lower().split()
		vListing 	= list(set(m_List) & set(k_List))
			
		if (len(vListing)>=1):
			return True
	
	return False

def textGenerationLstm(corpus, MainKeyword, SubKeywords, maxresults, load=False):
	#corpusNewLine = speechify.sentSegmenter(corpus, asString=False, posTags=False)
	corpusNewLine = speechify.sentSegmenterSimple(corpus, asString=False)
	# Load Penn Treebank Dataset
	outputWords=""
	corpus = Corpus()
	ids = corpus.get_data_string(corpusNewLine, batch_size)
	vocab_size = len(corpus.dictionary)
	num_batches = ids.size(1) // seq_length
	
	# RNN Based Language Model
	class RNNLM(nn.Module):
		def __init__(self, vocab_size, embed_size, hidden_size, num_layers):
			super(RNNLM, self).__init__()
			self.embed = nn.Embedding(vocab_size, embed_size)
			self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
			self.linear = nn.Linear(hidden_size, vocab_size)
			
			self.init_weights()
			
		def init_weights(self):
			self.embed.weight.data.uniform_(-0.1, 0.1)
			self.linear.bias.data.fill_(0)
			self.linear.weight.data.uniform_(-0.1, 0.1)
			
		def forward(self, x, h):
			# Embed word ids to vectors
			x = self.embed(x) 
			
			# Forward propagate RNN  
			out, h = self.lstm(x, h)
			
			# Reshape output to (batch_size*sequence_length, hidden_size)
			out = out.contiguous().view(out.size(0)*out.size(1), out.size(2))
			
			# Decode hidden states of all time step
			out = self.linear(out)  
			return out, h
	model = RNNLM(vocab_size, embed_size, hidden_size, num_layers)
	
	# Loss and Optimizer
	criterion = nn.CrossEntropyLoss()
	optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

	# Truncated Backpropagation 
	def detach(states):
		return [Variable(state.data) for state in states] 

	# Training
	for epoch in range(num_epochs):
		# Initial hidden and memory states
		states = (Variable(torch.zeros(num_layers, batch_size, hidden_size)),
				  Variable(torch.zeros(num_layers, batch_size, hidden_size)))
		
		for i in range(0, ids.size(1) - seq_length, seq_length):
			# Get batch inputs and targets
			inputs = Variable(ids[:, i:i+seq_length])
			targets = Variable(ids[:, (i+1):(i+1)+seq_length].contiguous())
			
			# Forward + Backward + Optimize
			model.zero_grad()
			states = detach(states)
			outputs, states = model(inputs, states) 
			loss = criterion(outputs, targets.view(-1))
			loss.backward()
			torch.nn.utils.clip_grad_norm(model.parameters(), 0.5)
			optimizer.step()
			
			step = (i+1) // seq_length
			if step % 100 == 0:
			#    print ('Epoch [%d/%d], Step[%d/%d], Loss: %.3f, Perplexity: %5.2f' %
			#           (epoch+1, num_epochs, step, num_batches, loss.data[0], np.exp(loss.data[0])))
				print ('Epoch [%d/%d], Loss: %.3f, Perplexity: %5.2f' %
					   (epoch+1, num_epochs, loss.data[0], np.exp(loss.data[0])))
				print(str(dTime.now()))
	
	# Sampling
	# Set intial hidden ane memory states
	state = (Variable(torch.zeros(num_layers, 1, hidden_size)), Variable(torch.zeros(num_layers, 1, hidden_size)))
	
	# Select one word id randomly
	prob = torch.ones(vocab_size)
	input = Variable(torch.multinomial(prob, num_samples=1).unsqueeze(1), volatile=True)
	
	for i in range(num_samples):
		# Forward propagate rnn 
		output, state = model(input, state)
		
		# Sample a word id
		prob = output.squeeze().data.exp()
		word_id = torch.multinomial(prob, 1)[0]
		
		# Feed sampled word id to next time step
		input.data.fill_(word_id)
		
		# File write
		word = corpus.dictionary.idx2word[word_id]
		word = '\n' if word == '<eos>' else word + ' '
		###f.write(word)
		outputWords=outputWords+word
	#    if (i+1) % 100 == 0:
	#        print('Sampled [%d/%d] words and save to %s'%(i+1, num_samples, sample_path))
	return True