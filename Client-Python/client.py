from socket import *
import socket
from threading import Thread
 
HOST = raw_input("Server: ")
PORT = 8000 
def main():
	global running
	running = True
	global name 
	uws = socket.socket(AF_INET, SOCK_STREAM) 
	uws.connect((HOST, PORT)) 
	s = socket.ssl(uws)
	name = raw_input("Username: ")
	s.write(name)
	while s.read(1024) == "pass":
		passwd = raw_input("Password: ")
		print "loading please wait"
		s.write(passwd)

	if s.read(1024) == "make":
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
		print s.read(1024)
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
	    	s.write(name+": "+message)

def recive(s):
	global running
	while running:
		try:
			data = s.read(1024) 
		except Exception, e:
			running = False
		print data

main()