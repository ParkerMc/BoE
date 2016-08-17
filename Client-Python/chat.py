from socket import *
from socket import ssl as sslc
from threading import Thread
import settings

def recv(s):
	data = s.read(1024)
	try:
		return data[:1], data[1:]; # return data
	except:
		return None;
def main():
	print "Run with -t for terminal ver"
	
def bash():
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
	s.write("\x00"+username)
	pType, data = recv(s)
	while data != "incorect"and pType == "\x01":
		passwd = raw_input("Password: ")
		print "loading please wait"
		s.write("\x01"+passwd)
		pType, data = recv(s)

	if data == "make":
		make = "  "
		while make not in ["n","N","y","Y",""]:
			make = raw_input("User does not exist make user.(y/[n]): ")
		if make != "":
			s.write("\x03"+make.replace("N","n").replace("Y","y"))
		else:
			s.write("\x03"+"n")
		pType, data = recv(s)
		if make.replace("Y","y") == "y" and pType == "\01":
			passwd = raw_input("Password: ")
			print "loading please wait"
			s.write("\x01"+passwd)

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
	    	s.write("\x05"+username+": "+message)

def recive(s):
	global running
	while running:
		try:
			pType, data = recv(s)
			if not data: break
		except Exception, e:
			running = False
		if pType == "\x04" or pType == "\x05":
			print data
