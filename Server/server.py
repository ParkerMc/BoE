from socket import *
from threading import Thread
from os import path
import datetime, ssl

def serverInt():
	global running
	global file
	global ftext
	global conns
	global threads
	global welcomeMsg

	running = True
	file = False
	ftext = []
	threads = [] # For all the threads
	conns = [] # For all the connections

	f = open("chat/Main/welcome.chat","r")
	welcomeMsg = f.readline()
	f.close()

def main():
	uwrapeds = socket(AF_INET, SOCK_STREAM) # Make socket
	uwrapeds.bind(('localhost', 8000)) # Bind to ip and port
	uwrapeds.listen(5) # number of connections listening for
	s = ssl.wrap_socket(uwrapeds, keyfile="ssl.pem", certfile="ssl.pem") # Wrap with ssl
	print "Server is running...... \n"
	global conns
	global threads
	global welcomeMsg
	threadi = 0 # Index for threads
	try:
		while running:
			conn, addr = s.accept() # Accept incomeing connection
			conns.append((threadi,conn)) # Add to connections array
			data = recieveData(conn) # Get user name
			addToFile("") # Load chat history to array
			global ftext # Get array with text
			conn.write("".join(ftext)) # send to client
			broadcastData(data+"@"+addr[0]+ " is now connected! \n") # Send connection msg to every one
			conn.sendall(welcomeMsg) # Send welcome msg to new connection
			threads.append(Thread(target = connectionHandler, args = (conn, data, threadi, ))) # Add threads
			threads[threadi].start() # Start thread
			threadi += 1; # add one to thread index
	except KeyboardInterrupt:
		print "killed"

def recieveData(conn): # Recive Data form client
	data = conn.recv(1024)	# Get the data
	print  data, "\n" # Print it to server
	return data; # return data

def broadcastData(data, name=None): # send data
	global conns # Get all connections
	for i,j in conns: # loop through
		j.sendall(data) # and send data

def removeConn(tid):# remove conn form array
	global conns # get conns
	for i, j in conns: # loop though
		if i == tid: # and find the right id
			conns.pop(i) # remove
			broadcastData(name+" left.") # left msg to all
			j.close() # close connection

def connectionHandler(conn, name, tid): # Handle the connections
	conRunning = True
	while running and conRunning: # keep looping till end or lose connection
		try:
			data = recieveData(conn)# get data
			if data == "quit": # if quit
				removeConn(tid) # remove connection
				conRunning = False #end loop
			else:					#else
				addToFile(data) # save to file
				broadcastData(data) # send to everyone
		except Exception, e: # if error
			removeConn(tid) # remove connection
			conRunning = False #end loop


def addToFile(text): # To load and add text to the file
					 # For ONLY loading the file use ""
	global file # For the file obj
	global ftext # For the file text
	if not file: # If file is not loaded
		if path.isfile("chat/Main/"+str(datetime.date.today())+".chat"): # If it exists add the text to array 
			file = open("chat/Main/"+str(datetime.date.today())+".chat","r") # Open file
			ftext = file.readlines() # Read lines to array
			file.close() # Close the file
			file = open("chat/Main/"+str(datetime.date.today())+".chat","w") # Opens that file in write mode
			file.write("".join(ftext)) # Write the same lines to the file or else they will get overiden

		else: # If file dose not exist and no file is loaded make it
			ftext = [] # Reset array
			file = open("chat/Main/"+str(datetime.date.today())+".chat","w") # open file
	
	elif not path.isfile("chat/Main/"+str(datetime.date.today())+".chat"): # If file dose not exist make it 
		file.close() # Close old file
		ftext = [] # Reset Array
		file = open("chat/Main/"+str(datetime.date.today())+".chat","w") # Open file
	
	if text != "": # Add text to array and file
		ftext.append(text+"\n") # Add text to string
		file.write(text+"\n") # Add text to file

serverInt()
main()
