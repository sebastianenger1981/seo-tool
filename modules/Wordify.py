# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore

import nltk
import random
import chardet
import string
import os, sys, logging, re, time, math, json, uuid, html
import pprint  # pretty-printer
from textblob_de import TextBlobDE
from textblob import TextBlob
#import spacy# pip3 install --upgrade spacy
#from spacy.en import English
#from spacy.de import German
from nltk.corpus import stopwords	
#import libleipzig	# pip3 install --upgrade libleipzig
from urllib.parse import urlparse# pip3 install --upgrade urlparse
from urllib import parse# pip3 install --upgrade urlparse
import requests		# pip3 install --upgrade requests
from requests.auth import HTTPBasicAuth
import html.parser
import datetime
import subprocess
from google.cloud import translate
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import goslate # pip3 install --upgrade goslate
import codecs
import unicodedata
from unidecode import unidecode
from langdetect import detect	# pip3 install --upgrade langdetect
from bs4 import BeautifulSoup, Comment 	# pip3 install --upgrade beautifulsoup4 && pip install 
from pprint import PrettyPrinter
from textblob_de.packages import pattern_de as pd
from unicodedata import normalize

pp=PrettyPrinter(indent=4)
debug=False

os.system("export GOOGLE_APPLICATION_CREDENTIALS='/home/buz/buzzgreator/key/100BiereTranslate-8a809e939d5e.json'")
UserAgent			= "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
UserAgentMobile		= "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
Headers 			= {'user-agent': UserAgentMobile}
gs 					= goslate.Goslate()

DEVELOPER_KEY 		= "AIzaSyDvkxDa_2pC60rM3PgSt8YAIa4MbUcu8HY"

listAllowedV 		= [u"VMFIN", u"VMINF", u"VMPP", u"VVFIN", u"VVIMP", u"VVINF", u"VVIZU", u"VVPP", u"VERB"]
listAllowedN 		= [u"NN",u"NNP",u"NNPS",u"PROPN",u"NOUN",u"NE", u"NNE"]

MinSynExchangeWordLength = 4
"""
import nltk
>>> nltk.download('all', halt_on_error=False)
"""
def replaceUmlauts(corpus):
	f_Text=""
	for t in corpus:
		#print("T:",t,ord(t))
		if ord(t)==196:
			f_Text=f_Text+"AE"
		elif ord(t)==214:
			f_Text=f_Text+"OE"
		elif ord(t)==220:
			f_Text=f_Text+"UE"
		elif ord(t)==223:
			f_Text=f_Text+"sz"
		elif ord(t)==228:
			f_Text=f_Text+"ae"
		elif ord(t)==246:
			f_Text=f_Text+"oe"
		elif ord(t)==252:
			f_Text=f_Text+"ue"
		else:
			f_Text=f_Text+t
	#print("replaceUmlauts() f_Text:",f_Text)
	#print()
	#f_Text = unicodedata.normalize('NFKD', f_Text).encode('ASCII', 'ignore')
	#f_Text = f_Text.decode()
	#print("replaceUmlauts() f_Text normalize:",f_Text)
	#print()
	#print("replace", f_Text)
	return f_Text

def replaceUmlautsReverse(corpus):
	f_Text=corpus
	f_Text=f_Text.replace('AE', u'Ä')
	f_Text=f_Text.replace('OE', u'Ö')
	f_Text=f_Text.replace('UE', u'Ü')
	f_Text=f_Text.replace('sz', u'ß')
	f_Text=f_Text.replace('ae', u'ä')
	f_Text=f_Text.replace('ue', u'ü')
	f_Text=f_Text.replace('oe', u'ö')
	return f_Text

def removeUhrzeiten(t):
	t=re.sub('(\w{3,25})(\s+)(\d{1,2})(\s+)(\d{2,4})', '',t)
	t=re.sub('(\d{2,4})[/.-](\d{1,2})[/.-](\d{1,2})', '',t)
	t=re.sub('(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})', '',t)
	t=re.sub('(\d{1,2})[:](\d{1,2})', '',t)
	return str(t)

def beautifyCorpusSimple(corpus):
	import modules.Speechify as speechify
	import modules.Sentify as sentify
	if isinstance(corpus, list):
		corpus = " ".join(corpus)
	if not isinstance(corpus, str):
		return False
	
	t_sent = speechify.sentSegmenterSimple(corpus, asString=False)
	#t_sent = speechify.sentSegmenter(corpus, asString=False, posTags=False)
	#print("sentSegmenterSimple():", len(t_sent))
	
	t_corpus=""
	for t in t_sent:
		t=removeUhrzeiten(t)
		if not sentify.isNotBlacklisted(t):
			continue
		if not sentify.isSentenceStructureAdvanced(t):
			continue
		if not sentify.isGoodSpecialCharsSimple(t, 5):
			continue
		if not sentify.isNotDublicateString(t):
			continue
		if not sentify.isLongEnoughSentence(t):
			continue
		if not sentify.isGoodSentenceSimple(t):
			continue
		"""
		if not sentify.isLongEnoughSentence(t):
			print("not long enough:", encodeToLatin1(t))
			continue
		"""
		t_corpus=t_corpus+t
	
	t_corpus = ' '.join(t_corpus.split()) # 
	t_corpus=t_corpus.replace('.', '. ')
	t_corpus=t_corpus.replace('!', '! ')
	t_corpus=t_corpus.replace('?', '? ')
	return t_corpus

def beautifyCorpus(corpus):
	import modules.Speechify as speechify
	import modules.Sentify as sentify
	if isinstance(corpus, list):
		corpus = " ".join(corpus)
	if not isinstance(corpus, str):
		return False
	
	t_sent = speechify.sentSegmenterSimple(corpus, asString=False)
	#t_sent = speechify.sentSegmenter(corpus, asString=False, posTags=False)
	t_corpus=""
	for t in t_sent:
		t=removeUhrzeiten(t)
		if sentify.isGoodSentence(t):
			t_corpus=t_corpus+t
	
	t_corpus = ' '.join(t_corpus.split()) # http://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
	
	t_corpus=t_corpus.replace('.', '. ')
	t_corpus=t_corpus.replace('!', '! ')
	t_corpus=t_corpus.replace('?', '? ')
	return t_corpus

def encodeToWindows(text):
	#print(b''+text+''.encode('cp1252'))
	bt=b""+text+"".encode('cp1252')
	return bt
	#return str(text)
	#return str(text, encoding='utf-8',errors="strict")
	if isinstance(text, str):
		# Text nach Unicode umwandeln
		s=text.encode()
		s_unicode = s.decode("cp852")
		# Text nach UTF-8 umwandeln
		s_utf8 = s_unicode.encode("utf-8")
		s_unicode1 = s.decode("utf-8")
		return s_unicode
		#encResults = text.encode('utf-8')
		#return str(encResults.decode('utf-8'))
	else:
		encResults = text.decode('utf-8')
		return str(encResults.encode('utf-8'))
	#encResults = text.encode('utf-8', "ignore")
	#return str(encResults.decode('latin-1', "ignore"))
	#return str(encResults.encode('cp1252', "remove"))
	
"""	
def encodeToWindows(text):
	if isinstance(text, str):
		encResults = text.encode('utf-8')
		return str(encResults.decode('cp1252'))
	else:
		encResults = text.decode('utf-8')
		return str(encResults.encode('cp1252'))
	#encResults = text.encode('utf-8', "ignore")
	#return str(encResults.decode('latin-1', "ignore"))
	#return str(encResults.encode('cp1252', "remove"))
"""

def encodeToLatin1(text):
	#n_String=replaceUmlauts(text)
	encResults = text.encode('utf-8', "ignore")
	#encResults = text.encode('utf-8', "ignore")
	return str(encResults.decode('latin-1', "ignore"))

def encodeToUTF8Adv(text):
	encResults = text.encode('utf-8', "ignore")
	#return str(encResults.decode('latin-1', "ignore"))
	return str(encResults.decode('utf-8', "remove"))

def encodeToUTF8(text):
	return text.encode('utf-8', "ignore")

def only_letters(string):
	return all((letter.isalpha() or letter.isspace()) for letter in string)
	prog = re.compile('\p{Cased_Letter}')
	result = prog.fullmatch(string)
	if result is not None:
		return True
	else:
		return False
	#return all((letter.isalpha() or letter.isspace()) for letter in string)

def getWikiPlainContent(w_List):
	# Wikipedia Result corpus
	corpus=""
	for t in w_List:
		if not isinstance(t, list):
			continue
		
		if len(t)<=5:
			continue
		
		tag = t[2]
		a 	= t[3]
		b 	= t[5]
		if b == "de" and a and tag in "alltext":
			corpus = corpus + a
	return corpus

def removeAfter(string):
	t_count = 0
	for t in string:
		#for suffix in [u"|", u"»", u">", u"<", u"[", u"]", u"{", u"}", u"(", u")", u"_"]:
		#if not t.isalnum() and not t.isspace() and t not in ['.','!','?','"',",",";","-"]:
		if t in [u"|", u"»", u">", u"<", u"[", u"]", u"{", u"}", u"(", u")", u"_"]:
			"""
			print("Text:", string)
			print("Match:", suffix)
			print("pos:", t_count)
			print("\tReturn:",string[:t_count])
			print("Text:", string)
			print("Ele:", t)
			print("Return:",string[:t_count].strip())
			"""
			return string[:t_count].strip()
		t_count = t_count + 1
	return string

def removeUrlFromString(text):
	if not isinstance(text, str):
		return False
	p=re.compile(r'http\S+', re.DOTALL)
	textv1=re.sub(p, '', text)
	p=re.compile(r'https\S+', re.DOTALL)
	textv2=re.sub(p, '', textv1)
	return textv2

def replaceSpecialChars(f_Text):
	#import modules.Sentify as sentify
	if not isinstance(f_Text, str):
		return False
	#print("replaceSpecialChars(): Length before:", len(f_Text))
	
	#printable = set(string.printable)
	#f_Text=list(filter(lambda x: x in printable, f_Text))
	#return "".join(f_Text)
	f_Text=f_Text.encode("utf-8")
	f_Text=f_Text.decode()
	f_Text=replaceUmlauts(f_Text)
	finalText=""
	for f in f_Text:
		f=re.sub("\\xf6", "oe",f) # ö
		f=re.sub("\\xfc", "ue",f) # ü
		f=re.sub("\\xe4", "ae",f) # ä
		f=re.sub("\\xdf", "sz",f) # ß
		f=re.sub(u"ö", "oe",f) # ö
		f=re.sub(u"ü", "ue",f) # ü
		f=re.sub(u"ä", "ae",f) # ä
		f=re.sub(u"ß", "sz",f) # ß
		f=f.replace(u'Ä',r'AE')
		f=f.replace(u'Ö',r'OE')
		f=f.replace(u'Ü',r'UE')
		f=f.replace(u'ß',r'sz')
		f=f.replace(u'ä',r'ae')
		f=f.replace(u'ü',r'ue')
		f=f.replace(u'ö',r'oe')
		finalText=finalText+f
	#print("replaceSpecialChars(END):", f_Text)
	f_Text=str(finalText)
	#print("replaceSpecialChars(): Length after:", len(f_Text))
	f_Text=unicodedata.normalize('NFKD', f_Text).encode('ASCII', 'ignore')
	return f_Text
	
	"""
	r_text=""
	for t in f_Text:
		#print(type(t))
		#print("t:", t)
		
		if ord(t) > 127:# makes sense here, because in replaceUmlauts() we replace german umlauts to ASCII
			t=""
		r_text=r_text+t
	#muss hier raus: r_text = re.sub('\s+',' ', r_text).strip()
	return r_text
	"""
	"""
	for p in text:
		# count all not alpha numeric, non-space and non sentence delimiter
		#if not p.isalnum() and not p.isspace() and not p in [',','\\','.','!','?','"','-','\'']:
		#if not p.isalnum() and not p.isspace() and not p in ['.','!','?','"']:
		if not p.isalnum() and not p.isspace() and not sentify.is_ascii(p):
			# eventuell hier: p.decode() einsetzen
			text = text[:cur_pos] + "" + text[cur_pos + 1:]
		else:
			# everything good here
			text = text[:cur_pos] + p + text[cur_pos + 1:]
		cur_pos = cur_pos + 1
	
	text = re.sub('\s+',' ', text).strip()
	text = re.sub(' +',' ', text).strip()
	"""
	return text

#d = findIT(verb_lemmatized_org, verb_alt)
def findVerbTense(verb_lemma, verb_tense):
	# pd.conjugate(verb_neu, tense, person, singular, mood=stimmung)
	resList = []
	pers = [1,2,3]
	numb = [pd.SG, pd.PL]
	mood = [pd.INDICATIVE,pd.IMPERATIVE,pd.SUBJUNCTIVE]
	tens = [pd.PRESENT,pd.PAST]
	
	for t in tens:
		# tense -> präsenz oder past
		for m in mood:
		# Stimmung:
			for n in numb:
			#	# anzahl
				for p in pers:
					# personen
					#print(conjugate(verb_lema, t, p, n, mood=m))
					c = pd.conjugate(verb_lemma, t, p, n, mood=m)
					#print(c, " -> tense:", t, " person:", p, " mehrzahl:", n, " stimmung:", m)
					#print(c, " -> tense:", t, " person:", p, " mehrzahl:", n, " findmatchverb:", f_findVerb)
					#print(c == f_findVerb)
					if c is not None and c == verb_tense:
						resList.append([c, t, p, n, m])
	return resList

def conjugateVerb(verb_tense, verb_neu):
	if not isinstance(verb_tense, str):
		return False
	if not isinstance(verb_neu, str):
		return False
	
	import modules.Speechify as speechify
	
	verb_lemma=speechify.spacyLemmatizer(verb_tense)
	d=findVerbTense(verb_lemma, verb_tense)
	vn=verb_lemma
	
	for ele in d:
		#for pele in ele:
		tense = ele[1]
		person = ele[2]
		singular = ele[3]
		stimmung = ele[4]
		neu = pd.conjugate(verb_neu, tense, person, singular, mood=stimmung)
		#print("Algorithmisch berechnete Zielform des 'Zielverbs':", neu)
		#print("Zielsatz:", "Ich "+neu+" den Weg entlang.")
		vn=u""+neu+""
	return vn

def replaceSynonyms(text, tType, times):
	#debug=True
	if len(text)<2:
		if debug:
			return text+" (N.E.0)"
		return text
	if not isinstance(text, str):
		if debug:
			return text+" (N.E.0)"
		return text
	
	import modules.Speechify as speechify
	import modules.Sentify as sentify
	
	if tType == 0:
		listAllowed = listAllowedV
	elif tType == 1:
		listAllowed = listAllowedN
	elif tType == 3:
		listAllowed = listAllowedV + listAllowedN
		
		if debug:
			print("wordify.synonymReplace() tType Option THREE set!")
	
	r_Text		= ""
	pos_corpus 	= speechify.sentSegmenter(text, asString=True, posTags=True)
	#corpus 		= pos_corpus.split("::")
	corpus 		= pos_corpus.split(" ")
	for u in corpus:
		if not isinstance(u, str) or len(u)<3:
			continue
		
		a 		= u.split("::")
		w 		= a[0]
		pos_tag = a[1]
		
		x = re.search('\(.*?\)',w)
		if x is not None: # if we have something like "laufen (S.E.0)"
			r_Text = r_Text+" "+w
			continue
		
		#if not w.isalpha():
		#	r_Text = r_Text+" "+w
		#	continue
		
		#if sentify.isGoodSpecialCharsSimple(w, 1) and pos_tag in listAllowed:
		if pos_tag in listAllowed:
			#if debug:
			#	1#print("wordify.replaceSynonyms() - Current Word:",w)
			#	#print("wordify.replaceSynonyms() - Current times:",times)
			
			new_word = ""
			my_w 	= w
			
			if tType == 0 or (tType == 3 and pos_tag in listAllowedV): #VERB #VERB and NOUN
				my_w = speechify.spacyLemmatizer(w)
			
			#t_nw = getSynLeipzig(my_w)
			t_sn=synonymOpentheasaurus(my_w)
			t_nw=synonymWikimedia(my_w)
			
			#print("wordify.w:", w)
			#print("wordify.my_w:", my_w)
			#print("wordify.t_sn:", t_sn)
			#print("wordify.t_nw:", t_nw)
			
			if ((t_nw is not False and t_nw is not None) or (t_sn is not False and t_sn is not None)) and times >= 1:
				new_List = []
				if t_nw is not False and t_nw is not None:
					new_List = new_List + t_nw
				if t_sn is not False and t_sn is not None:
					new_List = new_List + t_sn
				if len(new_List)>=1:
					while w in new_List: new_List.remove(w) 		# remove original Word from new_List
					while my_w in new_List: new_List.remove(my_w) 	# remove original Word from new_List
					new_word=w
					###new_word = random.choice(new_List)
					new_List.reverse()
					if len(new_List)>=1:
						new_word=new_List.pop()
					o=new_word
					if tType == 0 or (tType == 3 and pos_tag in listAllowedV): #VERB and NOUN #VERB
						o = conjugateVerb(w, new_word)
					
					if debug:
						print("wordify.tType:", tType)
						print("wordify.Synonym Results:", len(new_List))
						print("wordify.Orginal Word:", w)
						print("wordify.Exchange Word:", o)
						print()
					
					if True:
						w = o+' (S.E.'+str(tType)+')'
					else:
						w = o
					times = times - 1
		r_Text = r_Text+" "+w
	
	#	return encodeToUTF8Adv(r_Text)
	#	r_Text=wordify.replaceSpecialChars(r_Text)
	#return encodeToLatin1(r_Text)
	return r_Text

def replaceSynonymsSimple(corpus, tType): # 1 Wort, 1 Type
	import modules.Speechify as speechify
	#debug=True
	if len(corpus)<2:
		return corpus+"(NE0)"
	if not isinstance(corpus, str):
		return corpus+"(NE0)"
	
	y = re.search('\(.*?\)',corpus)
	if y is not None:
		return corpus+"(NE0)"
	
	if tType == 0:
		listAllowed = listAllowedV
		m_Type="(SE1)"
	elif tType == 1:
		listAllowed = listAllowedN
		m_Type="(SE2)"
	elif tType == 3:
		listAllowed = listAllowedV + listAllowedN
		m_Type="(SE2)"
	
	r_Text=""
	my_w=corpus
	w=corpus
	
	#if tType == 0 or (tType == 3 and pos_tag in listAllowedV): #VERB #VERB and NOUN
	if tType == 0 or (tType == 3 and corpus.islower()): #VERB and NOUN
		my_w = speechify.spacyLemmatizer(w)
		m_Type="(SE1)"
	
	#t_nw = getSynLeipzig(my_w)
	t_sn=synonymOpentheasaurus(my_w)
	t_nw=synonymWikimedia(my_w)
	
	#print("wordify.w:", w)
	#print("wordify.my_w:", my_w)
	#print("wordify.t_sn:", t_sn)
	#print("wordify.t_nw:", t_nw)
	
	if ((t_nw is not False and t_nw is not None) or (t_sn is not False and t_sn is not None)):
		new_List = []
		if t_nw is not False and t_nw is not None:
			new_List = new_List + t_nw
		if t_sn is not False and t_sn is not None:
			new_List = new_List + t_sn
		if len(new_List)>=1:
			while w in new_List: new_List.remove(w) 		# remove original Word from new_List
			while my_w in new_List: new_List.remove(my_w) 	# remove original Word from new_List
			new_word=w
			###new_word = random.choice(new_List)
			new_List.reverse()
			if len(new_List)>=1:
				new_word=new_List.pop()
			o=new_word
			if tType == 0 or (tType == 3 and corpus.islower()): #VERB and NOUN #VERB
				o = conjugateVerb(w, new_word)
				m_Type="(SE1)"
			
			if debug:
				print("wordify.tType:", tType)
				print("wordify.Synonym Results:", len(new_List))
				print("wordify.Orginal Word:", w)
				print("wordify.Exchange Word:", o)
				print()
			
			w = o+m_Type
	r_Text = w
	return r_Text

def getWikiExternalLinks(html_content):
	ExternalWikiLinks	= []
	soup1 		= BeautifulSoup(html_content, "html5lib")
	comments 	= soup1.findAll(text=lambda text:isinstance(text, Comment)) # remove comments
	[comment.extract() for comment in comments]
	for script in soup1(["script", "style", 'footer', 'head']):
		script.extract()# rip it out
	soup1.prettify()
	for b in soup1.find_all("a", class_="external free"):	#Wikipedia Specific HTML to external Links
		#print("External Wiki:", b["href"])
		ExternalWikiLinks.append(b["href"])
	return ExternalWikiLinks

def getWikiPediaTextSummary(w_list, MainKeyword, SubKeywords):
	#import modules.Sentify as sentify
	#import modules.Speechify as speechify
	
	sumText = ""
	for t in w_list[0]:
		if not isinstance(t, list):
			continue
		
		if len(t)<=5:
			continue
		
		tag 	= t[2]
		corpus 	= t[3]
		b 		= t[5]
		if b == "de" and corpus and tag in "p":
			#corpus = corpus.translate(None, "(){}<>")
			corpus = re.sub("\[\d\]","", corpus)
			#print("getWikiPediaTextSummary(): ",corpus)
			"""
			#sText = speechify.sentSegmenter(corpus, asString=False, posTags=False)
			if len(sText) >= 5:
				1#sumText = sText[0]+"#"+sText[1]+"#"+sText[2]+"#"+sText[3]+"#"+sText[4]
			else:
				1#sumText=" ".join(sText)
			"""
			return corpus
			#sumText = sentify.summarizeText(corpus, MainKeyword, SubKeywords, 3, asString=True)
	return ""

def getWikiPediaSummary(keyword):
	import modules.Fileify as fileify
	
	if not isinstance(keyword, str):
		return False
	
	#https://github.com/goldsmith/Wikipedia
	
	# keyword definieren
	# getWebpage()
	#https://de.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search=nintendo+switch&namespace=0&limit=10&suggest=true
	#https://de.wikipedia.org/w/api.php?action=opensearch&format=xml&search=nintendo&namespace=0&limit=10&suggest=true
	if debug:
		print("sentify.Sentify->getWikiPediaSummary() - Make WikiSearch Call: ", keyword)
	
	r_List		= []
	u_List		= []
	ExternalWikiLinks= []
	wikiRsltUrl = ""
	wikiPage 	= "https://de.wikipedia.org/w/api.php?action=opensearch&format=xml&search="+keyword+"&namespace=0&limit=10&suggest=true"
	htmlContent = fileify.getWebpagesSimple(wikiPage, "/tmp/", ret=True)
	soup 		= BeautifulSoup(htmlContent, 'xml')
	allUrls		= soup.find_all('Url')
	for a in allUrls:
		t = a.text
		u_List.append(t)
	#print(u_List)
	
	if u_List and len(u_List) >= 1:
		shortid 			= fileify.createShortid()
		wikiRsltUrl 		= u_List[0]
		#print("Url:", wikiRsltUrl)
		htmlRsltCont 		= fileify.getWebpagesSimple(wikiRsltUrl,"/tmp/", ret=True)
		#print("content:", encodeToLatin1(htmlRsltCont))
		r_List 				= fileify.extractFromHTML(htmlRsltCont, shortid, "/tmp/", nocheck=True)
		eLinks 				= getWikiExternalLinks(htmlRsltCont)
		ExternalWikiLinks.extend(eLinks)
		#print("Wikipedia:", r_List)
	"""
	if u_List and len(u_List) >= 6:
		for a in range(0,5):
		#for a in [0,1,2,3,4,5]:
			shortid 		= fileify.createShortid()
			wikiRsltUrl 	= u_List[a]
			htmlRsltCont 	= fileify.getWebpagesSimple(wikiRsltUrl, "/tmp/", ret=True)
			w 				= fileify.extractFromHTML(htmlRsltCont, shortid, "/tmp/", nocheck=True)
			eLinks 			= getWikiExternalLinks(htmlRsltCont)
			ExternalWikiLinks.extend(eLinks)
			#print(w)
			r_List.extend(w)
	elif u_List and len(u_List) >= 3:
		for a in range(0,2):
		#for a in [0,1,2]:
			shortid 		= fileify.createShortid()
			wikiRsltUrl 	= u_List[a]
			htmlRsltCont 	= fileify.getWebpagesSimple(wikiRsltUrl, "/tmp/", ret=True)
			w 				= fileify.extractFromHTML(htmlRsltCont, shortid, "/tmp/", nocheck=True)
			eLinks 			= getWikiExternalLinks(htmlRsltCont)
			ExternalWikiLinks.extend(eLinks)
			r_List.extend(w)
	elif u_List and len(u_List) >= 1:
		shortid 			= fileify.createShortid()
		wikiRsltUrl 		= u_List[0]
		#print("Url:", wikiRsltUrl)
		htmlRsltCont 		= fileify.getWebpagesSimple(wikiRsltUrl,"/tmp/", ret=True)
		#print("content:", encodeToLatin1(htmlRsltCont))
		r_List 				= fileify.extractFromHTML(htmlRsltCont, shortid, "/tmp/", nocheck=True)
		eLinks 				= getWikiExternalLinks(htmlRsltCont)
		ExternalWikiLinks.extend(eLinks)
		#print("Wikipedia:", r_List)
	"""
	
	if debug:
		print("wordify.getWikiPediaSummary() - WikiSearch Results: ", len(r_List))
	return ([r_List, ExternalWikiLinks])

def youtubeVideoSearch(searchquery, language):
	import modules.Speechify as speechify
	import modules.Sentify as sentify
	
	if not isinstance(searchquery, str):
		return False
	
	YOUTUBE_MAX_RESULTS			= 50 # 50 is max 
	YOUTUBE_API_SERVICE_NAME	= "youtube"
	YOUTUBE_API_VERSION 		= "v3"
	youtube 					= build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

	videos=[]
	finVideos=[]
	
	# Call the search.list method to retrieve results matching the specified
	# query term.
	try:
		search_response = youtube.search().list(
			q=searchquery+" "+language,
			part="id,snippet",
			regionCode="DE",
			maxResults=YOUTUBE_MAX_RESULTS
		).execute()
	except HttpError as e:
		print("An HTTP error %d occurred:\n%s" ,e.resp.status, e.content)
	else:
	
		#https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id=YTo_R_2Uo_E&key=AIzaSyDvkxDa_2pC60rM3PgSt8YAIa4MbUcu8HY
		# Add each result to the appropriate list, and then display the lists of
		# matching videos, channels, and playlists.
		for search_result in search_response.get("items", []):
			#print(search_result)
			#exit(1)
			if search_result["id"]["kind"] == "youtube#video":
				encVideoTitle = encodeToLatin1(search_result["snippet"]["title"])
				searchVideoID = search_result["id"]["videoId"]
				video_response = youtube.videos().list(
					id=searchVideoID,
					part='snippet, contentDetails'
				).execute()
				for video_result in video_response.get("items", []):
					videoDesc 	= encodeToLatin1(video_result["snippet"]["description"])
					videoTitle 	= encodeToLatin1(video_result["snippet"]["title"])
					#print("Title:", videoTitle)
					#print("Desc:", videoDesc)
					videos.append([videoTitle, videoDesc])
				#videos.append("%s (%s)" % (encVideoTitle, ))
		
		for v in videos:
			title=v[0]	# todo -> title müssen auch noch bearbeitet werden
			desc=v[1]
			title=removeAfter(title)
			#t_checking=speechify.sentSegmenter(desc, asString=False, posTags=False)
			t_checking=speechify.sentSegmenterSimple(desc, asString=False)
			r_String=""
			for b in t_checking:
				#if sentify.isNotBlacklisted(t) and sentify.isLongEnoughSentence(t, dynamic=True) and sentify.isSentenceStructure(t) and sentify.isNotDublicateString(t) and sentify.isGoodSpecialCharsSimple(t) and sentify.isGoodSentenceStart(t):
				#if sentify.isGoodSentence(b):
				if sentify.isNotBlacklisted(b) and sentify.isLongEnoughSentence(b) and sentify.isNotDublicateString(b) and sentify.isGoodSpecialCharsSimple(b) and sentify.isSentenceStructureAdvanced(b):
					r_String=r_String+b
			
			# nur deutschen Kontent zuerst
			#if intDetectLanguage(title) == "de" and intDetectLanguage(r_String) == "de" and len(r_String) >= 140:
			if intDetectLanguage(title) == "de" and intDetectLanguage(r_String) == "de":
				finVideos.extend([title, r_String])
	return finVideos

def calcSentiment(text):
	if not isinstance(text, str):
		return False
	
	blob = TextBlobDE(text)
	senti = blob.sentiment
	return senti[0]
	
def isGoodText(text, kw):
	if not isinstance(text, str):
		return False
	
	t_text 	= text.lower()
	t_kw	= kw.lower()
	
	if t_kw in t_text:
		return True
	elif t_text.find(t_kw) != -1:
		return True
	
	return False

def detectLanguage(text):
	if not isinstance(text, str):
		return False
	
	#text 	= unidecode(text)
	text 	= unidecode(text)
	t_tmp 	= text.split(" ")
	#print("detectLanguage(text):", text)
	if text is not None and len(t_tmp) >=7 and len(text) > 55:
		LANGUAGE = "german"
		sVar = ""
		try:
			sVar = detect(text)
		except:
			1
		
		if sVar in "de":
			LANGUAGE = "german"
		elif sVar in "en":
			LANGUAGE = "english"
		return LANGUAGE
	return "german"

def intDetectLanguage(text):
	if not isinstance(text, str):
		return False
	
	#text = unidecode(text)
	if text is not None:
		try:
			sval = detect(text)
			return sval
		except:
			1
	return "de"

def beautifySynList(t_List):
	c=len(t_List)
	topList=[]
	if c >= 6:
		topList=t_List[:5]
	elif c >= 4:
		topList=t_List[:3]
	elif c >= 2:
		topList=t_List[:1]
	else:
		return t_List
	return topList

def synonymOpentheasaurus(word):
	import modules.Fileify as fileify
	
	if not isinstance(word, str):
		return []
	if len(word)<MinSynExchangeWordLength:
		return []
	
	cache = "/home/buz/buzzgreator/synonyms/theasaurus-"+word
	if os.path.isfile(cache):
		return fileify.binaryRead(cache)
	
	if debug:
		print("wordify.synonymOpentheasaurus(word): ", word)
	"""
	nimm erstes Synonym vom Webcall
	wenn erstes_Syn nicht gleich (word):
		return erstes_Syn
	else:
		return zweites_Syn
	
	"""
	# aktuell wird nur Synonym unterstützt
	url		= "https://www.openthesaurus.de/synonyme/search?format=application/json&q="+word
	headers = {"content-type": "application/json"}
	try:
		r1 = requests.post(url,timeout=30,headers=headers)
		r1.encoding 	= 'utf-8'
		content_txpe 	= r1.headers.get('content-type')
	except Exception as exp:
		if debug:
			print("wordify.synonymOpentheasaurus(word): Failure on WebCall")
	
	else:
		if r1.status_code != 200 or content_txpe is None or content_txpe.find('json') == -1:
			return []
		
		listSynonyms 	= []
		str_response = r1.content.decode('latin-1', "ignore")
		#str_response = response.content.encode('utf-8', "ignore")
		#str_response = str(str_response.decode('latin-1', "ignore"))
		obj = json.loads(str_response)
		#pp.pprint(obj)
		#pretty(obj, indent=9)
		for key1, value1 in obj.items():
			for key2 in value1:
				if not isinstance(key2,str):
					for key3, value3 in key2.items():
						if key3 in "terms":
							for key4 in value3:
								badFlag = False
								try:
									if key4['level']:
										#print("Umgangssprache entdeckt")
										badFlag = True
								except Exception as er:
									1
								
								####els = list(key4.items())
								#print("key4:", key4)
								#print("value3:", value3)
								#print("els:", els)
								#print("elscount:", len(els))
								####isLevel = str(key4)
								####e = str(els[-1])
								####k = str(e[0])
								#isUmgangssprachlich = str(key4)
								#print("Level", isLevel)
								for key5, value5 in key4.items():
									#print("k:","-",k,"->",e)
									#if isLevel in "umgangssprachlich" or isLevel in "level":
									#	#badFlag = True
									#	continue
									#print("key5:", key5)
									#print("value4:", value5)
									#print("key:", key5)
									#print("value:", value5)
									#firstval = ""
									#if (len(value5)>=1):
									#	firstval = value5[0]
									#if "." not in value5 and "level" not in k and firstval.isupper():
									#if "." not in value5 and len(els) < 2 and firstval.isupper():
									if "." not in value5 and value5 not in listSynonyms and value5.lower() != word.lower() and badFlag is False:
										if debug:
											print("wordify.synonymOpentheasaurus() - Pre Filter check:", value5)
										if only_letters(value5):
											if debug:
												print("wordify.synonymOpentheasaurus() - Success Filter check:", value5)
											v = u""+value5+""
											listSynonyms.append(v)
											#print("save firstval:", firstval)
											#print("save value:", value5)
	
		if (len(listSynonyms)>=1):
			fileify.binaryWrite(listSynonyms, cache)
			return beautifySynList(listSynonyms)
		else:
			return []

def googleTranslate(text, toLang):
	###https://github.com/opennmt/opennmt
	if not isinstance(text, str):
		return False
	
	try:
		# https://cloud.google.com/translate/docs/languages
		translate_client 	= translate.Client()
		result 				= translate_client.translate(text, target_language=toLang)
		if debug:
			print(u'Text: {}'.format(result['input']))
			print(u'Translation: {}'.format(result['translatedText']))
			print(u'Detected source language: {}'.format(
			result['detectedSourceLanguage']))
			print(u'Needed Target language: {}'.format(toLang))
			print()
		
		#if result['translatedText'].find("unknown") != -1:
		if result['translatedText'] != text:
			#print("return:", encodeToLatin1(result['translatedText']) )
			#return encodeToLatin1(result['translatedText'])
			#return result['translatedText'].encode('utf-8').decode()
			return str(result['translatedText'])
		else:
			return False
			replaceText = replaceSynonyms(text, 3, 1)
			if text != replaceText:
				return str(replaceText)
			else:
				return False
		
		
		#return result['translatedText'].encode('utf-8')
		#pp.pprint(translation)
		#print("Zielsprache: " +lang[lang_from_ip.upper()]),
		#print()
		#print('Werbetext:   {}'.format(markov_sample))
		#print()
		#print('Translation: {}'.format(translation['translatedText'].encode('utf-8')))
		#print('Uebersetzung: {}'.format(remove_non_ascii(translation['translatedText'])))
		#print()
		#vartmp = input("\t #### Enter fuer naechste Texterstellung! ####")
	except Exception as strerror:
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	return False

	
def synonymWikimedia(word):
	import modules.Fileify as fileify
	
	if not isinstance(word, str):
		return []
	if len(word)<MinSynExchangeWordLength:
		return []
	
	cache = "/home/buz/buzzgreator/synonyms/wiki-"+word
	if os.path.isfile(cache):
		return fileify.binaryRead(cache)
	
	if debug:
		print("wordify.synonymWikimedia(word) - Make WikiMedia Synonym Search Call: ", word)
	
	finalList	= []
	r_List		= []
	u_List		= []
	ExternalWikiLinks= []
	wikiRsltUrl = ""
	wikiPage 	= "https://de.wiktionary.org/w/api.php?action=opensearch&format=json&formatversion=2&namespace=0&limit=10&suggest=true&search="+word
	
	htmlContent = fileify.getWebpagesSimple(wikiPage, "/tmp/", ret=True)
	splitter=htmlContent.split('"')
	for link in splitter:
		l = link.lower()
		if l.startswith("https://"):
			#print("LKink:",link)
			u_List.append(link)
	
	if u_List and len(u_List) >= 1: 
		shortid 		= fileify.createShortid()
		wikiRsltUrl 	= u_List[0]
		#print("Loading Url:", wikiRsltUrl)
		htmlRsltCont 	= fileify.getWebpagesSimple(wikiRsltUrl, "/tmp/", ret=True)
		html_contentv1 	= encodeToLatin1(htmlRsltCont)
		soup1 			= BeautifulSoup(html_contentv1, "html5lib")
		comments 		= soup1.findAll(text=lambda text:isinstance(text, Comment)) # remove comments
		[comment.extract() for comment in comments]
		for script in soup1(["script", "style", 'footer', 'head']):
			script.extract()# rip it out
		soup1.prettify()
		for b in soup1.find_all("p"):
			if not len(b.attrs) == 2:
				continue
			c=b.attrs
			for tag in c.keys():
				t_tag = tag
				t_title = c[tag]
				if t_tag.find("title") != - 1 and t_title.find("bedeutungsgleich gebrauchte W") != -1:
					p=b.find_next("dl")
					a=p.find_all("a")
					for ele in a:
						#print("ele:", ele)
						m = re.search(u"Seite nicht vorhanden",str(ele))
						if debug:
							print("wordify.synonymWikimedia() - Pre Filter check:", ele.text)
						if m is None and only_letters(ele.text):
							finalList.append(ele.text.strip())
							if debug:
								print("wordify.synonymWikimedia() - Success Filter check:", ele.text)
							#print("a:", ele.text.strip())
		fileify.binaryWrite(finalList, cache)
		return finalList
	return []

def rawUniLeipzigWebcall(word):
	# http://api.corpora.uni-leipzig.de/ws/swagger-ui.html#!/available-corpora-service/getAvailableCorporaUsingGET
	
	# get new Synonyms: http://api.corpora.uni-leipzig.de/ws/swagger-ui.html#!/similarity-service/getCoocSimilarWordsUsingGET_1
	
	if not isinstance(word, str):
		return False
	
	# aktuell wird nur Synonym unterstützt
	url		="http://anonymous:anonymous@pcai055.informatik.uni-leipzig.de:8100/axis/services/Synonyms?wsdl"
	
	headers = {"content-type": "text/xml", "SOAPAction": "executeRequest"}
	body 	= """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dat="http://datatypes.webservice.wortschatz.uni_leipzig.de" xmlns:urn="http://wortschatz.uni-leipzig.de/axis/services/Thesaurus" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <urn:execute>
            <urn:objRequestParameters>
                <urn:parameters>
                    <urn:dataVectors>
                        <dat:dataRow>Wort</dat:dataRow>
                        <dat:dataRow>"""+word+"""</dat:dataRow>
                    </urn:dataVectors>
                    <urn:dataVectors>
                        <dat:dataRow>Limit</dat:dataRow>
                        <dat:dataRow>30</dat:dataRow>
                    </urn:dataVectors>
                </urn:parameters>
                <urn:corpus>de</urn:corpus>
            </urn:objRequestParameters>
        </urn:execute>
    </env:Body>
</env:Envelope>"""
	
	r1flag = False
	try:
		response = requests.post(url,data=body,timeout=5,headers=headers,auth=HTTPBasicAuth('anonymous', 'anonymous'))
		response.encoding = 'utf-8'
		r1flag = True
	except:
		1
	
	t_parse 		= html.parser.HTMLParser()
	listSynonyms 	= []
	setSynonyms 	= set()
	#import chardet
	#print(chardet.detect(response.content))
	
	if r1flag is True:
		for ele in re.findall(b'dataRow>(.*?)</ns', response.content):
			t_ele 		= ele.decode("ascii") 
			t_ele		= html.unescape(t_ele).encode('utf-8', "ignore")
			t_ele		= str(t_ele.decode('latin-1', "ignore"))
			#t_ele 		= str(t_ele).encode('latin-1', "ignore")
			#t_ele 		= ele.encode('ascii', "ignore")
			#t_ele 		= str(ele.decode('latin-1', "ignore"))

			#t_ele 		= ele.encode('utf-8', "ignore")
			#t_ele 		= ele.decode('utf-8', "ignore")
			##t_ele 		= t_ele.encode('latin-1', "ignore")
			#t_ele = ele.decode("latin-1")
			#t_ele = t_parse.unescape(t_ele)
			if b"dataRow" not in ele and len(ele)>=1:
				v = u""+t_ele+""
				setSynonyms.add(v)
	
	return list(setSynonyms)

def WortschatzServiceMonitor():
	url = 'http://anonymous:anonymous@pcai055.informatik.uni-leipzig.de:8100/axis/services/ServiceOverview?wsdl';
	
	r1flag = False
	try:
		r1 			= requests.get(url, headers=Headers, timeout=5)
		r1.encoding = 'utf-8'
		r1flag 		= True
	except:
		1
	
	if r1flag and r1.status_code == 200:
		#print("WortschatzServiceMonitor(): Success")
		return True
	else:
		#print("WortschatzServiceMonitor(): Failure")
		return False

def getSynLeipzig(word):
	
	#debug
	return False
	
	
	if not isinstance(word, str):
		return False
	
	if debug:
		print("wordify.getSynLeipzig(word): ", word)
		
	#print ("Auto Syn - Leipzig: ", libleipzig.Thesaurus("Auto",10))
	retContent 		= []
	retSaveMysql 	= dict()
	
	if len(word) < 1:
		return False

	for i in range(1, 5):
		if WortschatzServiceMonitor():
			synLeipzig = rawUniLeipzigWebcall(word)
			if len(synLeipzig) >= 1:
				return beautifySynList(synLeipzig)
			else:
				return False
		else:
			print(datetime.datetime.now(), " -> Uni Leipzig Webservice Down")
			time.sleep(5)

	return False

def pretty(d, indent=4):
	for key, value in d.items():
		print('\t' * indent + str(key))
		if isinstance(value, dict):
			pretty(value, indent+1)
		else:
			print ('\t' * (indent+1) + str(value))

	return True

"""
def getSynLeipzig(word):

    #print ("Auto Syn - Leipzig: ", libleipzig.Thesaurus("Auto",10))
    retContent 		= []
    retSaveMysql 	= dict()
	
    if len(word) < 1:
        return False
	
    for i in range(1, 25):
        if WortschatzServiceMonitor():
            try:
                #synLeipzig = libleipzig.Thesaurus(sl, 150)
                synLeipzig = rawUniLeipzigWebcall(word)
                print(synLeipzig)
                exit(1)
            except:
                print("Synonym Leipzig > is down")
        else:
            time.sleep(1)
	
    return retContent
"""