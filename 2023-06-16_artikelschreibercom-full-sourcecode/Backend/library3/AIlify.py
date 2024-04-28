# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore
"""
Copyright (c) 2023, Sebastian Enger, M.Sc.
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree (BSD-4-Clause). 

Frontend and Backend Source Code for Project:
- https://www.artikelschreiber.com/
- https://www.artikelschreiben.com/
- https://www.unaique.net/
"""
import re

import sys
sys.path.append('/home/unaique/library3')

import os
os.environ['TRANSFORMERS_CACHE'] 	= '/home/unaique/transformers_models_v3'
os.environ["MODEL_DIR"] 			= '/home/unaique/transformers_models_v3'
#os.environ['TRANSFORMERS_CACHE'] 	= '/dev/shm/'
#os.environ["MODEL_DIR"] 			= '/dev/shm'
os.environ['TF_CPP_MIN_LOG_LEVEL'] 	= '3'  # or any {'0', '1', '2'}
os.environ['TOKENIZERS_PARALLELISM']= 'true'

import openai	# https://github.com/openai/openai-python            pip install --upgrade openai
openai.api_key 						= "##################"

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import torch	# # pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu # https://pytorch.org/get-started/locally/
import random
from PIL import Image, ImageDraw, ImageFont

#import fasttext # pip3 install -U fasttext
import numpy as np
#from fasttext import load_model
#from fasttext import util
from scipy.spatial.distance import cosine
from numpy import dot
from numpy.linalg import norm

# START: Google knowledge_graph processing
import pandas as pd
import numpy as np
#import advertools # pip3 install advertools
#from advertools import knowledge_graph
import logging
serf_logger = logging.getLogger()
serf_logger.setLevel(logging.WARNING)
keyKG = '#################' # Google knowledge_graph API key
import signal
from contextlib import contextmanager
# END: Google knowledge_graph processing

import logging
logging.getLogger().disabled = True
logging.disable(logging.WARNING)
logging.disable(logging.INFO)

#import language_tool_python # pip3 install --upgrade language_tool_python
import warnings
warnings.filterwarnings("ignore")
#import concurrent.futures
#from concurrent.futures import ThreadPoolExecutor
#import collections
import os
import io
import json
import time
from time import sleep
import datetime
from datetime import datetime as dTime
#from sklearn.feature_extraction.text import CountVectorizer
#import contextualSpellCheck # pip3 install -U contextualSpellCheck
#import spacy  # See "Installing spaCy"

#from nltk.corpus import stopwords # https://stackoverflow.com/questions/48385829/how-to-install-stop-words-package-for-anaconda
#from textblob import TextBlob as TB			# python3 -m pip install -U textblob  python3 -m textblob.download_corpora
#from textblob_de import TextBlobDE as TBde		# python3 -m pip install -U textblob-de
#from tld import get_tld
#from tld import get_fld	#  pip3 install -U tld

#from googleapiclient.discovery import build
#from google.cloud import translate		#  pip3 install --upgrade google-cloud
#import numpy
#import subprocess
#from multiprocessing import Pool
#from multiprocessing.pool import ThreadPool
#from time import time as timer

#import wikipediaapi
#import wikipedia
#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
#import os, uuid, json
"""
import os
os.chdir('/home/unaique/transformers_models/translation_module/')
lang="de"
os.system("git clone https://huggingface.co/Helsinki-NLP/opus-mt-"+lang+"-en")
os.system("git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-"+lang)
"""
#from transformers import MarianTokenizer, MarianMTModel

# pip3 install -U pattern
# pip3 install -U transformers
import torch # pip3 install -U transformers torch spacy gensim
import transformers
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelWithLMHead, pipeline

# pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu # https://pytorch.org/
from transformers import T5Config, T5ForConditionalGeneration, T5Tokenizer #, pipeline
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

transformers.logging.set_verbosity(50)
# pip3 install -U tokenizers
#from datetime import datetime

#tokenizer_sentences 	= AutoTokenizer.from_pretrained('xlm-roberta-base')
tokenizer_sentences 	= AutoTokenizer.from_pretrained('/home/unaique/transformers_models_v3/xlm-roberta-base')
# git clone https://huggingface.co/xlm-roberta-base

import sys
sys.path.append('/home/unaique/library3')
#import Rankify as rankify
#import library.Gensim as gSim
#import library.Matchify as mtchify
#import library.Encodify as encodify
###import library.DBify as dbify
#import library.Textify as textify
#import library.Htmlify as htmlify
#import library.Simplify as sentSimpler
#import library.Gensim as gSim

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#import mlconjug3 # pip3 install -U mlconjug3
#from fasttext import train_supervised	# pip3 install -U fasttext
#import fasttext

import math
#from Plagscan import PlagiarismChecker
from difflib import SequenceMatcher

#from Rankify import split_into_sentences as split_sentences

import yake # pip3 install -U yake -> https://github.com/LIAAD/yake

language_en				= "en"
language_de				= "de"
language_es				= "es"
language_fr				= "fr"
language_it				= "it"
language_ru				= "ru"
language_zh				= "zh"
language_pt				= "pt"
language_jp				= "ja"
language_hi				= "hi"
language_ar				= "ar"
language_tr				= "tr"

max_ngram_size 			= 1
deduplication_thresold 	= 0.9
deduplication_algo 		= 'seqm'
windowSize 				= 1
numOfKeywords 			= 15

# https://github.com/LIAAD/yake/tree/master/yake/StopwordsList
custom_kw_extractor_en 	= yake.KeywordExtractor(lan=language_en, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_de 	= yake.KeywordExtractor(lan=language_de, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_es 	= yake.KeywordExtractor(lan=language_es, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_fr 	= yake.KeywordExtractor(lan=language_fr, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_it 	= yake.KeywordExtractor(lan=language_it, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_ru 	= yake.KeywordExtractor(lan=language_ru, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_zh 	= yake.KeywordExtractor(lan=language_zh, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_pt 	= yake.KeywordExtractor(lan=language_pt, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_jp 	= yake.KeywordExtractor(lan=language_jp, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_hi 	= yake.KeywordExtractor(lan=language_hi, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_ar 	= yake.KeywordExtractor(lan=language_ar, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
custom_kw_extractor_tr 	= yake.KeywordExtractor(lan=language_tr, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)


#https://keywordseverywhere.com/api-key.html?code=#########
# https://keywordseverywhere.com/credits.html?apiKey=###########&id=127452
KW_EVERYWHERE_API 	= "###########"

WordsBeforePriorityItemAdvanced = 7 # erst nach 7 Wörtern in Subkeyword und Mainkeyword -> Idee: ASCOM: Wenn mehr als x Wörter bei MK und SK dann nutze PriorityItem in vollem Funktionsumfang (Stanza Support)


class AI:
	def __init__(self):
		self.description 	= "AI related Functions for ArtikelSchreiber.com Backend"
		self.openai_key 	= str("################")	# test-key
		#self.openai_key 	= str("")	# production-key

	def set_global_logging_level(self, level=logging.ERROR, prefices=[""]):
		"""
		Source: https://github.com/huggingface/transformers/issues/3050#issuecomment-682167272
		Override logging levels of different modules based on their name as a prefix.
		It needs to be invoked after the modules have been loaded so that their loggers have been initialized.

		Args:
			- level: desired level. e.g. logging.INFO. Optional. Default is logging.ERROR
			- prefices: list of one or more str prefices to match (e.g. ["transformers", "torch"]). Optional.
			  Default is `[""]` to match all active loggers.
			  The match is a case-sensitive `module_name.startswith(prefix)`
		"""
		prefix_re = re.compile(fr'^(?:{ "|".join(prefices) })')
		for name in logging.root.manager.loggerDict:
			if re.match(prefix_re, name):
				logging.getLogger(name).setLevel(level)

	set_global_logging_level(logging.ERROR)

	####
	## ABSTRACTIVE SUMMARZIZER
	####
	WHITESPACE_HANDLER 		= lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))


	def topicModeling(self, blob_of_text, p_textlanguage):
		###print("gensim.topicModelingViaKeywords()")
		keywords		= list()
		results			= set()
		resList 		= list()
		try:
			if p_textlanguage.lower() == "de":
				keywords	= custom_kw_extractor_de.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "en":
				keywords	= custom_kw_extractor_en.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "fr":
				keywords	= custom_kw_extractor_fr.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "es":
				keywords	= custom_kw_extractor_es.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "it":
				keywords	= custom_kw_extractor_it.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "ru":
				keywords	= custom_kw_extractor_ru.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "zh" or p_textlanguage.lower() == "cn":
				keywords	= custom_kw_extractor_zh.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "jp":
				keywords	= custom_kw_extractor_jp.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "pt":
				keywords	= custom_kw_extractor_pt.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "hi" or p_textlanguage.lower() == "in":
				keywords	= custom_kw_extractor_hi.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "ar" or p_textlanguage.lower() == "sa":
				keywords	= custom_kw_extractor_ar.extract_keywords(blob_of_text)
			elif p_textlanguage.lower() == "tr":
				keywords	= custom_kw_extractor_tr.extract_keywords(blob_of_text)
			else:
				keywords	= custom_kw_extractor_en.extract_keywords(blob_of_text)

			for kw in keywords:
				results.add(str(kw[0]))
		except Exception as ae1:
			pass

		resList = list(results)
		#finList = resList[:25]
		return str(";".join(resList))


	def plagiarismChecker(self, org, ai):
		# https://www.codespeedy.com/sequencematcher-in-python/
		# https://www.geeksforgeeks.org/compare-sequences-in-python-using-dfflib-module/
		sequence 	= SequenceMatcher(None, a=org.lower(), b=ai.lower(), autojunk=True) #comparing both the strings
		s			= sequence.ratio()
		plagScore	= int(float("{0:.2f}".format(s))*100)
		return plagScore


	# Reference: https://discuss.huggingface.co/t/summarization-on-long-documents/920/7
	def create_nest_sentences_ai(self, rankify_obj, document:str, token_max_length):
		nested 		= list()
		sent 		= list()
		length 		= int(0)
		#tokenizer 	= AutoTokenizer.from_pretrained('xlm-roberta-base')
		#for sentence in sentences_list:
		for sentence in rankify_obj.split_sentences(document):
			tokens_in_sentence = tokenizer_sentences(str(sentence), truncation=True, padding=True)[0] # hugging face transformer tokenizer
			length += len(tokens_in_sentence)
			if length < token_max_length:
				sent.append(sentence)
			else:
				nested.append(sent)
				sent 		= list()
				length 	= int(0)
		if sent:
			nested.append(sent)

		return nested

	#def summarizer_gen(summarizer, sequence:str, maximum_tokens:int, minimum_tokens:int):
	#	output = summarizer(sequence, num_beams=4, max_length=maximum_tokens, min_length=minimum_tokens, do_sample=False)
	#	#return output[0].get('summary_text')
	#	return str(output[0].get('summary_text'))

	# Reference: https://huggingface.co/facebook/bart-large-mnli
	def load_summary_model(self, language):	# git clone https://huggingface.co/uer/pegasus-base-chinese-cluecorpussmall
		# pip3 install -U tokenizers
		"""
		LOCAL DOWNLOAD PATHS ARE CORRECT
		"""
		model_name_it 	= "/home/unaique/transformers_models_v3/it5-base-news-summarization" 				# https://huggingface.co/ARTeLab/it5-summarization-mlsum/tree/main
		model_name_de 	= "/home/unaique/transformers_models_v3/T5-Base_GNAD"	# de
		model_name_en	= "/home/unaique/transformers_models_v3/pegasus-xsum"					# en google/pegasus-xsum https://huggingface.co/google/pegasus-xsum/tree/main
		model_name_fr	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/" 		# https://huggingface.co/WikinewsSum/t5-base-with-title-multi-fr-wiki-news
		model_name_zh	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/" 		# chinese: https://huggingface.co/uer/pegasus-base-chinese-cluecorpussmall
		model_name_ru	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/"
		model_name_es	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/" 		# spanish: https://huggingface.co/josmunpen/mt5-small-spanish-summarization
		model_name_tr 	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/"
		model_name_jp	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/"		# git clone https://huggingface.co/csebuetnlp/mT5_multilingual_XLSum
		model_name_pt	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/"
		model_name_hi	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/"
		model_name_ar	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/"
		model_name_xx 	= "/home/unaique/transformers_models_v3/mT5_multilingual_XLSum/"

		my_model_name 	= str("")
		if language.lower() == "de":
			my_model_name 	= model_name_de
		elif language.lower() == "en":
			my_model_name 	= model_name_en
		elif language.lower() == "it":
			my_model_name 	= model_name_it
		elif language.lower() == "fr":
			my_model_name 	= model_name_fr
		elif language.lower() == "zh" or language.lower() == "cn":
			my_model_name 	= model_name_zh
		elif language.lower() == "ru":
			my_model_name 	= model_name_ru
		elif language.lower() == "es":
			my_model_name 	= model_name_es
		elif language.lower() == "jp" or language.lower() == "ja":
			my_model_name 	= model_name_jp
		elif language.lower() == "pt":
			my_model_name 	= model_name_pt
		elif language.lower() == "hi" or language.lower() == "in":
			my_model_name 	= model_name_hi
		elif language.lower() == "ar" or language.lower() == "sa":
			my_model_name 	= model_name_ar
		elif language.lower() == "tr":
			my_model_name 	= model_name_tr
		else:
			my_model_name = model_name_xx

		summarizer 		= pipeline(task='summarization', model=my_model_name)
		return summarizer

	def abstractiveSummarizer(self, rankify_obj, language, text, enableFastmode):
		if enableFastmode:
			return str("")

		summary 				= list()
		final_summary			= list()

		try:
			"""
			load1, load5, load15 	= psutil.getloadavg()

			if load1 > 7:
				cut_at_word_count	= 600
			elif load1 > 6:
				cut_at_word_count	= 1200
			elif load1 > 4:
				cut_at_word_count	= 3500
			else:
				cut_at_word_count	= 7500
			"""

			cut_at_word_count	= 7500	# ca 10 Seiten Text
			text_tmp			= text.replace("-", " ")
			words 				= len(text_tmp.split(" "))
			if words > cut_at_word_count:
				#word_tokens 	= text.replace("\n"," ").split(" ")
				word_tokens 	= text.replace("\n","").split(" ")
				word_token_1000	= word_tokens[0:cut_at_word_count]	# reduziere den Inhalt auf 750 Wörter
				text1			= " ".join(word_token_1000)
				text1			= text1.replace(".",". ")
				text1			= text1.replace("!","! ")
				text1			= text1.replace("?","? ")
				text 			= text1
				str_test 		= text[-3:]	# letzten drei zeichen vom String
				if str_test.count('.') == 1 or str_test.count('!') == 1 or str_test.count('?') == 1:
					1
				else:
					text 		= text + "."

			#load1, load5, load15 = psutil.getloadavg()
			countWords      	= rankify_obj.count_words_regex(text)
			if countWords >= 10000:
				token_length 	= 512 	#2048 - 512 is the max the DL model can process
			elif countWords >= 5500:
				token_length 	= 448 	#1024
			elif countWords >= 2500:
				token_length 	= 384	#512
			elif countWords >= 1500:
				token_length 	= 192
			elif countWords >= 1000:
				token_length 	= 145 	#128
			elif countWords >= 500:
				token_length 	= 100	# 64
			else:
				token_length 	= 128

			summarizer			= self.load_summary_model(language)
			#print(type(summarizer))

			nested_sentences 	= self.create_nest_sentences_ai(rankify_obj, document = text, token_max_length = token_length)
			sentEndings			= ['.','!','?']

			for n in range(0, len(nested_sentences)):
				chunk_summary	= list()
				lastChar 		= str("")
				text_chunk 		= " ".join(map(str, nested_sentences[n]))
				#output 			= summarizer(text_chunk, num_beams=4, max_length=150, min_length=15, do_sample=True, clean_up_tokenization_spaces=True)	# https://huggingface.co/docs/transformers/v4.15.0/en/main_classes/pipelines#transformers.SummarizationPipeline
				output 			= summarizer(text_chunk, num_beams=2, clean_up_tokenization_spaces=True)
				chunk_summary	= str(output[0].get('summary_text'))
				sents 			= rankify_obj.split_sentences(chunk_summary)	# from Rankify import split_into_sentences as split_sentences
				if len(sents) > 0:
					for sent in sents:
						myChunkList		= list(sent.strip())
						lastChar 		= myChunkList[-1]
						isBadTextFlag	= rankify_obj.isCode(sent)
						#print("Lastchar:'"+lastChar+"'")
						if sentEndings.count(lastChar) == 1 and not isBadTextFlag and len(sent) > 5:
							summary.append(sent)
				else:
					summary.append(chunk_summary)

			final_summary 		= str(" ".join(summary))

			# RAM Sparen
			del nested_sentences
			del summarizer
			del summary

		except Exception as aas1:
		#	#print(aas1)
			pass

		return final_summary

	def genereteContentByOpenAIAdvanced(self, MainKeyword, SubKeywords, related_searches, Language):
		teler			= dict()
		teler["openai"]	= str("")
		seo_keywords	= str("")

		if len(related_searches) < 1:
			related_searches = [MainKeyword]
		else:
			for kw in related_searches:
				if len(kw) > 1:
					seo_keywords += str('"'+kw+'", ')

		myLanguage 			= str("Deutsch")
		if Language.lower() == "en":
			myLanguage 		= str("Englisch")
			myBlogLanguage 	= str("en")
		elif Language.lower() == "de":
			myLanguage 		= str("Deutsch")
			myBlogLanguage 	= str("de")
		elif Language.lower() == "es":
			myLanguage 		= str("Spanisch")
			myBlogLanguage 	= str("es")
		elif Language.lower() == "fr":
			myLanguage 		= str("Französisch")
			myBlogLanguage 	= str("fr")
		elif Language.lower() == "it":
			myLanguage 		= str("Italienisch")
			myBlogLanguage 	= str("it")
		elif Language.lower() == "ru":
			myLanguage 		= str("Russisch")
			myBlogLanguage 	= str("ru")
		elif Language.lower() == "zh" or Language.lower() == "cn":
			myLanguage 		= str("Chinesisch")
			myBlogLanguage 	= str("cn")
		elif Language.lower() == "jp" or Language.lower() == "ja":
			myLanguage 		= str("Japanisch")
			myBlogLanguage 	= str("jp")
		elif Language.lower() == "pt":
			myLanguage 		= str("Portugisisch")
			myBlogLanguage 	= str("pt")
		elif Language.lower() == "hi" or Language.lower() == "in":
			myLanguage 		= str("Indisch")
			myBlogLanguage 	= str("in")
		elif Language.lower() == "ar" or Language.lower() == "sa":
			myLanguage 		= str("Arabisch")
			myBlogLanguage 	= str("sa")
		elif Language.lower() == "tr":
			myLanguage 		= str("Türkisch")
			myBlogLanguage 	= str("tr")

		if (MainKeyword != SubKeywords) and len(MainKeyword) > 1 and len(SubKeywords) > 1:
			instructions = str('Schreibe mir einen viralen Artikel zum Thema "'+MainKeyword+'", "'+SubKeywords+'". Schreibe in einem informativen, aber auch humorvollen Schreibstil, wobei du als professioneller Journalist und Blogautor schreibst, der sich mit Betriebswirtschaft und Marketing exzellent auskennt. Deine Zielgruppe ist 16-35. Deine Texte schreibst du plagiatsfrei in perfektem '+myLanguage+' ohne Schreibfehler. Optimiere den Blogartikel auf die SEO Keywords: '+seo_keywords+'. Ziel der SEO Optimierung ist es mittels Suchmaschinen mehr Besucher für meinen Blog zu gewinnen.')
		else:
			instructions = str('Schreibe mir einen viralen Artikel zum Thema "'+MainKeyword+'". Schreibe in einem informativen, aber auch humorvollen Schreibstil, wobei du als professioneller Journalist und Blogautor schreibst, der sich mit Betriebswirtschaft und Marketing exzellent auskennt. Deine Zielgruppe ist 16-35. Deine Texte schreibst du plagiatsfrei in perfektem '+myLanguage+' ohne Schreibfehler. Optimiere den Blogartikel auf die SEO Keywords: '+seo_keywords+'. Ziel der SEO Optimierung ist es mittels Suchmaschinen mehr Besucher für meinen Blog zu gewinnen.')

		"""
		 messages=[
		        {"role": "system", "content": "You are a helpful assistant."},
		        {"role": "user", "content": "Knock knock."},
		        {"role": "assistant", "content": "Who's there?"},
		        {"role": "user", "content": "Orange."},
		    ],
		"""
		#in {"role": "user", "content": info_text} dort das reinpacken:
		try:
			completion 			= openai.ChatCompletion.create(
				model			= "gpt-3.5-turbo",
				temperature 	= 0.85,	# https://platform.openai.com/docs/api-reference/chat/create
				n 				= 1,
				max_tokens 		= 1241,
				presence_penalty = 0.5,
				frequency_penalty= 0.5,
				user			="artikelschreiber.com", #https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
				messages		= [
					#{"role": "system", "content": add_instructions},
					{"role": "user", "content": instructions}
				]
				)
			#print(completion.choices[0].message.content)
			#return str(completion.choices[0].message.content)
			teler["openai"]	= str(completion.choices[0].message.content)
		except openai.error.OpenAIError as e:
			#print("AIIlify.genereteContentByOpenAIAdvanced(text, language) Error:")
			#print(e.http_status)
			#print(e.error)
			pass

		return teler

	def genereteContentByOpenAI(self, text, language):
		info_text 				= (text[:100]) if len(text) > 100 else text
		teler					= dict()
		teler["openai"]			= str("")
		teler["language"]		= str(language)
		add_instructions 		= str("")
		if language.lower() == "de":
			add_instructions1 	= "Sie sind ein erfahrener Journalist,der in einem beschreibenden, objektiven Stil einen positiven Ton anschlägt und wertvolle Informationen liefert.Sie schreiben einen plagiatsfreien Text in deutscher Sprache.Schreibe einen Artikel über "
			#add_instructions2 	= "Sie sind ein erfahrener Journalist,der in einem beschreibenden, objektiven Stil einen positiven Ton anschlägt und wertvolle Informationen liefert.Sie schreiben einen plagiatsfreien Text in deutscher Sprache."
		elif language.lower() == "fr":
			add_instructions1 	= "Vous gardez un ton positif dans un style descriptif et objectif et vous fournissez des informations précieuses.Vous rédigez un texte sans plagiat en langue française.Écrire un article sur "
			#add_instructions2 	= "Vous gardez un ton positif dans un style descriptif et objectif et vous fournissez des informations précieuses.Vous rédigez un texte sans plagiat en langue française."
		elif language.lower() == "es":
			add_instructions1 	= "Mantén un tono positivo en un estilo descriptivo y objetivo y proporciona información valiosa.Redactas textos libres de plagio en lengua española.Escriba un artículo sobre "
			#add_instructions2 	= "Mantén un tono positivo en un estilo descriptivo y objetivo y proporciona información valiosa.Redactas textos libres de plagio en lengua española."
		elif language.lower() == "it":
			add_instructions1 	= "Agite come se foste un giornalista esperto, mantenendo un tono positivo in uno stile descrittivo e oggettivo e fornendo informazioni preziose.Scrivete un testo senza plagio in lingua italiana.Scrivere un articolo su "
			#add_instructions2 	= "Agite come se foste un giornalista esperto, mantenendo un tono positivo in uno stile descrittivo e oggettivo e fornendo informazioni preziose.Scrivete un testo senza plagio in lingua italiana."
		elif language.lower() == "en":
			add_instructions1 	= "Act as you are an expert journalist writer.You keep the tone positive in a descriptive,objective style and provide valuable information.You write plagiarism free text in English language.Write an article about "
			#add_instructions2 	= "Act as you are an expert journalist writer.You keep the tone positive in a descriptive,objective style and provide valuable information.You write plagiarism free text in English language."
		else:
			add_instructions1 	= "Act as you are an expert journalist writer.You keep the tone positive in a descriptive,objective style and provide valuable information.You write plagiarism free text in English language.Write an article about "
			#add_instructions2 	= "Act as you are an expert journalist writer.You keep the tone positive in a descriptive,objective style and provide valuable information.You write plagiarism free text in English language."
		#print("debug:"+add_instructions)
		"""
		 messages=[
		        {"role": "system", "content": "You are a helpful assistant."},
		        {"role": "user", "content": "Knock knock."},
		        {"role": "assistant", "content": "Who's there?"},
		        {"role": "user", "content": "Orange."},
		    ],
		"""
		"""
		try:	# Qualität zu Schlecht!
			completion1 			= openai.Completion.create(
				model				= "babbage",	# 0.0005 Cent pro 1000 Token (750 Words)
				temperature 		= 0.9,	# https://platform.openai.com/docs/api-reference/chat/create
				n 					= 1,
				max_tokens 			= 1022,
				presence_penalty 	= 0.33,
				frequency_penalty	= 0.33,
				prompt				= add_instructions1+" "+info_text,
				user				= "artikelschreiber.com", #https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
				#messages		= [
				#	{"role": "system", "content": add_instructions},
				#	{"role": "user", "content": info_text}
				#]
				)
			#print(completion.choices[0].message.content)
			#return str(completion.choices[0].message.content)
			teler["openai"]	= str(completion1.choices[0].text)
			print("Mainify.openAI Text :",str("babbage"))
			return teler	# hier ist ein Return!!!!
		except openai.error.OpenAIError as e:
			print("AIIlify.genereteContentByOpenAI(text, language) Error:")
			print(e.http_status)
			print(e.error)
		"""
		try:
			completion2 			= openai.ChatCompletion.create(
				model				= "gpt-3.5-turbo",	# 0.002 Cent pro 1000 Token (750 Words)
				temperature 		= 0.881,	# https://platform.openai.com/docs/api-reference/chat/create
				n 					= 1,
				max_tokens 			= 422,
				presence_penalty 	= 0.53,
				frequency_penalty	= 0.53,
				user				="artikelschreiber.com", #https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
				messages			= [
					{"role": "system", "content": add_instructions1},
					{"role": "user", "content": info_text}
				]
			)
			#print(completion.choices[0].message.content)
			#return str(completion.choices[0].message.content)
			teler["openai"]	= str(completion2.choices[0].message.content)
			#print("Mainify.openAI Text :",str("gpt-3.5-turbo"))
		except openai.error.OpenAIError as e:
			print("AIIlify.genereteContentByOpenAI(text, language) Error:")
			print(e.http_status)
			print(e.error)

		return teler

	def isGoodContent(self, text):
		try:
			response = openai.Moderation.create(
			    input=text
			)

			is_forbidden1 = response["results"][0]['categories']['hate']
			is_forbidden2 = response["results"][0]['categories']['hate/threatening']
			is_forbidden3 = response["results"][0]['categories']['self-harm']
			is_forbidden4 = response["results"][0]['categories']['sexual']
			is_forbidden5 = response["results"][0]['categories']['sexual/minors']
			is_forbidden6 = response["results"][0]['categories']['violence']
			is_forbidden7 = response["results"][0]['categories']['violence/graphic']
			"""
			print("Debug is_forbidden1:",str(is_forbidden1))
			print("Debug is_forbidden2:",str(is_forbidden2))
			print("Debug is_forbidden3:",str(is_forbidden3))
			print("Debug is_forbidden4:",str(is_forbidden4))
			print("Debug is_forbidden5:",str(is_forbidden5))
			print("Debug is_forbidden6:",str(is_forbidden6))
			print("Debug is_forbidden7:",str(is_forbidden7))
			"""
			if not is_forbidden1 and not is_forbidden2 and not is_forbidden3 and not is_forbidden4 and not is_forbidden5 and not is_forbidden6 and not is_forbidden7:
				return True
			else:
				return False

		except openai.error.OpenAIError as e:
			print("AIIlify.genereteContentByOpenAI(text, language) Error:")
			print(e.http_status)
			print(e.error)

		return False

	def countFalse(self, lst):
		# https://www.geeksforgeeks.org/python-count-true-booleans-in-a-list/
		return int(lst.count(False))
