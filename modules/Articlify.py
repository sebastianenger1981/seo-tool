# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore
import re
import time
import chardet
from time import sleep
from datetime import datetime as dTime
from random import randrange
from pprint import PrettyPrinter
from sklearn.feature_extraction.text import CountVectorizer

import modules.Wordify as wordify
import modules.TextGenify as genify
import modules.Speechify as speechify
import modules.Sentify as sentify
import modules.CosineSimilarity as cosine
import modules.Gensim as gSim
import modules.Fileify as fileify

pp 	= PrettyPrinter(indent=4)

#from modules.pytorch_lib.data_utils import Dictionary, Corpus
debug=True
#debug=False

def beautifyArticle(f, fullCorpus, MainKeyword, SubKeywords, WDirBinary, SessionID):
	vec = CountVectorizer(analyzer='char')
	
	headlineOrg=""
	#hit=float(-1)
	corpus = f['content']
	sid = f['shortid']
	hit = f['hit']
	tag = f['tag']
	
	#sent_new_syn=speechify.sentSegmenter(corpus, asString=False, posTags=False)
	sent_new_syn=speechify.sentSegmenterSimple(corpus, asString=False)
	sent_new=sent_new_syn
	sent_new_syn=prepareContent(sent_new_syn)
	sentence_new_syn="".join(sent_new_syn)
	
	resultListHeadline= gSim.gensimDoc2Vec(corpus, MainKeyword, advanced=False)
	if len(resultListHeadline)==0:
		resultListHeadline= gSim.gensimDoc2Vec(corpus, SubKeywords, advanced=False)
		if len(resultListHeadline)==0:
			resultListHeadline	= gSim.gensimDoc2Vec(fullCorpus, MainKeyword, advanced=False)
	
	try:
		vec.fit(sent_new_syn)
	except Exception as e:
		import sys, os
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		#print("Error while creating Markov Sample with: tModel.make_sentence():")
	
	for f in resultListHeadline:
		#print(type(f))
		#for f in cc:
		headlineOrg = f['content']
		#hit = f['hit']
		if not sentify.isGoodSentence(headlineOrg):
			continue
		speechIndex = cosine.sklearnCosineSimilaritySimple(sent_new, vec, headlineOrg)
		if speechIndex > 0.86 and len(headlineOrg) >= 33 and len(headlineOrg) < 115:
			break
	
	# 	Headline Generation
	headline = sentify.createHeadline(MainKeyword, SubKeywords, headlineOrg, simpleType=False)
	
	#Get Wikipedia Summary
	w_list1=wordify.getWikiPediaSummary(MainKeyword)
	w_list2=wordify.getWikiPediaSummary(SubKeywords)
	wikiText1=wordify.getWikiPediaTextSummary(w_list1, MainKeyword, SubKeywords)
	wikiText2=wordify.getWikiPediaTextSummary(w_list2, MainKeyword, SubKeywords)
	w_List=w_list1[0]+w_list2[0]
	#wikiTextCorpus=wordify.getWikiPlainContent(w_List)
	
	"""
	#Todo: FillingSentences aus Doc2Vec noch synonyme ersetzen für Verben und Nomen
	#fillingSentences1=gSim.gensimDoc2Vec(fullCorpus, headlineOrg, advanced=False)
	fillingSentences2v1=gSim.gensimDoc2Vec(fullCorpus, MainKeyword, advanced=False)
	#fillingSentences2v2=gSim.gensimDoc2Vec(fullCorpus, SubKeywords, advanced=False)
	fillingSentences2=fillingSentences2v1#+fillingSentences2v2
	#fillingSentences3=gSim.gensimDoc2Vec(fullCorpus, SubKeywords, advanced=True)
	
	pList=gSim.flattenDoc2VecList(fillingSentences2)
	resultListFilling = genify.getBestMarkovHits(pList, fullCorpus)
	
	print("articlify.beautifyArticle() Processing FullCorpus Markov Textgeneration")
	l_MarkovV1=genify.textGeneration(fullCorpus, MainKeyword, SubKeywords, 25)
	#l_MarkovV2=genify.textGeneration(corpus, MainKeyword, SubKeywords, 4500, advanced=True)
	resultListMarkov=genify.getBestMarkovHits(l_MarkovV1, corpus)
	"""
	
	
	"""
	print("articlify.beautifyArticle() Processing WikiPedia Markov Textgeneration")
	resultListMarkovWikiV1=genify.textGeneration(wikiTextCorpus, MainKeyword, SubKeywords, 25)
	resultListMarkovWiki=genify.getBestMarkovHits(resultListMarkovWikiV1, corpus)
	"""
	
	if debug:
		"""
		print("corpus-beautifyArticle():", len(corpus))
		print("corpus-beautifyArticle() is sid:", sid)
		print()
		print("headline: ", headline)
		print()
		print("Text Lenght: ", len(corpus))
		print()
		print("Article Source Lenght:", len(sentence_new_syn))
		print()
		print("Article Source List Lenght:", len(sent_new_syn))
		print()
		print("wikiText1:\n", wikiText1)
		print()
		print("wikiText1 Lenght:", len(wikiText1))
		print()
		print("IntroTextWiki: ", wikiText1)
		print()
		print("Length wikiTextCorpus:", len(wikiTextCorpus))
		print()
		print("Markov Wiki Samples (WIKICORPUS): ", len(resultListMarkovWiki))
		print()
		print("Length resultListMarkov:", len(resultListMarkov))
		print()
		"""
		#exit(1)
		#sleep(5.05)
		#from pprint import PrettyPrinter
		#pp 	= PrettyPrinter(indent=4)
		#pp.pprint(sent_new_syn)
		
	#### Build article
	myArticlePlain=[]
	myArticle=[]
	NoDuplicate=set()# no dublicate markov content
	# Headline
	
	""" Structure:
		1. Headline
		2. Wiki IntroTextWiki
		3. Orginal Sentences (100%)
		4. MarkovWiki
		5. Filling Sentences
		6. Markov Normal
	"""
	
	# 1. Headline 2. Wiki IntroTextWiki
	#myArticle.append(headline+"\n\n")
	#myArticlePlain.append(headline)
	
	# WikiTextSumary
	if len(wikiText1)>35 and len(wikiText2)>35:
		myArticle.append(wikiText1+"(FI3) "+wikiText2+"(FI3)")
	elif len(wikiText1)>35:
		myArticle.append(wikiText1+"(FI3)")
	
	# 3. Orginal Sentences (100%)
	c=0
	for sent in sent_new_syn:
		#if sent not in NoDuplicate:
		myArticle.append(sent+"(OI1)")
		NoDuplicate.add(sent)
		c=c+1
	
	"""
	# 4. MarkovWiki
	c=0
	for sent in resultListMarkovWiki:
		if c < 10 and c < len(resultListMarkovWiki):
			if sent not in NoDuplicate:
				isMainKeyword = genify.matchMainKeyword(sent, MainKeyword)
				isSubKeyword = genify.matchMainKeyword(sent, SubKeywords)
				
				if isMainKeyword:
					myArticle.append(sent+"(GI1)")
				elif isMainKeyword:
					myArticle.append(sent+"(GI2)")
				else:
					myArticle.append(sent+"(GI3)")
				
				NoDuplicate.add(sent)
				c=c+1
	
	# 5. Filling Sentences
	c=0
	for sent in resultListFilling:	
		if c < 10 and c < len(resultListFilling):
			if sent not in NoDuplicate:
				isMainKeyword = genify.matchMainKeyword(sent, MainKeyword)
				isSubKeyword = genify.matchMainKeyword(sent, SubKeywords)
				
				if isMainKeyword:
					myArticle.append(sent+"(FI1)")
				elif isMainKeyword:
					myArticle.append(sent+"(FI2)")
				else:
					myArticle.append(sent+"(FI3)")
				
				NoDuplicate.add(sent)
				c=c+1
	
	# 6. Markov Normal
	c=0
	for sent in resultListMarkov:
		if c < 7 and c < len(resultListMarkov):
			if sent not in NoDuplicate:
				isMainKeyword = genify.matchMainKeyword(sent, MainKeyword)
				isSubKeyword = genify.matchMainKeyword(sent, SubKeywords)
				
				if isMainKeyword:
					myArticle.append(sent+"(GI1)")
				elif isMainKeyword:
					myArticle.append(sent+"(GI2)")
				else:
					myArticle.append(sent+"(GI3)")
				
				NoDuplicate.add(sent)
				#resultListMarkov.remove(sent)
				c=c+1
	"""
	
	myArticle=''.join(''.join(elems) for elems in myArticle)
	#myArticleTmp=''.join(''.join(elems) for elems in myArticle)
	aStart = str(dTime.now())
	myArticle=exchangeContent(myArticle)
	aEnd = str(dTime.now())
	#myArticleTmp=wordify.encodeToLatin1(myArticleTmp)
	#myArticle=wordify.encodeToUTF8Adv(myArticle)
	
	myArticle = headline+"\n\n" + myArticle+"\n\n"
	myArticlePlain=re.sub('\(\w{3}\)',' ', myArticle)
	
	if debug:
		#print("Article:", wordify.encodeToLatin1(myArticle))
		print("New Article Lenght:",len(myArticle))
		print("New PrepareContent Lenght:",len(" ".join(sent_new)))
		fileify.plainWrite(myArticle, "/home/buz/buzzgreator/article/"+MainKeyword+"-"+SubKeywords+"-"+sid+"-"+"_artikel.txt")
		fileify.plainWrite(myArticlePlain, "/home/buz/buzzgreator/article/"+MainKeyword+"-"+SubKeywords+"-"+sid+"-"+"_artikelplain.txt")
		#print("Article Encoding:", chardet.detect(myArticletmp.decode()))
		print()
	
	"""
	fileify.binaryWrite(myArticlePlain, WDirBinary+sid+"-myArticlePlain.bin")
	fileify.binaryWrite(myArticle, WDirBinary+sid+"-myArticle.bin")
	fileify.plainWrite(myArticle, WDirBinary+sid+"-artikel.txt")
	fileify.plainWrite(myArticle, "/home/buz/buzzgreator/article/"+MainKeyword+"->"+SubKeywords+"->"+sid+"->"+"_artikel.txt")
	fileify.plainWrite(myArticlePlain, "/home/buz/buzzgreator/article/"+MainKeyword+"->"+SubKeywords+"->"+sid+"<-"+"_artikelplain.txt")
	"""
	
	
	
	myArticlev1=myArticle+"<br/><br/><br/>OriginalContent:<br/><br/>"+corpus
	fileify.plainWrite(myArticlev1,"/home/www/wwwontipp/results/"+SessionID+".txt")
	print("Ariclyfily RETURN")
	print("beautifyArticle() exchangeContent Start:", aStart)
	print("beautifyArticle() exchangeContent End:", aEnd)
	return myArticle

def prepareContent(textList):
	debug=False
	"""
	if isinstance(textList, list):
		orgText = " ".join(orgText)
	if not isinstance(orgText, str):
		return False
	"""
	
	vec = CountVectorizer(analyzer='char')
	sentLenght=len(textList)
	sentCheck=int(round((sentLenght/100)*77)) # ab 65 Prozent des Contents wird gescheckt
	text=" ".join(textList)
	topics=gSim.topicModeling(text)
	
	goodFlag=False
	try:
		vec.fit(textList)
	except Exception as e:
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		#print("Error while creating Markov Sample with: tModel.make_sentence():")
	else:
		goodFlag=True
	
	print("Ariclyfily.prepareContent() textList():", len(textList))
	sc=0
	textNewList=[]
	#p = re.compile('\(\w{3}\)')
	for sent in textList:
		sent=sent.strip()
		sent=wordify.removeUhrzeiten(sent)
		#sent=re.sub('\s{2,}',' ',sent)
		#sent=wordify.encodeToLatin1(sent)
		
		if not sentify.isNotBlacklisted(sent):
			if debug:
				sent=wordify.encodeToLatin1(sent)
				print("Ariclyfily.prepareContent() sentify.isNotBlacklisted():", sent)
			continue
		
		if not sentify.isLongEnoughSentence(sent):
			if debug:
				sent=wordify.encodeToLatin1(sent)
				print("Ariclyfily.prepareContent() sentify.isLongEnoughSentence():", sent)
			continue
		
		if not sentify.isGoodSentenceSimple(sent):
			continue
		
		if not sentify.isGoodSentence(sent):
			continue
		
		if sc>=sentCheck:
			isMatch=False
			t_List=[]
			for t in topics:
				isMatch=genify.matchMainKeyword(t, sent)
				t_List.append(isMatch)
			
			if any(t_List):
				textNewList.append(sent)# save sentences
				#print("Topic Modelling HIT: ", sent)
				#speechIndex = cosine.sklearnCosineSimilaritySimple(textList, vec, sent)
				#print("Topic Modelling HIT INDEX: ", speechIndex)
				#print()
				continue
			
			#print("Sentence (RAW):", goodFlag, sc, sent)
			if goodFlag:
				speechIndex=cosine.sklearnCosineSimilaritySimple(textList, vec, sent)
				if speechIndex>0.86:#0.9
					if debug:
						sent=wordify.encodeToLatin1(sent)
						print("Sentence:", sent, " -> speechIndex:",speechIndex)
					textNewList.append(sent)
		elif sc < sentCheck:
			textNewList.append(sent)
		sc=sc+1
	
	print("Ariclyfily.prepareContent() textNewList():", len(textNewList))
	return textNewList

def exchangeContent(orgText):
	debug=False
	if isinstance(orgText, list):
		orgText = " ".join(orgText)
	if not isinstance(orgText, str):
		return False
	"""
	2. Satz Umwandlungen:
	- Jeder Satz muss eine: S.E.1 oder/und S.E.0 haben
	- Jeder dritte Satz: NounTranslate, jedoch darf eine vorhandene Austauschoption nicht überschrieben werden
	- Wort, das getauscht wurde, darf nicht nochmal getauscht werden
	- jedes SE0 muss mindestens 4 Worte vom nächsten SE0 entfernt liegen
	- jedes SE1 muss mindestens 3 Worte vom nächsten SE1 entfernt liegen
	- dazu jedes Wort in jedem Satz bearbeiten
	--> Wordify.replaceSynonymsSimple()
	
	-> dazu die Funktion def changeArticleStructure(sumText): in ArticlyFy anpassen
	"""
	
	r_Sentence=""
	listAllowedV=[u"VMFIN", u"VMINF", u"VMPP", u"VVFIN", u"VVIMP", u"VVINF", u"VVIZU", u"VVPP", u"VERB"]
	listAllowedN=[u"NN",u"NNP",u"NNPS",u"PROPN",u"NOUN",u"NE", u"NNE"]
	#sentences=speechify.sentSegmenter(orgText, asString=True, posTags=True)
	#sentences1=t_Sent.split("\n")
	####corpus=wordify.beautifyCorpusSimple(orgText)
	#sentencesCorpus=speechify.sentSegmenter(orgText, asString=False, posTags=False)
	
	print("Corpus (Article) Raw:", len(orgText))
	#print("Corpus (Article) Good:", len(corpus))
	
	sc=0
	p = re.compile('\(\w{3}\)')
	p1 = re.compile('\"')	# Wenn Zitate, dann darin nix ändern
	p2 = re.compile('\'')
	token = speechify.doSpeechify(orgText)
	l_Sent=len(list(token.sents))
	l_lastSentHit=0
	l_lastVerbHit=0
	l_lastNounHit=0
	for span in token.sents:
		sent=str(span)
		#if not sentify.isGoodSentence(sent):
		#	continue
		if debug:
			l_SentLenght=len(list(span))
			print("Sentence Nr.:", sc, " von ", l_Sent, " Sentence Lenght:", l_SentLenght)
		words=sent.split()
		c=0
		l_lastVerbHit=0
		l_lastNounHit=0
		for word in span:
			pos_tag=word.pos_
			ner=word.ent_type_
			w=word.text
			if p.search(word.text) is not None: # sowas hier: witzig(NB1)
				r_Sentence=r_Sentence+" "+w
				continue
			if p1.search(word.text) is not None: # sowas hier: 'witzig'
				r_Sentence=r_Sentence+" "+w
				continue
			if p2.search(word.text) is not None: # sowas hier: "witzig.(OI1)Einerseits"
				r_Sentence=r_Sentence+" "+w
				continue
			#print("exchangeContent():", ner)
			#print("exchangeContent():", pos_tag)
			#print("Word of Sentence Nr.:", sc, c)
			#print word.orth_, word.tag_, word.dep_, word.head.orth_
			if sc >= (l_lastSentHit + 3) and l_lastSentHit !=sc: # letze mal blockTranslate war nicht beim aktuellen Eintrag #alle 3 Sätze ein NB1
				if w.isalpha() and len(ner) == 0:
					if debug:
						print("Articlify.sentify.blockTranslateSimple(w)",sc," sc: -> l:",l_lastSentHit)
					w = sentify.blockTranslateSimple(w) # Jeder dritte Satz: NounTranslate
					l_lastSentHit=sc
			
			if c >= (l_lastVerbHit + 8) and pos_tag in listAllowedV: #alle 5 Worte ein SE1
				wv1=w
				if w.isalpha() and len(ner) == 0: #no entity match
					w=wordify.replaceSynonymsSimple(w, 0)# "Modified (VERB):"
				if w != wv1:
					if debug:
						print("Articlify.wordify.replaceSynonymsSimple(w, 0) Successfull",c," c: -> l:",l_lastVerbHit)
					l_lastVerbHit=c
			
			if c >= (l_lastNounHit + 11) and pos_tag in listAllowedN: #alle 8 Worte ein SE2
				wv1=w
				if w.isalpha() and len(ner) == 0:
					w=wordify.replaceSynonymsSimple(w, 1)# "Modified (NOUN):"
				if w != wv1:
					if debug:
						print("Articlify.wordify.replaceSynonymsSimple(w, 1) Successfull",c," c: -> l:",l_lastNounHit)
					l_lastNounHit=c
			
			v=w
			v=v.replace('.','')
			v=v.replace(',','')
			if (w.isdigit() or v.isdigit()) and len(ner) == 0:
			#if w.isdigit() and c % 3 == 0:
				if v.isdigit():
					w=sentify.convertNumber2Word(v)
				else:
					w=sentify.convertNumber2Word(w)
				
				if debug:
					print("Ariclyfy.sentify.convertNumber2Word()")
			
			r_Sentence=r_Sentence+" "+w
			c=c+1
		sc=sc+1
	return r_Sentence

def getBestArticleValue(text, fullcorpus, w_list1, w_list2, MainKeyword, SubKeywords):
	import modules.CosineSimilarity as cosine
	import modules.Gensim as gSim
	import modules.Wordify as wordify
	import modules.Speechify as speechify
	import modules.Sentify as sentify
	import modules.TextGenify as genify
	
	SimRankPointBase=int(5) # 3?
	overallPoints=float(0.0000)
	isMainKeyword=""
	isSubKeyword=""
	
	# temporary fix
	if len(text)<=250:
		return float(0.0)
	
	topics = gSim.topicModeling(text)
	if len(topics)==0:
		return float(0.0)
	
	for t in topics:
		if MainKeyword.lower() == t.lower():
			overallPoints=overallPoints+float(500)
		if SubKeywords.lower() == t.lower():
			overallPoints=overallPoints+float(400)
		
		isMainKeyword = genify.matchMainKeyword(t, MainKeyword)
		isSubKeyword = genify.matchMainKeyword(t, SubKeywords)
		if isMainKeyword is True:
			print("getBestArticleValue(): -topics- isMainKeyword is True():", t," -> ", MainKeyword)
			overallPoints=overallPoints+float(10)
		if isSubKeyword is True:
			print("getBestArticleValue(): -topics- isSubKeyword is True():", t," -> ", SubKeywords)
			overallPoints=overallPoints+float(5)
		
		if t.lower() in MainKeyword.lower():
			print("getBestArticleValue(): -topics- isMainKeyword is True():", t," -> ", MainKeyword)
			overallPoints=overallPoints+float(20)
		if t.lower() in SubKeywords.lower():
			print("getBestArticleValue(): -topics- isSubKeyword is True():", t," -> ", SubKeywords)
			overallPoints=overallPoints+float(10)
	
	if MainKeyword.lower() in text.lower():
		print("getBestArticleValue(): (text, MainKeyword)", MainKeyword)
		overallPoints=overallPoints+float(75)
	if SubKeywords.lower() in text.lower():
		print("getBestArticleValue(): (text, isSubKeyword)", SubKeywords)
		overallPoints=overallPoints+float(35)
	""" 5.3 Allgemeines: END """
	
	""" 5.4 Sprache: Start """
	if wordify.intDetectLanguage(text) == "de":
		overallPoints=overallPoints+float(1)
	""" 5.4 Sprache: End """
	
	wordCounts = int(len(text.split()))
	overallPoints=overallPoints+float((wordCounts/1000)*0.3)
	
	overallPoints=round(overallPoints,3)
	return overallPoints