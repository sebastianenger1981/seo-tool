

#https://github.com/msiemens/tinydb
#https://tinydb.readthedocs.io/en/latest/usage.html#queries
import time
from tinydb import TinyDB, Query #  pip3 install -U tinydb

def getEntryDB(MainKeyword, SubKeywords, IPAddress, ResultLink):
	db 			= TinyDB("/home/unaique/library/sqlite/nodouble_results.json")
	qsearch 	= Query()

	MainKeyword = str(MainKeyword)
	SubKeywords = str(SubKeywords)
	IPAddress	= str(IPAddress)
	ResultLink	= str(ResultLink)

	key3 		= str(MainKeyword+SubKeywords).strip().lower().replace(" ","")
	timestamp2 	= int(time.time()) - int(30)
	s 			= db.search((qsearch.query == key3) & (qsearch.url == ResultLink) & (qsearch.ipaddress == IPAddress) & (qsearch.timestamp > timestamp2))
	if len(s) > 0:
		return str(ResultLink)
	else:
		return str("")

def setEntryDB(MainKeyword, SubKeywords, IPAddress, ResultLink):
	db 			= TinyDB("/home/unaique/library/sqlite/nodouble_results.json")
	qsearch 	= Query()

	MainKeyword = str(MainKeyword)
	SubKeywords = str(SubKeywords)
	IPAddress	= str(IPAddress)
	ResultLink	= str(ResultLink)

	key3 		= str(MainKeyword+SubKeywords).strip().lower().replace(" ","")
	timestamp2 	= int(time.time()) - int(300)
	s 			= db.search((qsearch.query == key3) & (qsearch.url == ResultLink) & (qsearch.ipaddress == IPAddress) & (qsearch.timestamp > timestamp2))

	timestamp1 	= int(time.time())
	b 			= {'url':ResultLink,'ipaddress':IPAddress,'query':key3, 'timestamp':timestamp1}

	if len(s) < 1:
		db.insert(b)
	else:
		db.update(b)

	s1 			= db.search((qsearch.query == key3) & (qsearch.url == ResultLink) & (qsearch.ipaddress == IPAddress))
	if len(s1) < 1:
		db.insert(b)
	else:
		db.update(b)

	return True


#setEntryDB("MainKeyword", "SubKeywords", "IPAddress", "ResultLink")
d = getEntryDB("MainKeyword", "SubKeywords", "IPAddress", "ResultLink")
print(d)
print(len(d))
