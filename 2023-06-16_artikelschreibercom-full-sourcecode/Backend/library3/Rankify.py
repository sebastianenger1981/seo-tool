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

import logging
logging.getLogger().disabled = True
logging.disable(logging.WARNING)
logging.disable(logging.INFO)

import urllib.parse

import sys
sys.path.append('/home/unaique/library3')
#sys.path.append('/home/unaique/library')

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

"""
Fix SSL Problems:
# https://gankrin.org/how-to-fix-ssl-certificate_verify_failed-error-error-in-python/
$ sudo update-ca-certificates --fresh
$ export SSL_CERT_DIR=/etc/ssl/certs
"""

# pip3 install -U aiohttp asyncio
# https://www.twilio.com/blog/-asynchrone-http-anforderungen-python-aiohttp-asyncio
#import aiohttp
#import asyncio
import requests	# pip3 install --upgrade requests

import bleach #https://pypi.org/project/bleach/

from dns import resolver,reversename

import json

import codecs

import string
from string import printable

from unidecode import unidecode

import re

import random

import os

import socket

from bs4 import BeautifulSoup, Comment
import extruct # https://github.com/scrapinghub/extruct ///  pip install -U extruct
from w3lib.html import get_base_url # https://github.com/scrapy/w3lib /// pip install -U w3lib
import regex as re1 # pip3 install -U regex

from urllib.parse import urljoin
from urllib.parse import urlencode
from urllib.parse import urlparse

import urllib3
urllib3.disable_warnings()

from newspaper import Article
#import newspaper #pip3 install -U newspaper3k
article 			= Article('')

# compile regexes, so we don't do this on the fly and rely on caching
#from typing import Any, Dict, Pattern
from typing import Pattern

from langdetect import detect	# also https://github.com/saffsd/langid.py -  pip3 install -U langdetect
import langid # pip3 install -U langid
from langua import Predict # pip3 install -U langua https://github.com/whiletruelearn/langua
import pycld2 as cld2 # pip install -U pycld2

#from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser	# pip3 install -U sumy
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from html import unescape

import geoip2.database
geoReader 			= geoip2.database.Reader("/home/unaique/library3/geoip/GeoLite2-City.mmdb")

# https://github.com/P3TERX/GeoLite.mmdb - Downloads
#https://geoip2.readthedocs.io/en/latest/
# pip3 install -U geoip2
# https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=############&suffix=tar.gz
# Account/User ID ###########
# License key ################

# pip3 install -U IP2Location
#https://www.ip2location.com/development-libraries/ip2location/python
#https://github.com/chrislim2888/IP2Location-Python
# Web: https://lite.ip2location.com/ - User: Sebastian@rechthaben.net - Pass: zVkXkqH6v+8SG@$
# Direct Download: https://www.ip2location.com/download/?token=##############&file=DB11LITEBIN
# Free Download: Sources: https://download.ip2location.com/lite/
import IP2Location
database 			= IP2Location.IP2Location(os.path.join("data", "/home/unaique/library3/geoip/IP2LOCATION-LITE-DB11.BIN"))

import unicodedata # pip3 install -U unidecode

import psutil	# pip3 install -U psutil https://www.geeksforgeeks.org/how-to-get-current-cpu-and-ram-usage-in-python/

import datetime as dt

from html5validate import validate
#pip3 install -U html5lib
from lxml import etree
from io import StringIO

# https://hackersandslackers.com/scrape-metadata-json-ld/
# https://hackersandslackers.com/scraping-urls-with-beautifulsoup/
# https://github.com/hackersandslackers/beautifulsoup-tutorial
# https://github.com/practical-data-science/ecommercetools
# https://github.com/mozilla/bleach
# next and previous tags: https://stackoverflow.com/questions/53437616/beautifulsoup-find-elements-directly-below-and-above-heading-with-specific-str

"""
from AIlify import AI
myAI = AI()
#print(type(myAI))
#sys.exit(1)
"""

"""
# Start: Globale Variablen für Rankify
headline_min_length	= 7		# chars
min_word_count		= 7		# words
min_text_length		= 140	# chars
max_spaces_count 	= 5		# '     '
headlines_list 		= ["h1","h2","h3","h4","h5","h6"]
# Ende: Globale Variablen für Rankify
"""

VALUESERP_KEY 		= '########################'
punct 				= set(string.punctuation)

UserAgent			= "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
UserAgentMobile		= "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) FxiOS/7.5b3349 Mobile/14F89 Safari/603.2.4"#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
Headers 			= {'user-agent': UserAgent, 'Content-Type': 'text/html; charset=utf-8', 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate'}
#HeadersSimple		= {'user-agent': UserAgentMobile, 'Content-Type': 'text/html; charset=utf-8', 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate'}
HeadersSimple		= {'user-agent': UserAgentMobile, 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate'}
HeadersSimpleADV	= {'user-agent': UserAgentMobile, 'Authorization': 'ce78143f444846d14d338f0da26a2434', 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate'}


stoplist_domains	= "/home/unaique/library3/blacklists/adblock.txt" # Quelle: https://github.com/carlospolop/MalwareWorld und https://malwareworld.com/textlists/suspiciousDomains.txt
stoplist_shops		= "/home/unaique/library3/blacklists/shops.txt"
stoplist_paywall  	= "/home/unaique/library3/blacklists/paywall.txt"
stoplist_porn		= "/home/unaique/library3/blacklists/pornstopwordlist.txt"
stoplist_captcha	= "/home/unaique/library3/blacklists/captcha.txt"

f_domains			= open(stoplist_domains, "r", encoding='utf-8')
f_shops				= open(stoplist_shops, "r", encoding='utf-8')
f_paywall			= open(stoplist_paywall, "r", encoding='utf-8')
f_porn				= open(stoplist_porn, "r", encoding='utf-8')
f_captcha			= open(stoplist_captcha, "r", encoding='utf-8')

"""
stoplist_domains_blocker	= list(set(f_domains.readlines()))
stoplist_shops_blocker		= list(set(f_shops.readlines()))
stoplist_paywall_blocker	= list(set(f_paywall.readlines()))
stoplist_porn_blocker		= list(set(f_porn.readlines()))
stoplist_captcha_blocker	= list(set(f_captcha.readlines()))
"""

RE_LINEBREAK: Pattern 		= re.compile(r"(\r\n|[\n\v])+")
RE_NONBREAKING_SPACE: Pattern = re.compile(r"[^\S\n\v]+")
RE_ZWSP: Pattern 			= re.compile(r"[\u200B\u2060\uFEFF]+")

RE_BRACKETS_CURLY 			= re.compile(r"\{[^{}]*?\}")
RE_BRACKETS_ROUND 			= re.compile(r"\([^()]*?\)")
RE_BRACKETS_SQUARE 			= re.compile(r"\[[^\[\]]*?\]")

RE_BULLET_POINTS 			= re.compile(
	# require bullet points as first non-whitespace char on a new line, like a list
	r"((^|\n)\s*?)"
	r"([\u2022\u2023\u2043\u204C\u204D\u2219\u25aa\u25CF\u25E6\u29BE\u29BF\u30fb])",
)

# source: https://gist.github.com/dperini/729294
RE_URL: Pattern = re.compile(
	r"(?:^|(?<![\w/.]))"
	# protocol identifier
	# r"(?:(?:https?|ftp)://)"  <-- alt?
	r"(?:(?:https?://|ftp://|www\d{0,3}\.))"
	# user:pass authentication
	r"(?:\S+(?::\S*)?@)?"
	r"(?:"
	# IP address exclusion
	# private & local networks
	r"(?!(?:10|127)(?:\.\d{1,3}){3})"
	r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
	r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
	# IP address dotted notation octets
	# excludes loopback network 0.0.0.0
	# excludes reserved space >= 224.0.0.0
	# excludes network & broadcast addresses
	# (first & last IP address of each class)
	r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
	r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
	r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
	r"|"
	# host name
	r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
	# domain name
	r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
	# TLD identifier
	r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
	r")"
	# port number
	r"(?::\d{2,5})?"
	# resource path
	r"(?:/\S*)?"
	r"(?:$|(?![\w?!+&/]))",
	flags=re.IGNORECASE,
)

RE_SHORT_URL: Pattern = re.compile(
	r"(?:^|(?<![\w/.]))"
	# optional scheme
	r"(?:(?:https?://)?)"
	# domain
	r"(?:\w-?)*?\w+(?:\.[a-z]{2,12}){1,3}"
	r"/"
	# hash
	r"[^\s.,?!'\"|+]{2,12}"
	r"(?:$|(?![\w?!+&/]))",
	flags=re.IGNORECASE,
)

RE_EMAIL: Pattern = re.compile(
	r"(?:mailto:)?"
	r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}"
	r"(?:$|(?=\b))",
	flags=re.IGNORECASE,
)

RE_USER_HANDLE: Pattern = re.compile(
	r"(?:^|(?<![\w@.]))@\w+",
	flags=re.IGNORECASE,
)

RE_HASHTAG: Pattern = re.compile(
	r"(?:^|(?<![\w#＃.]))(#|＃)(?!\d)\w+",
	flags=re.IGNORECASE,
)

RE_PHONE_NUMBER: Pattern = re.compile(
	# core components of a phone number
	r"(?:^|(?<=[^\w)]))(\+?1[ .-]?)?(\(?\d{3}\)?[ .-]?)?(\d{3}[ .-]?\d{4})"
	# extensions, etc.
	r"(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W))",
	flags=re.IGNORECASE,
)

RE_NUMBER: Pattern = re.compile(
	r"(?:^|(?<=[^\w,.]))[+–-]?"
	r"(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)"
	r"(?:$|(?=\b))"
)

RE_CURRENCY_SYMBOL: Pattern = re.compile(
	r"[$¢£¤¥ƒ֏؋৲৳૱௹฿៛ℳ元円圆圓﷼\u20A0-\u20C0]",
)

RE_EMOJI: Pattern
if sys.maxunicode < 0x10ffff:
	RE_EMOJI = re.compile(
		r"[\u2600-\u26FF\u2700-\u27BF]",
		flags=re.IGNORECASE,
	)
else:
	RE_EMOJI = re.compile(
		r"[\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]",
		flags=re.IGNORECASE,
	)

RE_HYPHENATED_WORD: Pattern = re.compile(
	r"(\w{2,}(?<!\d))\-\s+((?!\d)\w{2,})",
	flags=re.IGNORECASE,
)

# for split_sentences()
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|de|edu|gov)"

imp_keywords = [
'©',
'Copyright',
'Impressum',
'Imprint',
'Terms',
'AGB',
'Services',
'DSGVO',
'GDPR',
'Datenschutz',
'Datenverarbeitung',
'Datenschutzerklärung',
'Allgemeine Geschäftsbedingungen',
'Kontaktformular',
'Kontakt',
'Support'
]


low_quality_content = [
'Cookies',
'Cookies anpassen',
'Cookies einstellen',
'Websiteaufrufe',
'Cookie-Bestimmung',
'Cookie-Bestimmungen',
'Drittanbieter',
'Zielgruppen',
'Problembehandlung',
'personenbezogene Daten',
'Standardgeräteinformationen',
'Standardgeräteinformation',
'Cookie-Einstellungen',
'Cookie-Einstellung',
'personalisierte Anzeigen',
'Verarbeitungszwecke',
'Geräte-Kennungen',
'Zielgruppen',
'Nutzungsverhalten',
'Webangebot',
'JavaScript nicht aktiviert ist',
'Nutzung mit Werbung',
'Privacy Center',
'Personendaten',
'Zustimmungs-Dialog',
'Nutzungsprofils',
'Nutzungsprofil',
'Nutzererfahrung',
'Kommentarlogin',
'Account deaktivieren',
'Tracking',
'Passwort ändern',
'Benutzerdaten erfolgreich',
'Benutzerkonto',
'Datenschutzeinstellungen',
'Wir verwenden Cookies',
'welche Cookies wir speichern dürfen und welche nicht',
'muss JavaScript in Ihrem Browser aktiviert sein',
'der Nutzung mit Werbung zuzustimmen',
'ohne Werbung und ohne Werbetracking',
'Zustimmung ist jederzeit widerrufbar',
'Please enable JavaScript',
'JavaScript is not available',
'JavaScript is disabled in this browser',
'Javascript deaktiviert',
'Browser unterstützt kein Javascript',
'muss Javascript aktiviert werden',
'Altersüberprüfung',
'BorlabsCookie',
'borlabsCookieConfig',
'borlabsCookieContentBlocker',
'JavaScript seems to be disabled in your browser',
'You must have JavaScript enabled in your browser',
'Sie haben einen Adblocker aktiviert',
'Adblock',
'Adblocker',
'Anzeige',
'Informiere mich über neue Beiträge per E-Mail',
'Benachrichtigung bei weiteren Kommentaren',
]

social_links = [
'www.blogger.com/blog-this.g',
'buffer.com/add',
'share.diasporafoundation.org/',
'del.icio.us/save',
'digg.com/submit',
'www.douban.com/recommend/',
'www.evernote.com/clip.action',
'www.facebook.com/sharer.php',
'share.flipboard.com/bookmarklet/popout',
'flattr.com/submit/auto',
'getpocket.com/edit',
'mail.google.com/mail/',
'www.google.com/bookmarks/mark',
'news.ycombinator.com/submitlink',
'www.instapaper.com/edit',
'iorbix.com/m-share',
'story.kakao.com/share',
'pushtokindle.fivefilters.org/send.php',
'www.kooapp.com/create',
'lineit.line.me/share/ui',
'www.linkedin.com/shareArticle',
'www.livejournal.com/update.bml',
'connect.mail.ru/share',
'meneame.net/submit.php',
'connect.ok.ru/dk',
'outlook.live.com/mail/deeplink/compose',
'pinterest.com/pin/create/button/',
'sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey',
'reddit.com/submit',
'widget.renren.com/dialog/share',
'web.skype.com/share',
'snapchat.com/scan',
'surfingbird.ru/share',
't.me/share/url',
'www.stumbleupon.com/submit',
'sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey',
'trello.com/add-card',
'www.tumblr.com/share',
'twitter.com/intent/tweet',
'vk.com/share.php',
'api.qrserver.com/v1/create-qr-code/',
'service.weibo.com/share/share.php',
'web.whatsapp.com/send',
'wordpress.com/wp-admin/press-this.php',
'compose.mail.yahoo.com/',
'www.yummly.com/urb/verify',
'www.xing.com/spi/shares/new'
]


class Rank:
	def __init__(self):
		self.description 				= "AI related Functions for ArtikelSchreiber.com Backend"
		self.searchfastmode 			= False
		self.aifastmode 				= False
		# Start: Globale Variablen für Rankify
		self.headline_min_length		= int(7)	# chars
		self.min_word_count				= int(7)	# words
		self.min_text_length			= int(140)	# chars
		self.max_spaces_count 			= int(5)	# '     '
		self.max_load_fastmode 			= int(5)	# bei diesem Load auf dem Server wird auf jeden Fall der Fastmode aktiviert
		self.points_for_not_fastmode	= int(16)	# bei 17 Punkten haben wir einen Gewinnerartikel, wenn wir den Fastmodus NICHT benutzen
		self.points_for_use_fastmode	= int(11)	# bei 13 Punkten haben wir einen Gewinnerartikel, wenn wir den Fastmodus benutzen sollen
		self.headlines_list 			= ["h1","h2","h3","h4","h5","h6"]
		self.stoplist_domains_blocker	= list(set(f_domains.readlines()))
		self.stoplist_shops_blocker		= list(set(f_shops.readlines()))
		self.stoplist_paywall_blocker	= list(set(f_paywall.readlines()))
		self.stoplist_porn_blocker		= list(set(f_porn.readlines()))
		self.stoplist_captcha_blocker	= list(set(f_captcha.readlines()))
		self.stopdict_domains_blocker	= self.prepareDomainListBlocker()	# muss "unter" dem Befehl "self.stoplist_domains_blocker	= list(set(f_domains.readlines()))" stehen!

	def prepareDomainListBlocker(self):
		dict_test = {}
		for url in self.stoplist_domains_blocker:
			dict_test[url]=url
		return dict_test

	def count_broken_character(self, string_input):
		# Declaring variable for special characters
		special_char = int(0)

		for i in range(0, len(string_input)):
		# len(string) function to count the
		# number of characters in given string.
			ch = string_input[i]

			#.isalpha() function checks whether character
			#is alphabet or not.
			if (ch.isalnum()):
				continue

			#.isdigit() function checks whether character
			#is a number or not.
			elif (ch.isspace()):
				continue

			elif (ch in punct):
				continue

			elif set(string_input).difference(printable):
				special_char += int(1)

			else:
				special_char += int(1)

		"""
		if special_char >= 1:
			print("String contains {} Special Character/s ".format(special_char))
		else:
			print("There are no Special Characters in this String.")
		"""
		return special_char

	def doSerpSearch(self, MainKeyword, SubKeywords, language, ip_obj):
		search_query	= str(MainKeyword+", "+SubKeywords)
		isYoutubeFlag 	= False
		gl_google_country = {
			# https://www.valueserp.com/docs/search-api/reference/google-countries
			# ascom internal language shortcode: google country equivalent
			"de": "de",
			"en": "us",
			"es": "es",
			"fr": "fr",
			"it": "it",
			"ru": "ru",
			"cn": "cn",
			"zh": "cn",
			"jp": "jp",
			"ja": "jp",
			"pt": "pt",
			"in": "in",
			"hi": "in",
			"sa": "sa",
			"ar": "sa",
			"tr": "tr",
		}

		gl_google_language = {
			# https://www.valueserp.com/docs/search-api/reference/google-countries
			# ascom internal language shortcode: google country equivalent
			"de": "lang_de",
			"en": "lang_en",
			"es": "lang_es",
			"fr": "lang_fr",
			"it": "lang_it",
			"ru": "lang_ru",
			"cn": "lang_zh-tw",
			"zh": "lang_zh-tw",
			"jp": "lang_ja",
			"ja": "lang_ja",
			"pt": "lang_pt",
			"in": "lang_en",
			"hi": "lang_en",
			"sa": "lang_ar",
			"ar": "lang_ar",
			"tr": "lang_tr",
		}

		"""
		The gl parameter determines the Google country to use for the query. View the full list of supported glvalues https://www.valueserp.com/docs/search-api/reference/google-countries. Defaults to us.
		The hl parameter determines the Google UI language to return results. View the full list of supported hlvalues https://www.valueserp.com/docs/search-api/reference/google-languages. Defaults to en.
		"""
		params = {
			'api_key': VALUESERP_KEY,
			'flatten_results': True,
			#'include_answer_box': True,	# flatten_results und include_answer_box funktionieren beide nicht zusammen
			#'include_advertiser_info': True,	# dies kostet 1 Creditpunkt mehr! somit 2 statt nur 1 beim weglassen dieser include_advertiser_info option
			'q': search_query,
			'gl': gl_google_country[language],
			'hl': 'de',
			'num': '75', #'100',
			'location': "lat:"+ip_obj.get("ip_latitude")+",lon:"+ip_obj.get("ip_longitude"),
			'safe': 'active',# or enable safe search: 'active', disable safe mode: "off"
			'lr': gl_google_language[language]	# https://www.valueserp.com/docs/search-api/reference/google-lr-languages
		}

		if isYoutubeFlag:
			params['search_type'] = 'videos'

		myteler 			= dict()
		youtube_videos		= list()
		related_searches	= list()
		related_questions	= list()
		organic_results		= list()
		answer_box			= list()
		isSuccess 			= False
		api_result_content 	= str("")
		
		try:
			api_result 				= requests.get('https://api.valueserp.com/search', params, timeout=300)
			if api_result.status_code == 200:
				api_result_content 	= api_result.json()
				isSuccess 			= api_result_content.get("request_info", False).get("success", False)
		except Exception as as1:
			pass

		"""
		r           		= codecs.open("/home/unaique/library3/ARCHIV/valueserp.json", 'r', encoding='utf-8')
		api_result_content 	= json.loads(r.read())
		isSuccess			= True
		r.close()
		"""

		myteler["serp"]								= api_result_content	# ist ein dict, muss mit print(json.dumps(myteler["serp"], indent=2)) zu json umgewandelt werden

		if not isSuccess:
			myteler["isSuccess"]					= False
			myteler["serp_youtube_videos"]			= list()
			myteler["serp_related_searches"]		= list()
			myteler["serp_faq_related_questions"]	= list()
			myteler["serp_organic_results"]			= list()
			myteler["serp_mainkeyword"]				= str(MainKeyword)
			myteler["serp_subkeywords"]				= str(SubKeywords)
			return myteler

		elif isSuccess: # All options here:  https://www.valueserp.com/docs/search-api/results/google/search
			myteler["isSuccess"]					= True

			if isYoutubeFlag:
				inline_videos_objs		= api_result_content.get("video_results","")
				for iv_obj in inline_videos_objs:
					yt 					= dict()
					yt_title 			= str(iv_obj.get("title",""))
					yt_link  			= str(iv_obj.get("link",""))
					#yt_date 			= str(iv_obj.get("date",""))
					yt_date_utc  		= str(iv_obj.get("date_utc",""))
					yt_snippet  		= str(iv_obj.get("snippet",""))
					yt_image  			= str(iv_obj.get("image",""))
					yt_length  			= str(iv_obj.get("length",""))

					if len(yt_title) > 3 and len(yt_link) > 3 and yt_link.find("https://www.youtube.com/") != -1:
						yt["youtube_video"] 	= yt_link
						yt["youtube_title"] 	= yt_title
						yt["youtube_date_utc"] 	= yt_date_utc
						yt["youtube_snippet"] 	= yt_snippet
						yt["youtube_length"] 	= yt_length
						yt["youtube_image"] 	= yt_image
						youtube_videos.append(yt)
				return youtube_videos

			else:
				related_searches_objs	= api_result_content.get("related_searches","")
				for rs_obj in related_searches_objs:
					rs 					= dict()
					rs_title 			= str(rs_obj.get("query",""))
					if len(rs_title) > 3:
						rs["related_searches"] 		= rs_title
						related_searches.append(rs)

				related_questions_objs	= api_result_content.get("related_questions","")
				for rq_obj in related_questions_objs:
					rq 					= dict()
					rq_source_link		= str("")
					rq_source_title		= str("")
					try:
						rq_source_link		= str(rq_obj.get("source","").get("link",""))
						rq_source_title		= str(rq_obj.get("source","").get("title",""))
					except Exception as as1:
						pass

					rq_question			= str(rq_obj.get("question",""))
					rq_answer			= str(rq_obj.get("answer",""))

					if len(rq_question) > 3 and len(rq_answer) > 3 and len(rq_source_title) > 3 and len(rq_source_link) > 3:
						rq["faq_question"] 		= rq_question
						rq["faq_answer"] 		= rq_answer
						rq["faq_source_link"] 	= rq_source_link
						rq["faq_source_title"] 	= rq_source_title
						related_questions.append(rq)

				organic_results_objs	= api_result_content.get("organic_results","")
				for or_obj in organic_results_objs:
					or_d 				= dict()

					or_position			= str(or_obj.get("position",""))
					or_title			= str(or_obj.get("title",""))
					or_link				= str(or_obj.get("link",""))
					or_snippet			= str(or_obj.get("snippet",""))
					or_cached_page_link = str(or_obj.get("cached_page_link",""))	# https://webcache.googleusercontent.com/search?q=cache:or_4V5fHFHkJ:https://www.gruender.de/vertrieb/amazon-seo/&cd=12&hl=de&ct=clnk&gl=de&lr=lang_de&vwsrc=1
					or_about			= str("")

					try:
						or_about		= str(or_obj.get("about_this_result","").get("your_search_and_this_result",""))
					except Exception as as1:
						pass

					or_date				= str(or_obj.get("date",""))
					or_date_utc			= str(or_obj.get("date_utc",""))

					or_rich_snippet_rating 			= str("")
					or_rich_snippet_reviews 		= str("")
					try:
						or_rich_snippet_rating		= str(or_obj.get("rich_snippet","").get("top","").get("detected_extensions","").get("rating",int(0)))
						or_rich_snippet_reviews		= str(or_obj.get("rich_snippet","").get("top","").get("detected_extensions","").get("reviews",int(0)))
					except Exception as as1:
						pass

					if (len(or_position) >= 1 and len(or_title) > 3 and len(or_link) > 3 and len(or_snippet) > 3) or (len(or_title) > 3 and len(or_link) > 3 and or_link.find("youtube.com/") != -1 or or_link.find("youtu.be/") != -1or or_link.find("http://") != -1 or or_link.find("https://") != -1):
						isUrlBlacklisted 								= self.isDomainBlacklisted(or_link)
						if not isUrlBlacklisted:
							or_d["organic_results_position"] 				= or_position
							or_d["organic_results_title"] 					= or_title
							or_d["organic_results_link"] 					= or_link
							or_d["organic_results_snippet"] 				= or_snippet
							or_d["organic_results_cached_page"] 			= or_cached_page_link
							or_d["organic_results_about_list"] 				= or_about
							or_d["organic_results_date"] 					= or_date
							or_d["organic_results_date_utc"] 				= or_date_utc
							or_d["organic_results_rich_snippet_rating"] 	= or_rich_snippet_rating
							or_d["organic_results_rich_snippet_reviews"] 	= or_rich_snippet_reviews
							organic_results.append(or_d)

				inline_videos_objs	= api_result_content.get("inline_videos","")
				for iv_obj in inline_videos_objs:
					yt 					= dict()
					yt_title 			= str(iv_obj.get("title",""))
					yt_link  			= str(iv_obj.get("link",""))

					yt_date_utc  		= str(iv_obj.get("date_utc",""))
					yt_snippet  		= str(iv_obj.get("snippet",""))
					yt_image  			= str(iv_obj.get("image",""))
					yt_length  			= str(iv_obj.get("length",""))

					# Source: https://gist.github.com/rodrigoborgesdeoliveira/987683cfbfcc8d800192da1e73adc486
					if len(yt_title) > 3 and len(yt_link) > 3 and ((yt_link.find("youtube.com/") != -1 and yt_link.find("watch?v=") != -1) or yt_link.find("youtu.be") != -1 or yt_link.find("youtube.com/embed/") != -1 or yt_link.find("youtube-nocookie.com/embed/") != -1):
						yt["youtube_video"] 	= yt_link
						yt["youtube_title"] 	= yt_title
						yt["youtube_date_utc"] 	= yt_date_utc
						yt["youtube_snippet"] 	= yt_snippet
						yt["youtube_length"] 	= yt_length
						yt["youtube_image"] 	= yt_image
						youtube_videos.append(yt)

				if len(youtube_videos) < 1:
					for my_obj in organic_results:
						yt 					= dict()
						yt_link 			= str(my_obj.get("organic_results_link"))
						my_content_title 	= str(my_obj.get("organic_results_title"))

						if len(yt_link) > 3 and ((yt_link.find("youtube.com/") != -1 and yt_link.find("watch?v=") != -1) or yt_link.find("youtu.be") != -1 or yt_link.find("youtube.com/embed/") != -1 or yt_link.find("youtube-nocookie.com/embed/") != -1):
							yt["youtube_video"] 	= yt_link
							yt["youtube_title"] 	= my_content_title
							yt["youtube_date_utc"] 	= str("")
							yt["youtube_snippet"] 	= str("")
							yt["youtube_length"] 	= str("")
							yt["youtube_image"] 	= str("")
							youtube_videos.append(yt)

				myteler["serp_youtube_videos"]			= youtube_videos
				myteler["serp_related_searches"]		= related_searches
				myteler["serp_faq_related_questions"]	= related_questions
				myteler["serp_organic_results"]			= organic_results
				myteler["serp_mainkeyword"]				= str(MainKeyword)
				myteler["serp_subkeywords"]				= str(SubKeywords)
			return myteler

	def is_url(self, url):
		try:
			result = urlparse(url)
			return all([result.path])
		except ValueError:
			return False

	def validateHTML(self, html):
		"""
		import sys
		# https://github.com/danthedeckie/html5validate
		sys.path.append('/home/unaique/library')
		from html5validate import validate
		#pip3 install -U html5lib
		from lxml import etree
		from io import StringIO
		"""
		try:
			validate(html)
			return True
		except Exception as e1:
			try:
				parser = lxml.etree.HTMLParser(recover=False)
				lxml.etree.parse(StringIO(html), parser)
				return True
			except Exception as e1:
				return False

		return False

	# Ende: Globale Variablen für Rankify
	def countBadChars(self, text):
		if len(text) < 1:
			return 0
		text = str(text)
		#return sum(not c.isalnum() and not c.isspace() for c in text)
		return sum(c in string.punctuation for c in text)

	def useFastmode(self, text):
		# Load muss (!) zuerst, da er essentiell für den Server ist
		# kein Fastmode während der Entwicklungsphase
		isPorn = self.isPornBlacklisted(text)
		if isPorn:
			return True

		load1, load5, load15 	= psutil.getloadavg()
		if load1 >= self.max_load_fastmode:
			return True

		hourOfDay = int(dt.datetime.now().hour)
		if hourOfDay >= 8 and hourOfDay <= 16:# Stoßzeiten von 8 Uhr früh bis 16 Uhr Nachmittags, dort geringere Wahrscheinlichkeit für AI
			random_number = random.randint(0, 100)
		else:
			random_number = random.randint(0, 75)

		if random_number == 1:	# bei 2,3,4,5 also bei 1/5 fünftel der Anfragen dürfen wir KEIN KI nutzen, wir nehmen KI nur, wenn der Wert "int(1)" kommt
			return False # hier keine Else Schleife, weil wir noch den Load gucken können

		#return False # keine Fastmode, sprich wir dürfen KI Modul benutzen
		return True

	def remove_accents(self, input_str):
		nfkd_form 	= unicodedata.normalize('NFKD', input_str)
		only_ascii 	= nfkd_form.encode('ASCII', 'ignore')
		s_string	= str(only_ascii.decode('ASCII', "ignore"))
		return str(s_string)


	def isIntent(self, text):
		informative_intent 		= ['what','who','when','where','which','why','how']
		transactional_intent 	= ['buy','order','purchase','cheap','price','discount','shop','sale','offer']
		commercial_intent 		= ['best','top','review','comparison','compare','vs','versus','guide','ultimate']
		custom_intent 			= ['google','facebook','youtube','twitter','instagram','ebay','microsoft','apple','amazon','whatsapp'] # https://majestic.com/reports/majestic-million

		for element in informative_intent + transactional_intent + commercial_intent + custom_intent:
			if hasMatch(text, element):
				return True

		return False


	def getGeoInformationForLogging(self, ip):
		if len(ip) < 7:
			ip = "1.1.1.1"

		try:
			response 	= geoReader.city(ip)
			rec 		= database.get_all(ip)
			iso 		= str(response.country.iso_code)
			cn 			= str(response.country.name)
			ctn 		= str(response.city.name)
			pc 			= str(response.postal.code)
			lat 		= str(response.location.latitude)
			lon 		= str(response.location.longitude)
			region 		= str(response.subdivisions.most_specific.name)
			#return (iso+","+cn+","+ctn+","+pc+","+lat+","+lon)
			#return str(rec.country_short+","+rec.country_long+","+rec.region+","+rec.city+","+rec.zipcode+","+rec.latitude+","+rec.longitude+","+ip)

			cn1 		= str()
			region1		= str()
			cn1			= rec.country_long
			region1		= response.city.name

			if cn1 is None:
				cn1 	= str(response.country.name)
			else:
				cn1		= str(rec.country_long)

			if region1 is None:
				region1 = str(rec.region)
			else:
				region1	= str(response.city.name)

			return str(cn1+" -> "+region1)
		except Exception as a1:
			pass
		return str("iso"+","+"cn"+","+"region"+","+"ctn"+","+"pc"+","+"lat"+","+"lon"+","+"ip")


	def getGeoInformation(self, ip):
		if len(ip) < 7:
			ip = "1.1.1.1"

		try:
			response 	= geoReader.city(ip)
			iso 		= str(response.country.iso_code)
			cn 			= str(response.country.name)
			ctn 		= str(response.city.name)
			pc 			= str(response.postal.code)
			lat 		= str(response.location.latitude)
			lon 		= str(response.location.longitude)
			region 		= str(response.subdivisions.most_specific.name)
			#return (iso+","+cn+","+ctn+","+pc+","+lat+","+lon)
			return str(iso+","+cn+","+region+","+ctn+","+pc+","+lat+","+lon+","+ip)
		except Exception as a1:
			pass
		return str("iso"+","+"cn"+","+"region"+","+"ctn"+","+"pc"+","+"lat"+","+"lon"+","+"ip")


	def getGeoInformation2(self, ip):
		if len(ip) < 7:
			ip = "1.1.1.1"
		try:
			rec 		= database.get_all(ip)
			return str(rec.country_short+","+rec.country_long+","+rec.region+","+rec.city+","+rec.zipcode+","+rec.latitude+","+rec.longitude+","+ip)
		except Exception as as1:
			pass
		return str("iso"+","+"cn"+","+"region"+","+"ctn"+","+"pc"+","+"lat"+","+"lon"+","+"ip")


	def getGeoInformationAdvanced(self, ip):
		ip_obj 			= dict()

		iso 			= str("")
		cn 				= str("")
		ctn 			= str("")
		pc 				= str("")
		lat 			= str("48.364727")
		lon 			= str("10.900789")
		region 			= str("")

		iso2 			= str("")
		cn2 			= str("")
		ctn2 			= str("")
		pc2 			= str("")
		lat2 			= str("")
		lon2 			= str("")
		region2 		= str("")
		my_hostname		= str("")

		try:
			my_hostname	= str(socket.gethostbyaddr(ip)[0])
		except Exception as a1:
			pass

		if len(my_hostname) < 1:
			try:
				my_hostname	= str(socket.getnameinfo((ip, 0), 0)[0])
			except Exception as a1:
				pass

		if len(my_hostname) < 1:
			try:
				addr		= reversename.from_address(ip)
				my_hostname	= str(str(resolver.query(addr,"PTR")[0]))
			except Exception as a1:
				pass

		if len(my_hostname) < 1:
			my_hostname			= str(ip)

		ip_obj["ip_iso_code"] 	= iso
		ip_obj["ip_city"] 		= ctn
		ip_obj["ip_region"] 	= region
		ip_obj["ip_country"] 	= cn
		ip_obj["ip_postalcode"] = pc
		ip_obj["ip_latitude"] 	= lat
		ip_obj["ip_longitude"] 	= lon
		ip_obj["ip_address"] 	= str(ip)
		ip_obj["ip_hostname"] 	= str(my_hostname)

		lat 					= str("")	# Fallback, weil sonst in doSerpSearch() die LatLon Werte fehlen, wenn kein IP-to-Geo Auflösung funktioniert
		lon 					= str("")

		if len(ip) < 7:
			return ip_obj

		try:
			rec 		= database.get_all(ip)
			iso 		= str(rec.country_short)
			cn 			= str(rec.country_long)
			ctn 		= str(rec.city)
			pc 			= str(rec.zipcode)
			lat 		= str(rec.latitude)
			lon 		= str(rec.longitude)
			region 		= str(rec.region)
			#return str(rec.country_short+","+rec.country_long+","+rec.region+","+rec.city+","+rec.zipcode+","+rec.latitude+","+rec.longitude+","+ip)
		except Exception as as1:
			pass

		if len(iso) < 1 or len(cn) < 1 or len(region) < 1 or len(ctn) < 1 or len(pc) < 1 or len(lat) < 1 or len(lon) < 1:
			try:
				response 	= geoReader.city(ip)
				iso2 		= str(response.country.iso_code)
				cn2 		= str(response.country.name)
				ctn2 		= str(response.city.name)
				pc2 		= str(response.postal.code)
				lat2 		= str(response.location.latitude)
				lon2 		= str(response.location.longitude)
				region2 	= str(response.subdivisions.most_specific.name)
			except Exception as a1:
				pass

			if len(iso) < 1:
				iso = iso2
			if len(cn) < 1:
				cn = cn2
			if len(region) < 1:
				region = region2
			if len(ctn) < 1:
				ctn = ctn2
			if len(pc) < 1:
				pc = pc2
			if len(lat) < 1:
				lat = lat2
			if len(lon) < 1:
				lon = lon2

		ip_obj["ip_iso_code"] 	= iso
		ip_obj["ip_city"] 		= ctn
		ip_obj["ip_region"] 	= region
		ip_obj["ip_country"] 	= cn
		ip_obj["ip_postalcode"] = pc
		ip_obj["ip_latitude"] 	= lat
		ip_obj["ip_longitude"] 	= lon
		ip_obj["ip_address"] 	= str(ip)
		ip_obj["ip_hostname"] 	= str(my_hostname)
		return ip_obj


	def beautifyUpperLowercase(self, text):
		text1=self._beautifyUpperLowercase(text)
		text2=self._beautifyUpperLowercaseUmlauts(text1)
		return text2


	def _beautifyUpperLowercase(self, strString):
		#https://pypi.python.org/pypi/regex/
		#http://code.activestate.com/recipes/576984-split-a-string-on-capitalized-uppercase-char-using/
		if not isinstance(strString, str):
			strString=strString.decode("utf8")
		#result = re.sub(u'(?<=[A-Za-z])(?=[A-Z][a-z])', '<span style="color: blue">.</span> ', strString, re.UNICODE)
		result = re.sub(u'(?<=[A-Za-z])(?=[A-Z][a-z])', ' ', strString, re.UNICODE)
		return result


	def _beautifyUpperLowercaseUmlauts(self, strString):
		if not isinstance(strString, str):
			strString=strString.decode("utf8")
		#result = re.sub(u'(?<=[a-z])(?=[ÜÖÄ])', '<span style="color: blue">.</span> ', strString, re.UNICODE)
		result = re.sub(u'(?<=[a-z])(?=[ÜÖÄ])', ' ', strString, re.UNICODE)
		return result


	def doLsaSummarizer(self, text):
		# pip3 install -U sumy
		# https://github.com/miso-belica/sumy/tree/main/sumy/data/stopwords
		Language = self.detectTextLanguage(text)

		if "en" in Language.lower() or "en" == Language.lower():
			LANGUAGE = "english"
		elif "fr" in Language.lower() or "fr" == Language.lower():
			LANGUAGE = "french"
		elif "es" in Language.lower() or "es" == Language.lower():
			LANGUAGE = "spanish"
		elif "it" in Language.lower() or "it" == Language.lower():
			LANGUAGE = "italian"
		elif "ru" in Language.lower() or "ru" == Language.lower():
			LANGUAGE = "slovak"
		elif "zh" in Language.lower() or "zh" == Language.lower() or "cn" in Language.lower() or "cn" == Language.lower():
			LANGUAGE = "chinese"
		elif "de" in Language.lower() or "de" == Language.lower():
			LANGUAGE = "german"
		elif "pt" in Language.lower() or "pt" == Language.lower():
			LANGUAGE = "portuguese"
		elif "jp" in Language.lower() or "jp" == Language.lower():
			LANGUAGE = "japanese"
		elif "hi" in Language.lower() or "hi" == Language.lower() or "in" in Language.lower() or "in" == Language.lower():
			LANGUAGE = "hindi"
			hindi 	= self.split_sentences(text)
			if len(hindi) >= 3:
				return str(" ".join(hindi[:3]))
			else:
				return str(" ".join(hindi))
		elif "ar" in Language.lower() or "ar" == Language.lower() or "sa" in Language.lower() or "sa" == Language.lower():
			LANGUAGE = "arabic"
			hindi 	= self.split_sentences(text)
			if len(hindi) >= 3:
				return str(" ".join(hindi[:3]))
			else:
				return str(" ".join(hindi))
		else:
			LANGUAGE = "english"

		SENTENCES_COUNT	= 3
		text			= self.beautifyUpperLowercase(text)
		parser 			= PlaintextParser.from_string(text,Tokenizer(LANGUAGE))

		# or for plain text files
		# parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
		stemmer 		= Stemmer(LANGUAGE)
		summarizer 		= Summarizer(stemmer)
		summarizer.stop_words = get_stop_words(LANGUAGE)
		summarizer.null_words = get_stop_words(LANGUAGE)
		contentText		= str("")

		sent_list		= list()
		s_count			= 0
		for sentence in summarizer(parser.document, SENTENCES_COUNT):
			if s_count <= SENTENCES_COUNT:
				s_sent = str(sentence)
				#contentText=contentText+s_sent+" "
				sent_list.append(s_sent)
				s_count+=1

		return str(" ".join(sent_list))


	def detectTextLanguage0(self, text):	# https://github.com/whiletruelearn/langua
		#langT	=str("en")
		text		=str(text)
		pLangDetect = Predict()
		lang		= str()
		try:
			lang	= pLangDetect.get_lang(text)
		except Exception as e:
			pass#print("Language Detection failed: ",e)
		if lang in ['de','en','es','it','fr','ru','zh-cn','ja','pt','hi','ar','tr']:
			if lang == 'ja':
				return 'jp'
			if lang in 'zh-cn':
				return 'cn'
			if lang == 'hi':
				return 'in'
			if lang == 'ar':
				return 'sa'
			if lang == 'zh':
				return 'cn'
			return lang.lower()
		return str("")


	def detectTextLanguage1(self, text):
		#langT	=str("en")
		text		= str(text)
		lang		= str()
		try:
			lang	= detect(text)
		except Exception as e:
			pass#print("Language Detection failed: ",e)
		if lang in ['de','en','es','it','fr','ru','zh-cn','ja','pt','hi','ar','tr']:
			if lang == 'zh-cn':
				return 'cn'
			if lang == 'ja':
				return 'jp'
			if lang == 'hi':
				return 'in'
			if lang == 'ar':
				return 'sa'
			if lang == 'zh':
				return 'cn'
			return lang.lower()
		return str("")


	def detectTextLanguage2(self, text):	# https://github.com/saffsd/langid.py
		lang	= str()
		#langT	= str("en")
		text	= str(text)
		langid.set_languages(['de','en','es','it','fr','ru','zh','ja','pt','hi','ar','tr'])
		#try:
		langTemp= langid.classify(text)
		lang 	= langTemp[0].lower()
		#if lang in ['de','en','es','it','fr']:
		if lang in ['de','en','es','it','fr','ru','zh','ja','pt','hi','ar','tr']:
			if lang == 'ja':
				return 'jp'
			if lang == 'hi':
				return 'in'
			if lang == 'ar':
				return 'sa'
			if lang == 'zh':
				return 'cn'
			return lang.lower()
		#except Exception as e:
		#	pass#print("Language Detection failed: ",e)
		return str("")


	def detectTextLanguage3(self, text):	# https://github.com/aboSamoor/pycld2/blob/master/cld2/internal/generated_language.h
		#langT	= str("en")
		text	= str(text)
		lang	= str()
		try:
			isReliable, textBytesFound, details = cld2.detect(
				text, bestEffort=True
			)
			lang	= str(details[0][1]).lower()
		except Exception as e:
			pass#print("Language Detection failed: ",e)
		if lang in ['de','en','es','it','fr','ru','zh','ja','pt','hi','ar','tr']:
			if lang == 'ja':
				return 'jp'
			if lang == 'hi':
				return 'in'
			if lang == 'ar':
				return 'sa'
			if lang == 'zh':
				return 'cn'
			return lang.lower()
		return str("")


	def detectTextLanguage(self, text):
		# Language Detection via Fasttext: https://fasttext.cc/docs/en/language-identification.html
		text	= str(text)
		languz0	= str()
		languz1	= str()
		languz2	= str()
		languz3	= str()

		resList = list()

		try:
			languz0	= self.detectTextLanguage0(text)
			if len(languz0) == 2:
				resList.append(str(languz0.lower()))
		except Exception as as1:
			pass

		try:
			languz1	= self.detectTextLanguage1(text)
			if len(languz1) == 2:
				resList.append(str(languz1.lower()))
		except Exception as as1:
			pass
		try:
			languz2	= self.detectTextLanguage2(text)
			if len(languz2) == 2:
				resList.append(str(languz2.lower()))
		except Exception as as1:
			pass

		try:
			languz3	= self.detectTextLanguage3(text)
			if len(languz3) == 2:
				resList.append(str(languz3.lower()))
		except Exception as as1:
			pass

		return self.most_frequent(resList)


	def most_frequent(self, List):
		return max(set(List), key = List.count)


	def fixBrokenHTMLEntities(self, text):
		"""
		a.) &39;	(=DIGIT ONLY!)
		b.) replace "&" mit "&#"
		c.) html.unescape()
		richtig ist : "&#39;"
		"""
		###text  = "hd&39;Hc&36;"
		# match31	= '\&[a-z0-9A-Z]+\;'
		text 		= str(text)
		match37		= '\&[0-9]+\;' # &39;
		regex37		= re.compile(match37, re.IGNORECASE)
		match_obj	= regex37.findall(text)

		for elm in match_obj:
			elm_org = elm.replace("&","&#")
			elm_sub = unescape(elm_org)
			text 	= text.replace(elm, elm_sub)
			#print("elm_org",elm_org)
			#print("elm_sub",elm_sub)

		del match37
		del regex37
		del match_obj
		text 		= str(text)
		match37		= '\&#[0-9]+\;'	# t&#39;
		regex37		= re.compile(match37, re.IGNORECASE)
		match_obj	= regex37.findall(text)

		for elm in match_obj:
			elm_sub = unescape(elm)
			text 	= text.replace(elm, elm_sub)
			#print("elm_org",elm_org)
			#print("elm_sub",elm_sub)

		return text

	def isDomainBlacklisted(self, url):
		#return self.isBlacklisted(url, self.stoplist_domains_blocker)
		domain = str("")
		try:
			domain = urlparse(url).netloc
		except Exception as as1:
			pass

		if domain in self.stopdict_domains_blocker:
			return True
		return False

	def isPaywall(self, text):
		# return True: Blackliste gefunden
		# return False: Blackliste nicht gefunden
		#stoplist = "/home/unaique/library/blacklists/paywall.txt"
		return self.isBlacklisted(url, self.stoplist_paywall_blocker)

	def isPornBlacklisted(self, text):
		return self.isBlacklisted(text, self.stoplist_porn_blocker)

	def split_sentences(self, text):
		text = " " + text + "  "
		text = text.replace("\n"," ")
		text = re.sub(prefixes,"\\1<prd>",text)
		text = re.sub(websites,"<prd>\\1",text)
		if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
		text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
		text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
		text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
		text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
		text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
		text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
		text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
		if "”" in text: text = text.replace(".”","”.")
		if "\"" in text: text = text.replace(".\"","\".")
		if "!" in text: text = text.replace("!\"","\"!")
		if "?" in text: text = text.replace("?\"","\"?")
		text = text.replace(".",".<stop>")
		text = text.replace("?","?<stop>")
		text = text.replace("!","!<stop>")
		text = text.replace("<prd>",".")
		sentences = text.split("<stop>")
		sentences = sentences[:-1]
		sentences = [s.strip() for s in sentences]
		return sentences


	def getKnowledgeGraphMoreInfo(self, search, language):
		link 			= "https://kgsearch.googleapis.com/v1/entities:search?key=#######&limit=1&languages="+str(language)+"&indent=False&query="+str(search)
		response1 		= self.getWebpage(link)
		sentences  		= str("")
		if self.is_json(response1):
			try:
				response	= json.loads(response1)
				for element in response['itemListElement']:
					sentences = element['result']['detailedDescription']['articleBody']
			except Exception as a1:
				pass

			sents 			= self.split_sentences(sentences)
			sentences_c1	= sentences.count('.')
			sentences_c2	= sentences.count('!')
			sentences_c3	= sentences.count('?')

			if len(sents) > 0:
				return str(sents[0]) #sentences.split('.')[0]
			elif sentences_c1 == 1 or sentences_c2 == 1 or sentences_c3 == 1:
				return str(sentences)
			elif len(sentences) > 10:
				return str(sentences)
		return str("")

	def is_json(self, myjson):
		try:
			json.loads(myjson)
		except ValueError as e:
			return False
		return True

	def BingAPI(self, MainKeyword, SubKeywords, Language, enableFastmode):
		enableFastmode 		= self.useFastmode(MainKeyword+" "+SubKeywords)

		res_set        	 	= set()
		addSearchMK			= str()
		addSearchSK			= str()
		maxCounter 			= int(10)	# Quant gibt maximal 10 results her

		if enableFastmode:
			maxCounter 		= int(5)


		mk_words 			= self.count_words_regex(MainKeyword)
		sk_words 			= self.count_words_regex(SubKeywords)

		"""
		if (MainKeyword.count(" ") == 0 or mk_words == 0) and not enableFastmode:
			addSearchMK		= self.getKnowledgeGraphMoreInfo(MainKeyword, Language)

		if (SubKeywords.count(" ") == 0 or sk_words == 0) and not enableFastmode:
			addSearchSK		= self.getKnowledgeGraphMoreInfo(SubKeywords, Language)
		"""

		if mk_words >= 10:
			#addSearchSK_v2	= getKnowledgeGraphMoreInfo(SubKeywords, Language)
			#query_string    = str(SubKeywords+", "+addSearchSK_v2)
			query_string    = str(SubKeywords)
		elif sk_words >= 10:
			#addSearchMK_v2	= getKnowledgeGraphMoreInfo(MainKeyword, Language)
			#query_string    = str(MainKeyword+", "+addSearchMK_v2)
			query_string    = str(MainKeyword)
		else:
			#query_string    = str(MainKeyword+", "+addSearchMK+", "+SubKeywords+", "+addSearchSK)
			query_string    = str(MainKeyword+", "+SubKeywords)

		if "de" in Language.lower() or Language.lower() == "de":
			lang			= "de"
		elif "en" in Language.lower() or Language.lower() == "en":
			lang			= "en"
		elif "fr" in Language.lower() or Language.lower() == "fr":
			lang			= "fr"
		elif "es" in Language.lower() or Language.lower() == "es":
			lang			= "es"
		elif "it" in Language.lower() or Language.lower() == "it":
			lang			= "it"
		elif "ru" in Language.lower() or Language.lower() == "ru":
			lang			= "ru"
		elif "zh" in Language.lower() or Language.lower() == "zh" or "cn" in Language.lower() or Language.lower() == "cn":
			lang			= "CHT"
		elif "pt" in Language.lower() or Language.lower() == "pt":
			lang			= "pt"
		elif "jp" in Language.lower() or Language.lower() == "jp":
			lang			= "ja"
		elif "hi" in Language.lower() or Language.lower() == "hi" or "in" in Language.lower() or Language.lower() == "in":
			lang			= "en"
		elif "ar" in Language.lower() or Language.lower() == "ar" or "sa" in Language.lower() or Language.lower() == "sa":
			lang			= "en"
		elif "tr" in Language.lower() or Language.lower() == "tr":
			lang			= "tr"
		else:
			lang			= "en"

		#try:
		# https://github.com/searx/searx/tree/master/searx/engines
		#link 			= "https://api.qwant.com/v3/search/web?q=Hundenahrung&count=10&offset=0&locale=de_de"
		base_url 		= 'https://www.bing.com/'
		search_string 	= 'search?{query}&first=0'
		query 			= 'language:{} {}'.format(lang.upper(), query_string)
		search_path 	= search_string.format(query=urlencode({'q': query}), offset=0)
		website         = base_url + search_path

		#print(website)
		html_page       = self.getWebpage(website)
		#print(html_page)
		soup            = BeautifulSoup(html_page, "lxml")
		mcounter 		= int(0)
		for link in soup.findAll('a'):
			myLink		= str(link.get('href'))
			#myLink		= str(link.text)
			if self.is_url(myLink) and myLink.find("bing.com") == -1 and myLink.find("javascript:") == -1 and len(myLink) > 12 and not myLink.startswith('/') and (myLink.lower().startswith("http") or myLink.lower().startswith("https") ) and mcounter < maxCounter:
				#print("Link:",myLink)
				res_set.add(myLink)
				mcounter += int(1)

		#except Exception as a:
		#	#print("htmlify",a)
		#	pass
		return res_set

	def QuantAPI(self, MainKeyword, SubKeywords, Language, enableFastmode):
		enableFastmode 		= self.useFastmode(MainKeyword+" "+SubKeywords)

		res_set        	 	= set()
		addSearchMK			= str()
		addSearchSK			= str()
		maxCounter 			= int(10)	# Quant gibt maximal 10 results her

		if enableFastmode:
			maxCounter 		= int(5)


		mk_words 			= self.count_words_regex(MainKeyword)
		sk_words 			= self.count_words_regex(SubKeywords)

		"""
		if (MainKeyword.count(" ") == 0 or mk_words == 0) and not enableFastmode:
			addSearchMK		= self.getKnowledgeGraphMoreInfo(MainKeyword, Language)

		if (SubKeywords.count(" ") == 0 or sk_words == 0) and not enableFastmode:
			addSearchSK		= self.getKnowledgeGraphMoreInfo(SubKeywords, Language)
		"""

		if mk_words >= 10:
			#addSearchSK_v2	= getKnowledgeGraphMoreInfo(SubKeywords, Language)
			#query_string    = str(SubKeywords+", "+addSearchSK_v2)
			query_string    = str(SubKeywords)
		elif sk_words >= 10:
			#addSearchMK_v2	= getKnowledgeGraphMoreInfo(MainKeyword, Language)
			#query_string    = str(MainKeyword+", "+addSearchMK_v2)
			query_string    = str(MainKeyword)
		else:
			#query_string    = str(MainKeyword+", "+addSearchMK+", "+SubKeywords+", "+addSearchSK)
			query_string    = str(MainKeyword+", "+SubKeywords)

		if "de" in Language.lower() or Language.lower() == "de":
			lang			= "de_de"
		elif "en" in Language.lower() or Language.lower() == "en":
			lang			= "en_us"
		elif "fr" in Language.lower() or Language.lower() == "fr":
			lang			= "fr_fr"
		elif "es" in Language.lower() or Language.lower() == "es":
			lang			= "es_es"
		elif "it" in Language.lower() or Language.lower() == "it":
			lang			= "it_it"
		elif "ru" in Language.lower() or Language.lower() == "ru":
			lang			= "us_en"
		elif "zh" in Language.lower() or Language.lower() == "zh" or "cn" in Language.lower() or Language.lower() == "cn":
			lang			= "zh_cn"
		elif "pt" in Language.lower() or Language.lower() == "pt":
			lang			= "pt_pt"
		elif "jp" in Language.lower() or Language.lower() == "jp":
			lang			= "us_en"
		elif "hi" in Language.lower() or Language.lower() == "hi" or "in" in Language.lower() or Language.lower() == "in":
			lang			= "us_en"
		elif "ar" in Language.lower() or Language.lower() == "ar" or "sa" in Language.lower() or Language.lower() == "sa":
			lang			= "us_en"
		elif "tr" in Language.lower() or Language.lower() == "tr":
			lang			= "us_en"
		else:
			lang			= "us_en"

		#try:
		# https://github.com/searx/searx/tree/master/searx/engines
		#link 			= "https://api.qwant.com/v3/search/web?q=Hundenahrung&count=10&offset=0&locale=de_de"
		website         = "https://api.qwant.com/v3/search/web?q="+query_string+"&count=10&offset=0&locale="+lang
		#print(website)
		html_page       = self.getWebpage(website)
		if self.is_json(html_page):
			#print("isjson")
			search_results 	= json.loads(html_page)
			data 			= search_results.get('data', {})
			mcounter 		= int(0)
			if search_results.get('status') == 'success':
				mainline = data.get('result', {}).get('items', {}).get('mainline', {})
				if not mainline:
					return res_set

				for row in mainline:
					mainline_type = row.get('type', 'web')
					if mainline_type != 'web':
						continue

					mainline_items = row.get('items', [])
					for item in mainline_items:
						#title 	= item.get('title', None)
						myLink = item.get('url', "")
						#if not textify.isDomainBlacklisted(myLink) and len(myLink) > 12 and not myLink.lower().endswith(".pdf") and (myLink.lower().startswith("http") or myLink.lower().startswith("https") ):
						#if len(myLink) > 12 and (myLink.lower().startswith("http") or myLink.lower().startswith("https") ) and mcounter < maxCounter:
						#print("/api.qwant.com Adding Website:",str(myLink))
						res_set.add(myLink)
						mcounter += int(1)

		#except Exception as a:
		#	#print("htmlify",a)
		#	pass
		return res_set


	def DuckduckgoAPI(self, MainKeyword, SubKeywords, Language, enableFastmode):
		#print("DuckduckgoAPI")
		res_set        	 	= set()
		addSearchMK			= str()
		addSearchSK			= str()
		maxCounter 			= int(50)

		if enableFastmode:
			maxCounter 		= int(5)

		mk_words 			= self.count_words_regex(MainKeyword)
		sk_words 			= self.count_words_regex(SubKeywords)

		if mk_words >= 10:
			#addSearchSK_v2	= getKnowledgeGraphMoreInfo(SubKeywords, Language)
			#query_string    = str(SubKeywords+", "+addSearchSK_v2)
			query_string    = str(SubKeywords)
		elif sk_words >= 10:
			#addSearchMK_v2	= getKnowledgeGraphMoreInfo(MainKeyword, Language)
			#query_string    = str(MainKeyword+", "+addSearchMK_v2)
			query_string    = str(MainKeyword)
		else:
			#query_string    = str(MainKeyword+", "+addSearchMK+", "+SubKeywords+", "+addSearchSK)
			query_string    = str(MainKeyword+", "+SubKeywords)

		# https://api.duckduckgo.com/api
		# https://duckduckgo.com/params
		# https://help.duckduckgo.com/duckduckgo-help-pages/results/syntax/
		if "de" in Language.lower() or Language.lower() == "de":
			lang			= "de-de"
		elif "en" in Language.lower() or Language.lower() == "en":
			lang			= "us-en"
		elif "fr" in Language.lower() or Language.lower() == "fr":
			lang			= "fr-fr"
		elif "es" in Language.lower() or Language.lower() == "es":
			lang			= "es-es"
		elif "it" in Language.lower() or Language.lower() == "it":
			lang			= "it-it"
		elif "ru" in Language.lower() or Language.lower() == "ru":
			lang			= "ru-ru"
		elif "zh" in Language.lower() or Language.lower() == "zh" or "cn" in Language.lower() or Language.lower() == "cn":
			lang			= "cn-zh"
		elif "pt" in Language.lower() or Language.lower() == "pt":
			lang			= "pt-pt"
		elif "jp" in Language.lower() or Language.lower() == "jp":
			lang			= "jp-jp"
		elif "hi" in Language.lower() or Language.lower() == "hi" or "in" in Language.lower() or Language.lower() == "in":
			lang			= "in-en"
		elif "ar" in Language.lower() or Language.lower() == "ar" or "sa" in Language.lower() or Language.lower() == "sa":
			lang			= "xa-ar"
		elif "tr" in Language.lower() or Language.lower() == "tr":
			lang			= "tr-tr"
		else:
			lang			= "us-en"

		#print("DuckduckgoAPI fetch")
		#try:
		#website         = "https://html.duckduckgo.com/html/?q="+query_string+"&lang="+lang
		# https://help.duckduckgo.com/features/safe-search/ -> &kp=1 (strict), &kp=-1 (moderate - don't show explicit results), or &kp=-2 (off)
		#website         = "https://html.duckduckgo.com/html/?q="+query_string+"&lang="+lang+"&kl="+lang+"&kp=1&kaf=1&t=artikelschreiber.com" #"&lang=de-de&kl=de-de"
		website         = "https://duckduckgo.com/html?q="+query_string+"&kl="+lang+"&ia=web&kp=1&kaf=1&t=artikelschreiber.com"
		html_page       = self.getWebpage(website)
		#print("DuckduckgoAPI html",website)
		soup            = BeautifulSoup(html_page, "lxml")
		mcounter 		= int(0)
		for link in soup.findAll('a', attrs={'class' : 'result__url'}):
			#myLink		= str(link.get('href'))
			myLink		= str(link.text)
			#print("DuckduckgoAPI Link:",myLink)
			if len(myLink) > 12 and not myLink.startswith('/') and (myLink.lower().startswith("http") or myLink.lower().startswith("https") ) and mcounter < maxCounter:
				res_set.add(myLink)
				mcounter += int(1)

		#except Exception as a:
		#	#print("htmlify",a)
		#	pass

		return res_set

	def getWebpage(self, link):
		#ftfy.fix_text(text, *, fix_entities='auto', remove_terminal_escapes=True, fix_encoding=True, fix_latin_ligatures=True, fix_character_width=True, uncurl_quotes=True, fix_line_breaks=True, fix_surrogates=True, remove_control_chars=True, remove_bom=True, normalization='NFC', max_decode_length=1000000)
		if isinstance(link, str) and (link.lower().startswith("http") or link.lower().startswith("https")):
			# use python request library for fetching
			#print("getWebpage(self, link)",link)
			try:
				with requests.get(link, headers=HeadersSimple, timeout=60, verify=False, allow_redirects=True) as r1: #keep alive
					#r1 			= requests.get(link, headers=HeadersSimple, timeout=6, verify=False)
					#r1.encoding = r1.apparent_encoding
					#r1.encoding = 'utf-8'
					#r1.encoding = 'latin-1'
					myStatus		= r1.status_code
					myText 			= str(r1.text)
					myContent		= str(r1.headers['content-type'])
					myText			= myText.replace('\n', ' ')
					myText			= myText.replace("\n", ' ')
					mT1 			= myText.strip()
					#print("getWebpage(self, link),Status Code:",myStatus," -> ",link)
					if myStatus == 200:
						#print("htmlify.getWebpage() Webpage size HTTP:", str(myStatus)," -> ", len(myText)," -> ", myContent)
						return str(mT1)
					else:
						return str("")
			except Exception as er:
				#print("Unexpected error: getWebpage(link)", sys.exc_info()[0])
				#exc_type, exc_obj, exc_tb = sys.exc_info()
				#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				#print(exc_type, fname, exc_tb.tb_lineno)
				return str("")
				pass

		#print("htmlify.getWebpage(link): Empty HTML Document!")
		return str("")

	def isLowQualityContent(self, text):
		# Um so höher die Zahl bzw. der Counter, um so schlechter der Score
		mycounter = int(0)
		for stopword in low_quality_content:
			if self.isFound(text, stopword):
				#print("Stopword found:",stopword)
				mycounter += int(1)
		#True, False
		return mycounter

	def isLowQualityContentText(self, text):
		# Um so höher die Zahl bzw. der Counter, um so schlechter der Score
		mycounter = False
		for stopword in low_quality_content:
			if self.isFound(text, stopword):
				#print("Stopword found:",stopword)
				mycounter = True	# schlechte Ergebnisse, dh. geringwertiger Content
		#True, False
		return mycounter


	def remove_control_characters1(self, s):
		return re1.sub(r'\p{C}', '', s)


	def isFound(self, text, stopword):
		# return True: Stopwort in Text gefunden
		# return False: Stopwort nicht in Text gefunden
		#print("Text:'"+text+"' und Stopword:'"+stopword+"'")
		t_text_org		= str(text)
		text 			= str(text.lower().strip("\n"))
		text_len 		= len(text)
		stopword 		= str(stopword).lower()
		space_stopword 	= str(" ")+str(stopword)+str(" ")

		#https://www.pythontutorial.net/python-regex/python-regex-word-boundary/
		matches1 		= re.finditer(r'\b'+stopword+'\b', text)

		for match in matches1:
			if match:
				return True

		if text.count(space_stopword) >= 1:
			#if space_stopword.find(text) != -1:
			#print("isBlacklisted() text.find() Match:",text,ele)
			return True

		if stopword == t_text_org.lower():
			return True

		if stopword in text:
			return True

		if "_" in text or "-" in text and text_len >= 2 and text_len < 6:
			#print("Text:'"+text+"' und Stopword:'"+stopword+"'")
			if text.find(stopword) != -1:
				return True

		return False


	def get_dictionary_by_key_value(self, dictionary, target_key, target_value):
		"""Return a dictionary that contains a target key value pair.

		Args:
			dictionary: Metadata dictionary containing lists of other dictionaries.
			target_key: Target key to search for within a dictionary inside a list.
			target_value: Target value to search for within a dictionary inside a list.

		Returns:
			target_dictionary: Target dictionary that contains target key value pair.
		"""

		for key in dictionary:
			if len(dictionary[key]) > 0:
				for item in dictionary[key]:
					if item[target_key] == target_value:
						return item


	def get_title(self, html):
		"""Scrape page title."""
		#title = str("")
		#import os, sys
		try:
			#if html.title.string:
			#	title = html.title.string
			for title in html.find_all('title'):
				return str(title.get_text())
		except Exception as as1:
			#print("Catching Exception at get_title(self, html):", e)
			#print("Unexpected error:", sys.exc_info()[0])
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			pass
		try:
			if html.find("meta", property="og:title"):
				description = html.find("meta", property="og:title").get('content')
				return self.extractTextFromHTML(description)
		except Exception as as1:
			#print("Catching Exception at get_title(self, html):", e)
			#print("Unexpected error:", sys.exc_info()[0])
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			pass
		try:
			if html.find("meta", property="twitter:title"):
				description = html.find("meta", property="twitter:title").get('content')
				return self.extractTextFromHTML(description)
		except Exception as as1:
			#print("Catching Exception at get_title(self, html):", e)
			#print("Unexpected error:", sys.exc_info()[0])
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			pass
		try:
			if html.find("h1"):
				title = html.find("h1").string
				return title
		except Exception as as1:
			#print("Catching Exception at get_title(self, html):", e)
			#print("Unexpected error:", sys.exc_info()[0])
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			pass
		try:
			if html.find_all("h1"):
				title = html.find_all("h1")[0].string
				return title
		except Exception as as1:
			#print("Catching Exception at get_title(self, html):", e)
			#print("Unexpected error:", sys.exc_info()[0])
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			pass
		try:
			if title:
				title = title.split('|')[0].strip()
			#title = title.split('-')[0].strip()
		except Exception as as1:
			#print("Catching Exception at get_title(self, html):", e)
			#print("Unexpected error:", sys.exc_info()[0])
			#exc_type, exc_obj, exc_tb = sys.exc_info()
			#fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			#print(exc_type, fname, exc_tb.tb_lineno)
			pass
		return str("")


	def get_description(self, html):
		#description = str("")
		try:
			if html.find("meta", property="og:description"):
				description = html.find("meta", property="og:description").get('content')
				return description
		except Exception as as1:
			pass
		try:
			if html.find("meta", property="description"):
				description = html.find("meta", property="description").get('content')
				return description
		except Exception as as1:
			pass
		try:
			if html.find("meta", property="twitter:description"):
				description = html.find("meta", property="twitter:description").get('content')
				return description
		except Exception as as1:
			pass
		try:
			if html.find("p"):
				description = html.find("p").get('content')
				return self.extractTextFromHTML(description)
		except Exception as as1:
			pass

		return str("")


	def get_image(self, html, web_url):
		"""Scrape share image."""
		#image = str("")
		try:
			if html.find("meta", property="image"):
				image = html.find("meta", property="image").get('content')
				li = urljoin(web_url, image)
				return li
		except Exception as as1:
			pass
		try:
			if html.find("meta", property="og:image"):
				image = html.find("meta", property="og:image").get('content')
				li = urljoin(web_url, image)
				return li
		except Exception as as1:
			pass
		try:
			if html.find("meta", property="twitter:image"):
				image = html.find("meta", property="twitter:image").get('content')
				li = urljoin(web_url, image)
				return li
		except Exception as as1:
			pass
		try:
			if html.find_all("img", src=True):
				image = html.find_all("img")
				if image:
					image = html.find_all("img")[0].get('src')
					li = urljoin(web_url, image)
					return li
		except Exception as as1:
			pass
		return str("")


	def get_video(self, html):
		#og_video = str("")
		try:
			og_video = html.find("meta", property="og:video").get('content')
			return og_video
			#og_language2 = html.find("meta", attrs={'property':'og:locale'}).get('content')
		except Exception as as1:
			pass
		return str("")


	def get_meta_keywords(self, soup, text, url):
		listKeywordBlogs 	= ["BlogPosting", "NewsArticle", "Article", "CreativeWork", "Organization","Product"]
		# https://practicaldatascience.co.uk/data-science/how-to-scrape-schemaorg-metadata-using-python
		try:
			base_url 	= get_base_url(text, url)
			metadata 	= extruct.extract(text,
									   base_url=base_url,
									   uniform=True,
									   syntaxes=['json-ld',
											 'microdata',
											 'opengraph'])
		except Exception as as1:
			pass

		for element in listKeywordBlogs:
			try:
				kw = get_dictionary_by_key_value(metadata, "@type", element)
				return str(kw['keywords'])
			except Exception as as1:
				pass

		try:
			kwords 	= str(soup.find("meta", attrs={'name':'keywords'}).get('content'))

			if len(kwords) > 21:
				return kwords

		except Exception as as1:
			pass

		return str("")


	def get_og_locale(self, html):

		og_language = str("")
		LANGUAGE 	= str("")
		try:
			og_language = html.find("meta", property="og:locale").get('content')
			#og_language2 = html.find("meta", attrs={'property':'og:locale'}).get('content')
		except Exception as as1:
			pass

		if self.isFound(og_language, "en"):
			LANGUAGE = "en"
		if self.isFound(og_language, "fr"):
			LANGUAGE = "fr"
		if self.isFound(og_language, "es"):
			LANGUAGE = "es"
		if self.isFound(og_language, "it"):
			LANGUAGE = "it"
		if self.isFound(og_language, "ar") or self.isFound(og_language, "sa"):
			LANGUAGE = "ar"
		if self.isFound(og_language, "tr"):
			LANGUAGE = "tr"
		if self.isFound(og_language, "ru"):
			LANGUAGE = "ru"
		if self.isFound(og_language, "zh") or self.isFound(og_language, "cn"):
			LANGUAGE = "zh"
		if self.isFound(og_language, "de"):
			LANGUAGE = "de"
		if self.isFound(og_language, "pt"):
			LANGUAGE = "pt"
		if self.isFound(og_language, "jp") or self.isFound(og_language, "ja"):
			LANGUAGE = "ja"
		if self.isFound(og_language, "in") or self.isFound(og_language, "hi"):
			LANGUAGE = "in"

		if len(LANGUAGE) == 2:
			return str(LANGUAGE)

		try:
			#og_language1 = html.find("meta", property="og:locale").get('content')
			og_language = html.find("meta", attrs={'property':'og:locale'}).get('content')
		except Exception as as1:
			pass

		if self.isFound(og_language, "en"):
			LANGUAGE = "en"
		if self.isFound(og_language, "fr"):
			LANGUAGE = "fr"
		if self.isFound(og_language, "es"):
			LANGUAGE = "es"
		if self.isFound(og_language, "it"):
			LANGUAGE = "it"
		if self.isFound(og_language, "ar") or self.isFound(og_language, "sa"):
			LANGUAGE = "ar"
		if self.isFound(og_language, "tr"):
			LANGUAGE = "tr"
		if self.isFound(og_language, "ru"):
			LANGUAGE = "ru"
		if self.isFound(og_language, "zh") or self.isFound(og_language, "cn"):
			LANGUAGE = "zh"
		if self.isFound(og_language, "de"):
			LANGUAGE = "de"
		if self.isFound(og_language, "pt"):
			LANGUAGE = "pt"
		if self.isFound(og_language, "jp") or self.isFound(og_language, "ja"):
			LANGUAGE = "ja"
		if self.isFound(og_language, "in") or self.isFound(og_language, "hi"):
			LANGUAGE = "in"

		if len(LANGUAGE) == 2:
			return str(LANGUAGE)

		try:
			# <html lang="en" dir="ltr" class="ltr no-js">
			# <html lang="de-DE" prefix="og: https://ogp.me/ns#">
			og_language = html.find("html").attrs.get('lang')
		except Exception as as1:
			pass

		if self.isFound(og_language, "en"):
			LANGUAGE = "en"
		if self.isFound(og_language, "fr"):
			LANGUAGE = "fr"
		if self.isFound(og_language, "es"):
			LANGUAGE = "es"
		if self.isFound(og_language, "it"):
			LANGUAGE = "it"
		if self.isFound(og_language, "ar") or self.isFound(og_language, "sa"):
			LANGUAGE = "ar"
		if self.isFound(og_language, "tr"):
			LANGUAGE = "tr"
		if self.isFound(og_language, "ru"):
			LANGUAGE = "ru"
		if self.isFound(og_language, "zh") or self.isFound(og_language, "cn"):
			LANGUAGE = "zh"
		if self.isFound(og_language, "de"):
			LANGUAGE = "de"
		if self.isFound(og_language, "pt"):
			LANGUAGE = "pt"
		if self.isFound(og_language, "jp") or self.isFound(og_language, "ja"):
			LANGUAGE = "ja"
		if self.isFound(og_language, "in") or self.isFound(og_language, "hi"):
			LANGUAGE = "in"

		if len(LANGUAGE) == 2:
			return str(LANGUAGE)

		return str("")


	def get_links(self, html, web_url):
		links = set()
		for link in html.findAll('a'):
			link_href = link.get('href')
			if not self.isFound(link_href,"javascript"):
				li = urljoin(web_url, link_href) # https://stackoverflow.com/questions/44001007/scrape-the-absolute-url-instead-of-a-relative-path-in-python
				links.add(li)
		return list(links)


	def count_words_regex(self, text):
		# Counting words with regular expressions -> https://datagy.io/python-count-words/#:~:text=%23-,Counting%20words,-with%20regular%20expressions
		return len(re.findall(r'\w+', text))


	# https://practicaldatascience.co.uk/data-science/how-to-identify-internal-and-external-links-using-python#:~:text=Determine%20whether%20the%20link%20is%20internal%20or%20external
	def is_internal(self, url, domain):
		if not bool(urlparse(url).netloc):
			return True
		elif url.startswith(domain):
			return True
		else:
			return False #is_external


	def isBlacklisted(self, text, stoplist):
		# return True: Stopwort in Blackliste gefunden
		# return False: Stopwort nicht in Blackliste gefunden
		text 	= str(text.lower().strip("\n"))
		for x in range(len(stoplist)):
			ele2	= str(stoplist[x].lower().strip("\n"))
			if not ele2.startswith("#") and len(ele2) >= 1:
			#	print("Ele:",ele2)
				if self.isFound(text, ele2):
				#	print("Stopword isFound:'",ele2,"'")
					return True
				if ele2.find(text) != -1 or text.find(ele2) != -1:
				#	print("Stopword is -find-:'",ele2,"'")
					return True

		return False


	def currency_symbols(self, text: str, repl: str = "_CUR_") -> str:
		"""Replace all currency symbols in ``text`` with ``repl``."""
		return RE_CURRENCY_SYMBOL.sub(repl, text)


	def emails(self, text: str, repl: str = "_EMAIL_") -> str:
		"""Replace all email addresses in ``text`` with ``repl``."""
		return RE_EMAIL.sub(repl, text)


	def emojis(self, text: str, repl: str = "_EMOJI_") -> str:
		"""
		Replace all emoji and pictographs in ``text`` with ``repl``.

		Note:
			If your Python has a narrow unicode build ("USC-2"), only dingbats
			and miscellaneous symbols are replaced because Python isn't able
			to represent the unicode data for things like emoticons. Sorry!
		"""
		return RE_EMOJI.sub(repl, text)


	def hashtags(self, text: str, repl: str = "_TAG_") -> str:
		"""Replace all hashtags in ``text`` with ``repl``."""
		return RE_HASHTAG.sub(repl, text)


	def numbers(self, text: str, repl: str = "_NUMBER_") -> str:
		"""Replace all numbers in ``text`` with ``repl``."""
		return RE_NUMBER.sub(repl, text)


	def phone_numbers(self, text: str, repl: str = "_PHONE_") -> str:
		"""Replace all phone numbers in ``text`` with ``repl``."""
		return RE_PHONE_NUMBER.sub(repl, text)


	def urls(self, text: str, repl: str = "_URL_") -> str:
		"""Replace all URLs in ``text`` with ``repl``."""
		return RE_SHORT_URL.sub(repl, RE_URL.sub(repl, text))


	def user_handles(self, text: str, repl: str = "_USER_") -> str:
		"""Replace all (Twitter-style) user handles in ``text`` with ``repl``."""
		return RE_USER_HANDLE.sub(repl, text)


	def preprocess_text(self, x):
		x = str(x)
		#x = currency_symbols(x, " ")
		x = self.emails(x, " ")
		x = self.phone_numbers(x, " ")
		x = self.emojis(x, " ")
		x = self.hashtags(x, " ")
		x = self.user_handles(x, " ")
		x = re.sub(r"\s{2,}", " ", x) 		# over spaces

		"""
		if isCode(x):
			x = currency_symbols(x, "")
			#x = urls(x, "")
			#x = x.encode("ascii", "ignore").decode() # unicode
			x = re.sub("[^.,!?A-Za-z0-9]+", " ", x) # special charachters except .,!?
			x = ""
		"""
		return str(x)


	def isCode(self, text):
		myCode 		= ["=","{","}",":","|","$","_","(",")",">","<"]
		myCount 	= 0
		for c in myCode:
			myCount += text.count(c)
		if myCount > 3:
			return True	# BAD: We have JavaScript Code
		return False	# Good: We have NO JavaScript Code


	def count_spaces(self, s):
		return len(s) - len(s.strip())


	def extractTextFromHTML(self, html):
		try:
			article.set_html(html)
			article.parse()
			return str(article.text)
		except Exception as as1:
			pass


		try:
			#soup 			= BeautifulSoup(html, "html5lib") #"lxml") # pip install -U html5lib # https://zetcode.com/python/beautifulsoup/
			#soup 			= BeautifulSoup(html, "html.parser")
			soup 			= BeautifulSoup(html, "lxml")

			for tag in soup():
				# CSS to remove attributes -> https://itecnote.com/tecnote/python-remove-all-inline-styles-using-beautifulsoup/
				for attribute in ["class", "id", "name", "style"]:
					del tag[attribute]

			for data in soup(['style', 'script', 'comment']):
				# Remove tags -> https://www.geeksforgeeks.org/remove-all-style-scripts-and-html-tags-using-beautifulsoup/
				data.decompose()

			myText = str(soup.find('body').text) # https://www.geeksforgeeks.org/find-the-text-of-the-given-tag-using-beautifulsoup/
			return re.sub(r"\s{2,}", " ", myText)
		except Exception as as1:
			pass


		try:
			f       			= re.findall('\>(.*?)\<', html , re.MULTILINE | re.DOTALL)
			rList   			= list()
			lastStr 			= str("")
			for ele in f:
				ele	= ele.strip()
				t = self.remove_control_characters1(ele)
				rList.append(t)
			return str(self.remove_text_inside_brackets(" ".join(rList)))
		except Exception as as1:
			pass

		return str("")


	def headline_extractor(self, headline, soup):
		# Hinweis: Wir befinden uns bei der Artikel Quelle sogut wie immer auf einer URI nicht auf einer URL, somit gehen wir davon aus, dass alle H3-Sub-Unterschriften genau einer H1-Überschrift übergeordnet sind
		tmp_cont_list			= list()
		tmp_str					= str("")
		resultLists				= list()
		myTelerHeadlines		= {}
		sit 					= soup.findAll(headline)
		headline_text			= str("")
		for h1 in sit:
			h 					= h1.text.strip()			# Überschrift
			tags 				= h1.find_next_siblings() 	# Alle Texte unterhalb dieser Überschrift
			headl_txt 			= self.preprocess_text(h)
			headl_txt_len		= len(headl_txt)

			if headl_txt and headl_txt_len >= self.headline_min_length:
				headline_text	= headl_txt

			for tag in tags:
				tag_content 	= str(tag.get_text()) 		# -> not working: extractTextFromHTML(str(tag).string)
				tag_content_len = len(tag_content)
				if tag_content and tag_content_len >= self.headline_min_length:
					count_space_int = self.count_spaces(tag_content)
					if count_space_int <= self.max_spaces_count and self.count_words_regex(tag_content) >= self.min_word_count and tag_content_len >= self.min_text_length:
						#print(h+" -> # \t\t Spaces:",count_space_int," -> "+tag_content+" -> Len:",tag_content_len)
						#headline_text	= preprocess_text(h)
						tmp_str12	= self.preprocess_text(tag_content)
						tmp_cont_list.append(tmp_str12)
						tmp_str12	= str("")

		tmp_str 													= str(" ".join(tmp_cont_list))

		if headline.lower() == "h1":
			myTelerHeadlines[headline] 								= headline_text
			myTelerHeadlines[headline+"_text"] 						= headline_text
			myTelerHeadlines[headline+"_text_low_quality_score"] 	= self.isLowQualityContent(headline_text)
			myTelerHeadlines[headline+"_text_ai"]					= str("")		# h1-Überschrift wird nie mittels KI umgewandelt
			myTelerHeadlines[headline+"_text_ai_plagscore"]			= int(0)		# h1-Überschrift wird nie mittels KI umgewandelt
			myTelerHeadlines[headline+"_text_till_end"]				= headline_text
			myTelerHeadlines[headline+"_text_till_end_low_quality_score"] 	= self.isLowQualityContent(headline_text)
			resultLists.append(myTelerHeadlines)
			del myTelerHeadlines
			del tmp_str

		else:
			myTelerHeadlines[headline] 								= headline_text
			myTelerHeadlines[headline+"_text"] 						= tmp_str
			myTelerHeadlines[headline+"_text_low_quality_score"] 	= self.isLowQualityContent(tmp_str)
			myTelerHeadlines[headline+"_text_ai"]					= str("")
			myTelerHeadlines[headline+"_text_ai_plagscore"]			= int(0)
			myTelerHeadlines[headline+"_text_till_end"]				= str("")
			myTelerHeadlines[headline+"_text_till_end_low_quality_score"] 	= int(0)
			resultLists.append(myTelerHeadlines)
			del myTelerHeadlines
			del tmp_str

		return resultLists


	def headline_to_html_end_extractor(self, headline, matching_text, soup):
		#soup 			= BeautifulSoup(html, "html5lib") # wir brauchen hier das html5lib
		# Code für H2-Headline bis zum finalen "</html>"-Tag
		tmp_set 		= set()
		tmp_list 		= list()
		hit_found 		= False
		#[tag.name for tag in soup.find_all()] https://www.geeksforgeeks.org/get-all-html-tags-with-beautifulsoup/
		for tag in soup.find_all():
			tag_text 				= str(tag.text)
			tag_content				= tag.prettify()	# str(tag) oder tag.prettify() enthält das HTML -> https://stackoverflow.com/questions/25729589/how-to-get-html-from-a-beautiful-soup-object
			tag_name				= str(tag.name)
			tag_text_preprocessed 	= preprocess_text(tag_text)
			#if self.isFound(tag_name, headline):#(headline in tag_name or headline == tag_name):
			#	1#print("'"+tag_name+"'---#headline#--->>>"+tag_text)
			#if self.isFound(tag_text, matching_text):# and self.isFound(tag_name, headline):
			#	1#print("'"+tag_name+"'---#isFound#--->>>"+tag_text)
			if self.isFound(tag_text, matching_text) and self.isFound(tag_name, headline):
				#print("'"+tag_name+"'---#isFound#--->>>"+tag_text)
				hit_found = True
			if hit_found and tag_text_preprocessed not in tmp_set and re.findall(r'\w+[.!?]$', tag_text_preprocessed, re.MULTILINE | re.DOTALL | re.IGNORECASE | re.UNICODE):
				tmp_list.append(tag_content)
				tmp_set.add(tag_text_preprocessed)	# der Text soll nicht doppelt sein, jedes zugefügte Wort muss eine Satzendung haben [.!?]
				#print("Word with Sentence Ending:",tag_text)
				#print(tag.attrs)
		#print(hit_found)
		#print(matching_text)
		#sys.exit(1)
		pre_html = str(" ".join(tmp_list))
		return self.extractTextFromHTML(pre_html)

	def generateBeautifulTitle(self, text):
		special_char_map 	= {ord('ä'):'ae', ord('ü'):'ue', ord('ö'):'oe', ord('ß'):'ss'} # https://stackoverflow.com/questions/2054746/how-to-search-and-replace-utf-8-special-characters-in-python
		result 				= re.sub(r'(\w{2,})\.(\w{2,})', 'ArtikelSchreiber.com', text)
		title				= result.translate(special_char_map)
		title_split 		= list()

		if title.find("|") != -1:
			title_split = title.split("|")
		elif title.find(" - ") != -1:
			title_split = title.split(" - ") # we want this " Walking - The good choice?" and not those "4-Tage-Bart"
			#print("'-' split:",title_split)
		elif title.find(":") != -1:
			title_split = title.split(":")
			#print("':' split:",title_split)
		elif title.find("?") != -1:
			title_split = title.split("?")
			#print("'?' split:",title_split)
		elif title.find("&") != -1:
			title_split = title.split("&")
			#print("'&' split:",title_split)
		elif title.find(",") != -1:
			title_split = title.split(",")
			#print("',' split:",title_split)
		elif title.find(";") != -1:
			title_split = title.split(";")
			#print("';' split:",title_split)

		if len(title_split) >= 2:
			return str(title_split[0]).strip()
		else:
			return str(title)
		return str(text)

	def generateCanonicalURL(self, myTmpTitle, alternative_url, language):
		seo_lang_add 		= dict()
		seo_lang_add["de"] 	= str("artikel")
		seo_lang_add["en"] 	= str("article")
		seo_lang_add["it"] 	= str("articolo")
		seo_lang_add["es"] 	= str("articulo")
		seo_lang_add["fr"] 	= str("article")

		special_char_map 	= {ord('ä'):'ae', ord('ü'):'ue', ord('ö'):'oe', ord('ß'):'ss'} # https://stackoverflow.com/questions/2054746/how-to-search-and-replace-utf-8-special-characters-in-python

		regex 				= re.compile('[^a-zA-Z0-9 öäüßÖÄÜ]')

		ws_filter 			= re.compile(r"\s+") # multiple space "    " to one space " "
		max_canonical_words = int(5)			# maximum Website Title words in the final canonical url

		title_tmp		= myTmpTitle
		title 			= ws_filter.sub(" ",title_tmp).strip()
		title_content 	= str("")
		title_split		= list()

		if title.find(":") != -1:
			title_split = title.split(":")
			#print("':' split:",title_split)

		if title.find(" - ") != -1:
			title_split = title.split(" - ") # we want this " Walking - The good choice?" and not those "4-Tage-Bart"
			#print("'-' split:",title_split)

		if title.find("|") != -1:
			title_split = title.split("|")
			#print("'|' split:",title_split)

		if title.find("?") != -1:
			title_split = title.split("?")
			#print("'?' split:",title_split)

		if title.find("&") != -1:
			title_split = title.split("&")
			#print("'&' split:",title_split)

		if title.find(",") != -1:
			title_split = title.split(",")
			#print("',' split:",title_split)

		if title.find(";") != -1:
			title_split = title.split(";")
			#print("';' split:",title_split)

		if len(title_split) >= 2:
			title_content_1 = str(title_split[0]).strip()
			title_content_2 = str(title_split[1]).strip()

			#print("DEBUG title_content_1:",title_content_1)
			#print("DEBUG title_content_2:",title_content_2)

			title_content_1= ''.join(c for c in title_content_1 if not c.isalpha() or not c.isspace() or not c.isdigit()).strip() # The isalpha() method returns True if all the characters are alphabet letters (a-z).
			title_content_1= regex.sub('', title_content_1).strip()	# remove non letter and digits from string: https://stackoverflow.com/questions/22520932/python-remove-all-non-alphabet-chars-from-string

			title_content_2= ''.join(c for c in title_content_2 if not c.isalpha() or not c.isspace() or not c.isdigit()).strip() # The isalpha() method returns True if all the characters are alphabet letters (a-z).
			title_content_2= regex.sub('', title_content_2).strip()	# remove non letter and digits from string: https://stackoverflow.com/questions/22520932/python-remove-all-non-alphabet-chars-from-string

			#print("DEBUG title_content_1:",title_content_1)
			#print("DEBUG title_content_2:",title_content_2)

			title_content_1_word_list = list(title_content_1.split(" "))
			title_content_2_word_list = list(title_content_2.split(" "))

			title_content_1_word_count= len(title_content_1_word_list)
			title_content_2_word_count= len(title_content_2_word_list)

			title_content	= title_content_1
			if title_content_1_word_count < 6:
				#print("DEBUG title_content_1_word_count:",title_content_1_word_count)
				#print("DEBUG title_content_2_word_count:",title_content_2_word_count)

				max_additional_words= max_canonical_words - title_content_1_word_count
				#print("DEBUG max_additional_words:",max_additional_words)
				x_zero 				= int(0)
				for x in title_content_2_word_list:
					add_word 	= str("")
					if x_zero < max_additional_words:	# maximal 5 wörter pro canonical url aus dem Titel der Webseite nehmen
						#try:
						add_word_tmp= str(title_content_2_word_list[x_zero]) # str(title_split[1]).strip()
						#print("DEBUG add_word_tmp:",add_word_tmp)
						t_split_more= ''.join(c for c in add_word_tmp if not c.isalpha() or not c.isspace() or not c.isdigit()).strip() # The isalpha() method returns True if all the characters are alphabet letters (a-z).
						add_word	= regex.sub('', t_split_more).strip()	# remove non letter and digits from string: https://stackoverflow.com/questions/22520932/python-remove-all-non-alphabet-chars-from-string
						#except Exception as a1:
						#	pass

					title_content 	+= str(" ")+str(add_word)
					x_zero 			+= int(1)
			#print("DEBUG title_content 2:",title_content)

		if len(title_content) < 1:
			# nimm einfach die ersten 5 wörter
			title_split 	= title.split(" ")
			title_content 	= alternative_url
			try:
				if len(title_split) >= 5:
					title_split[0]	= ''.join(c for c in title_split[0] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[0]	= regex.sub('', title_split[0]).strip()
					title_split[1]	= ''.join(c for c in title_split[1] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[1]	= regex.sub('', title_split[1]).strip()
					title_split[2]	= ''.join(c for c in title_split[2] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[2]	= regex.sub('', title_split[2]).strip()
					title_split[3]	= ''.join(c for c in title_split[3] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[3]	= regex.sub('', title_split[3]).strip()
					title_split[4]	= ''.join(c for c in title_split[4] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[4]	= regex.sub('', title_split[4]).strip()

					title_content 	= str(title_split[0]+" "+title_split[1]+" "+title_split[2]+" "+title_split[3]+" "+title_split[4])
				elif len(title_split) >= 4:
					title_split[0]	= ''.join(c for c in title_split[0] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[0]	= regex.sub('', title_split[0]).strip()
					title_split[1]	= ''.join(c for c in title_split[1] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[1]	= regex.sub('', title_split[1]).strip()
					title_split[2]	= ''.join(c for c in title_split[2] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[2]	= regex.sub('', title_split[2]).strip()
					title_split[3]	= ''.join(c for c in title_split[3] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[3]	= regex.sub('', title_split[3]).strip()

					title_content 	= str(title_split[0]+" "+title_split[1]+" "+title_split[2]+" "+title_split[3])
				elif len(title_split) >= 3:
					title_split[0]	= ''.join(c for c in title_split[0] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[0]	= regex.sub('', title_split[0]).strip()
					title_split[1]	= ''.join(c for c in title_split[1] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[1]	= regex.sub('', title_split[1]).strip()
					title_split[2]	= ''.join(c for c in title_split[2] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[2]	= regex.sub('', title_split[2]).strip()

					title_content 	= str(title_split[0]+" "+title_split[1]+" "+title_split[2])
				elif len(title_split) >= 2:
					title_split[0]	= ''.join(c for c in title_split[0] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[0]	= regex.sub('', title_split[0]).strip()
					title_split[1]	= ''.join(c for c in title_split[1] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[1]	= regex.sub('', title_split[1]).strip()

					title_content 	= str(title_split[0]+" "+title_split[1])
				elif len(title_split) >= 1:
					title_split[0]	= ''.join(c for c in title_split[0] if not c.isalpha() or not c.isspace() or not c.isdigit()).strip()
					title_split[0]	= regex.sub('', title_split[0]).strip()

					title_content	= str(title_split[0])
			except Exception as as1:
				return str(alternative_url)
				pass

		title_content 		= title_content.strip()
		title_content		= str(title_content.lower())
		#print("DEBUG title 1:",title_content)
		title_content		= title_content.translate(special_char_map)
		#print("DEBUG title 2:",title_content)
		title_content 		= ws_filter.sub(" ",title_content).strip()
		title_content_final = str(unidecode(title_content).replace(" ","-"))
		canonical_url 		= "https://www.artikelschreiber.com/texts/"+str(seo_lang_add[language])+"-"+title_content_final+".html"

		return canonical_url

	def calculateRank(self, myAI_obj, url, session, ip_obj, serp_obj):
		#telerN1 		= {'mainkeyword':MainKeyword, 'subkeyword':SubKeywords, 'articleraw':articleRaw, 'articletext':b_text, 'score':score, 'sessionid':SessionID, 'summary':p_summary, 'sprachprofil':p_sprachprofil, 'headline':article_headline, 'description':p_description,'articleurl':p_articleurl, 'metakeys':p_metakeys, 'addontext_json':myAddonText_json, 'language':Language, 'aitext_json':p_aitext_json}
		teler											= dict()#{}
		points 											= int(0)

		if not isinstance(url, str):
			teler['points'] 							= int(-10)
			return teler

		html 											= self.getWebpage(url)
		if not isinstance(html, str):
			teler['points'] 							= int(-10)
			return teler

		social_found 									= False
		imp_found										= False

		title											= str("")
		description										= str("")
		video											= str("")
		language										= str("")
		h_headline										= str("")
		h_text											= str("")
		h_text_ai										= str("")
		h_text_till_end									= str("")

		teler.update(ip_obj)							# IP Informationen ins aktueller teler-objekt schreiben
		teler.update(serp_obj)							# Wenn SERP Support aktiv, dann das hier auch aktivieren:

		teler['isGoodContent'] 							= False
		teler['openai'] 								= str("")
		teler['fastmode'] 								= False
		#teler['ip'] 									= str(ip_address)
		teler['url'] 									= str(url)
		teler['html'] 									= str(html)
		teler['session'] 								= str(session)
		teler["topics"]									= str("")
		teler["detected_language"]						= str("")
		teler["language"]								= str("")
		teler["summary"] 								= str("")
		teler["title"]									= str("")
		teler['title_raw']								= str("")
		teler["article_text"]							= str("")
		teler["article_text_ai"]						= str("")
		teler["article_text_ai_plagscore"]				= int(0)
		teler["article_text_low_quality_score"]			= int(0)
		teler['suggestions']							= list()
		teler['canonical']								= str("https://www.artikelschreiber.com/")
		teler['points'] 								= int(0)
		teler['ai_enabled'] 							= False
		teler["article_text_ai_raw"]					= str("")
		teler["openai_raw"]								= str("")
		teler["h1_text_ai_raw"]							= str("")
		teler["h2_text_ai_raw"]							= str("")
		teler["h3_text_ai_raw"]							= str("")
		teler['alternative_url']						= str("https://www.artikelschreiber.com/")

		# Wenn das html genau HTML5 konform ist
		if self.validateHTML(html):
			points 										+= int(1)

		# kurze Url
		if len(url) < 85:
			points 										+= int(1)

		####HTML Quelltext >200KB: -5p
		if len(html) < 200000:
			points 										+= int(1)

		try:
			#soup 										= BeautifulSoup(html, "html5lib") #"lxml") # pip install -U html5lib # https://zetcode.com/python/beautifulsoup/
			soup 										= BeautifulSoup(html, "lxml")
		except Exception as as1:
			soup 										= BeautifulSoup(html, "html.parser")

		for tag in soup():
			# CSS to remove attributes -> https://itecnote.com/tecnote/python-remove-all-inline-styles-using-beautifulsoup/
			for attribute in ["class", "id", "style"]:
				del tag[attribute]

		for data in soup(['style', 'script', 'comment']):
			# Remove tags -> https://www.geeksforgeeks.org/remove-all-style-scripts-and-html-tags-using-beautifulsoup/
			data.decompose()

		for headline in self.headlines_list:
			resultLists 														= self.headline_extractor(headline, soup)
			if len(resultLists) > 0:
				for element in resultLists:
					try:
						h_headline												= element.get(headline)
						h_text													= element.get(headline+"_text")
						h_text_ai												= element.get(headline+"_text_ai")

						h_text_low_quality_score								= element.get(headline+"_text_low_quality_score")
						h_text_till_end_low_quality_score						= element.get(headline+"_text_till_end_low_quality_score")

						teler[headline] 										= h_headline
						teler[headline+"_text"] 								= h_text
						teler[headline+"_text_low_quality_score"] 				= h_text_low_quality_score
						teler[headline+"_text_ai"] 								= h_text_ai
						teler[headline+"_text_till_end"] 						= str("")
						teler[headline+"_text_till_end_low_quality_score"] 		= h_text_till_end_low_quality_score

						if (self.isFound(headline,"h1") or self.isFound(headline,"h2") or self.isFound(headline,"h3")) and len(h_headline) >= self.headline_min_length and h_text_low_quality_score == 0:
							# bei H1,H2,H3 gibt es Bonuspunkte, wenn Headline lang genug ist und der Text Quality Score stimmt
							points 											+= int(1)
						elif (self.isFound(headline,"h1") or self.isFound(headline,"h2") or self.isFound(headline,"h3")) and len(h_headline) < self.headline_min_length:
							# bei H1,H2,H3 gibt es Punktabzug, wenn die Headline zu kurz ist
							points 											-= int(1)
						elif (self.isFound(headline,"h4") or self.isFound(headline,"h5") or self.isFound(headline,"h6")) and len(h_headline) >= self.headline_min_length and h_text_low_quality_score == 0:
							# bei H4,H5,H6 gibt es Bonuspunkte, wenn Headline lang genung ist und der Text Quality Score stimmt
							points 											+= int(1)
						elif (self.isFound(headline,"h4") or self.isFound(headline,"h5") or self.isFound(headline,"h6")) and len(h_headline) < self.headline_min_length:
							# bei bei H4,H5,H6 gibt es Punktabzug, wenn die Headline zu kurz ist
							points 											-= int(1)
						elif (self.isFound(headline,"h1") or self.isFound(headline,"h2") or self.isFound(headline,"h3")) and count_spaces(h_text) <= self.max_spaces_count and count_words_regex(h_text) >= self.min_word_count and len(h_text) >= self.min_text_length and h_text_low_quality_score == 0:
							# bei H1,H2,H3 gibt es Bonuspunkte, wenn alles OK ist
							points 											+= int(1)
						elif not (self.isFound(headline,"h1") or self.isFound(headline,"h2") or self.isFound(headline,"h3")) and count_spaces(h_text) <= self.max_spaces_count and count_words_regex(h_text) >= self.min_word_count and len(h_text) >= self.min_text_length and h_text_low_quality_score == 0:
							# bei H4,H5,H6 gibt es Punktabzug, wenn etwas falsch ist
							points 											-= int(1)
						elif (self.isFound(headline,"h4") or self.isFound(headline,"h5") or self.isFound(headline,"h6")) and count_spaces(h_text) <= self.max_spaces_count and count_words_regex(h_text) >= self.min_word_count and len(h_text) >= self.min_text_length and h_text_low_quality_score == 0:
							# bei H4,H5,H6 gibt es Bonuspunkte, wenn alles OK ist
							points 											+= int(1)
						elif not (self.isFound(headline,"h4") or self.isFound(headline,"h5") or self.isFound(headline,"h6")) and count_spaces(h_text) <= self.max_spaces_count and count_words_regex(h_text) >= self.min_word_count and len(h_text) >= self.min_text_length and h_text_low_quality_score == 0:
							# bei bei H1,H2,H3 gibt es Punktabzug, wenn etwas falsch ist
							points 											-= int(1)
					except Exception as as1:
						pass

					# ###
					# die eigentliche H-Textinhaltsblöcke bis zum Ende des gesamten Textes
					###
					try:
						teler[headline+"_text_till_end"] 						= self.headline_to_html_end_extractor(headline, h_headline, soup)
						h_text_till_end 										= element.get(headline+"_text_till_end")
						h_text_till_end_low_quality_score						= self.isLowQualityContent(h_text_till_end)
						teler[headline+"_text_till_end_low_quality_score"] 		= h_text_till_end_low_quality_score

						if self.count_spaces(h_text_till_end) <= self.max_spaces_count and self.count_words_regex(h_text_till_end) >= self.min_word_count and len(h_text_till_end) >= self.min_text_length and h_text_till_end_low_quality_score == 0:
							points 												+= int(1)	# h_text_till_end
						else:
							points 												-= int(1)

					except Exception as as1:
						pass

		try:
			#h 					= soup.title.text.strip() # soup.select('title')[0].text.strip()	# print(soup.title)
			h 					= self.get_title(soup)
			title 				= str(self.preprocess_text(h))
			if len(title) >= self.headline_min_length:
				teler['title_raw'] = str(h)
				teler['title'] 	= self.generateBeautifulTitle(title)
				points 			+= int(1)
			else:
				teler['title'] 	= str("")	# leer setzen wenn kein Inhalt
		except Exception as a1:
			teler['title'] 		= str("")	# leer setzen wenn kein Inhalt
			pass


		try:
			h 							= self.get_description(soup)
			description 				= str(self.preprocess_text(h))
			if len(description) >= 100 and len(description) < 154:
				teler['description'] 	= description
				points 					+= int(1)
			else:
				teler['description'] 	= str("")	# leer setzen wenn kein Inhalt
		except Exception as a1:
			teler['description'] 	= str("")	# leer setzen wenn kein Inhalt
			pass


		try:
			h 					= self.get_image(soup, url)
			image 				= str(self.preprocess_text(h))
			if len(image) >= self.headline_min_length:
				teler['image'] 	= image
				points 			+= int(1)
			else:
				teler['image'] 	= str("")	# leer setzen wenn kein Inhalt
		except Exception as a1:
			teler['image'] 	= str("")	# leer setzen wenn kein Inhalt
			pass


		try:
			h 					= self.get_video(soup)
			video 				= str(self.preprocess_text(h))
			if len(video) >= self.headline_min_length:
				teler['video'] 	= video
				points 			+= int(1)
			else:
				teler['video'] 	= str("")	# leer setzen wenn kein Inhalt
		except Exception as a1:
			teler['video'] 	= str("")	# leer setzen wenn kein Inhalt
			pass


		try:
			og_language				= self.get_og_locale(soup)
			#og_language 			= str(self.preprocess_text(h))
			og_language_len 		= len(og_language)
			if og_language_len >= 2 and og_language_len < self.headline_min_length:
				teler['language'] 	= str("")
				teler['language'] 	= og_language
				points 				+= int(1)
			else:
				teler['language'] 	= str("")
		except Exception as a1:
			teler['language'] 	= str("")
			pass


		try:
			h 					= self.get_links(soup, url)
			if len(h) > 0:
				teler['links'] 	= h
			else:
				teler['links'] 	= list()
		except Exception as a1:
			teler['links'] 	= list()
			pass


		try:
			h 						= self.get_meta_keywords(soup, html, url)
			h1						= h.replace(", ",";").strip()
			h1						= h1.replace(" ,",";").strip()
			h1						= h1.replace(",",";").strip()
			if len(h1) > 0:
				teler['keywords'] 	= h1
				points 				+= int(1)
			elif len(h) > 0:
				teler['keywords'] 	= h
				points 				+= int(1)
			else:
				teler['keywords'] 	= str("")	# leer setzen wenn kein Inhalt
		except Exception as a1:
			pass

		###
		# Social Links finden
		###
		teler['socials'] 			= False
		for socials in social_links:
			if self.isFound(html, socials):
				teler['socials']	= True
				points 				+= int(1)
				break

		###
		# Wichtige Keywords finden ("Impressum") finden
		###
		teler['important'] 			= False
		for imp1 in imp_keywords:
			if self.isFound(html, imp1):
				teler['important'] 	= True
				points 				+= int(1)
				break


		try:
			article_text									= self.extractTextFromHTML(html)
			article_processed 								= str(self.preprocess_text(article_text))
			article_score									= self.isLowQualityContent(article_processed)

			"""
			h1_text											= teler.get("h1_text")
			h1_score										= teler.get("h1_low_quality_score")
			h2_text											= teler.get("h2_text")
			h2_score										= teler.get("h2_low_quality_score")
			h3_text											= teler.get("h3_text")
			h3_score										= teler.get("h3_low_quality_score")

			myText											= str("")
			if article_score == 0:
				myText 										+= article_text
			if h1_score == 0:
				myText 										+= h1_text
			if h2_score == 0:
				myText 										+= h2_text
			if h3_score == 0:
				myText 										+= h3_text

			#if len(myText) < self.min_text_length:
			#myText 											= article_text+" "+h1_text+" "+h2_text+" "+h3_text

			article_processed 								= str(self.preprocess_text(article_text))
			mylow_quality_score								= self.isLowQualityContent(article_processed)
			# hier ist der komplette Artikel drin - Fallback
			"""
			teler["article_text"] 							= article_processed
			teler["article_text_low_quality_score"]			= mylow_quality_score

			if self.count_spaces(article_processed) <= self.max_spaces_count and self.count_words_regex(article_processed) >= self.min_word_count and len(article_processed) >= self.min_text_length and mylow_quality_score == 0:
				points 										+= int(1)
			else:
				points 										-= int(1)

		except Exception as a1:
			pass

		try:
			myText 											= str("")

			article_text 									= teler.get("article_text")
			article_score 									= teler.get("article_text_low_quality_score")
			h1_text											= teler.get("h1_text")
			h1_score										= teler.get("h1_low_quality_score")
			h2_text											= teler.get("h2_text")
			h2_score										= teler.get("h2_low_quality_score")
			h3_text											= teler.get("h3_text")
			h3_score										= teler.get("h3_low_quality_score")

			if article_score == 0:
				myText 										+= article_text
			if h1_score == 0:
				myText 										+= h1_text
			if h2_score == 0:
				myText 										+= h2_text
			if h3_score == 0:
				myText 										+= h3_text

			if len(myText) < self.min_text_length:
				myText 										= article_text+" "+h1_text+" "+h2_text+" "+h3_text

			teler["summary"] 								= self.doLsaSummarizer(myText)
			summary_text 									= teler.get("summary")

			if self.count_spaces(summary_text) <= self.max_spaces_count and self.count_words_regex(summary_text) >= self.min_word_count and len(summary_text) >= self.min_text_length and mylow_quality_score == 0:
				points 										+= int(1)
			else:
				points 										-= int(1)
		except Exception as a1:
			pass


		try:
			myText 											= str("")

			article_text 									= teler.get("article_text")
			article_score 									= teler.get("article_text_low_quality_score")
			h1_text											= teler.get("h1_text")
			h1_score										= teler.get("h1_low_quality_score")
			h2_text											= teler.get("h2_text")
			h2_score										= teler.get("h2_low_quality_score")
			h3_text											= teler.get("h3_text")
			h3_score										= teler.get("h3_low_quality_score")

			if article_score == 0:
				myText 										+= article_text
			if h1_score == 0:
				myText 										+= h1_text
			if h2_score == 0:
				myText 										+= h2_text
			if h3_score == 0:
				myText 										+= h3_text

			if len(myText) < self.min_text_length:
				myText 										= article_text+" "+h1_text+" "+h2_text+" "+h3_text

			teler["detected_language"]						= self.detectTextLanguage(myText)

		except Exception as a1:
			teler["detected_language"]						= str("")
			pass

		try:
			myText 											= str("")

			article_text 									= teler.get("article_text")
			article_score 									= teler.get("article_text_low_quality_score")
			h1_text											= teler.get("h1_text")
			h1_score										= teler.get("h1_low_quality_score")
			h2_text											= teler.get("h2_text")
			h2_score										= teler.get("h2_low_quality_score")
			h3_text											= teler.get("h3_text")
			h3_score										= teler.get("h3_low_quality_score")

			if article_score == 0:
				myText 										+= article_text
			if h1_score == 0:
				myText 										+= h1_text
			if h2_score == 0:
				myText 										+= h2_text
			if h3_score == 0:
				myText 										+= h3_text

			if len(myText) < self.min_text_length:
				myText 										= article_text+" "+h1_text+" "+h2_text+" "+h3_text

			og_language 									= teler.get("language")
			detected_language 								= teler.get("detected_language")

			if len(og_language) == 2:
				teler["topics"]								= myAI_obj.topicModeling(myText, og_language)
			else:
				teler["topics"]								= myAI_obj.topicModeling(myText, detected_language)

			article_topics 									= teler.get("topics")
			#pprint(article_topics)

			if len(article_topics) >= self.headline_min_length*10:	# 70 Zeichen
				points 										+= int(1)
			else:
				points 										-= int(1)
		except Exception as a1:
			teler["topics"]									= str("")
			pass


		try:
			suggestions											= list()
			nodouble											= set()

			article_keywords									= teler.get("keywords")
			article_topics 										= teler.get("topics")

			if len(article_keywords) >= self.headline_min_length-4:	# somit 3 Zeichen lang
				topics			= article_keywords.split(';')
				for word_text in topics:
					w_len = len(word_text)
					if word_text.strip() not in nodouble and w_len > 3:
						suggestions.append("mk="+word_text.strip())
						nodouble.add(word_text.strip())

			if len(article_topics) >= self.headline_min_length-4:
				topics			= article_topics.split(';')
				for word_text in topics:
					w_len = len(word_text)
					if word_text.strip() not in nodouble and w_len > 3:
						suggestions.append("mk="+word_text.strip())
						nodouble.add(word_text.strip())

			teler['suggestions'] 								= list(suggestions)	# wichtig, weil Sets nicht json serialisiert werden können
		except Exception as a1:
			pass

		try:
			#alternative_url "canonical fallback link" Link:
			topo												= teler.get("topics")
			sessionShort 										= str(session[:3]).lower()
			topic1 												= list(topo.lower().split(";"))
			if len(topic1) >= 2:
				topic											= str(self.remove_accents(topic1[0]))
				rand 											= str(self.remove_accents(topic1[1]))
				rand2 											= str(self.remove_accents(topic1[2]))
				#points 											+= int(1)
			elif len(topic1) >= 1:
				topic											= str(self.remove_accents(topic1[0]))
				rand 											= str(self.remove_accents(topic1[1]))
				rand2 											= str(self.remove_accents(topic1[1]))
				#points 											+= int(1)
			elif len(topic1) >= 0:
				topic											= str(self.remove_accents(topic1[0]))
				rand 											= str(self.remove_accents(topic1[0]))
				rand2 											= str(self.remove_accents(topic1[0]))
				#points 											-= int(1)
			else:
				topic											= str(self.remove_accents("blog"))
				rand 											= str(self.remove_accents("entry"))
				rand2 											= str(self.remove_accents("id"))
				#points 											-= int(1)

			og_language 										= teler.get("language")
			detected_language 									= teler.get("detected_language")

			if len(og_language) == 2:
				language										= og_language
			else:
				language										= detected_language

			# old: filename											= str(topic+"-"+rand+"-"+rand2+"-"+sessionShort).lower()+".html"
			filename											= str("article-"+topic+"-"+rand+"-"+str(language).lower()+"-"+sessionShort).lower()+".html"
			# old: absolute_canonical 							= "https://www.artikelschreiber.com/"+str(language)+"/blog/"+filename
			teler['alternative_url'] 							= "https://www.artikelschreiber.com/texts/"+filename
		except Exception as a1:
			teler['alternative_url']							= str("https://www.artikelschreiber.com/")
			pass

		try:
			#canonical Link:
			alternative_url 									= teler.get("alternative_url")

			og_language 										= teler.get("language")
			detected_language 									= teler.get("detected_language")

			if len(og_language) == 2:
				language										= og_language
			else:
				language										= detected_language

			myTmpTitle 											= teler.get("title")
			teler['canonical'] 									= self.generateCanonicalURL(myTmpTitle, alternative_url, language)
			points 												+= int(2)
		except Exception as a1:
			teler['canonical']									= alternative_url
			points 												+= int(1)
			pass

		try: # content/quellcode verhältnis zwischen 40 und 70 Prozent?
			article_text 										= teler.get("article_text")
			if len(article_text)/210000 >= 0.4 and len(article_text)/210000 < 0.71:
				points 											+= int(1)
		except Exception as as1:
			pass

		try: ####HTML hat Google oder Bing Ads: +5p
			if html.find("pagead2.googlesyndication.com/pagead/js/adsbygoogle.js") != -1:
				points 											+= int(1)
		except Exception as as1:
			pass

		try: ####Strukturierte Daten vorhanden im HTML: +5p
			if html.find("application/ld+json") != -1:
				points 											+= int(1)
		except Exception as as1:
			pass

		try: # Wenn Text zuviele Zeichen enthält, die kein Buchstabe oder Zahl ist
			article_text 										= teler.get("article_text")
			bchar 				= self.countBadChars(text)
			ltext 				= len(article_text)
			bcharScore 			= float("{0:.3f}".format((bchar/ltext)*100))
			if bcharScore >= 3.2:
				points 											-= int(1)
		except Exception as as1:
			pass

		try: # Wenn Text eine Paywall ist
			if self.isPaywall(html):
				points 											-= int(10)
		except Exception as as1:
			pass

		try:####<ul><ol> im html dann: +5, zuerst <ol> inhalt finden, dann dort separat li elemente auslesen
			ul					= re.findall("<ul>(.*?)</ul>", html, re.IGNORECASE)
			ol					= re.findall("<ol>(.*?)</ol>", html, re.IGNORECASE)

			for t in list(ul + ol):
				if self.isFound("<li>", t):
					points 										+= int(1)
					break
		except Exception as as1:
			pass

		"""
		#TODO###Kurze Sätze mit 9 bis 13 Wörtern: +5p
		"""

		# Session: b459d00a59a0aca81c7415947e03746f-ARTIKELSCHREIBER_de.json enthält sehr viele falsch geschriebene Buchstaben, so ein Mist muss rausgefiltert werden und einen Rank von 0 bekommen!
		content_text_special_chars 						= teler.get("h1_text")+teler.get("h2_text")+teler.get("h3_text")+teler.get("h4_text")+teler.get("h5_text")+teler.get("article_text")
		count_broken_chars 								= self.count_broken_character(content_text_special_chars)
		isLowQualityContent 							= self.isLowQualityContentText(content_text_special_chars)

		if count_broken_chars > 20 or isLowQualityContent:
			teler['points'] 							= int(0)
		else:
			teler['points'] 							= points
		return teler

