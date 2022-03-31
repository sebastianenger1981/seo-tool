# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import datetime
aTime 				= datetime.datetime.now()

os.system("killall nginx");
os.system("killall apache2");
os.system("clear")

print("############################################")
print("## KI Autoblogger: SEO Marketing Tools    ##")
print("## by Sebastian Enger, M.Sc.              ##")
print("## Web: https://www.artikelschreiber.com/ ##")
print("## Web: https://www.unaique.com/          ##")
print("## Web: https://www.unaique.net/          ##")
print("## Version vom: 27.2.2022 - 1.4.1.1       ##")
print("###############################################")

project_path = "/home/seo-marketing-tool"

print("Schritt 1: Installiere benötigte Linux Software.")

software_installer = list()
software_installer.append("apt-get update -y && apt-get upgrade -y")
software_installer.append("apt-get install -y php7.4-xmlrpc snap net-tools software-properties-common python3 python3-pip build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget screen php php-cli php-fpm php-json php-common php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath") #nginx
software_installer.append("snap install core; sudo snap refresh core")
software_installer.append("apt-get remove -y apache2 certbot")
software_installer.append("pip3 install --upgrade requests")
software_installer.append("apt -y autoremove")
software_installer.append("snap install --classic certbot")
software_installer.append("ln -s /snap/bin/certbot /usr/bin/certbot")
software_installer.append("killall apache2 nginx")
for exec in software_installer:
	os.system(exec)

import configparser
config 		= configparser.ConfigParser()
config.read(project_path+'/files/seo-marketing-tool.conf')

from pprint import pprint   # pretty-printer
import requests	            # pip3 install --upgrade requests
import urllib.parse
import codecs
import socket
import fcntl
import struct
import json
import time
import sys
from datetime import date

def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack(b'256s', ifname[:15].encode())
	)[20:24])

def getWebpagesSimple(link):
	UserAgentMobile			= "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) FxiOS/7.5b3349 Mobile/14F89 Safari/603.2.4"#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
	HeadersSimple			= {'user-agent': UserAgentMobile, 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate'}

	if link.lower().startswith("http") or link.lower().startswith("https"):
		try:
			r1 			= requests.get(link, headers=HeadersSimple, timeout=300, verify=True)
			myStatus	= r1.status_code
			myText 		= str(r1.text)
			myContent	= str(r1.headers['content-type'])
			mT1 		= myText.strip()
			if "html" in myContent or "json" in myContent and myStatus == 200:
				return mT1
		except Exception as er:
			print("Unexpected error: getWebpagesSimple(link)", sys.exc_info()[0])
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

	return str("")

def createNginxConfig(mydomain, my_www_domain, myIP, mywwwroot):
	with codecs.open(project_path+"/files/nginx/nginx-standard.conf", 'r', encoding='utf8') as f:
		nginx_conf = f.read()
		f.close()

	x = nginx_conf.replace("MYDOMAIN", mydomain)
	x = x.replace("MY_WWW_DOMAIN", my_www_domain)
	x = x.replace("MYIP", myIP)
	x = x.replace("MYWWWROOT", mywwwroot)

	with codecs.open("/etc/nginx/nginx.conf", 'w+', encoding='utf8') as f:
		f.write(x)
		f.close()

	return True

def createNginxSSLConfig(mydomain, my_www_domain, myIP, mywwwroot, cert_path):
	for filename in os.listdir(cert_path):
		if filename.endswith(".pem"):
			if "chain" in filename.lower():
				r = open(cert_path+"/"+filename)
				x = r.read()
				with codecs.open(project_path+"/files/ssl/chain1.pem", 'w+', encoding='utf8') as f:
					f.write(x)
					f.close()
			if "fullchain" in filename.lower():
				r = open(cert_path+"/"+filename)
				x = r.read()
				with codecs.open(project_path+"/files/ssl/fullchain1.pem", 'w+', encoding='utf8') as f:
					f.write(x)
					f.close()
			if "privkey" in filename.lower():
				r = open(cert_path+"/"+filename)
				x = r.read()
				with codecs.open(project_path+"/files/ssl/privkey1.pem", 'w+', encoding='utf8') as f:
					f.write(x)
					f.close()

	with codecs.open(project_path+"/files/nginx/nginx-ssl.conf", 'r', encoding='utf8') as f:
		nginx_conf = f.read()
		f.close()

	x = nginx_conf.replace("MYDOMAIN", mydomain)
	x = x.replace("MY_WWW_DOMAIN", my_www_domain)
	x = x.replace("MYIP", myIP)
	x = x.replace("MYWWWROOT", mywwwroot)

	with codecs.open("/etc/nginx/nginx.conf", 'w+', encoding='utf8') as f:
		f.write(x)
		f.close()

	os.system("chmod -R 755 "+project_path+"/files/")
	os.system("chown -R root:www-data"+project_path+"/files/")

	return True

def createIndexFile(unaique_html_template, custom_link_top1, custom_link_top2, custom_link_top3, custom_link_name_top1, custom_link_name_top2, custom_link_name_top3, headline, structured_data, summary, textbyai, textbyai_simple, topics, my_www_domain, mywwwroot, google_analytics_id, optimized, article_score ):
	if article_score > 0:
		as_score = '<span style="color:#006400;">'+str(article_score)+'</span>'
	else:
		as_score = '<span style="color:#8B0000;">'+str(article_score)+'</span>'

	with codecs.open(unaique_html_template, 'r', encoding='utf8') as f:
		html_tpl = f.read()
		f.close()

	x = html_tpl.replace("{custom_link_top1}", custom_link_top1)
	x = x.replace("{custom_link_top2}", custom_link_top2)
	x = x.replace("{custom_link_top3}", custom_link_top3)

	x = x.replace("{custom_link_name_top1}", custom_link_name_top1)
	x = x.replace("{custom_link_name_top2}", custom_link_name_top2)
	x = x.replace("{custom_link_name_top3}", custom_link_name_top3)

	x = x.replace("{title}", headline)
	x = x.replace("{headline}", headline)
	x = x.replace("{description}", headline)
	structured_data = structured_data.replace("https://www.unaique.net", "https://"+my_www_domain)
	x = x.replace("{structured_data}", structured_data)
	x = x.replace("{summary}", summary)
	x = x.replace("{textbyai}", textbyai)
	x = x.replace("{topics}", topics)
	x = x.replace("{my_www_domain}", "https://"+my_www_domain)
	x = x.replace("{keywords}", topics)
	x = x.replace("{google_analytics_id}", google_analytics_id)

	with codecs.open(mywwwroot+"/index.html", 'w+', encoding='utf8') as f:
		f.write(x)
		f.close()

	os.system("chmod -R 755 "+mywwwroot)
	os.system("chown -R www-data:www-data "+mywwwroot);

	return True


def doCreateSitemaps(ssl_domain):
	# /home/seo-auto-scaler/files/wwwroot/robots.txt
	with codecs.open(project_path+"/files/wwwroot/robots.txt", 'r', encoding='utf8') as f:
		txt_tpl1 = f.read()
		f.close()

	x = txt_tpl1.replace("{ssl_domain}", ssl_domain)
	with codecs.open(project_path+"/files/wwwroot/robots.txt", 'w+', encoding='utf8') as f:
		f.write(x)
		f.close()

	# /home/seo-auto-scaler/files/wwwroot/sitemap.xml
	with codecs.open(project_path+"/files/wwwroot/sitemap.xml", 'r', encoding='utf8') as f:
		txt_tpl2 = f.read()
		f.close()

	x2 = txt_tpl2.replace("{ssl_domain}", ssl_domain+"/")
	d = str(date.today())
	x2 = x2.replace("{my_date}", d)
	with codecs.open(project_path+"/files/wwwroot/sitemap.xml", 'w+', encoding='utf8') as f2:
		f2.write(x2)
		f2.close()

	return True

def doSubmitSitemaps(ssl_domain):
	"""
	Bing und Google sind wichtig. Yahoo informiert sich über Bing. Duckduckgo nimmt von Google und Bing die Informationen zur Sitemap.
	Damit ist sichergestellt, dass die neue Webseite von allen bekannten Crawlern indexiert wird und Traffic sendet.
	"""
	my_sitemap          = ssl_domain + "/" + "sitemap.xml"
	my_sitemap_bing     = "https://www.bing.com/webmaster/ping.aspx?siteMap="+my_sitemap
	my_sitemap_google   = "https://www.google.com/webmasters/sitemaps/ping?sitemap="+my_sitemap
	print("\t -> Informiere Bing über die neue Webseite.")
	web1                = getWebpagesSimple(my_sitemap_bing)
	print("\t -> Informiere Google über die neue Webseite.")
	web2                = getWebpagesSimple(my_sitemap_google)

	return True

def makeWebapiCall(unaique_api_request, unaique_api):
	#api_hook = "https://www.unaique.net/en/api/index.php?language="+language+"&keyword="+urllib.parse.quote(search_query)
	#https://www.unaique.net/en/api/index.php?session=ad16185319532ee05a91ebf4d2c3374e-API
	web1                = getWebpagesSimple(unaique_api_request)
	x                   = json.loads(web1)
	session             = x.get("session") #{title}    {description}
	status	            = x.get("status")
	api_hook            = unaique_api+"?session="+session
	for i in range(310):
		i               = i + 1
		time.sleep(30)
		web2            = getWebpagesSimple(api_hook)
		y               = json.loads(web2)
		status2	        = y.get("status")
		print("\t -> Versuche neuen Artikel von der KI abzuholen ("+str(status2)+") -> Versuch: "+str(i)+" von 100.")
		if status2 == 200:
			print("\t -> Abholen des geschriebenen Artikels von der KI war erfolgreich.")
			return api_hook
	return api_hook


print("Schritt 2: Lese aus Konfiguration die Einstellungen aus.")
custom_link_top1        = str(config['DEFAULT']['custom_link_top1'])
custom_link_top2        = str(config['DEFAULT']['custom_link_top2'])
custom_link_top3        = str(config['DEFAULT']['custom_link_top3'])
custom_link_name_top1   = str(config['DEFAULT']['custom_link_name_top1'])
custom_link_name_top2   = str(config['DEFAULT']['custom_link_name_top2'])
custom_link_name_top3   = str(config['DEFAULT']['custom_link_name_top3'])
search_query            = str(config['DEFAULT']['search_query'])
language_text           = str(config['DEFAULT']['language_text'])
mydomain                = str(config['DEFAULT']['mydomain'])
my_www_domain           = str(config['DEFAULT']['my_www_domain'])
mywwwroot               = str(config['DEFAULT']['mywwwroot'])
google_analytics_id     = str(config['DEFAULT']['google_analytics_id'])
use_ssl                 = str(config['DEFAULT']['use_ssl'])
unaique_api             = str(config['DEFAULT']['unaique_api'])
unaique_session         = str(config['DEFAULT']['unaique_session'])
myIP                    = get_ip_address('eth0')
unaique_html_template   = str("")
unaique_api_request     = unaique_api+"?language="+language_text+"&keyword="+urllib.parse.quote(search_query)
ssl_domain              = "https://"+my_www_domain
t                       = str("")

if language_text == "de":
	unaique_html_template   = project_path+"/files/wwwroot/de/index.tpl"
	t="deutschen"
else:
	unaique_html_template   = project_path+"/files/wwwroot/en/index.tpl"
	t="englischen"

if len(unaique_session) > 1:
	unaique_api_request    = unaique_api+"?session="+unaique_session

print("Schritt 3: Erstelle das benötigte Webverzeichnis.")
try:
	os.system("rm -rf "+mywwwroot)
	os.system("rm -rf /usr/share/nginx/files/nginx.conf")
	os.system("rm -rf /etc/nginx/nginx.conf")
	os.system("rm -rf /etc/nginx/nginx.conf")
except Exception as e1:
	pass

try:
	os.makedirs(mywwwroot)
	os.system("chmod -R 755 "+mywwwroot)
	os.system("chown -R www-data:www-data "+mywwwroot)
except Exception as e1:
	pass

try:
	os.makedirs(mywwwroot+"/.well-known/acme-challenge/")
	os.system("chmod -R 755 "+mywwwroot+"/.well-known/acme-challenge/")
	os.system("chown -R www-data:www-data "+mywwwroot+"/.well-known/acme-challenge/")
except Exception as e1:
	pass

try:
	os.makedirs("/usr/share/nginx/files/")
except Exception as e1:
	pass

print("Schritt 4: Erstelle die benötigte Konfiguration für den Webserver.")
if use_ssl == "1":
	print("Schritt 4.1: Nutze SSL https://"+my_www_domain)
	#os.system("rm -rf /etc/letsencrypt/archive/"+mydomain+"/*")"
	#os.system("rm -rf /etc/letsencrypt/archive/"+my_www_domain+"/*")"
	os.system("certbot certonly --register-unsafely-without-email --agree-tos --dry-run -d "+mydomain+" -d "+my_www_domain+" --authenticator standalone") # muss in live version raus: --dry-run
	a="/etc/letsencrypt/archive/"+mydomain
	b="/etc/letsencrypt/archive/"+my_www_domain
	if os.path.isdir(a):
		createNginxSSLConfig(mydomain, my_www_domain, myIP, mywwwroot, a)
	elif os.path.isdir():
		createNginxSSLConfig(mydomain, my_www_domain, myIP, mywwwroot, b)
	doCreateSitemaps(ssl_domain)
else:
	ssl_domain = "http://"+my_www_domain
	print("Schritt 4.1: Nutze http://")
	createNginxConfig(mydomain, my_www_domain, myIP, mywwwroot)
	doCreateSitemaps(ssl_domain)


print("Schritt 5: Starte den Webserver.")
#os.system("/usr/sbin/nginx -t -c /etc/nginx/nginx.conf")
os.system("/usr/sbin/nginx -c /etc/nginx/nginx.conf")
#os.system("pidof nginx")

print("Schritt 6: Schreibe Text mit Hilfe Künstlicher Intelligenz (unaique.net API).")
unaique_api_request2 = makeWebapiCall(unaique_api_request, unaique_api)
web                 = getWebpagesSimple(unaique_api_request2)
y                   = json.loads(web)

headline            = y.get("title")             #{title}    {description}
summary	            = y.get("summary")
#structured_data	    = y.get("structured_data")
#structured_data	    = unescape(structured_data)
textbyai            = y.get("unique_text")
textbyai_simple     = textbyai #y.get("textbyai_advanced")
topics              = y.get("topics")
topics              = topics.replace("#", "")
status              = y.get("status")
optimized           = y.get("unique_text")
article_score       = int(y.get("article_score"))
# links: {custom_link_top1} {custom_link_name_top1}
words_content       = textbyai.split(" ")
words               = len(words_content)
today               = date.today()
articleBody         = summary
try:
    articleBody     = " ".join(words_content[0:25])
except Exception as e1:
    pass


structured_data     = """
	<script type="application/ld+json">
		{ "@context": "https://schema.org",
		 "@type": "BlogPosting",
		 "mainEntityOfPage": {
			 "@type": "WebPage",
			 "@id": "https://{my_www_domain}"
		  },
		  "publisher": {
				"@type": "Organization",
				"name": "UNAIQUE.NET",
				"url": "https://{my_www_domain}",
				"logo": {
					"@type": "ImageObject",
					"url": "https://{my_www_domain}/images/apple-icon-180x180.png",
					"width":"180",
					"height":"180"
				}
		 },
		 "author": "https://www.unaique.net/",
		 "headline": "{headline}",
		 "alternativeHeadline": "{headline} | {my_www_domain}",
		 "image": "https://{my_www_domain}/images/apple-icon-180x180.png",
		 "award": "Der Artikel",
		 "genre": "text article",
		 "keywords": "{topics}",
		 "wordcount": "{words}",
		 "datePublished": "{today}",
		 "dateCreated": "{today}",
		 "dateModified": "{today}",
		 "description": "{headline}",
		 "url": "https://{my_www_domain}",
		 "articleBody": "{articlebody}"
		 }
	</script>
"""

structured_data = structured_data.replace("{my_www_domain}", str(my_www_domain))
structured_data = structured_data.replace("{headline}", str(headline))
structured_data = structured_data.replace("{today}", str(today))
structured_data = structured_data.replace("{words}", str(words))
structured_data = structured_data.replace("{topics}", str(topics))
structured_data = structured_data.replace("{articlebody}", str(articleBody))

print("Schritt 8: Kopiere die CSS und JavaScript Dateien für die Webseite.")
os.system("/usr/bin/cp -rf "+project_path+"/files/wwwroot/* "+mywwwroot)

print("Schritt 9: Erstelle die Webseite mit Inhalten und Links.")
createIndexFile(unaique_html_template, custom_link_top1, custom_link_top2, custom_link_top3, custom_link_name_top1, custom_link_name_top2, custom_link_name_top3, headline, structured_data, summary, textbyai, textbyai_simple, topics, my_www_domain, mywwwroot, google_analytics_id, optimized, article_score )

print("Schritt 10: Informiere Google und Bing über die neue Webseite.")
doSubmitSitemaps(ssl_domain)

print("Schritt 11: Webseite http://"+my_www_domain+" ist nun verfügbar!")
print("Schritt 12: Informiere deinen Domain Provider:")
print("\t -> Domain '"+str(mydomain)+"' setze 'A-Record' für '@' mit IP '"+str(myIP)+"'")
print("\t -> Domain '"+str(my_www_domain)+"' setze 'A-Record' für 'www' mit IP '"+str(myIP)+"'")
bTime 				= datetime.datetime.now()
deltaRuntime 		= bTime - aTime
print("Schritt 13: Veröffentlichung eines "+str(t)+" Artikels zum Thema '"+str(search_query)+"' war erfolgreich.")
print("Schritt 14: Laufzeit des Programmes: "+str(deltaRuntime)+" Minuten")
print("Schritt 15: KI Autoblogger fertig - Beende mich.")
sys.exit(0)
