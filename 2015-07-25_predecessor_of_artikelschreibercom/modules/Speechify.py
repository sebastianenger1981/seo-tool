# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore

import nltk
import uuid
import hashlib
import os, sys, logging, re, time
from pprint import pprint  # pretty-printer
from operator import itemgetter
from textblob_de import TextBlobDE as TextBlob
from textblob_de.lemmatizers import PatternParserLemmatizer
import spacy# pip3 install --upgrade spacy
from spacy.en import English
from spacy.de import German
from nltk.corpus import stopwords
from spacy.tokens.token import Token as SpacyToken
from spacy.tokens.span import Span as SpacySpan
from pprint import PrettyPrinter
from datetime import datetime
from treetagger import TreeTagger
import subprocess
from segtok.segmenter import split_single, split_multi, MAY_CROSS_ONE_LINE, \
    split_newline, rewrite_line_separators, ABBREVIATIONS, CONTINUATIONS, \
    NON_UNIX_LINEBREAK, to_unix_linebreaks
# pip3 install -U segtok

import modules.Wordify as wordify
import modules.Fileify as fileify

debug=False

pp=PrettyPrinter(indent=4)
tt_de=TreeTagger(language='german')

os.system("export TREETAGGER_HOME='/home/buz/buzzgreator/treetagger/cmd'")
os.system("export GOOGLE_APPLICATION_CREDENTIALS='/home/buz/buzzgreator/key/100BiereTranslate-8a809e939d5e.json'")

return_code1 = subprocess.call("export TREETAGGER_HOME='/home/buz/buzzgreator/treetagger/cmd'", shell=True)  
return_code2 = subprocess.call("export GOOGLE_APPLICATION_CREDENTIALS='/home/buz/buzzgreator/key/100BiereTranslate-8a809e939d5e.json'", shell=True)  
#https://hugonlp.wordpress.com/2015/10/07/how-to-do-pos-tagging-and-lemmatization-in-languages-other-than-english/
#http://textacy.readthedocs.io/en/latest/_modules/textacy/similarity.html
#http://textacy.readthedocs.io/en/latest/_modules/textacy/spacy_utils.html
nlp = spacy.load('de')
#nlp = German()

def doSpeechify(text):
	if not isinstance(text, str):
		return False
	return nlp(text)

def spacyLemmatizer(text):
	#Hint: It is using TreeTagger -> http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/
	if not isinstance(text, str):
		return False
	
	try:
		for t in tt_de.tag(text): # TreeTagger(language='german')
			if len(t)==3:
				lema = t[2]
				if lema.find("unknown") != -1:
					lema = text
				if debug:
					print("speechify.spacyLemmatizer():", lema)
				return lema
	except Exception as esc:
		1
	return text #is False

def splitOnLowerUppercase(strText):
	if not isinstance(strText, str):
		return False
	
	x 	= ""
	i 	= 0
	strText = wordify.encodeToUTF8(strText)
	strString = str(strText,'utf-8')
	#print(type(strText))
	#print(type(strString))
	for c in strString:
	#	print("c:", c)
	#	print(type(c))
	#	print("strString[i-1]:", strString[i-1])
		if i == 0: 
			x = x + str(c)
		elif c in [',','\\','.','!','?','"','-','\'']:
			x = x + str(c)
		elif c in [u'ß',u'ö',u'ä',u'ü',u'Ö',u'Ä',u'Ü']:
			x = x + str(c)
		elif c.isupper() and not strString[i-1].isupper():
			#x += ' %s' % c
			x = x +" "+str(c)
		else:
			#x += c
			x = x + str(c)
		i += 1
	#	print("i:", i)
	#	print(type(i))
	#return wordify.encodeToLatin1(x.strip())
	return x.strip()

def removePosTagsFromString(text, singleWord):
	if not isinstance(text, str):
		return False
	
	if singleWord:
		a 		= text.split("::")
		word 	= a[0]
		return word
	else:
		t_List 	= text.split()
		sent 	= []
		for t in t_List:
			a 		= t.split("::")
			word 	= a[0]
			sent.append(word)
		
		sent.append(" ")
		textstring = " ".join(sent)
		return re.sub(r"\s+", ' ', textstring)
		#return re.sub(r' +', ' ', textstring)
	return False

def posTagging(text, asString):
	if not isinstance(text, str):
		return False
	
	nlp_text 	= doSpeechify(text)
	sents 		= []
	for word in nlp_text:
		#print(type(word.pos_))
		#print word.orth_, word.tag_, word.dep_, word.head.orth_
		eleString = word.text+"::"+(word.pos_)
		sents.append(eleString)
	if asString:
		return " ".join(sents)
	else:
		return sents

def sentPosSegmenter(text):
	if not isinstance(text, str):
		return False
	
	nlp_text 	= list(split_single(text))
	sents 		= []
	
	for span in nlp_text:
		token 	= doSpeechify(span)
		sTmp 	= []
		for word in token:
			#print word.orth_, word.tag_, word.dep_, word.head.orth_
			#eleString = word.text+"::"+(word.pos_)
			sTmp.append(word.pos_)
		sents.append(" ".join(sTmp))
	return sents

def traverse(list_of_lists, tree_types=(list, tuple)):
	return [y for x in list_of_lists for y in x]
	#return list(map(itemgetter(0), o))
	"""
	if isinstance(o, tree_types):
		for value in o:
			for subvalue in traverse(value, tree_types):
				yield subvalue
	else:
		yield o
	"""

# Originally by Bruno Polaco
def traversev1(item, reverse=False):
    its = [item] #stack of items to-be-processed
    out = [] # Output (no longer generator)
    ite = False
    while len(its) > 0:
        it = its.pop()
        try: # Check if item is iterable
            iter(it)
            ite = not isinstance(it, str)
        except TypeError:
            ite = False
        if ite: # Do something with it
            for i in it:
                its.append(i)
        else:
            out.append(it)
    if not reverse:
        out.reverse()
    return out

def sentSegmenterSimple(text, asString):
	#https://github.com/fnl/segtok
	if isinstance(text, list):
		text = " ".join(text)
	if not isinstance(text, str):
		print("Speechify.sentSegmenterSimple():", type(text))
		return False
	#import modules.Sentify as sentify
	
	#nlp_text 	= list(split_single(text))
	sents 		= []
	sentsPos 	= []
	sTmp 		= []
	sTmpPos 	= []
	#nlp_text 	= doSpeechify(text)
	#sentify.isGoodSentence(markov_sample)
	for a in split_single(text):
		sents.append(a+"\n")
	"""
	Ablauf:
	1. sec=sektog Sentences
	2. secv1=sec
	3. if string=True: return sec
	4. if pos=True: next	
	5. 	next: for s in sec: token = doSpeechify(text) for word in token:
	6. return posTagSenteces
	"""
	
	#for n in nlp_text:
	#	sents.append(n+"\n")
	
	if asString is True:
		#myArticle=''.join(''.join(elems) for elems in myArticle)
		#sents.append(" ".join(sTmp))
		my=' '.join(''.join(elems) for elems in sents)
		return my
	else:
		#sents.append(sTmp)
		return sents

def sentSegmenter(text, asString, posTags):
	#https://github.com/fnl/segtok
	if isinstance(text, list):
		text = " ".join(text)
	if not isinstance(text, str):
		print("Speechify.sentSegmenter():", type(text))
		return False
	
	import modules.Sentify as sentify
	
	#nlp_text 	= list(split_single(text))
	sents 		= []
	sentsPos 	= []
	sTmp 		= []
	sTmpPos 	= []
	nlp_text 	= doSpeechify(text)
	#sentify.isGoodSentence(markov_sample)
	"""
	Ablauf:
	1. sec=sektog Sentences
	2. secv1=sec
	3. if string=True: return sec
	4. if pos=True: next	
	5. 	next: for s in sec: token = doSpeechify(text) for word in token:
	6. return posTagSenteces
	"""
	
	for n in nlp_text.sents:
		#if not sentify.isGoodSentence(n):
		#	continue
		token = n#doSpeechify(n.strip())
		for word in n:
			#print word.orth_, word.tag_, word.dep_, word.head.orth_
			eleString = word.text+"::"+(word.pos_)
			sTmpPos.append(eleString)
			sTmp.append(word.text)
			if word.pos_ in "PUNCT" and word.text in [".","!","?"]:
				myPos=' '.join(''.join(elems) for elems in sTmpPos)
				my=' '.join(''.join(elems) for elems in sTmp)
				sentsPos.append(myPos+"\n")
				sents.append(my+"\n")
				sTmpPos = []
				sTmp 	= []
		
	if posTags is True:
		if asString is True:
			#myArticle=''.join(''.join(elems) for elems in myArticle)
			#sents.append(" ".join(sTmp))
			my=' '.join(''.join(elems) for elems in sentsPos)
			return my
		else:
			#sents.append(sTmp)
			return traverse(sents)
	else:
		if asString is True:
			#myArticle=''.join(''.join(elems) for elems in myArticle)
			#sents.append(" ".join(sTmp))
			my=' '.join(''.join(elems) for elems in sents)
			return my
		else:
			#sents.append(sTmp)
			return sents
	
def sentSegmenterv2(text, asString, posTags):
	#https://github.com/fnl/segtok
	if not isinstance(text, str):
		return False
	import modules.Sentify as sentify
	
	nlp_text 	= list(split_single(text))
	sents 		= []
	sentsv1 	= []
	sTmp 		= []
	#nlp_text1 	= doSpeechify(text)
	#sentify.isGoodSentence(markov_sample)
	"""
	Ablauf:
	1. sec=sektog Sentences
	2. secv1=sec
	3. if string=True: return sec
	4. if pos=True: next	
	5. 	next: for s in sec: token = doSpeechify(text) for word in token:
	6. return posTagSenteces
	"""
	
	for n in nlp_text:
		#if not sentify.isGoodSentence(n):
		#	continue
		
		sents.append(n+"\n")
	
	if posTags is False:
		if asString is True:
			#myArticle=''.join(''.join(elems) for elems in myArticle)
			#sents.append(" ".join(sTmp))
			my=' '.join(''.join(elems) for elems in sents)
			return my
		else:
			#sents.append(sTmp)
			return traverse(sents)
	
	if posTags is True:
		for text in sents:
			token = doSpeechify(text.strip())
			for word in token:
				#print word.orth_, word.tag_, word.dep_, word.head.orth_
				eleString = word.text+"::"+(word.pos_)
				sTmp.append(eleString)
				if word.pos_ in "PUNCT" and word.text in [".","!","?"]:
					#sTmp.append("\n")
					my=' '.join(''.join(elems) for elems in sTmp)
					sentsv1.append(my+"\n")
					sTmp = []
			
		if asString is True:
			#myArticle=''.join(''.join(elems) for elems in myArticle)
			#sents.append(" ".join(sTmp))
			my=' '.join(''.join(elems) for elems in sentsv1)
			return my
		else:
			#sents.append(sTmp)
			return traverse(sentsv1)

def sentSegmenterv1(text, asString, posTags):
	#https://github.com/fnl/segtok
	if not isinstance(text, str):
		return False
	
	#text		= wordify.encodeToLatin1(text)
	#text		= wordify.encodeToUTF8(text)
	#nlp_text 	= doSpeechify(text)
	nlp_text 	= list(split_single(text))
	sents 		= []
	
	if posTags is True:
		for span in nlp_text:
			token 	= doSpeechify(span)
			sTmp 	= []
			for word in token:
				#print word.orth_, word.tag_, word.dep_, word.head.orth_
				eleString = word.text+"::"+(word.pos_)
				sTmp.append(eleString)
		if asString is True:
			sents.append(" ".join(sTmp))
			return " ".join(sents)
		else:
			sents.append(sTmp)
			return sents
	
	else:
		#print("Working with non-postagging:")
		for span in nlp_text:
		#	print("Working in span:", span)
			sent = span
			sent = re.sub('\s+',' ',sent).strip()
			sent = re.sub(' +',' ',sent).strip()
			sents.append(span)
			#print("Speechify: sentSegmenter:", sent)
		#return "\n".join(sents)
		#print("len(sents):", len(sents))
		if asString is True:
			return "\n".join(sents)
		else:
			return sents
	
	nlp_text 	= doSpeechify(text)
	if posTags is True:
		for span in nlp_text.sents:
			sent = ''.join(nlp_text[i].string for i in range(span.start, span.end)).strip()
			token 	= doSpeechify(sent)
			sTmp 	= []
			for word in token:
				#print word.orth_, word.tag_, word.dep_, word.head.orth_
				eleString = word.text+"::"+(word.pos_)
				sTmp.append(eleString)
		if asString is True:
			sents.append(" ".join(sTmp))
			return " ".join(sents)
		else:
			sents.append(sTmp)
			return sents
	else:
		#print("Working with non-postagging:")
		for span in nlp_text.sents:
			sent = ''.join(nlp_text[i].string for i in range(span.start, span.end)).strip()
			sent = re.sub('\s+',' ',sent).strip()
			sent = re.sub(' +',' ',sent).strip()
			sents.append(sent)
			#print("Speechify: sentSegmenter:", sent)
		#return "\n".join(sents)
		#print("len(sents):", len(sents))
		if asString is True:
			return "\n".join(sents)
		else:
			return sents
	
	return []

def normalized_str(token):
    """
    Return as-is text for tokens that are proper nouns or acronyms, lemmatized
    text for everything else.
    Args:
        token (``spacy.Token`` or ``spacy.Span``)
    Returns:
        str
    """
    if isinstance(token, SpacyToken):
        return token.text if preserve_case(token) else token.lemma_
    elif isinstance(token, SpacySpan):
        return ' '.join(subtok.text if preserve_case(subtok) else subtok.lemma_
                        for subtok in token)
    else:
        msg = 'Input must be a spacy Token or Span, not {}.'.format(type(token))
        raise TypeError(msg)
		
"""
def sentSegmenter(text, asString=True, posTags=True):
	if not isinstance(text, str):
		return False
	
	nlp_text 	= doSpeechify(text)
	sents 		= []
	
	if posTags:
		for span in nlp_text.sents:
			sent = ''.join(nlp_text[i].string for i in range(span.start, span.end)).strip()
			#sents.append(sent)
			token 	= doSpeechify(sent)
			sTmp 	= []
			for word in token:
				#print word.orth_, word.tag_, word.dep_, word.head.orth_
				eleString = word.text+"::"+(word.pos_)
				sTmp.append(eleString)
			if asString is True:
				sents.append(" ".join(sTmp))
			else:
				sents.append(sTmp)
	else:
		for span in nlp_text.sents:
			sent = ''.join(nlp_text[i].string for i in range(span.start, span.end)).strip()
			sent = re.sub('\s+',' ',sent).strip()
			sent = re.sub(' +',' ',sent).strip()
			sents.append(sent)
			#print("Speechify: sentSegmenter:", sent)
		#return "\n".join(sents)
		
	if asString is True:
		return "\n".join(sents)
	else:
		return sents

"""