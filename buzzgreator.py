# -*- coding: utf-8 -*-
#!/usr/bin/env python
# https://developers.google.com/custom-search/docs/xml_results#countryCodes
#https://www.linkedin.com/countserv/count/share?format=jsonp&url=https://www.buzzerstar.com 
# pip install --upgrade spacy tensorflow gensim sumy keras markovify google-api-python-client beautifulsoup4

"""
DEEPWRITER
"""

import re
import sys
import os
import pickle
import codecs
import string
import time
import glob
import getopt
import argparse
import tempfile
import datetime
import chardet # pip install chardet
sys.setrecursionlimit(1500)
os.system("export PYTHONIOENCODING=UTF-8")
os.system("clear")

from unidecode import unidecode
# detect() language
from bs4 import BeautifulSoup, Comment# pip3 install --upgrade beautifulsoup4 && pip install html5li
import html
import unicodedata
from datetime import datetime as dTime
import subprocess 

# load my own modules
import modules.CosineSimilarity as cosine
import modules.Gensim as gSim
import modules.Wordify as wordify
import modules.Speechify as speechify
#import modules.Servify as servify
import modules.Sentify as sentify
import modules.TextGenify as genify
import modules.Fileify as fileify
import modules.CosineSimilarity as simify
import modules.Articlify as articlify
#python -c "import nltk; nltk.download()" -> Download -> all

from pprint import PrettyPrinter
pp 	= PrettyPrinter(indent=4)

subprocess.run("export GOOGLE_APPLICATION_CREDENTIALS='/home/buz/buzzgreator/key/100BiereTranslate-8a809e939d5e.json'", shell=True, check=True)
subprocess.run("export TREETAGGER_HOME='/home/buz/buzzgreator/treetagger/cmd'", shell=True, check=True)
MainKeyword	= ""
SubKeywords	= ""

"""
try:
	opts, args = getopt.getopt(sys.argv,"hm:s:",["mainkeyword=","subkeyword="])
except getopt.GetoptError:
	print('buzzgreator.py -m MainKeyword -s Subkeyword')
else:
	print(args)
	print(opts)
	for opt, arg in opts:
		if opt == '-h':
			print('buzzgreator.py -m MainKeyword -s Subkeyword')
			sys.exit()
		elif opt in ("-m", "--mainkeyword"):
			MainKeyword = arg
		elif opt in ("-s", "--subkeyword"):
			SubKeywords = arg
		else:
			print('buzzgreator.py -m MainKeyword -s Subkeyword')
			sys.exit()
"""
# python3 buzzgreator.py --mainkw "TEST1 Test1zwei" --subkw "TEST2 Test2_drei"
# python3 buzzgreator.py --mainkw "DSDS" --subkw "Dieter Bohlen" --session "2323"
parser = argparse.ArgumentParser()
parser.add_argument('--mainkw', action="append")
parser.add_argument('--subkw', action="append")
parser.add_argument('--session', action="append")
"""
parser.add_argument('--mainkw')
parser.add_argument('--subkw')
"""
args = parser.parse_args()
#print(args)
v=vars(args)
q1=" ".join(v["mainkw"])
q2=" ".join(v["subkw"])
q3=" ".join(v["session"])
MainKeyword	= q1.strip()
SubKeywords	= q2.strip()
SessionID	= q3.strip()
MainKeyword = wordify.encodeToUTF8Adv(MainKeyword)
SubKeywords = wordify.encodeToUTF8Adv(SubKeywords)
subKW		= SubKeywords.lower().strip().split(",")

print("MainKeyword:", MainKeyword)
print("SubKeywords:", SubKeywords)
print("SessionID:", SessionID)

# https://github.com/cemoody/lda2vec
####os.system('clear')
#https://github.com/explosion/sense2vec
"""
sumy lsa --text="Ich gehe mit meiner Freundin spazieren. Wir laufen im Wald und sehen Tiere. Es ist ein toller Tag." --language=german  --length=1
"""

ContentUrlList			= []
cpu_pool				= int(20) 	# cpu threads
multiCpuTasks			= set()
MinArticleCharLenght	= 5000

"""
allowedRuleString		= "-".join(allowedRule)
allowedRuleString 		= allowedRuleString.replace("PUNCT","")
allowedRuleString 		= allowedRuleString.replace("SPACE","")
allowedRuleString 		= re.sub(r"\s+", '-', allowedRuleString)
"""
StandardDirectory 		= "/home/buz/buzzgreator"		# path to work in
StoreDirectory 			= "/home/buz/buzzgreator/store"	# path to store all temp files 
TodayDirectory 			= "/home/buz/buzzgreator/store"	# path to store all temp 

now 					= datetime.datetime.now()
CurDate					= now.strftime("%Y-%m-%d")

TodayWorkDirectory		= TodayDirectory+"/"+CurDate
MainKeywordDir			= re.sub(r'\s+', '+', MainKeyword)
SubKeywordsDir			= re.sub(r'\s+', '+', SubKeywords)
WDir					= TodayWorkDirectory+"/"+MainKeywordDir.lower()
WDirSubKW				= TodayWorkDirectory+"/"+MainKeywordDir.lower()+"/"+SubKeywordsDir.lower()
WDirHtml				= WDirSubKW+"/html/"
WDirBinary				= WDirSubKW+"/bin/"

aCreatStart 			= str(dTime.now())
corpus=""
c1=""

if not os.path.exists(StandardDirectory):
    os.makedirs(StandardDirectory)
if not os.path.exists(StoreDirectory):
    os.makedirs(StoreDirectory)
if not os.path.exists(TodayWorkDirectory):
    os.makedirs(TodayWorkDirectory)
if not os.path.exists(WDir):
    os.makedirs(WDir)
if not os.path.exists(WDirHtml):
    os.makedirs(WDirHtml)
if not os.path.exists(WDirBinary):
    os.makedirs(WDirBinary)
if not os.path.exists(WDirSubKW):
    os.makedirs(WDirSubKW)

#### http://danielhnyk.cz/simple-server-client-aplication-python-3/


##### https://github.com/fnl/progress_bar
##### https://github.com/serge-sans-paille/pythran
###  pip3 freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip3 install -U


"""
	except Exception as ex:
		print("Unexpected error:", sys.exc_info()[0])
		pp.pprint(strerror)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
"""

def remove_non_ascii(text):
	return unidecode(text)

"""
wordify.getWikiPediaSummary(MainKeyword) Funktion ist buggy
"""

ContentUrlList = list()
#hier

### Call Google to fetch relevant Webpages
resList1=fileify.doGoogleSearch(MainKeyword, SubKeywords)
ContentUrlList.extend(resList1)
resList3 = fileify.DuckDuckGoSearch(MainKeyword, SubKeywords)
ContentUrlList.extend(resList3)
fileify.binaryWrite(ContentUrlList, WDirBinary+"extractedlinks.bin")

# Wikipedia Append
w_list1 	= wordify.getWikiPediaSummary(MainKeyword)
w_list2 	= wordify.getWikiPediaSummary(SubKeywords)
WikiLinks 	= w_list1[1] + w_list2[1]
w_list 		= w_list1[0] + w_list2[0]
fileify.binaryWrite(w_list, WDirBinary+"wikipediatexts.bin")
ContentUrlList.extend(WikiLinks)

fileify.binaryWrite(ContentUrlList, WDirBinary+"extractedlinks.bin")

ContentUrlList = fileify.binaryRead(WDirBinary+"extractedlinks.bin")

# get max of 50 links
#ContentUrlList = ContentUrlList[:50]

print("buzzgreator.countLinks(): ", len(ContentUrlList))

### Download the found Webpages
t_count 			= 0
ContentUniqueSet 	= set()
ret=False
#with pymp.Parallel(cpu_pool) as p:
for j in ContentUrlList:
#for i in p.range(len(ContentUrlList)):
	#j=ContentUrlList[i]
	if not isinstance(j, list):
		continue
	if len(j) !=2:
		continue
	
	t_sid	= j[0]
	t_link 	= str(j[1])
	t_count = t_count + 1
	# todo: MultiProcessing -> all fetch via pool, then 15 seconds pause, then extract 
	if t_link not in ContentUniqueSet:
		fileify.getWebpagesSimple(t_link, WDirHtml, ret)
		ContentUniqueSet.add(t_link)

### Extract HTML from downloaded Webpages
path = WDirBinary+"extractedtexts.bin"
if os.path.isfile(path):
	os.remove(path)

print(WDirHtml+"*.html")
files = glob.glob(WDirHtml+"*.html")
print("Count files:", len(files))
for file in files:
	t_fname = os.path.basename(file)
	print("buzzgreator.extractFromHTML()", file)
	t_temp	= t_fname.split(".")
	t_sid	= t_temp[0]
	f 		= open(file, 'r', encoding='utf-8')
	v 		= f.read()
	f.close()
	try:
		fileify.extractFromHTML(v, t_sid, WDirHtml, True)
	except (ValueError, KeyError, TypeError, Exception):
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)

# Read ExtractHtml created .bin-Files
f_list 	= []
files 	= glob.glob(WDirHtml+"/*.bin")
for file in files:
	print("Processing File:", file)
	f = fileify.binaryRead(file)
	f_list.append(f)
fileify.binaryWrite(f_list, WDirBinary+"extractedtexts.bin")
#hier


#Auslagern -> aufrufen, bevor die Funktion aufgerufen wurde
w_list1=wordify.getWikiPediaSummary(MainKeyword)
w_list2=wordify.getWikiPediaSummary(SubKeywords)
fileify.binaryWrite(w_list1, WDirBinary+"wikipediatexts_w_list1.bin")
fileify.binaryWrite(w_list2, WDirBinary+"wikipediatexts_w_list2.bin")
WikiLinks=w_list1[1] + w_list2[1]
WikiTexts=w_list1[0] + w_list2[0]

# Wikipedia Result corpus
t_WikiTextCorpus=wordify.getWikiPlainContent(WikiTexts)
fileify.binaryWrite(t_WikiTextCorpus, WDirBinary+"wikipediatexts.bin")

# Load WikiPedia Texts
t_WikiTextCorpus=fileify.binaryRead(WDirBinary+"wikipediatexts.bin")


### Load extracted Textinformation
f_list=fileify.binaryRead(WDirBinary+"extractedtexts.bin")
q = open(WDirBinary+"corpus.txt", 'w', encoding="utf-8")
for z in f_list:
	#print(type(z))
	for y in z:
		#print(type(y))
		tag 	= y['tag']
		content = y['content']
		#tel = {'hit':float(0),'shortid':shortid,'tag':tag,'content':t_returnString}
		if tag in "alltext":
			corpus = corpus + content + "\n"
corpus=wordify.beautifyCorpus(corpus)
q.write(corpus)
q.close

f_list=fileify.binaryRead(WDirBinary+"extractedtexts.bin")
corpus=fileify.plainRead(WDirBinary+"corpus.txt")
#corpus=c1+t_WikiTextCorpus
r_List=fileify.binaryRead(WDirBinary+"sortedPreResults.bin")

print("len(corpus plain):", len(corpus))
print("len(corpus beautify):", len(corpus))
print("len(f_list):", len(f_list))
print("len(r_List):", len(r_List))

if isinstance(r_List, list) and len(r_List)<1:
	ccount=0
	r_List=[]
	for z in f_list:
		for y in z:
			tag 	= y['tag']
			content = y['content']
			lang 	= wordify.intDetectLanguage(content)
			#tel = {'hit':float(0),'shortid':shortid,'tag':tag,'content':t_returnString}
			if lang in "de" and tag in "alltext" and len(content) >= MinArticleCharLenght and ccount < 150:
				ccount=ccount+1
				aStart = str(dTime.now())
				flVal = articlify.getBestArticleValue(content, corpus, w_list1, w_list2, MainKeyword, SubKeywords)
				y['hit']=flVal
				aEnd = str(dTime.now())
				print("getBestArticleValue() Start:", aStart)
				print("getBestArticleValue() End:", aEnd)
				print("getBestArticleValue() Current Value:", flVal)
				print("getBestArticleValue() Current Content length:", len(content))
				print()
				r_List.append([flVal,y])
				"""
				#if flVal>125 and len(content) < 45000:
				if flVal>=220 and len(content) < 45000:
					aStart = str(dTime.now())
					aArticleContent=articlify.beautifyArticle(y, corpus, MainKeyword, SubKeywords, WDirBinary)
					aEnd = str(dTime.now())
					fileify.binaryWrite(aArticleContent, WDirBinary+"articlecontent.bin")
					print("beautifyArticle() Start:", aStart)
					print("beautifyArticle() End:", aEnd)
				"""
	r_List=sorted(r_List, reverse=True, key=lambda x: x[0])
	fileify.binaryWrite(r_List, WDirBinary+"sortedPreResults.bin")

finalArticleContent=""
r_count=list(0,1,2)
for r in r_List:
	#if r_count == 0:
	for r in r_count:
		hit=r[0]
		y=r[1]
		content = y['content']
		print("hit:",hit)
		#print(type(y))
		#print("content:", len(content))
		aStart = str(dTime.now())
		aArticleContent=articlify.beautifyArticle(y, corpus, MainKeyword, SubKeywords, WDirBinary, SessionID)
		finalArticleContent+=aArticleContent
		aEnd = str(dTime.now())
		fileify.binaryWrite(aArticleContent, WDirBinary+"articlecontent.bin")
		print("beautifyArticle() Start:", aStart)
		print("beautifyArticle() End:", aEnd)
		exit(1)
	r_count=r_count+1

myArticlePlain=re.sub('\(\w{3}\)',' ', finalArticleContent)
print("Article:", wordify.encodeToLatin1(myArticlePlain))
aCreatEnd = str(dTime.now())
print("Start of Creation:", aCreatStart)
print("End of Creation:", aCreatEnd)
exit(1)