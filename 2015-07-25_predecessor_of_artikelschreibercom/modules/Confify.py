# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore

#https://docs.python.org/3/library/configparser.html
import os
import subprocess
import configparser

os.system("export TREETAGGER_HOME='/home/buz/buzzgreator/treetagger/cmd'")
os.system("export GOOGLE_APPLICATION_CREDENTIALS='/home/buz/buzzgreator/key/100BiereTranslate-8a809e939d5e.json'")

return_code1 = subprocess.call("export TREETAGGER_HOME='/home/buz/buzzgreator/treetagger/cmd'", shell=True)  
return_code2 = subprocess.call("export GOOGLE_APPLICATION_CREDENTIALS='/home/buz/buzzgreator/key/100BiereTranslate-8a809e939d5e.json'", shell=True)

#type="sentify, genify, default, "
def doConfigParse():
	config = configparser.ConfigParser()
	config.read('/home/buz/buzzgreator/modules/config/schreiber.cfg')
	return config
