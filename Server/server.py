from socket import *
from threading import Thread
from passlib.hash import sha256_crypt
from os import path
import datetime, ssl

def serverInt():
	global running
	global file
	global ftext
	global conns
	global threads
	global welcomeMsg
	global users

	running = True
	file = False
	ftext = []
	threads = [] # For all the threads
	conns = [] # For all the connections
	users = False #for users
	loadusers() #loadusers
	addToFile("") # Load chat history to array

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
			threads.append(Thread(target = connectionHandler, args = (conn, threadi, addr, ))) # Add threads
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
		try:
			j.sendall(data) # and send data
		except: None

def removeConn(tid,name):# remove conn form array
	global conns # get conns
	k = 0
	for i, j in conns: # loop though
		if i == tid: # and find the right id
			conns.pop(k) # remove
			broadcastData(name+" left.") # left msg to all
			j.close() # close connection
		k += 1

def connectionHandler(conn, tid, addr): # Handle the connections
	conRunning = True
	username = recieveData(conn) # Get username
	global users #get users
	found = False
	for i, j, k, l in users: # loop though users
		if i == username: # if it is the user name
			found = True # set found
			conn.sendall("pass") # send for the password
			passwd = conn.recv(1024) # Get password
			passright = sha256_crypt.verify(passwd, j)
			if not passright: # check password
				passright = sha256_crypt.verify(passwd, j)
				conn.sendall("pass") # send for the password
				passwd = conn.recv(1024) # Get password
				if not sha256_crypt.verify(passwd, j): # check password
					passright = sha256_crypt.verify(passwd, j)
					conn.sendall("pass") # send for the password
					passwd = conn.recv(1024) # Get password
					if not sha256_crypt.verify(passwd, j): conRunning = False # check password if rond stop
			if passright: 
				conn.sendall("null")
				conn.sendall("null")

	if not found:
		conn.sendall("make")
		conn.sendall("make")
		if recieveData(conn) == "y":
			conn.sendall("pass") # send for the password
			passwd = conn.recv(1024) # Get password
			passh = sha256_crypt.encrypt(passwd)
			makeUser(username,passh,0,"none")
		else:
			conRunning = False
	if conRunning:
		global ftext # Get array with text
		print "".join(ftext)
		conn.sendall("".join(ftext)) # send to client
		broadcastData(username+"@"+addr[0]+ " is now connected! \n") # Send connection msg to every one
		conn.sendall(welcomeMsg) # Send welcome msg to new connection
	while running and conRunning: # keep looping till end or lose connection
		try:
			data = recieveData(conn)# get data
			if data == "quit": # if quit
				removeConn(tid,username) # remove connection
				conRunning = False #end loop
			else:					#else
				addToFile(data) # save to file
				broadcastData(data) # send to everyone
		except Exception, e: # if error
			removeConn(tid,username) # remove connection
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

def loadusers():
	global users
	users = []
	f = open("users.csv","r") # open file
	ft = f.readlines() # readlines
	f.close() # close file
	for i in ft:
		j = i.replace("\n","").split(",")
		users.append((j[0],j[1],j[2],j[3]))
	ft = None # delate ft

def makeUser(username, passwd ,level,icon): # make user
	global users
	users.append((username,passwd,level,icon))
	f = open("users.csv","w")
	for i, j, k, l in users: f.write(i+","+j+","+str(k)+","+l+"\n")
	f.close()

serverInt()
main()
