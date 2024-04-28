# -*- coding: utf-8 -*-
#!/usr/bin/env python3

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

# pip3 install --upgrade spacy tensorflow gensim sumy keras markovify google-api-python-client beautifulsoup4

# https://stackoverflow.com/questions/35569042/ssl-certificate-verify-failed-with-python3
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import gc
import warnings
warnings.filterwarnings("ignore")
import codecs
import logging
#logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
logging.getLogger().disabled = True

# add the handlers to the logger
import os
import time
import json
import stat
import datetime
from datetime import datetime as dTime
from datetime import date
import psutil	# pip3 install -U psutil https://www.geeksforgeeks.org/how-to-get-current-cpu-and-ram-usage-in-python/
import sqlite3 as sql3

from random import randint
from time import sleep


sql3_lite_db 	= "/home/unaique/library3/sqlite/nodouble.sqlite"
# https://www.pragmaticlinux.com/2020/12/monitor-cpu-and-ram-usage-in-python-with-psutil/

from bionic_reading import BionicReading	# Bionic reading: https://github.com/Jwuthri/Riffling

import sys
sys.path.append('/home/unaique/library3')

#from pprint import pprint
#aTime 						= datetime.datetime.now()

from AIlify import AI
myAI = AI()
from Rankify import Rank
myRank = Rank()
#print(type(myRank))

class Suble:
	def __init__(self):
		self.description = "Contains all main functions for v3 ArtikelSchreiber.com"

	def mainFunktionSublinify(self, MainKeyword, SubKeywords, SessionID, Language, IPAddress):
		MainKeyword				= MainKeyword.strip() #str(MainKeyword.strip())
		SubKeywords				= SubKeywords.strip() #str(SubKeywords.strip())

		ip_obj 					= myRank.getGeoInformationAdvanced(IPAddress)
		enableFastmode 			= myRank.useFastmode(MainKeyword+" "+SubKeywords)
		my_ip_info				= str(ip_obj.get("ip_hostname")+" # "+ip_obj.get("ip_country")+" : "+ip_obj.get("ip_region")+" -> "+ip_obj.get("ip_city"))

		sessionType 			= "artikelschreiber"
		articleSuccessPoints	= int(0)
		points 					= int(0)
		results 				= list()
		myResultElement 		= dict() #str("")
		resultList 				= list()
		tel						= dict()
		resultList 				= list()
		related_searches		= list()
		ai_enabled_openai		= False

		MainKeyword_Entity		= myRank.fixBrokenHTMLEntities(MainKeyword)
		SubKeywords_Entity 		= myRank.fixBrokenHTMLEntities(SubKeywords)

		SessionID				= str(SessionID.strip())
		Language				= str(Language.lower().strip())
		aTime 					= datetime.datetime.now()
		MainKeyword 			= MainKeyword.replace("+"," ")
		SubKeywords 			= SubKeywords.replace("+"," ")
		MainKeyword 			= MainKeyword.replace("#","")
		SubKeywords 			= SubKeywords.replace("#","")
		IPAddress				= str(IPAddress)

		if SessionID.find("API") != -1:
			return 1
			# if SessionID == unaiquecom: do AI stuff

		try:
			source 				= sql3.connect(sql3_lite_db)
			cursor 				= source.cursor()
			timestamp1 			= int(time.time())
			IPAddress			= str(IPAddress)
			key3 				= str(MainKeyword+SubKeywords+IPAddress).strip().lower().replace(" ","")
			addingValues2 		= "SELECT timestamp FROM doubleentries WHERE key ='"+str(key3)+"'"
			cursor.execute(addingValues2)
			source.commit()
			timestamp2 			= int(cursor.fetchall()[0][0])
			source.close()

			if timestamp2 + int(1900) >= timestamp1:
				sec2 = str(timestamp1-timestamp2)
				#print("Mainify.mainFunktion: NoDoubleException(): mk="+MainKeyword+", sk="+SubKeywords)
				#print("Mainify.mainFunktion: NoDoubleException(): Intervall:"+sec2+"/1800 seconds")
				gc.collect()
				return False
			else:
				source 				= sql3.connect(sql3_lite_db)
				cursor 				= source.cursor()
				timestamp1 			= int(time.time())
				IPAddress			= str(IPAddress)
				key3 				= str(MainKeyword+SubKeywords+IPAddress).strip().lower().replace(" ","")
				addingValues3 		= "UPDATE doubleentries SET timestamp = '"+str(timestamp1)+"' WHERE key = '"+str(key3)+"'"
				cursor.execute(addingValues3)
				source.commit()
				source.close()
				#print("Mainify.mainFunktion: NoDoubleException(): Updated timestamp for key='"+str(key3)+"'")
		except Exception as aas1:
			pass

		# https://mymasterdesigner.com/2021/09/12/sqlite-database-with-python-for-data-science/
		try:
			source 				= sql3.connect(sql3_lite_db)
			cursor 				= source.cursor()
			now3 				= int(time.time())
			IPAddress			= str(IPAddress)
			key 				= str(MainKeyword+SubKeywords+IPAddress).strip().lower().replace(" ","")
			addingValues 		= "INSERT INTO doubleentries (timestamp, key) VALUES ('"+str(now3)+"','"+str(key)+"')"
			cursor.execute(addingValues)
			source.commit()
			source.close()
		except Exception as aa1:
			pass

		myBlogLanguage 		= str("")
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

		load1, load5, load15 = psutil.getloadavg()
		#ipInfo4 			 = myRank.getGeoInformationForLogging(IPAddress)
		i 					= datetime.datetime.now()
		tt_time 			= i.isoformat().split('.', 1)[0]
		print()
		print("######################################################")
		print("Mainify.mainFunktion:"+" "+str(SessionID))
		print("Mainify.Language    :",myLanguage)
		#myMK 				= MainKeyword #encodify.encodeToUTF8Adv(MainKeyword)
		#mySK 				= SubKeywords #encodify.encodeToUTF8Adv(SubKeywords)
		print("Mainify.MainKeyword :",MainKeyword_Entity)
		print("Mainify.SubKeywords :",SubKeywords_Entity)
		print("Mainify.IPAddress   :",str(my_ip_info))
		print("Mainify.ServerLoad  :",str(load1))
		print("Mainify.CurrentTime :",str(tt_time))
		print("Mainify.FastMode    :",str(enableFastmode))

		if SessionID.find("UNAIQUECOM") != -1:
			teler					= dict()
			print("Mainify.openAI Text :",str("True"))
			#teler 					= myAI.genereteContentByOpenAI(MainKeyword, Language)
			#teler					= myAI.genereteContentByOpenAIAdvanced(MainKeyword, SubKeywords, related_searches, Language)
			for element in range(5):
				teler			= myAI.genereteContentByOpenAIAdvanced(MainKeyword, SubKeywords, related_searches, Language)
				openaiContent	= teler.get("openai",str(""))
				if len(openaiContent) > 10:
					tel["openai"]		= openaiContent
					ai_enabled_openai 	= True
					break
				else:
					sleep(randint(15,25))

			myOpenai				= teler.get("openai")
			isMyContentGood			= myAI.isGoodContent(myOpenai)
			teler["isGoodContent"]	= isMyContentGood

			with codecs.open("/home/www/logs/ARTIKELSCHREIBER/2023_artikelschreiben.log", 'a+', encoding='utf-8') as fa:
				#fa.write(str(SessionID)+"###"+str(MainKeyword)+"###"+str(SubKeywords)+"###"+str(myLanguage)+"###"+str(ipInfo4)+"###"+str("")+"###"+str("")+"\n")
				fa.write(str(tt_time)+"###"+str(SessionID)+"###"+str(MainKeyword)+"###"+str(SubKeywords)+"###"+str(myLanguage)+"###"+str(my_ip_info)+"\n")
			fa.close()

			try:
				p_datastorage		= json.dumps(teler, ensure_ascii=False)
				dataFile			= "/home/www/security/unaiqueASCOM/latest_artikelschreibencom.json"
				if os.path.exists(dataFile):
					os.unlink(dataFile)
				f = open(dataFile, "w", encoding='utf-8')
				f.write(p_datastorage)
				f.close()

				os.system("chown www-data:www-data "+dataFile)
				os.system("chmod 755 "+dataFile)

			except Exception as a1:
				pass

			try:
				p_datastorage		= json.dumps(teler, ensure_ascii=False)
				dataFile			= "/home/www/security/unaiqueASCOM/"+str(SessionID)+"_"+str(Language)+".json"
				if os.path.exists(dataFile):
					os.unlink(dataFile)
				f = open(dataFile, "w+", encoding='utf-8')
				f.write(p_datastorage)
				f.close()

				os.system("chown www-data:www-data "+dataFile)
				os.system("chmod 755 "+dataFile)

				print("Mainify.openAI Text :",str("Done"))
				print("######################################################")

			except Exception as a1:
				pass

			finally:
				gc.collect()
				del teler
				return True

		#search_query						= str(MainKeyword+", "+SubKeywords)
		serp_obj 							= myRank.doSerpSearch(MainKeyword, SubKeywords, Language, ip_obj)
		#print("issuccess",serp_obj)
		print("Mainify.SerpSearch 1:",str(serp_obj.get("isSuccess",False)))

		if serp_obj.get("isSuccess",False):
			my_serp_organic_results_object 	= serp_obj.get("serp_organic_results", list())
			print("Mainify.SerpResults :",len(my_serp_organic_results_object))
			#print("my_serp_organic_results_object",my_serp_organic_results_object)
			my_serp_related_searches_object	= serp_obj.get("serp_related_searches", list())
			#print("my_serp_related_searches_object",my_serp_related_searches_object)

			my_count_max 	= 5
			my_count 		= int(0)
			for rs_obj in my_serp_related_searches_object:
				rs 							= rs_obj.get("related_searches","")
				if len(rs) > 1:
					related_searches.append(rs)
				if my_count > my_count_max:
					break

			#print("related_searches",related_searches)
			my_count_max 	= 35
			my_count 		= int(0)
			for or_obj in my_serp_organic_results_object:
				my_url	 					= or_obj.get("organic_results_link","")
				if len(my_url) > 1:
					resultList.append(my_url)
					my_count += int(1)

				if my_count > my_count_max:
					break
				# hinweis: das update.object in Zeile 281 auch noch auskommentieren!

		if len(resultList) < 1:
			# Wenn keine Ergebnisse, dann versuche es mit anderen Spracheinstellungen, den gegenüberliegenden, aus Deutsch mache dann Englisch
			if Language.lower() == "en":
				myLanguage 		= str("de")
			elif Language.lower() == "de":
				myLanguage 		= str("en")
			else:
				myLanguage 		= str("en")

			serp_obj 							= myRank.doSerpSearch(MainKeyword, SubKeywords, myLanguage, ip_obj)
			print("Mainify.SerpSearch 2:",str(serp_obj.get("isSuccess",False)))

			if serp_obj.get("isSuccess",False):
				my_serp_organic_results_object 	= serp_obj.get("serp_organic_results", list())
				print("Mainify.SerpResults :",len(my_serp_organic_results_object))
				my_serp_related_searches_object	= serp_obj.get("serp_related_searches", list())
				#print("my_serp_related_searches_object",my_serp_related_searches_object)

				my_count_max 	= 5
				my_count 		= int(0)
				for rs_obj in my_serp_related_searches_object:
					rs 							= rs_obj.get("related_searches","")
					if len(rs) > 1:
						related_searches.append(rs)
					if my_count > my_count_max:
						break

				#print("related_searches",related_searches)
				my_count_max 	= 35
				my_count 		= int(0)
				for or_obj in my_serp_organic_results_object:
					my_url	 					= or_obj.get("organic_results_link","")
					if len(my_url) > 1:
						resultList.append(my_url)
						my_count += int(1)

					if my_count > my_count_max:
						break

		if len(resultList) < 1:
			dataFile="/home/www/unaiquenet_noresults/"+str(SessionID)
			if os.path.exists(dataFile):
				os.unlink(dataFile)
			f = open(dataFile, "w+", encoding='utf-8')
			f.write("no results")
			f.close()
			os.chmod(dataFile, stat.S_IRWXO|stat.S_IRWXG|stat.S_IRWXU)
			print("Mainify.NoResults   : True -> ",MainKeyword)
			gc.collect()
			return False

		if enableFastmode:
			articleSuccessPoints 					= myRank.points_for_use_fastmode	# bei 13 Punkten haben wir einen Gewinnerartikel, wenn wir den Fastmodus benutzen sollen
		else:
			articleSuccessPoints 					= myRank.points_for_not_fastmode	# bei 16 Punkten haben wir einen Gewinnerartikel, wenn wir den Fastmodus NICHT benutzen

		for url in resultList:
			tel 									= myRank.calculateRank(myAI, url, SessionID, ip_obj, serp_obj)	# hier in der Anweisung heißt es "tel" in dem restlichen myRank Code "teler"
			points 									= tel.get('points')
			if points >= 0:	# keine negativen Werte nehmen, das ist keine Ergebnisse
				results.append(tel)

			if points >= articleSuccessPoints: 	# when a Rankify Object has more than 14 points we take it
				#print("########### we take this one")
				break # stop for loop: for url in resultList:

		#if points < articleSuccessPoints:
		try:
			myResultElement 					= sorted(results, key=lambda k: k.get('points'), reverse=True)[0]
		except Exception as as1:
			myResultElement 					= tel	# sonst nehmen wir das letzte "tel"-Objekt aus der "for url in resultList:"-Schleife
			pass

		if isinstance(myResultElement, dict):
			tel 								= myResultElement
		else:
			dataFile="/home/www/unaiquenet_noresults/"+str(SessionID)
			if os.path.exists(dataFile):
				os.unlink(dataFile)
			f = open(dataFile, "w+", encoding='utf-8')
			f.write("no results")
			f.close()
			os.chmod(dataFile, stat.S_IRWXO|stat.S_IRWXG|stat.S_IRWXU)
			print("Mainify.NoResults  : True -> ",MainKeyword)
			gc.collect()
			return False
			#sys.exit(1)

		#print("Mainify.FastMode    :",str(enableFastmode))
		print("######################################################")
		tel['fastmode']								= enableFastmode
		og_htmlLanguage 							= tel.get("language")
		detected_htmlLanguage 						= tel.get("detected_language")

		if len(og_htmlLanguage) == 2:
			htmlLanguage							= og_htmlLanguage
		else:
			htmlLanguage							= detected_htmlLanguage

		for h_element in myRank.headlines_list:
			try:
				myContent 						= tel.get(h_element+"_text")
				myLowQualityScore 				= tel.get(h_element+"_text_low_quality_score")
				myContent_len 					= len(myContent)

				if myContent_len >= myRank.min_text_length:
					print("Headline	:",h_element)
					print("Words		--->\t:",myRank.count_words_regex(myContent))
					print("Length		--->\t:",myContent_len)
					print("Penalty 	--->\t:",myLowQualityScore)
					print("---------------------------")

				if h_element in ["h1","h2","h3"] and myContent_len >= myRank.min_text_length:	# nur h1,h2,h3 Textblockinhalte werden via KI umgewandelt
					#sentences_list 				= myRank.split_into_sentences(myContent)
					#word_count_int 				= myRank.count_words_regex(myContent)
					myAIContent 				= myAI.abstractiveSummarizer(myRank, htmlLanguage, myContent, enableFastmode)
					tel[h_element+"_text_ai"] 	= myAIContent
					myLowQualityScore2			= myRank.isLowQualityContent(myAIContent)
					plagscore 					= myAI.plagiarismChecker(myContent, myAIContent)
					if len(myAIContent) > myRank.headline_min_length:
						tel['ai_enabled'] 		= True
					tel[h_element+"_text_ai_plagscore"]			= plagscore
					tel[h_element+"_text_low_quality_score"]	= myLowQualityScore2
					#print("Headline	:",h_element)
					if len(myAIContent) > 0:
						print("Words (AI)	--->\t:",myRank.count_words_regex(myAIContent))
						print("Length (AI)	--->\t:",len(myAIContent))
						print("Penalty (AI)	--->\t:",myLowQualityScore2)
						print("Plagscore (AI)	--->\t:",str(100-plagscore)+str("%"))
						#print("Content (AI)		--->\t:",myAIContent)
						print("###############################")
			except Exception as as1:
				pass

		articletext 								= tel.get("article_text")
		myLowQualityScore 							= tel.get("article_text_low_quality_score")
		articletext_len 							= len(articletext)

		print("Article		:",articletext_len,"Chars")
		print("Words		--->\t:",myRank.count_words_regex(articletext))
		print("Length		--->\t:",len(articletext))
		print("Penalty		--->\t:",myLowQualityScore)
		print("---------------------------")

		if articletext_len >= myRank.min_text_length:
			myAIContent2 								= myAI.abstractiveSummarizer(myRank, htmlLanguage, articletext, enableFastmode)
			tel["article_text_ai"] 						= myAIContent2
			myLowQualityScore3							= myRank.isLowQualityContent(myAIContent2)
			plagscore2 									= myAI.plagiarismChecker(articletext, myAIContent2)
			if len(myAIContent2) > myRank.headline_min_length:
				tel['ai_enabled'] 						= True
			tel["article_text_ai_plagscore"]			= plagscore2
			tel["article_text_ai_low_quality_score"]	= myLowQualityScore3
			if len(myAIContent2) > 0:
				print("Words (AI)	--->\t:",myRank.count_words_regex(myAIContent2))
				print("Length (AI)	--->\t:",len(myAIContent2))
				print("Penalty (AI)	--->\t:",myLowQualityScore3)
				print("Plagscore (AI)	--->\t:",str(100-plagscore2)+str("%"))
				#print("Content (AI)		--->\t:",myAIContent2)
				print("###############################")

		"""
		# Bionic Reading aktivieren für die KI Inhalte
		try:
			inp											= tel.get("article_text_ai")
			tel["article_text_ai_raw"]					= inp
			t_tele										= BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="html", rare_words_behavior="underline", rare_words_max_freq=1, stopwords_behavior="ignore").read_faster(text=inp)
			if len(t_tele) >= len(inp):
				tel["article_text_ai"] 					= str(t_tele)
		except Exception as a1:
			pass

		try:
			inp											= tel.get("h1_text_ai")
			tel["h1_text_ai_raw"]						= inp
			t_tele										= BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="html", rare_words_behavior="underline", rare_words_max_freq=1, stopwords_behavior="ignore").read_faster(text=inp)
			if len(t_tele) >= len(inp):
				tel["h1_text_ai"] 						= str(t_tele)
		except Exception as a1:
			pass

		try:
			inp											= tel.get("h2_text_ai")
			tel["h2_text_ai_raw"]						= inp
			t_tele										= BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="html", rare_words_behavior="underline", rare_words_max_freq=1, stopwords_behavior="ignore").read_faster(text=inp)
			if len(t_tele) >= len(inp):
				tel["h2_text_ai"] 						= str(t_tele)
		except Exception as a1:
			pass

		try:
			inp											= tel.get("h3_text_ai")
			tel["h3_text_ai_raw"]						= inp
			t_tele										= BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="html", rare_words_behavior="underline", rare_words_max_freq=1, stopwords_behavior="ignore").read_faster(text=inp)
			if len(t_tele) >= len(inp):
				tel["h3_text_ai"] 						= str(t_tele)
		except Exception as a1:
			pass
		"""

		dataFile				= "/home/www/security/unaiqueASCOM/latest_artikelschreibercom_"+str(Language)+".json"
		isPorn 					= myRank.isPornBlacklisted(MainKeyword+", "+SubKeywords)
		if not isPorn:
			for element in range(5):
				telMyDict		= myAI.genereteContentByOpenAIAdvanced(MainKeyword, SubKeywords, related_searches, Language)
				openaiContent	= telMyDict.get("openai",str(""))
				if len(openaiContent) > 10:
					tel["openai"]		= openaiContent
					ai_enabled_openai 	= True
					break
				else:
					sleep(randint(15,25))

		bTime11 				= datetime.datetime.now()
		tt_time11 				= bTime11.isoformat().split('.', 1)[0]

		if SessionID.find("UNAIQUENET") != -1 :
			sessionType 		= "unaique"
			dataFile			= "/home/www/security/unaiqueASCOM/latest_unaiquenet_"+str(Language)+".json"

			with codecs.open("/home/www/logs/ARTIKELSCHREIBER/2023_unaiquenet.log", 'a+', encoding='utf-8') as fa:
				fa.write(str(tt_time11)+"###"+str(SessionID)+"###"+str(MainKeyword)+"###"+str(SubKeywords)+"###"+str(myLanguage)+"###"+str(my_ip_info)+"\n")
			fa.close()

		elif SessionID.find("ARTIKELSCHREIBER") != -1:
			sessionType 		= "artikelschreiber"
			dataFile			= "/home/www/security/unaiqueASCOM/latest_artikelschreibercom_"+str(Language)+".json"

			with codecs.open("/home/www/logs/ARTIKELSCHREIBER/2023_artikelschreiber.log", 'a+', encoding='utf-8') as fa:
				fa.write(str(tt_time11)+"###"+str(SessionID)+"###"+str(MainKeyword)+"###"+str(SubKeywords)+"###"+str(myLanguage)+"###"+str(my_ip_info)+"\n")
			fa.close()
		#elif SessionID.find("API") != -1:
		#	sessionType 		= "api"

		try:
			p_datastorage		= json.dumps(telMyDict, ensure_ascii=False)
			if os.path.exists(dataFile):
				os.unlink(dataFile)
			f = open(dataFile, "w", encoding='utf-8')
			f.write(p_datastorage)
			f.close()
			os.system("chown www-data:www-data "+dataFile)
			os.system("chmod 755 "+dataFile)
		except Exception as a1:
			pass

		"""
		try:
			inp							= tel.get("openai")
			tel["openai_raw"]			= inp
			t_tele						= BionicReading(fixation=0.6, saccades=0.75, opacity=0.7, output_format="html", rare_words_behavior="underline", rare_words_max_freq=1, stopwords_behavior="ignore").read_faster(text=inp)
			if len(t_tele) >= len(inp):
				tel["openai"] 			= str(t_tele)
		except Exception as a1:
			pass
		"""

		# Speichere hier das komplette Rankify Ergebnis dict als json Datei im Dateisystem ab
		myTitle					= tel.get("title")
		myDescription			= tel.get("description")
		myOpenai				= tel.get("openai")
		mySummary				= tel.get("summary")
		isMyContentGood			= myAI.isGoodContent(myTitle+", "+myDescription+", "+mySummary+", "+myOpenai)
		tel["isGoodContent"]	= isMyContentGood
		#print("Debug len(myOpenai):", str(len(myOpenai)))
		try:
			p_datastorage		= json.dumps(tel, ensure_ascii=False)
			dataFile			= "/home/www/security/unaiqueASCOM/"+str(SessionID)+"_"+str(htmlLanguage)+".json"
			if os.path.exists(dataFile):
				os.unlink(dataFile)
			f = open(dataFile, "w+")
			f.write(p_datastorage)
			f.close()
			os.system("chown www-data:www-data "+dataFile)
			os.system("chmod 755 "+dataFile)
		except Exception as a1:
			pass

		#ipInfo 				= myRank.getGeoInformation(IPAddress)
		#ipInfo2 			= myRank.getGeoInformation2(IPAddress)
		#i 					= datetime.datetime.now()
		#tt_time 			= i.isoformat()

		bTime 				= datetime.datetime.now()
		deltaTimeRun 		= bTime - aTime
		deltaTimeRun 		= str(deltaTimeRun)
		deltaTimeRun 		= deltaTimeRun.split('.', 1)[0]
		tt_time 			= bTime.isoformat().split('.', 1)[0]

		article_headline 	= tel.get("title")
		ai_enabled 			= tel.get("ai_enabled")
		article_url 		= tel.get("url")
		print()
		print("######################################################")
		print("######## ARTIKELSCHREIBER/UNAIQUE             ########")
		print("######## by Sebastian Enger, M.Sc.            ########")
		print("######## Version vom: 03.06.2023 - 7.0.2.5.3  ########")
		print("##################### RESULTS:START ##################")
		print("WINNER_URL:		",str(article_url))
		print("WINNER_HEADLINE:	",str(article_headline))
		print("MAIN_KEYWORD:		",str(MainKeyword))
		print("SUB_KEYWORD:		",str(SubKeywords))
		print("LANGUAGE:		",str(myLanguage))
		print("RUNTIME:		",str(deltaTimeRun))
		print("SERVER_LOAD:		",str(load1))
		print("POINTS:			",str(points))
		print("FASTMODE:		",str(enableFastmode))
		print("AI_ENABLED:		",str(ai_enabled))
		print("AI_OPENAI:		",str(ai_enabled_openai))
		print("SERP_ENABLED: 		",str(serp_obj.get("isSuccess",False)))
		print("SESSION_TYP:		",str(sessionType))
		print("SESSION_ID:		",str(SessionID))
		print("GEO:			",str(my_ip_info))
		print("CURRENT_TIME:		",str(tt_time))
		print("##################### RESULTS:END ####################")

		myBlogPage 		= str("")
		myBlogContent 	= str("")
		canonical 		= str("")
		filename 		= str("")

		try:
			if ai_enabled_openai and isMyContentGood and Language in ["de","en","it","fr","es","pt"]:
				#if ai_enabled and not isPorn1 and not isPorn2 and not isPorn3 and not isPorn4:
				myBlogPage 		= "https://www.artikelschreiber.com/api/blog_creator_textgenerator.php?lang="+myBlogLanguage+"&uniqueidentifier="+SessionID
				myBlogContent 	= myRank.getWebpage(myBlogPage)
				canonical 		= tel.get('canonical')	# <link rel="canonical" href="https://www.artikelschreiber.com/de/blog/zusammenschluss-europa-europaischen-373.html" />
				filename 		= canonical.replace("https://www.artikelschreiber.com/texts/","/home/www/wwwartikelschreiber/texts/")
				#print("Debug myBlogContent:",str(len(myBlogContent)))
				if len(myBlogContent) > 100 and myBlogContent.find('<!DOCTYPE html>') != -1:
					if os.path.exists(filename):
						os.unlink(filename)
					f = open(filename, "w+", encoding='utf-8')
					f.write(myBlogContent)
					f.close()
					os.system("chown www-data:www-data "+filename)
					os.system("chmod 755 "+filename)
					print("BLOG_ENTRY:		",str(canonical))
					#print("BLOG_DONE:		",str(True))

					today 				= str(date.today())
					sitemap_file 		= "/home/www/wwwartikelschreiber/sitemap_b.xml"
					if os.path.exists(sitemap_file):
						os.unlink(sitemap_file)

					sitemap_fa  		= open(sitemap_file, 'w+')
					sitemap_fa.write('<?xml version="1.0" encoding="UTF-8"?>')
					sitemap_fa.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')
					sitemap_fa.write('<url><loc>'+canonical+'</loc><lastmod>'+today+'</lastmod><changefreq>monthly</changefreq><priority>0.95</priority></url>')
					sitemap_fa.write('</urlset><!--?xml version="1.0" encoding="UTF-8"?-->')
					sitemap_fa.close()

					os.system("chown www-data:www-data "+sitemap_file)
					os.system("chmod 755 "+sitemap_file)

					#my_sitemap			= "https://www.artikelschreiber.com/sitemap_b.xml"
					#my_sitemap_bing   	= "https://www.bing.com/webmaster/ping.aspx?siteMap="+my_sitemap
					#my_sitemap_google 	= "https://www.google.com/ping?sitemap="+my_sitemap
					print("SITEMAP_DONE:		",str(True))
					print("##################### RESULTS:END ####################")
		except Exception as as1:
			pass

		#https://tutorial.eyehunts.com/python/python-file-modes-open-write-append-r-r-w-w-x-etc/
		with codecs.open("/home/www/logs/ARTIKELSCHREIBER/2023_shortlog.log", 'a+', encoding='utf-8') as fa:
			fa.write(str(tt_time)+"###"+str(SessionID)+"###"+str(MainKeyword)+"###"+str(SubKeywords)+"###"+str(myLanguage)+"###"+str(my_ip_info)+"###"+str(deltaTimeRun)+"\n")
		fa.close()
		gc.collect()
		return True

"""
MainKeyword="Mopet"
SubKeywords="Rundfahrt"
SessionID="1234SESSION-ASCOM"
Language="de"
IPAddress="12.14.15.121"

mainFunktionSublinify(MainKeyword, SubKeywords, SessionID, Language, IPAddress)
sys.exit(0)
"""
