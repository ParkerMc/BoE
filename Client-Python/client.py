from socket import *
from threading import Thread
 
HOST = raw_input("Server: ")
PORT = 8000 
def main():
	global running
	running = True
	global name 
	name = raw_input("Name: ")
	s = socket(AF_INET, SOCK_STREAM) 
	s.connect((HOST, PORT)) 
	s.send(name)
	print "Connected"
	rthread = Thread(target = recive, args = (s, ))
	rthread.start()
	while True:
	    message = raw_input("") 
	    if message == "quit":
	    	s.send("quit")
	        s.close() 
	        running = False
	        break; 
	    if message != "":
	    	s.send(name+": "+message)

def recive(s):
	global running
	while running:
		try:
			data = s.recv(1024) 
		except:
			running = False
		print data

main()