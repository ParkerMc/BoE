from socket import *
from socket import ssl as sslc
from threading import Thread
import settings


def main():
	if settings.host == "":	host = raw_input("Server: ")
	else: host = settings.host
	if settings.port == "":	port = raw_input("Port: ")
	else: port = settings.port
	global running
	running = True 
	uws = socket(AF_INET, SOCK_STREAM) 
	uws.connect((host, port)) 
	s = sslc(uws)
	global username
	if settings.username == "": username = raw_input("Username: ")
	else: username = settings.username
	s.write(username)
	data = s.read(1024)
	while data == "pass":
		passwd = raw_input("Password: ")
		print "loading please wait"
		s.write(passwd)
		data = s.read(1024)

	if data == "make":
		make = "  "
		while make not in ["n","N","y","Y",""]:
			make = raw_input("User does not exist make user.(y/[n]): ")
		if make != "":
			s.write(make.replace("N","n").replace("Y","y"))
		else:
			s.write("n")
		if make.replace("Y","y") == "y":
			s.read(1024)
			passwd = raw_input("Password: ")
			print "loading please wait"
			s.write(passwd)
			
		else:
			running = False

	if running:
		print "\n"+data
		print "Connected"
		rthread = Thread(target = recive, args = (s, ))
		rthread.start()
	while running:
	    message = raw_input("") 
	    if message == "quit":
	    	s.write("quit")
	        uws.close() 
	        running = False
	        break; 
	    if message != "":
	    	s.write(username+": "+message)

def recive(s):
	global running
	while running:
		try:
			data = s.read(1024) 
			if not data: break
		except Exception, e:
			running = False
		print data

