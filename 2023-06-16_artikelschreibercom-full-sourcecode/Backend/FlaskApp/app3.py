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
import os
import codecs
import datetime
from pathlib import Path
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=Warning)


from pydantic import BaseModel	#	pip3 install -U fastapi
import uvicorn	#	pip3 install -U uvicorn gunicorn
from fastapi import FastAPI, Form	#	pip3 install -U fastapi
#from starlette.responses import JSONResponse
#from starlette.applications import Starlette
#from starlette.middleware.wsgi import WSGIMiddleware

import sys
#sys.path.append('/home/unaique/library')
#import Mainify as mainify

sys.path.append('/home/unaique/library3')
#import Sublinify as subify
from Sublinify import Suble
mySubl = Suble()

version = f"{sys.version_info.major}.{sys.version_info.minor}"
#pip3 install -U gunicorn
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker --reload True app:app --bind 127.0.0.1:8000
#pip3 install python-multipart
#uvicorn main:app --host 0.0.0.0 --port 80
#uvicorn /home/unaique/FlaskApp/app:app --reload
#pip3 install fastapi uvicorn
app 		= FastAPI()
#app = Starlette()  # will fastapi app work here?
#app.add_middleware(WSGIMiddleware)
import time
noDoubleRes = dict()

print("######################################################")
print("### Loading Software Backend Version 7 'app3.py'!  ###")
print("######################################################")

"""
unaique_maintance 			= '/home/www/wwwunaiquenet/MAINTAINANCE.ACTIVE.TXT'
artikelschreiber_maintance 	= '/home/www/wwwartikelschreiber/MAINTAINANCE.ACTIVE.TXT'

if os.path.exists(unaique_maintance):
	os.unlink(unaique_maintance)
if os.path.exists(artikelschreiber_maintance):
	os.unlink(artikelschreiber_maintance)
"""

class Item(BaseModel):
	query: str
	sess: str
	lang: str
	ip: str

class LinkItem(BaseModel):
	sess: str
	link: str
	ip: str

class LittleItem(BaseModel):
	sess: str
	ip: str

class ASCOMItem(BaseModel):
	sid: str
	sk: str
	mk: str
	lg: str
	ip: str


#https://github.com/tiangolo/fastapi/tree/master/docs/src
#@app.get('/createTexts')
#def createTexts(MainKeyword: str = Form(...), SubKeywords: str = Form(...), SessionID: str = Form(...), Language: str = Form(...)):
#def createTexts(*, MainKeyword: str = Form(...), SubKeywords: str= Form(...), SessionID: str= Form(...), Language: str= Form(...)):
#############@app.get("/createTextsNet/mk/{MainKeyword}/sid/{SessionID}/lg/{Language}")
@app.post("/createTextsNet/")
def createTextsNet(item: Item):
#async def createTextsNet(MainKeyword: str, SessionID: str, Language: str):
	item_dict 	= item.dict()	# https://fastapi.tiangolo.com/tutorial/body/
	Language 	= str(item.lang)
	SessionID 	= str(item.sess)
	MainKeyword = str(item.query)
	IPAddress	= str(item.ip)
	"""
	timestamp1 	= int(time.time())
	key 		= str(MainKeyword+MainKeyword).replace(" ","").strip().lower()
	timestamp2 	= noDoubleRes.get(key)
	if timestamp2:
		timestamp2 	= int(timestamp2)
		#if int(timestamp2-timestamp1) < int(1800):
		if timestamp2 + int(1800) >= timestamp1:
			# Wenn zu schnell die gleichen Suchanfragen reinkommen, dann wird nur die erste Anfrage bearbeitet
			return True
	"""

	MainKeyword = MainKeyword.replace('+', ' ')
	MainKeyword = " ".join(MainKeyword.split(' ')[:45]) #MainKeyword[:154]

	#mySubl.mainFunktionSublinify(MainKeyword, MainKeyword, SessionID, Language, IPAddress)
	try:
		mySubl.mainFunktionSublinify(MainKeyword, MainKeyword, SessionID, Language, IPAddress)
	except Exception as e:
		#myNow		= str(datetime.datetime.now())
		#file 		= codecs.open("/home/unaique/FlaskApp/create.log", "a", "utf-8-sig")
		#file.write("\t\t\t"+myNow+"Exception caught\n")
		#file.close()
		print("Catching Exception mainFunktion():", e)
		#print("Unexpected error:", sys.exc_info()[0])
		print("Unexpected error:", sys.exc_info())
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	"""
	#mainify.mainFunktion(MainKeyword, MainKeyword, SessionID, Language)
	try:
		mainify.mainFunktion(MainKeyword, MainKeyword, SessionID, Language, IPAddress)
	except Exception as e:
		myNow		= str(datetime.datetime.now())
		file 		= codecs.open("/home/unaique/FlaskApp/create.log", "a", "utf-8-sig")
		file.write("\t\t\t"+myNow+"Exception caught\n")
		file.close()
		print("Catching Exception mainFunktion():", e)
		print("Unexpected error:", sys.exc_info()[0])
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	"""
	return True

#https://github.com/tiangolo/fastapi/tree/master/docs/src
#@app.get('/createTexts')
#def createTexts(MainKeyword: str = Form(...), SubKeywords: str = Form(...), SessionID: str = Form(...), Language: str = Form(...)):
#def createTexts(*, MainKeyword: str = Form(...), SubKeywords: str= Form(...), SessionID: str= Form(...), Language: str= Form(...)):
#@app.get("/createTexts/mk/{MainKeyword}/sk/{SubKeywords}/sid/{SessionID}/lg/{Language}")
#async def createTexts(MainKeyword: str, SubKeywords: str, SessionID: str, Language: str):
# def createTexts(MainKeyword: str, SubKeywords: str, SessionID: str, Language: str):
@app.post("/createTexts/")
def createTexts(item: ASCOMItem):
	item_dict 	= item.dict()	# https://fastapi.tiangolo.com/tutorial/body/
	Language 	= str(item.lg)
	SessionID 	= str(item.sid)
	MainKeyword = str(item.mk)
	SubKeywords	= str(item.sk)
	IPAddress	= str(item.ip)

	MainKeyword = str(MainKeyword)
	SubKeywords	= str(SubKeywords)
	"""
	timestamp1 	= int(time.time())	# 11 Uhr - aktuell
	key 		= str(MainKeyword+SubKeywords).replace(" ","").strip().lower()
	timestamp2 	= noDoubleRes.get(key) # 10:45 Uhr - letztes Mal dieser Eintrag

	if timestamp2:
		timestamp2 	= int(timestamp2)
		#if int(timestamp2-timestamp1) < int(1800):
		if timestamp2 + int(1800) >= timestamp1:
			# Wenn zu schnell die gleichen Suchanfragen reinkommen, dann wird nur die erste Anfrage bearbeitet
			return True
	"""
	MainKeyword = MainKeyword.replace('+', ' ')
	SubKeywords = SubKeywords.replace('+', ' ')
	MainKeyword = " ".join(MainKeyword.split()[:45]) #MainKeyword[:154]
	SubKeywords = " ".join(SubKeywords.split()[:45]) #SubKeywords[:154]

	"""
	#mainify.mainFunktion(MainKeyword, SubKeywords, SessionID, Language, IPAddress)
	try:
		mainify.mainFunktion(MainKeyword, SubKeywords, SessionID, Language, IPAddress)
	except Exception as e:
		#myNow		= str(datetime.datetime.now())
		#file 		= codecs.open("/home/unaique/FlaskApp/create.log", "a", "utf-8-sig")
		#file.write("\t\t\t"+myNow+"Exception caught\n")
		#file.close()
		print("Catching Exception mainFunktion():", e)
		#print("Unexpected error:", sys.exc_info()[0])
		print("Unexpected error:", sys.exc_info())
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	"""
	#mySubl.mainFunktionSublinify(MainKeyword, SubKeywords, SessionID, Language, IPAddress)
	try:
		mySubl.mainFunktionSublinify(MainKeyword, SubKeywords, SessionID, Language, IPAddress)
	except Exception as e:
		#myNow		= str(datetime.datetime.now())
		#file 		= codecs.open("/home/unaique/FlaskApp/create.log", "a", "utf-8-sig")
		#file.write("\t\t\t"+myNow+"Exception caught\n")
		#file.close()
		print("Catching Exception mainFunktion():", e)
		#print("Unexpected error:", sys.exc_info()[0])
		print("Unexpected error:", sys.exc_info())
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)

	return True
