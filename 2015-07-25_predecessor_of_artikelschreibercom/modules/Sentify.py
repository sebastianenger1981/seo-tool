# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore

import os, sys, logging, re, time, random
import time
import string
from alphabet_detector import AlphabetDetector
from num2words import num2words		# pip install num2words
from langdetect import detect	# pip3 install --upgrade langdetect
from bs4 import BeautifulSoup, Comment 	# pip3 install --upgrade beautifulsoup4 && pip install html5li
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer #as Summarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer #as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from textstat.textstat import textstat

import modules.Speechify as speechify
import modules.Wordify as wordify
#import modules.CosineSimilarity as cosine
#import modules.Gensim as gSim
#import modules.Servify as servify
import modules.Fileify as fileify
import modules.TextGenify as genify

from pprint import PrettyPrinter

ad 						= AlphabetDetector()
pp 						= PrettyPrinter(indent=4)
debug					= False
isGoodSpecialCharsMax 	= int(3)

os.system("export GOOGLE_APPLICATION_CREDENTIALS='/home/buz/buzzgreator/key/100BiereTranslate-8a809e939d5e.json'")

nlp_allowed 	= [u"NN",u"NNP",u"NNPS",u"PROPN",u"NOUN",u"NE", u"NNE"]
verb_allowed 	= [u"VMFIN", u"VMINF", u"VMPP", u"VVFIN", u"VVIMP", u"VVINF", u"VVIZU", u"VVPP", u"VERB"]

string_blocker 	= fileify.plainRead("/home/buz/buzzgreator/modules/blacklists/string_blocker.txt")
domain_blocker 	= fileify.plainRead("/home/buz/buzzgreator/modules/blacklists/domain_blocker.txt")
#fileify.plainRead(headl_corp, "/home/buz/buzzgreator/headl_corp.txt.bin")

p1=re.compile("https", re.IGNORECASE)
p2=re.compile("http", re.IGNORECASE)
p3=re.compile("ftp", re.IGNORECASE)
p4=re.compile("mailto", re.IGNORECASE)
p5=re.compile("www\.", re.IGNORECASE)
p6=re.compile("mail\.", re.IGNORECASE)
p7=re.compile("\.de", re.IGNORECASE)
p8=re.compile("\.net", re.IGNORECASE)
p9=re.compile("\.org", re.IGNORECASE)
p10=re.compile("\.com", re.IGNORECASE)
p11=re.compile("\.biz", re.IGNORECASE)
p12=re.compile("\.info", re.IGNORECASE)
p13=re.compile("(\w{1,})@(\w{1,})", re.IGNORECASE)

r_RegexList=[]
r_RegexList.append(p1)
r_RegexList.append(p2)
r_RegexList.append(p3)
r_RegexList.append(p4)
r_RegexList.append(p5)
r_RegexList.append(p6)
r_RegexList.append(p7)
r_RegexList.append(p8)
r_RegexList.append(p9)
r_RegexList.append(p10)
r_RegexList.append(p11)
r_RegexList.append(p12)
r_RegexList.append(p13)

# todo: String Whitelisting

def startswithNoun(sentence):
	if not isinstance(sentence, str):
		return False
	
	t_List 	= speechify.posTagging(sentence, asString=False)
	a 		= t_List[0].split("::")
	word 	= a[0]
	posTag 	= a[1]
	if posTag.upper() in nlp_allowed:
		return True
	return False

def endswithNoun(sentence):
	if not isinstance(sentence, str):
		return False
	
	t_List = speechify.posTagging(sentence, asString=False)
	a 		= t_List[-1].split("::") # eventuell das letzte Wort nehmen, statt das letzte Zeichen
	word 	= a[0]
	posTag 	= a[1]
	if posTag.upper() in nlp_allowed:
		return True
	return False

def isGoodSentenceStart(text):
	# Satz muss mit Grossbuchstaben oder mit einer Zahl beginnen
	t_Text 		= text[:1]
	#t_TextBig 	= text[:1].upper()
	if t_Text.isdigit() or t_Text.isalnum():# and t_Text == t_TextBig:
		return True
	return False

def isNotDublicateString(text):
	t_Text 			= text.lower()
	#debug 			= True
	patternElement 	= ""
	n				= 16# neun zeichen müssen gleich sein
       
	if len(t_Text) >= n+3:
		patternElement = t_Text[:n]
		patternElement = patternElement.strip()
		#print("PatternElement:", patternElement)
		r_Count = t_Text.count(patternElement)
		if r_Count > 1:
			if debug:
				print("sentify.isNotDublicateString(): -> multiplePattern Error:", r_Count, ",", patternElement)
			return False
	
	#satz = "Breath of the WildThe Legend of Zelda: Breath of the Wild auf der E3 angespielt."
	#['breath of th', 'e wildthe le', 'gend of zeld', 'a: breath of', ' the wild au', 'f der e3 ang', 'espielt.']
	t_List = [t_Text[i:i+n] for i in range(0, len(t_Text), n)]
	for t in t_List:
		t = t.strip()
		r_Count = t_Text.count(t)
		if r_Count > 1:
			if debug:
				print("sentify.isNotDublicateString(): -> multiplePattern Error:", r_Count, ",", t)
			return False
	
	return True

def beautifySentenceEnding(text):
	if not isinstance(text, str):
		return False
	
	allowedSentEndings = [u".", u"!", u"?"]
	e1 = text[-1:]
	
	if e1 in allowedSentEndings:
		return text
	
	if e1.isalnum() and not e1.isspace():
		return text + "."
	
	#if not e1.isalnum() and not e1.isspace() and e1 not in allowedSentEndings:
	if not e1.isalnum() and not e1.isspace():
		return text.replace(e1, '.')

	return text + "#"

"""
def correctLastCharOfSentence(text):
	if not isinstance(text, str):
		return False
	
	t_Text 		= re.sub( '\s+', ' ', text).strip()
	if t_Text.endswith('.'):
		return True
	elif t_Text.endswith('!'):
		return True
	elif t_Text.endswith('?'):
		return True
	else:
		return t_Text+"."
"""

def isReadability(text):
	if not isinstance(text, str):
		return float(0.1)
	if len(text)<=37:
		return float(0.1)
	if len(text.split())<=1:
		return float(0.1)
	
	#pip install textstat
	"""
	* 90-100 : Very Easy 
	* 80-89 : Easy 
	* 70-79 : Fairly Easy 
	* 60-69 : Standard 
	* 50-59 : Fairly Difficult 
	* 30-49 : Difficult 
	* 0-29 : Very Confusing
	"""
	try:
		v=textstat.flesch_reading_ease(text)
		return v
	except Exception as exp:
		1
	return float(0.1)

def isNotDomainBlacklisted(text):
	if not isinstance(text, str):
		return False
	
	if len(domain_blocker) > 3:
		t_List = domain_blocker.lower().split("\n")
		for ele in t_List:
			if len(ele) >= 2:
				ele		= ele.strip()
				if ele.startswith("#"):
					continue
				
				r_Count = text.count(ele)
				r_Find 	= text.find(ele)
				if r_Count > 1 or r_Find != -1:
					if debug:
						print("sentify.isNotDomainBlacklisted(): -> String Blacklist Error (Match Element):" + ele + " r_Count:" + str(r_Count) + " r_Find:"+str(r_Find))
					return False
				#my_regex = r"\b" + re.escape(ele) + r"\b"
				my_regex = r"\b" + ele + r"\b"
				if re.search(my_regex, text, flags=re.IGNORECASE) is not None:
					#print("regex blacklist match:",m)
					if debug:
						print("sentify.isNotDomainBlacklisted(): -> String Blacklist Error: - re.search - Match Element:", ele)
					return False
	return True

def isNotBlacklisted(text):
	if not isinstance(text, str):
		return False
	debug=True
	
	"""
	text=wordify.encodeToLatin1(text)
	text 		= text.lower()
	# filter -> 18.01.2017 um 09:29 oder January 22, 2017
	match0		= re.search('(\w{3,25})(\s+)(\d{1,2})(\s+)(\d{2,4})',text)
	match11		= re.search('(\d{2,4})[/.-](\d{1,2})[/.-](\d{1,2})',text)
	match12		= re.search('(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})',text)
	match2		= re.search('(\d{1,2})[:](\d{1,2})', text)
	#encoding 	= chardet.detect(text)
	
	if match12 is not None or match2 is not None: # was :"and"
		if debug:
			print("sentify.isNotBlacklisted(): -> String Blacklist Error (Match Element) match12 or match2:", text)
		return False
	if match11 is not None or match0 is not None:
		if debug:
			print("sentify.isNotBlacklisted(): -> String Blacklist Error (Match Element) match11 or match0:", text)
		return False
	
	if match2 is not None:
		if debug:
			print("sentify.isNotBlacklisted(): -> String Blacklist Error (Match Element) match2:", text)
		return False
	"""
	
	#print("text:", ad.detect_alphabet(text), text)
	if len(string_blocker) > 3:
		t_List = string_blocker.lower().split("\n")
		for ele in t_List:
			if len(ele) >= 1:
				ele	= ele.strip()
				if ele.startswith("#"):
					continue
				
				goodFlag=""
				try:
					u=text.index(ele)
				except Exception as strerror:
					#print("Unexpected error:", sys.exc_info()[0])
					#print(strerror)
					#exc_type, exc_obj, exc_tb = sys.exc_info()
					#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					#print(exc_type, fname, exc_tb.tb_lineno)
					#print("NOT found")
					goodFlag=True
				else:
					#print("hit found")
					goodFlag=False
				
				r_Count = text.count(ele)
				r_Find 	= text.find(ele)
				if goodFlag is False or r_Count > 1 or r_Find != -1:
					if debug:
						print("sentify.isNotBlacklisted(): -> String Blacklist Error (Match Element): goodFlag " + ele + " r_Count:" + str(r_Count) + " r_Find:"+str(r_Find))
					return False
				
				if ele in text or text in ele:
					if debug:
						print("sentify.isNotBlacklisted(): -> String Blacklist Error (Match Element) ele in text" )
					return False
				
				my_regex = r"\b" + re.escape(ele) + r"\b"
				#my_regex = r"\b" + ele + r"\b"
				if re.search(my_regex, text, flags=re.IGNORECASE) is not None:
					#print("regex blacklist match:",m)
					if debug:
						print("sentify.isNotBlacklisted(): -> String Blacklist Error: - re.search - Match Element:", ele)
					return False
	
	return True

"""
Satzverfremdung
"""
def isGoodSummary(text):
	if not isinstance(text, str):
		return False
	
	#t_tmptext = wordify.encodeToLatin1(t_text)
	corpus = speechify.splitOnLowerUppercase(text)
	print("Text:\t\t", t_text)
	sumry = sentify.summarizeText(corpus, "55%")
	print("Summary:\n\t", sumry)
	#pp.pprint(sumry)
	resultSet1 = gSim.gensimDoc2Vec(t_text, MainKeyword)
	print("Similarity Score:\t")
	print(resultSet1[0])
	return True
	
def summarizeText(text, MainKeyword, SubKeywords, sentenceCount, asString=True):
	# sentence_new, MainKeyword, SubKeywords, sumTextSentenceCount, asString=True
	if not isinstance(text, str):
		return False
	
	sentenceCount=100000
	t_text		= wordify.encodeToUTF8Adv(text)
	lang		= wordify.detectLanguage(t_text)
	FullText	= []
	#S_COUNT		= 10000
	parser 		= PlaintextParser.from_string(t_text, Tokenizer('german'))
	#parser 		= PlaintextParser.from_string(t_text)
	stemmer 	= Stemmer('german')# Stemmer(lang)
	#summarizer 	= TextRankSummarizer(stemmer)
	summarizer 	= LsaSummarizer(stemmer)
	summarizer.stop_words = get_stop_words('german')
	summarizer.null_words = get_stop_words('german')
	summarizer.bonus_words = [MainKeyword,SubKeywords]
	summarizer.stigma_words = ["und", "der", "die", "das", "oder", "wie", "aber"]
	
	for sentence in summarizer(parser.document, sentenceCount):
		s_sent = str(sentence)
		#if isGoodSentence(s_sent) is False:
		#	continue
		#t_sent = wordify.encodeToLatin1(s_sent)
		FullText.append(s_sent)
	if asString:
		return "".join(FullText)
	else:
		return FullText

def find_last(lst, sought_elt):
    for r_idx, elt in enumerate(reversed(lst)):
        if elt.find(sought_elt) != -1:
            pos = len(lst) - 1 - r_idx
            return lst[pos]
    return False

def find_lastPos(lst, sought_elt):
    for r_idx, elt in enumerate(reversed(lst)):
        if elt.find(sought_elt) != -1:
            pos = len(lst) - 1 - r_idx
            return pos
    return False

def blockTranslateSimple(word):
	if not isinstance(word, str):
		return False
	
	langList   	=  {"en":u"englisch","it":u"italienisch","es":u"spanisch","fr":u"französich"}
	#sprache 	= "englisch"
	returnText 	= ""
	"""
	if pos in nlp_allowed:
		t_type="(NB1)"
	elif pos in verb_allowed:
		t_type="(VB1)"
	else:
	"""
	t_type="(AB1)"
	
	#lang=fileify.weighted_choice([("en",50),("fr",10), ("it",25), ("es",15)])
	lang=fileify.weighted_choice([("en",100)])
	if lang in langList: 
		sprache = langList[lang]
	
	#print("Found Word Orginal:", word)
	transWord 	= wordify.googleTranslate(word, toLang=lang)
	#print("Found Word Translated:", transWord)
	if transWord and (transWord.lower() != word.lower()):
		"""
			newWord = u'"'+transWord+'"'+u" ("+sprache+" fuer '"+word+"')"
		"""
		newWord = u'"'+transWord.strip()+'"'+u" ("+sprache+" fuer '"+word.strip()+"')"+t_type
		returnText=returnText+" "+newWord
		
		if debug:
			print("deutsch Wort:", word)
			print("transl Wort:", transWord)
			print("new Wort:", returnText)
	else:
		newWord=""
		sentWordv1 = wordify.replaceSynonymsSimple(word, 0) # "Modified (NOUN|VERB):"
		sentWordv2 = wordify.replaceSynonymsSimple(word, 1) # "Modified (NOUN|VERB):"
		sentWordv1 = sentWordv1.strip()
		sentWordv2 = sentWordv2.strip()
		if sentWordv1.lower() != word.lower():
			newWord = u'"'+sentWordv1.strip()+'"'+u" (deutsch fuer '"+word.strip()+"')"+"(VB1)"
		elif sentWordv2.lower() != word.lower():
			newWord = u'"'+sentWordv2.strip()+'"'+u" (deutsch fuer '"+word.strip()+"')"+"(NB1)"
		else:
			returnText=returnText+" "+word+"(NE0)"
		returnText=returnText+" "+newWord
	return returnText

def nounBlockTranslate(sentence):
	if not isinstance(sentence, str):
		return False
	
	#https://docs.python.org/2.4/lib/standard-encodings.html
	langList   	=  {"en":u"englisch","it":u"italienisch","es":u"spanisch","fr":u"französich"}
	#sprache 	= "englisch"
	sentList 	= speechify.posTagging(sentence, asString=False)
	returnText 	= ""
	hasBeenSeen = set()
	goodFlag	= True
	
	for s in sentList:
		t_List = s.split()
		sent = []
		for t in t_List:
			a = t.split("::")
			word = a[0]
			pos = a[1]
			
			y = re.search('\(.*?\)',word)
			if y is not None:
				continue
			
			if pos in nlp_allowed:
				t_type="(NB1)"
			elif pos in verb_allowed:
				t_type="(VB1)"
			
			#if isGoodSpecialCharsSimple(word, 1) and pos in nlp_allowed and goodFlag is True:
			#if ((pos in nlp_allowed) or (pos in verb_allowed)):
			if pos in nlp_allowed and goodFlag is True:
				goodFlag	= False
				#lang=fileify.weighted_choice([("en",50),("fr",10), ("it",25), ("es",15)])
				lang=fileify.weighted_choice([("en",100)])
				if lang in langList: 
					sprache = langList[lang]
				
				#word = speechify.removePosTagsFromString(noun, singleWord=True)
				#print("Found Word Orginal:", word)
				transWord 	= wordify.googleTranslate(word, toLang=lang)
				#print("Found Word Translated:", transWord)
				if transWord and (transWord.lower() != word.lower()):
					"""
						newWord = u'"'+transWord+'"'+u" ("+sprache+" fuer '"+word+"')"
					"""
					#sentWord = wordify.replaceSynonyms(word, 1, 1) # "Modified (NOUN):"
					#sentWord = sentWord.strip()
					#newWord = u'"'+transWord.title()+'"'+u" ("+sprache+" fuer '"+sentWord+" (N.E.1)')"
					newWord = u'"'+transWord.title().strip()+'"'+u" ("+sprache+" fuer '"+word.strip()+"')"+t_type
					#encResults = newWord.encode('iso8859-15', "ignore")
					#returnText=returnText+" "+str(encResults.decode('latin-1', "ignore"))
					returnText=returnText+" "+newWord
					
					if debug:
						print("deutsch Wort:", word)
						print("transl Wort:", transWord)
						print("new Wort:", returnText)
				else:
					sentWord = wordify.replaceSynonymsSimple(word, 1) # "Modified (NOUN|VERB):"
					sentWord = sentWord.strip()
					sentWord = wordify.replaceUmlauts(sentWord)
					#newWord = u'"'+transWord.title()+'"'+u" ("+sprache+" fuer '"+sentWord+" (N.E.1)')"
					newWord = u'"'+sentWord.title().strip()+'"'+u" (deutsch fuer '"+word.strip()+"')"+t_type
					#encResults = newWord.encode('utf-8', "ignore")
					#returnText=returnText+" "+str(encResults.decode('iso8859-15', "ignore"))
					#returnText=wordify.encodeToLatin1(returnText+" "+newWord)
					#print("new Wort:", returnText)
					returnText=returnText+" "+newWord
			else:
				returnText=returnText+" "+word
	return returnText

def verbBlockTranslate(sentence):
	if not isinstance(sentence, str):
		return False
	
	#https://docs.python.org/2.4/lib/standard-encodings.html
	langList   	=  {"en":u"englisch","it":u"italienisch","es":u"spanisch","fr":u"französich"}
	#sprache 	= "englisch"
	sentList 	= speechify.posTagging(sentence, asString=False)
	returnText 	= ""
	hasBeenSeen = set()
	goodFlag	= True
	
	for s in sentList:
		t_List = s.split()
		sent = []
		for t in t_List:
			a = t.split("::")
			word = a[0]
			pos = a[1]
			
			y = re.search('\(.*?\)',word)
			if y is not None:
				continue
			
			if pos in nlp_allowed:
				t_type="(NB1)"
			elif pos in verb_allowed:
				t_type="(VB1)"
			
			#if isGoodSpecialCharsSimple(word, 1) and pos in nlp_allowed and goodFlag is True:
			#if ((pos in nlp_allowed) or (pos in verb_allowed)):
			if pos in verb_allowed and goodFlag is True:
				goodFlag	= False
				#lang=fileify.weighted_choice([("en",50),("fr",10), ("it",25), ("es",15)])
				lang=fileify.weighted_choice([("en",100)])
				if lang in langList: 
					sprache = langList[lang]
				
				#word = speechify.removePosTagsFromString(noun, singleWord=True)
				#print("Found Word Orginal:", word)
				transWord 	= wordify.googleTranslate(word, toLang=lang)
				#print("Found Word Translated:", transWord)
				if transWord and (transWord.lower() != word.lower()):
					"""
						newWord = u'"'+transWord+'"'+u" ("+sprache+" fuer '"+word+"')"
					"""
					#sentWord = wordify.replaceSynonyms(word, 1, 1) # "Modified (NOUN):"
					#sentWord = sentWord.strip()
					#newWord = u'"'+transWord.title()+'"'+u" ("+sprache+" fuer '"+sentWord+" (N.E.1)')"
					newWord = u'"'+transWord.title().strip()+'"'+u" ("+sprache+" fuer '"+word.strip()+"')"+t_type
					#encResults = newWord.encode('iso8859-15', "ignore")
					#returnText=returnText+" "+str(encResults.decode('latin-1', "ignore"))
					returnText=returnText+" "+newWord
					
					if debug:
						print("deutsch Wort:", word)
						print("transl Wort:", transWord)
						print("new Wort:", returnText)
				else:
					sentWord = wordify.replaceSynonymsSimple(word, 0) # "Modified (NOUN|VERB):"
					sentWord = sentWord.strip()
					sentWord = wordify.replaceUmlauts(sentWord)
					#newWord = u'"'+transWord.title()+'"'+u" ("+sprache+" fuer '"+sentWord+" (N.E.1)')"
					newWord = u'"'+sentWord.title().strip()+'"'+u" (deutsch fuer '"+word.strip()+"')"+t_type
					#encResults = newWord.encode('utf-8', "ignore")
					#returnText=returnText+" "+str(encResults.decode('iso8859-15', "ignore"))
					#returnText=wordify.encodeToLatin1(returnText+" "+newWord)
					#print("new Wort:", returnText)
					returnText=returnText+" "+newWord
			else:
				returnText=returnText+" "+word
	return returnText

def createHeadline(kw, subkw, text, simpleType):
	if not isinstance(text, str):
		return string.capwords(kw)+" - "+" ("+string.capwords(subkw)+")(GH2)"
	
	if simpleType:
		return string.capwords(kw)+" - "+text+"(GH1)"
	else:
		return string.capwords(kw)+" - "+text+" ("+string.capwords(subkw)+")(GH2)"

def sentenceNumber2Word(text):
	if not isinstance(text, str):
		return text
	
	if not text.isdigit():
		return text
	
	numbers		= "0123456789"
	pattern 	= re.compile("([0-9]{1,})")
	words 		= text.split()
	rList		= []
	
	#print("Words:", words)
	for w in words:
		t = w.replace('.','')
		t = t.replace('?','')
		t = t.replace('!','')
		#print("word:", t)
		if t.isnumeric() and not t in [u'.',u'?', u'!']:
			#print("number:", t)
			try:
				i = int(t)
				m = w
				w = convertNumber2Word(i)
				w = str(w)
				rList.extends(w)
			#	if m in ".":
			#		w = w + "ste
				#print("number2word:", w)
			except Exception:
				1
			else:
				rList.append(w)
	if len(rList) >= 1:
		return " ".join(rList)
	else:
		return text

def convertNumber2Word(digits):
	# https://pypi.python.org/pypi/num2words
	"""
	try:
		return num2words(digits, lang='de', ordinal=True)
	except NotImplementedError:
		return num2words(digits, lang='en', ordinal=True)
	return digits
	"""
	def isfloat(x):
		try:
			a = float(x)
		except ValueError:
			return False
		else:
			return True
	
	def isint(x):
		try:
			a = float(x)
			b = int(a)
		except ValueError:
			return False
		else:
			return a == b
			
	
	number=digits
	if isfloat(digits):
		number=float(digits)
	if isint(digits):
		number=int(digits)
	if isinstance(number, str):
		return digits
	
	try:
		if number > 2000:
			return num2words(number, lang='de', ordinal=False)+"(SE3)"
		if number < 2000:
			return num2words(number, lang='de', ordinal=True)+"(SE3)"
	except NotImplementedError:
		return num2words(number, lang='en', ordinal=False)+"(SE3)"
	return digits

def isGoodSpecialCharsAdvanced(text):
	if not isinstance(text, str):
		return False
	
	calcWordBonus=float(0)
	words=text.split()
	wordCharCountList=list(map(len, words))
	
	if len(words)<=0:
		return True
	
	for w in wordCharCountList:
		f=format((w/3)*0.15,'.7f')
		calcWordBonus=calcWordBonus+((w/3)*0.15)
	#calcWordBonus=format(calcWordBonus,'.3f')
	# (wordlenght/3)*0.15 Bonus
	#myText=wordify.encodeToLatin1(text)
	print("calcWordBonus:", calcWordBonus)
	print()
	
	bonus = int(0)
	for p in text:
		
		print("Char isspace():",p,ord(p),p.isspace())
		print("Char p in []:",p,ord(p),p in [',',';','.','!','?','"', u'ä',u'ö',u'ü',u'Ä',u'Ü',u'Ö',u'ß'])
		print("Char is_ascii():",p,ord(p),is_ascii(p))
		print("Char isalnum():",p,ord(p),p.isalnum())
		print()
		if p.isspace():
			#print("POSITIV) Character ID (is_space):",p,ord(p))
			continue
		if p in [',',';','.','!','?','"', u'ä',u'ö',u'ü',u'Ä',u'Ü',u'Ö',u'ß']:
			#print("POSITIV) Character ID (is_in[]):",p,ord(p))
			continue
		if not is_ascii(p):
			print("NEGATIVE) Character ID (is_ascii):",p,ord(p))
			1#### SET BONUS
		if not p.isalnum():
			print("NEGATIVE) Character ID (isalnum):",p,ord(p))
			1#### SET BONUS
	
	# Add all bonus -> if negativ bonus: return False
		
	if debug:
		print("sentify.isGoodSpecialChars(bonus):", bonus)
	if bonus > isGoodSpecialCharsMax:
		return False
	else:
		return True

def isGoodSpecialCharsSimple(text, isGoodSpecialCharsMaxI):
	if not isinstance(text, str):
		return False
	
	myText=wordify.encodeToLatin1(text)
	bonus = int(0)
	for p in myText:
		# count all not alpha numeric, non-space and non sentence delimiter
		#if not p.isalnum() and not p.isspace() and not p in [',','\\','.','!','?','"','-','\'']:
		if not p.isalnum() and not p.isspace() and not p in [u'ä',u'ö',u'ü',u'Ä',u'Ü',u'Ö',u'ß'] and not is_ascii(p):#if not p.isalnum() and not p.isspace() and not p in [u'ä',u'ö',u'ü',u'Ä',u'Ü',u'Ö',u'ß'] and not is_ascii(p):
			bonus = bonus + 1
			if debug:
				print("sentify.isGoodSpecialCharsSimple() Char:",p," is bad")
	if debug:
		print("sentify.isGoodSpecialCharsSimple(bonus):", bonus)
	if bonus > isGoodSpecialCharsMaxI:
		return False
	else:
		return True

def is_ascii(s):
	return all(ord(c) < 257 for c in s)
	#ORG: return all(ord(c) < 128 for c in s)#this works best to find ASCII chars
	#return lambda s: len(s) == len(s.encode())

def isGoodSpecialChars(text):
	if not isinstance(text, str):
		return False
	
	#myText=wordify.encodeToLatin1(text)
	bonus = int(0)
	myText=wordify.encodeToLatin1(text)
	for p in myText:
		# count all not alpha numeric, non-space and non sentence delimiter
		#if not p.isalnum() and not p.isspace() and not p in [',','\\','.','!','?','"','-','\'']:
		if not p.isalnum() and not p.isspace() and not p in [',',';','.','!','?','"', u'ä',u'ö',u'ü',u'Ä',u'Ü',u'Ö',u'ß'] and not is_ascii(p):
			bonus = bonus + 1
			if debug:
				print("sentify.isGoodSpecialChars() Char:",p," is bad")
			
	if debug:
		print("sentify.isGoodSpecialChars(bonus):", bonus)
	if bonus > isGoodSpecialCharsMax:
		return False
	else:
		return True

def isSentenceStructureAdvanced(text):
	# drei NOUN hintereinander riecht nach Shit
	#oder: wenn drei oder vier gross geschriebene Worte hintereinander -> blocken http://stackoverflow.com/questions/2167868/getting-next-element-while-cycling-through-a-list
	if not isinstance(text, str):
		return False
	
	sentList = text.split(" ")
	i=int(0)
	for c in sentList:
		try:
			if i==0:
				i=i+1
				continue
			
			if len(sentList) >= i+3:
				a=sentList[i]
				b=sentList[i+1]
				c=sentList[i+2]
				d=sentList[i+3]
				e=sentList[i+4]
				"""
				print("a:", a)
				print("b:", b)
				print("c:", c)
				print("d:", d)
				#print("e:", e)
				print()
				"""
				i=i+1
				# todo: If NOT NER TAGGER(a,b,c,d,e) 
				if a[0].isupper() and b[0].isupper() and c[0].isupper() and d[0].isupper() and e[0].isupper():
				#if a[0].isupper() and b[0].isupper() and c[0].isupper() and d[0].isupper():
					if debug:
						print("sentify.isSentenceStructureAdvanced(): Three Uppercase Words Error:")
					return False
		except Exception as e:
			1
	return True
	"""
	sentList = speechify.posTagging(text, asString=False)
	noun_flag = 0
	verb_flag = 0
	
	max=len(sentList)
	l = len(sentList)
	noun_one = int(0)
	for index, obj in enumerate(sentList):
		a = obj.split("::")
		if not a:
			continue
		noun_one = int(0)
		pos_tag = a[1]
		if pos_tag in nlp_allowed:
			noun_one = noun_one + 1
		if index < (l - 1):
			next_ = sentList[index + 1]
			a1 = obj.split("::")
			pos_tag = a1[1]
			if pos_tag in nlp_allowed:
				noun_one = noun_one + 1
		if index < (l - 2):
			next_ = sentList[index + 2]
			a2 = obj.split("::")
			pos_tag = a2[1]
			if pos_tag in nlp_allowed:
				noun_one = noun_one + 1
		if noun_one >= 3:
			return False
	return True
	"""

def isSentenceStructure(text):
	if not isinstance(text, str):
		return False
	
	sentList = speechify.posTagging(text, asString=False)
	noun_flag = 0
	verb_flag = 0
	for s in sentList:
		a = s.split("::")
		if a:
			pos_tag = a[1]
			if pos_tag in nlp_allowed:
				noun_flag = 1
			if pos_tag in verb_allowed:
				verb_flag = 1
				
	if noun_flag == 1 and verb_flag == 1:
		return True
	else:
		return False

def isLongEnoughSentence(text):
	if not isinstance(text, str):
		return False
	
	if (len(text) >= 430):
		return False
		
	if (len(text) < 12):
		return False
	
	return True

def isGoodCasing(text):
	if not isinstance(text, str):
		return False
	
	strText 	= wordify.encodeToUTF8(text)
	strString 	= str(strText,'utf-8')
	
	"""
	if re.search(r'(\s{3,})',strString):
		if debug:
			print("sentify.isGoodCasing(): -> re.search(r'(?:\s{3,})' Multiple Spaces Error ")
		return False
	
	if not re.search(r'[a-zA-Z0-9.!?,;-]{2,}',strString):
		if debug:
			print("sentify.isGoodCasing(): -> re.search([a-zA-Z0-9.!?,;-]{2,}) Error ")
		return False
	"""
	"""
	spaceMatch1 = "  "
	spaceMatch2 = "   "
	
	r_Count = text.count(spaceMatch2)
	if r_Count > 1:
		if debug:
			print("sentify.isGoodCasing(): -> spaceMatch2 Error")
		return False
	
	r_Count = text.count(spaceMatch1)
	if r_Count > 1:
		if debug:
			print("sentify.isGoodCasing(): -> spaceMatch1 Error")
		return False
	"""
	"""
	if not re.search(r'\s{3,}', strString):
		print("sentify.isGoodCasing(): -> re.search(r'\s{3,}') Error:'"+strString+"'")
		return False
	"""
	"""
		Entferne Sowas hier: “Begleite uns auf YouTube!Begleite uns auf YouTube!Begleite uns auf YouTube!Begleite uns auf YouTube!Begleite uns auf YouTube!Begleite uns auf YouTube!Begleite uns auf YouTube!
	"""
	
	dubString = isNotDublicateString(text)
	if not dubString:
		if debug:
			print("sentify.isGoodCasing(): -> dublicatePattern Error")
		return False
	
	i=0
	try:
		for c in strString:
			if c in [u'ß',u'ö',u'ä',u'ü',u'Ö',u'Ä',u'Ü']:
				1
			elif c != " " and len(strString) >=i+1:
				if c.islower() and strString[i+1].isupper():
					# zuviel positive falses
					#print("sentify.isGoodCasing(): -> aA Error")
					#aA
					return False
				if c.isdigit() and (strString[i+1].isupper() and strString[i+1].isalpha()):
					if debug:
						print("sentify.isGoodCasing(): -> 2P Error")
					return False
				elif c.isdigit() and strString[i+1].isalpha():
					# to much positive falses
					#print("sentify.isGoodCasing(): -> 2a Error")
					#2a -> Achtung, eventuell bei Adressen als Ausgabe gibt es Probleme
					1# return False
				elif c.isdigit() and strString[i+1].isdigit():
					1 # 11
				elif c.isalpha() and strString[i+1].isdigit():
					if debug:
						print("sentify.isGoodCasing(): -> a2 Error")
					# a2
					return False
				elif c.isdigit() and strString[i+1] not in ['.','!','?','"','-','\'', ':',' ']:
					if debug:
						print("sentify.isGoodCasing -> text.lower()/upper() Error:")
					return False
		i=i+1
	except:
		1
	if text.find('\\') != -1:
		if debug:
			print("sentify.isGoodCasing(): -> text.find(\\) Error")
		return False
	
	if re.search(r'\\', text):
		return False
	
	return True

def isGoodSentenceSimple(text):
	if not isinstance(text, str):
		return False
	for r in r_RegexList:
		x = r.search(text)
		if x is not None: # if we have something like "laufen (S.E.0)"
			#print("Found Match:", x)
			return False
	return True
	
def isGoodSentence(t):
	if isinstance(t, list):
		t = " ".join(t)
	if not isinstance(t, str):
		return False
	
	flag=True
		
	if not isNotBlacklisted(t):
		flag=False
	if not isSentenceStructureAdvanced(t):
		flag=False
	if not isGoodSpecialCharsSimple(t, 5):
		flag=False
	if not isNotDublicateString(t):
		flag=False
	if not isLongEnoughSentence(t):
		flag=False
	if not isGoodSentenceSimple(t):
		flag=False
	
	return flag

def isGoodSentencev1(text):
	if not isinstance(text, str):
		return False
	debug=True
	#text=wordify.replaceSpecialChars(text) # entferne erst alle sonderzeichen, bevor es durch diesen strikten filter geht
	#debug=True
	#if debug:
	#	1#print("sentify.isGoodSentence(): -> SENTENCES:", text)
	
	#letters		= "abcdefghijklmnopqrstuvwxyz"
	#numbers		= "0123456789"
	#words 		= text.split()
	#pattern 	= re.compile("([A-Z][0-9]{2,})")
	#print("sentify.isGoodSentence():", isGoodLong)
	#strText 	= wordify.encodeToUTF8(text)
	#strString 	= str(strText,'utf-8')
	#textLower	= text.lower()
	
	"""
	if not isLongEnoughSentence(text) or not isLongEnoughSentence(text, dynamic=False):
		if debug:
			print("sentify.isGoodSentence(): -> isLongEnoughSentence() Error")
		return False
	"""
	"""
	if not isNotBlacklisted(text):
		if debug:
			print("\tsentify.isGoodSentence(): -> isNotBlacklisted() Error")
		return False
	"""
	
	if not isLongEnoughSentence(text, dynamic=True):
		if debug:
			1#print("\tsentify.isGoodSentence(): -> isLongEnoughSentence() Error")
		return False
		
	
	if not isGoodSentenceStart(text):
		if debug:
			1#print("\tsentify.isGoodSentence(): -> isGoodSentenceStart() Error")
		return False
	
	if not isNotDublicateString(text):
		if debug:
			print("\tsentify.isGoodSentence(): -> isNotDublicateString() Error")
		return False
	"""
	if not isGoodCasing(text):
		if debug:
			print("\tsentify.isGoodSentence(): -> isGoodCasing() Error", text)
		return False
	"""
	
	if not isGoodSpecialCharsSimple(text, 5):
		if debug:
			print("\tsentify.isGoodSentence(): -> isGoodSpecialChars() Error:")
			#text = wordify.replaceSpecialChars(text)
		return False
	
	# zuviel false positive
	if not isSentenceStructureAdvanced(text):
		if debug:
			print("\tsentify.isSentenceStructureAdvanced(): Error")
			#text = wordify.replaceSpecialChars(text)
		return False
	
	return True