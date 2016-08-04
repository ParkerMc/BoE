from socket import *
from threading import Thread
 
HOST = raw_input("Server: ")
PORT = 8000 
def main():
	global running
	running = True
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

	    s.send(name+": "+message)

def recive(s):
	global running
	while running:
		data = s.recv(1024) 
		print data

main()