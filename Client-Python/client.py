from socket import *
import socket
from threading import Thread
 
HOST = raw_input("Server: ")
PORT = 8000 
def main():
	global running
	running = True
	global name 
	name = raw_input("Name: ")
	uws = socket.socket(AF_INET, SOCK_STREAM) 
	uws.connect((HOST, PORT)) 
	s = socket.ssl(uws)
	s.write(name)
	print "Connected"
	rthread = Thread(target = recive, args = (s, ))
	rthread.start()
	while True:
	    message = raw_input("") 
	    if message == "quit":
	    	s.write("quit")
	        s.close() 
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
			raise e
			running = False
		print data

main()