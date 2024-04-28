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
"""
import modules.CosineSimilarity as cosine
import modules.Gensim as gSim
import modules.Wordify as wordify
import modules.Speechify as speechify
"""
import modules.Servify as servify
"""
import modules.Sentify as sentify
import modules.TextGenify as genify
import modules.Fileify as fileify
import modules.CosineSimilarity as simify
import modules.Articlify as articlify
#python -c "import nltk; nltk.download()" -> Download -> all
"""
from pprint import PrettyPrinter
pp 	= PrettyPrinter(indent=4)

"""
MainKeyword	= ""
SubKeywords	= ""
# python3 buzzgreator.py --mainkw "TEST1 Test1zwei" --subkw "TEST2 Test2_drei"
# python3 buzzgreator.py --mainkw "Julia Jasmin Rühle" --subkw "Venus"
parser = argparse.ArgumentParser()
parser.add_argument('--mainkw', action="append")
parser.add_argument('--subkw', action="append")
parser.add_argument('--session', action="append")

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

"""
servify.start_server()
exit(1)