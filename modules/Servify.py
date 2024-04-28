# -*- coding: utf-8 -*-
#!/usr/bin/python3.5 -S -W ignore

from threading import Thread
import traceback
import socket
import time
import sys
import os

from datetime import datetime as dTime
import modules.Fileify as fileify
import modules.Wordify as wordify

TCP_IP 			= '127.0.0.1'
TCP_PORT 		= 2399
MAX_BUFFER_SIZE = 1024 * 1 # Normally 1024, but we want fast response

"""
0. index.php -> erstellt Session Token (nachdem gültige Email und Namen/Vornamen -> Telefonnummer eingegeben hat) (kein Cookie) (Session token wird auf dem Server behalten)
1. api.php?req=new -> checked intern ob Session Token gesetzt ist
2. api.php -> TCP_Send(TCP_IP,TCP_PORT)->Message: "mainkeyword=%mainkeyword#!#?#?#!#subkeyword=%subkeyword#!#?#?#!#"
3. client_thread(): read & Parse Message
4. client_thread(): import filyfiy: sid = fileify.createShortid()
5. client_thread(): print(sid) to api.php?req=new
6. client_thread(): python3 buzzgreator.py --mainkw "Julia Jasmin Rühle" --subkw "Venus" --session "SID"
7. buzzgreator.py schreibt Artikel ergebnis inkl. Resultcodes nach "/home/www/onetipp_artikel/sid.txt"
8. api.php?session=SID -> testet, ob "/home/www/onetipp_artikel/sid.txt" existiert und lesbar ist, gibt es via JQuery zurück
8.1. Session ID muss immer 12 Zeichen Nummern und Buchstaben sein, wenn dies nicht so ist, dann nicht auf dem Server ausführen
9. Session Token wird nach dem ausliefern des ersten Ergebnisses gelöscht
"""

def createSID():  
	print("Processing that nasty input!")
	res = fileify.createShortid()
	return res

#def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
def client_thread(conn, ip, port):
	# the input is in bytes, so decode it
	input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)
	
	# MAX_BUFFER_SIZE is how big the message can be
	# this is test if it's sufficiently big
	siz = sys.getsizeof(input_from_client_bytes)
	if siz >= MAX_BUFFER_SIZE:
		print("Servify.client_thread(): The length of input is probably too long: {}".format(siz))
	
	# decode input and strip the end of line
	input_from_client = input_from_client_bytes.decode("utf8").rstrip()
	input_from_client=wordify.encodeToLatin1(input_from_client)
	
	
	fromClient=input_from_client.split('#!#@#!#')
	mainKW=""
	subKW=""
	for ele in fromClient:
		if ele.find("mainKeyword") != -1:
			mainKW=ele.replace("mainKeyword=", "")
		if ele.find("subKeyword") != -1:
			subKW=ele.replace("subKeyword=", "")
	
	print("Servify.client_thread(): MainKeyword and SubKeyword from Client: mk={} sk={}".format(mainKW,subKW))
	# fwrite($client, "mainKeyword=$domainKeyword#!#@#!#subKeyword=$dosubKeyword\r\n");
	
	sidNumber = createSID()
	print("Servify.client_thread(): Sending Session ID to Client: {}".format(sidNumber))
	
	#sidNumber = fileify.createShortid()
	vysl = sidNumber.encode("utf8")  # encode the result string
	conn.sendall(vysl)  # send it to client
	conn.close()  # close connection
	print('Servify.client_thread(): Connection ' + ip + ':' + port + " ended")
	timestamp=str(int(time.time()))
	aCreatStart=str(dTime.now())
	logquery="humanTime="+aCreatStart+";"+"unixTime="+timestamp+";"+"conStatus="+ip+':'+port+";"+"articleID="+sidNumber+";"+"inputTcpClient="+input_from_client+";"+"mk="+mainKW+";"+"sk="+subKW+";"+"\n"
	fileify.plainWriteAppend(logquery, "/home/buz/buzzgreator/TreadingServerLog.txt")
	
	#python3 /home/buz/buzzgreator/testscript.py --mainkw "TEST1 Test1zwei" --subkw "TEST2 Test2_drei" --session "23232323"
	os.system("python3 /home/buz/buzzgreator/buzzgreator.py --mainkw \""+mainKW+"\" --subkw \""+subKW+"\" --session \""+sidNumber+"\"")
	return True

def start_server():
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# this is for easy starting/killing the app
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print('Servify.start_server(): Socket created')
	
	try:
		soc.bind((TCP_IP, TCP_PORT))
		print('Servify.start_server(): Socket bind complete')
	except socket.error as msg:
		print('Servify.start_server(): Bind failed. Error : ' + str(sys.exc_info()))
		sys.exit()
	
	#Start listening on socket
	soc.listen(10)
	print('Servify.start_server(): Socket now listening')
	
	# for handling task in separate jobs we need threading
	# this will make an infinite loop needed for 
	# not reseting server for every client
	while True:
		conn, addr = soc.accept()
		ip, port = str(addr[0]), str(addr[1])
		print('Servify.start_server(): Accepting connection from ' + ip + ':' + port)
		try:
			Thread(target=client_thread, args=(conn, ip, port)).start()
		except:
			print("Servify.start_server(): Terible error!")
			traceback.print_exc()
	soc.close()

def mysend(socket, msg):
	#sent = socket.send(msg.encode('utf-8'))
	#sent = socket.send("\r\n".encode('utf-8'))
	send_bufr = "%s\r\n" %(msg)
	#print(send_bufr)
	socket.send(bytearray(send_bufr, "utf-8"))
	#socket.sendall(msg.encode('utf-8'))
	return True
	"""
	totalsent 	= 0
	MSGLEN 		= len(msg)
	while totalsent < MSGLEN:
		sent = socket.send(msg[totalsent:].encode('utf-8'))
		if sent == 0:
			raise RuntimeError("socket connection broken")
		totalsent = totalsent + sent
		# send \r\n
	"""

def myreceive(socket, msg):
	chunks 		= []
	bytes_recd 	= 0
	"""
	data 		= socket.recv(BUFFER_SIZE)
	"""
	MSGLEN 		= len(msg)
	while bytes_recd < MSGLEN:
		chunk = socket.recv(min(MSGLEN - bytes_recd, 2048))
		if chunk == b'':
			raise RuntimeError("socket connection broken")
		chunks.append(chunk)
		bytes_recd = bytes_recd + len(chunk)
	return b''.join(chunks)
	#return data.decode('utf-8')

"""
def makeSentenceSplitterCall(data_out):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	# Connect the socket to the port where the server is listening
	server_address = (TCP_IP, TCP_PORT)
	#print('connecting to %s port %s' % server_address)
	socket.timeout(120)
	sock.connect(server_address)
	# Send Data
	mysend(sock, data_out)
	# recive Data
	data = myreceive(sock, data_out)
	return data.decode('utf-8')
	

def makeSentenceSplitterCall(data_out):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = (TCP_IP, TCP_PORT)
	print('connecting to %s port %s' % server_address)
	socket.timeout(120)
	sock.connect(server_address)
	try:
    
		# Send data
		#message = 'This is the message.  It will be repeated.'
		print('sending "%s"' % data_out)
		data_out = data_out.encode('utf-8')
		sock.sendall(data_out)
		sock.sendall("\r\n")
		
		# Look for the response
		amount_received = 0
		amount_expected = len(data_out)
		
		data = sock.recv(16)
		
		while amount_received < amount_expected:
			data = sock.recv(16)
			amount_received += len(data)
			print('received "%s"' % data)
		
		
	finally:
		print('closing socket')
		sock.close()
		
	return data.decode('utf-8')
"""