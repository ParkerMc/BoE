from socket import *
from threading import Thread
 
HOST = 'localhost'
PORT = 8000 
def main():
	global running
	running = True
	s = socket(AF_INET, SOCK_STREAM) 
	s.connect((HOST, PORT)) 
	print "Connected"
	rthread = Thread(target = recive, args = (s, ))
	rthread.start()
	while True:
	    message = raw_input("") 
	    if message == "quit":
	        s.close() 
	        running = False
	        break; 

	    s.send(message)

def recive(s):
	global running
	while running:
		data = s.recv(1024) 
		print data

main()