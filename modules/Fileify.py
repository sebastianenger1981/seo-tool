# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore

import re
import os
import sys
import time
import fcntl
import json
import pickle
import string
import hashlib
import random
import urllib
from random import random as rand
from bisect import bisect
import requests	# pip3 install --upgrade requests
from urllib.parse import urlparse# pip3 install --upgrade urlparse
import urllib # url=urllib.unquote(url).decode('utf8')
from googleapiclient.discovery import build
from google import google
from bs4 import BeautifulSoup, Comment 	# pip3 install --upgrade beautifulsoup4 && pip install html5lifrom datetime import datetime as dTime
from datetime import datetime as dTime

import modules.Wordify as wordify
debug=True
sys.setrecursionlimit(1500)

UserAgent				= "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
UserAgentMobile			= "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36"
Headers 				= {'user-agent': UserAgent, 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate'}
HeadersSimple			= {'user-agent': UserAgentMobile, 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate'}

#htmlTagsToExtract	 	= [u"strong", u"i", u"title", u"em", u"b", u"p", u"span", u"div", u"h1", u"h2", u"h3", u"h4", u"h5", u"h6", u"blockquote",u"article",u"header",u"ul",u"li",u"ol",u"main",u"pre",u"cite",u"textarea", u"aside", u"figcaption", u"footer", u"main", u"section", u"video"]
#htmlTagsToExtract	 	= [u"strong", u"title", u"em", u"b", u"p", u"span", u"div", u"h1", u"h2", u"h3", u"h4", u"h5", u"h6", u"blockquote", u"article", u"header",u"main", u"pre", u"cite", u"textarea", u"aside", u"figcaption", u"footer", u"main", u"section", u"video"]
htmlTagsToExtract	 	= [u"strong", u"title", u"em", u"b", u"p", u"div", u"h1", u"h2", u"h3", u"h4", u"h5", u"h6", u"blockquote", u"article"]

def DuckDuckGoSearch(MainKeyword, SubKeywords):
	import modules.Sentify as sentify
	if debug:
		print("fileify.DuckDuckGoSearch():", MainKeyword, SubKeywords)
	DuckResultList = []
	#https://duckduckgo.com/html/
	#https://duckduckgo.com/params
	#https://duckduckgo.com/html?q=Nintendo%20Switch&kp=1&kl=de-de&kaf=1&kh=1&k1=1&kaj=m&kv=-1
	"""
	1. html search
	2. result links extrahieren
	3. result links downloaden oder: links extrahieren, in List Sammlen und später downloaden
	"""
	
	p1 = "https://duckduckgo.com/html/?q="+MainKeyword+"&kp=1&kl=de-de&kaf=1&kh=1&k1=1&kaj=m&kv=-1&ia=web"
	p2 = "https://duckduckgo.com/html/?q="+MainKeyword+" AND "+SubKeywords+"&kp=1&kl=de-de&kaf=1&kh=1&k1=1&kaj=m&kv=-1&ia=web"
	
	for p in [p1, p2]:
		htmlContent1 	= getWebpagesSimple(p,"/tmp/", ret=True)
		soup1 			= BeautifulSoup(htmlContent1, "html5lib")
		#links1 = soup1.find_all('a', {'class': ['result__a']})
		data1 			= soup1.findAll('div', attrs={'class':'results_links'})
		for div in data1:
			linksfound = div.find_all('a', {'class': ['result__a']})
			for link in linksfound:
				l_tmp = str(link['href'])
				if l_tmp is None:
					continue
				l=l_tmp.lower()
				#print(l)
				if l.startswith("http"):
					if l not in DuckResultList and sentify.isNotDomainBlacklisted(l):
						sid = createShortid()
						DuckResultList.append([sid,l])
				else:
					t_Links=l.split("=")
					#print(len(t_Links))
					if len(t_Links)==3:
						t_Url=t_Links[2]
						#url=urllib.parse.unquote(t_Url).encode('utf8')
						url=urllib.parse.unquote(t_Url)
						if url not in DuckResultList and sentify.isNotDomainBlacklisted(url):
							sid = createShortid()
							DuckResultList.append([sid,url])
	return DuckResultList

def doGoogleSearch(MainKeyword, SubKeywords):
	GoogleResultList=list()
	for c in range(35):
		g=GoogleCustomSearch(MainKeyword, SubKeywords, c)
		GoogleResultList.extend(g)
		if len(GoogleResultList)>=550:
			return GoogleResultList
	return GoogleResultList

def GoogleCustomSearch(MainKeyword, SubKeywords, countGoogle):
	import modules.Sentify as sentify
	
	countGoogle=str(countGoogle)
	GoogleResultList=[]
	
	urlv2="https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=de&prettyPrint=true&googlehost=google.de&start="+countGoogle+"&cx=004726852717983880440:rof1dm__d_k&q="+MainKeyword
	urlv1="https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=de&prettyPrint=true&googlehost=google.de&start="+countGoogle+"&cx=004726852717983880440:rof1dm__d_k&q="+MainKeyword+" AND "+SubKeywords
	
	wv1=getWebpagesSimple(urlv1, "/tmp/", True)
	wv2=getWebpagesSimple(urlv2, "/tmp/", True)
	
	try:
		data = json.loads(wv1)
		# pretty printing of json-formatted string
		# print(json.dumps(decoded, sort_keys=True, indent=4))
		for line in data['results']:
			link = line['url']
			link=urllib.parse.unquote(link)
			#cacheUrl = line['cacheUrl']
			#print("link:", link)
			if sentify.isNotDomainBlacklisted(link):
				sid = createShortid()
				GoogleResultList.append([sid,link])
	
	except (ValueError, KeyError, TypeError, Exception):
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	
	
	
	try:
		data = json.loads(wv2)
		# pretty printing of json-formatted string
		# print(json.dumps(decoded, sort_keys=True, indent=4))
		for line in data['results']:
			link = line['url']
			link=urllib.parse.unquote(link)
			#cacheUrl = line['cacheUrl']
			#print("link:", link)
			if sentify.isNotDomainBlacklisted(link):
				sid = createShortid()
				GoogleResultList.append([sid,link])
	
	except (ValueError, KeyError, TypeError, Exception):
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	
	# todo: calcTrendRank JSON Parsing logik hier noch mit einbauen
	return GoogleResultList

# def extractFromHTML(parameterList):
def extractFromHTML(html_content, shortid, path, nocheck):
	if len(html_content) > 1550000: # 1 000 000
		return list()
	
	if not isinstance(html_content, str):
		return list()
		
	# create folder
	if not os.path.exists(path):
		os.makedirs(path)
	
	import modules.Speechify as speechify
	import modules.Sentify as sentify
	UniqueSentenceSet = set()
	
	if debug:
		print("fileify.extractFromHTML() STA:",str(dTime.now()))
	
	try:
		t_tuple			= ()
		lGood			= []
		s 				= set()
		l 				= []
		t_count 		= 0
		t_countFound 	= 0
		#soup 			= BeautifulSoup(html_content, "html5lib")
		soup 			= BeautifulSoup(html_content, "lxml")
		comments 		= soup.findAll(text=lambda text:isinstance(text, Comment)) # remove comments
		[comment.extract() for comment in comments]
		for script in soup(["script", "style", 'footer', 'head']):
			script.extract()# rip it out
		
		#[s.extract() for s not in soup(['style', 'script', '[document]', 'footer', 'head', 'title'])]
		#[s.extract() for s in soup(['body'])]
		t=""
		visible_text=""
		soup.prettify()
		if soup.getText():
			visible_text 	= soup.getText()
			t 				= visible_text
		
		#if len(t_texttmp)>=t_minlength and lang in "de" and not blacklisted:
		#t_texttmp 		= wordify.encodeToLatin1(visible_text)
		### hier nicht aktivieren, denn multiple spaces bedeuten schrott daten -> t_texttmp = re.sub( '\s+', ' ', t_texttmp ).strip()
		
		sub_sid 		= createShortid()
		t_ResultList 	= []
		t 				= re.sub('\s+',' ',t).strip()
		#t 				= re.sub(' +',' ',t).strip()
		#t_checking  	= t_texttmp.split()
		
		# deactivated because of speed issues
		#t_checking  	= speechify.sentSegmenter(t_texttmp, asString=False, posTags=False)
		#print("t_checking:",len(t_checking))
		
		#if sentify.isGoodCasing(t):
		if t not in UniqueSentenceSet:
			if nocheck is True:
				UniqueSentenceSet.add(t)
				t_ResultList.append(t)
			elif sentify.isGoodSentence(t):
				UniqueSentenceSet.add(t)
				t_ResultList.append(t)
			"""elif sentify.isNotBlacklisted(t) and sentify.isLongEnoughSentence(t) and sentify.isNotDublicateString(t) and sentify.isGoodSpecialChars(t) and sentify.isSentenceStructureAdvanced(t):
				UniqueSentenceSet.add(t)
				t_ResultList.append(t)
			"""
		t_returnString 	= ' '.join(''.join(elems) for elems in t_ResultList)
		#len_sent		= int(len(t_ResultList))
		#len_text 		= int(len(t_returnString))
		#len_words 		= int(len(t_returnString.split()))
		
		if len(t_ResultList) >= 1: 
			#t_returnString  = wordify.encodeToLatin1(t_returnString)
			#lesbarkeitsID	= sentify.isReadability(t_returnString)
			#lang 			= wordify.intDetectLanguage(t_returnString)
			#lGood.append([shortid, sub_sid, "alltext", t_returnString, lesbarkeitsID, lang])
			tel = {'hit':float(0),'shortid':shortid,'tag':"alltext",'content':t_returnString}
			lGood.append(tel)
		
		for tag in htmlTagsToExtract:
			if tag not in html_content:
				continue
			
			#print("buzzgreator.extractFromHTML() -> Tag:", tag)
			#soup1 		= BeautifulSoup(html_content, "lxml")
			soup1 		= BeautifulSoup(html_content, "html5lib")
			comments 	= soup1.findAll(text=lambda text:isinstance(text, Comment)) # remove comments
			[comment.extract() for comment in comments]
			#[s.extract() for s not in soup(['style', 'script', '[document]', 'footer', 'head', 'title'])]	
			#[s.extract() for s in soup(['body', 'title'])]
			for script in soup1(["script", "style", 'footer', 'head']):
				script.extract()# rip it out
			
			soup1.prettify()
			"""
				if "title" in tag: # remove nasty information from title Tag
					t_texttmp 	= removeAfter(t_texttmp)
			"""
			
			for ele in soup1.find_all(tag):
				t=""
				visible_text=""
				if ele is not None:
					if ele.text is not None:
						visible_text 	= ele.text
						t 				= ele.text
				
				sub_sid 		= createShortid()
				t_ResultList 	= []
				t 				= re.sub('\s+',' ',t).strip()
				#t 				= re.sub(' +',' ',t).strip()
				#t_checking  	= t_texttmp.split()
				#t_checking  	= speechify.sentSegmenter(t_texttmp, asString=False, posTags=False)
				#print("t_checking:",len(t_checking))
				
				if t not in UniqueSentenceSet:
					if nocheck is True:
						UniqueSentenceSet.add(t)
						t_ResultList.append(t)
					elif sentify.isGoodSentence(t):
					#sentify.isNotBlacklisted(t) and sentify.isLongEnoughSentence(t) and sentify.isNotDublicateString(t) and sentify.isGoodSpecialChars(t) and sentify.isSentenceStructureAdvanced(t):
						UniqueSentenceSet.add(t)
						t_ResultList.append(t)
				
				t_returnString 	= ' '.join(''.join(elems) for elems in t_ResultList)
				#len_sent		= int(len(t_ResultList))
				#len_text 		= int(len(t_returnString))
				#len_words 		= int(len(t_returnString.split()))
				if len(t_ResultList) >= 1:
					#t_returnString 	= wordify.encodeToLatin1(t_returnString)
					#lesbarkeitsID	= sentify.isReadability(t_returnString)
					#lang 			= wordify.intDetectLanguage(t_returnString)
					#lGood.append([shortid, sub_sid, tag, t_returnString, lesbarkeitsID, lang])
					tel = {'hit':float(0),'shortid':shortid,'tag':tag,'content':t_returnString}
					lGood.append(tel)
	except (ValueError, KeyError, TypeError, Exception):
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	
	if debug:
		print("fileify.extractFromHTML() END:",str(dTime.now()))
	
	if len(lGood)>=1:
		binaryWrite(lGood, path+"/"+shortid+".bin")
		if debug:
			print("fileify.extractFromHTML() Counter lGood:",len(lGood))
	
	return lGood

def getWebpagesSimple(link, WDirHtml, ret):
	myLink=link
	if myLink.lower().endswith('.pdf'):
		return False
	
	if not os.path.exists(WDirHtml):
		os.makedirs(WDirHtml)
	
	if debug:
		print("fileify.getWebpagesSimple():", link)
	
	try:
		r1 				= requests.get(link, headers=HeadersSimple, timeout=180)
		#r1.encoding 	= 'utf-8'
		content_txpe 	= r1.headers.get('content-type')
		myEncoding		= r1.encoding
		myText			= r1.text
		if myEncoding.find("utf-8") == -1:
			# if no utf-8 encoding found -> decode it to utf-8
			myText=""
			myText=wordify.encodeToUTF8Adv(r1.text)
		
	except Exception as er:
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		return False
	else:
		# we only want to download content type text, html, css, js and no binary files
		if r1.status_code == 200 and content_txpe is not None and content_txpe.find('text') != -1:
			#print("Downloading complete: -> ",link)
			content = myText
			if ret is True:
				return content
			
			#return content
			sid = createShortid()
			f = open(WDirHtml+"/"+sid+".html", 'w', encoding="utf-8")
			f.write(content)
			f.close
			return True
		elif r1.status_code == 200 and content_txpe is not None and content_txpe.find('application') != -1:
			#print("Downloading complete: -> ",link)
			content = myText
			if ret is True:
				return content
			
			#return content
			sid = createShortid()
			f = open(WDirHtml+"/"+sid+".html", 'w', encoding="utf-8")
			f.write(content)
			f.close
			return True
		else:
			print("Downloading failure: -> ",link)
			print("Status code:", r1.status_code)
			print()
	return False

def binaryWrite(corpus, filename):
	try:
		f = open(filename,'wb')
		fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
		pickle.dump(corpus, f)
		fcntl.flock(f, fcntl.LOCK_UN)
		f.close
		return True
	except (BlockingIOError, Exception) as e:
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	return []

def binaryWriteAppend(corpus, filename):
	o_Content = binaryRead(filename)
	try:
		f = open(filename,'wb')
		fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
		pickle.dump(o_Content+corpus, f)
		fcntl.flock(f, fcntl.LOCK_UN)
		f.close
		return True
	except (BlockingIOError, Exception) as e:
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	return []

def binaryRead(filename):
	if os.path.isfile(filename):
		try:
			f = open(filename,'rb')
			fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
			l = pickle.load(f)
			fcntl.flock(f, fcntl.LOCK_UN)
			f.close
			return l
		except (BlockingIOError, Exception) as e:
			print("Unexpected error:", sys.exc_info()[0])
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
	return []

def createShortid(size=23, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
	

def plainWriteAppend(corpus, filename):
	o_Content = plainRead(filename)
	try:
		f = open(filename,'w', encoding="utf8")
		#fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
		f.write(o_Content+corpus)
		#fcntl.flock(f, fcntl.LOCK_UN)
		f.close()
		return []
	except (BlockingIOError, Exception) as e:
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	return []

def plainWrite(corpus, filename):
	#t_Text = wordify.encodeToLatin1(corpus)
	try:
		f = open(filename,'w', encoding="utf8")
		#fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
		f.write(corpus)
		#fcntl.flock(f, fcntl.LOCK_UN)
		f.close()
		return []
	except (BlockingIOError, Exception) as e:
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	return []

def plainRead(filename):
	if os.path.isfile(filename):
		try:
			f = open(filename, "r")
			fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
			t_data = f.read()
			fcntl.flock(f, fcntl.LOCK_UN)
			f.close()
			return t_data
		except (BlockingIOError, Exception) as e:
			print("Unexpected error:", sys.exc_info()[0])
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
	"""
	#f = open(filename, "r", encoding="utf-8")
	f = open(filename, "r")
	fcntl.flock(f, fcntl.LOCK_UN)
	t_data = f.read()
	fcntl.flock(f, fcntl.LOCK_UN)
	f.close
	t_Text = wordify.encodeToLatin1(t_data)
	return t_data
	"""
	return []

"""
def GoogleSearch(MainKeyword, SubKeywords):
	# https://github.com/abenassi/Google-Search-API
	import modules.Sentify as sentify
	
	NoDublicatSet	=set()
	GoogleResultList=[]
	#MaxGoogleSearchRetry=int(15)
	
	#https://github.com/google/google-api-python-client/tree/master/samples
	if debug:
		print("fileify.GoogleSearch():", MainKeyword, ", ", SubKeywords)
	
	try:
		for c in range(15):
			#pip3 install selenium
			search_results=""
			search_results = google.search(MainKeyword, pages=c, lang='de')
			for s in search_results:
				t_link = s.link
				if sentify.isNotDomainBlacklisted(t_link) and t_link not in NoDublicatSet:
					sid = createShortid()
					GoogleResultList.append([sid,t_link])
					NoDublicatSet.add(t_link)
			search_results=""
			search_results = google.search(SubKeywords, pages=c, lang='de')
			for s in search_results:
				t_link = s.link
				if sentify.isNotDomainBlacklisted(t_link) and t_link not in NoDublicatSet:
					sid = createShortid()
					GoogleResultList.append([sid,t_link])
					NoDublicatSet.add(t_link)
	except Exception as er:
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	return GoogleResultList
"""
"""
def GoogleSearch(MainKeyword, SubKeywords):
	# https://github.com/abenassi/Google-Search-API
	import modules.Sentify as sentify
	
	def _get_link(li):
    #Return external link from a search.
    try:
        a = li.find("a")
        link = a["href"]
    except:
        return None
	
	NoDublicatSet	=set()
	GoogleResultList=[]
	#MaxGoogleSearchRetry=int(15)
	
	WDirSubKW	= "/var/tmp"# fix
	if not os.path.exists(WDirSubKW):
		os.makedirs(WDirSubKW)
	
	#https://github.com/google/google-api-python-client/tree/master/samples
	if debug:
		print("fileify.GoogleSearch():", MainKeyword, ", ", SubKeywords)
	
	try:
		for c in range(0,5,1):
			t_link="https://www.google.de/search?q="+MainKeyword+"&start="+c+"&num=100"
			htmlContent=getWebpagesSimple(t_link, WDirSubKW, ret=True)
			soup 			= BeautifulSoup(htmlContent, "lxml")
			comments 		= soup.findAll(text=lambda text:isinstance(text, Comment)) # remove comments
			[comment.extract() for comment in comments]
			for script in soup(["script", "style", 'footer', 'head']):
				script.extract()# rip it out
			soup.prettify()
			divs = soup.findAll("div", attrs={"class": "g"})
			for li in divs:
				 link = _get_link(li)
			
		
			#if len(t_texttmp)>=t_minlength and lang in "de" and not blacklisted:
			t 				= visible_text
	
			for s in search_results:
				t_link = s.link
				if sentify.isNotDomainBlacklisted(t_link) and t_link not in NoDublicatSet:
					sid = createShortid()
					GoogleResultList.append([sid,t_link])
					NoDublicatSet.add(t_link)
			search_results=""
			search_results = google.search(SubKeywords, pages=c, lang='de')
			for s in search_results:
				t_link = s.link
				if sentify.isNotDomainBlacklisted(t_link) and t_link not in NoDublicatSet:
					sid = createShortid()
					GoogleResultList.append([sid,t_link])
					NoDublicatSet.add(t_link)
	except Exception as er:
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	return GoogleResultList
"""
def weighted_choice(choices):
	values, weights = zip(*choices)
	total = 0
	cum_weights = []
	for w in weights:
		total += w
		cum_weights.append(total)
	x = rand() * total
	i = bisect(cum_weights, x)
	return values[i]