from socket import *
from threading import Thread
from passlib.hash import sha256_crypt
from os import path
import datetime, ssl, settings

def serverInt():
	global running
	global file
	global ftext
	global conns
	global threads
	global welcomeMsg
	global users
	global usersOn

	running = True
	file = False
	ftext = []
	threads = {} # For all the threads
	conns = {} # For all the connections
	users = False #for users
	usersOn = []
	loadusers() #loadusers
	addToFile("") # Load chat history to array

	f = open("chat/Main/welcome.chat","r")
	welcomeMsg = f.readline()
	f.close()

def main():
	uws = socket(AF_INET, SOCK_STREAM) # Make socket
	uws.bind((settings.host, settings.port)) # Bind to ip and port
	uws.listen(5) # number of connections listening for
	if settings.ssl:
		s = ssl.wrap_socket(uws, keyfile="ssl.pem", certfile="ssl.pem") # Wrap with ssl
	else:
		s = uws
	print "Server is running...... \n"
	global conns
	global threads
	global welcomeMsg
	try:
		while running:
			conn, addr = s.accept() # Accept incomeing connection
			pType, name = recieveData(conn) # Get username
			if pType=="\x00":
				if name not in usersOn:
					usersOn.append(name)
					threads[name] = Thread(target = connectionHandler, args = (conn, addr, name, )) # Add threads
					threads[name].start() # Start thread
				else:
					conn.sendall("\x05""The user "+name+" is all ready connected")
	except KeyboardInterrupt:
		print "killed"

def recieveData(conn): # Recive Data form client
	data = conn.recv(1024)	# Get the data
	try:
		return data[:1], data[1:]; # return data
	except:
		return None;

def broadcastData(data, name=None): # send data
	global conns # Get all connections
	print data + "\n"
	for j in conns.items(): # loop through
		j[1].sendall(data) # and send data

def removeConn(name):# remove conn form array
	global conns # get conns
	global usersOn#get users
	usersOn.remove(name) #remove name
	broadcastData("\x05"+name+" left.") # left msg to all
	conns[name].close() # close connection
	conns.pop(name) # remove

def checkPasswd(conn, hash):
	conn.sendall("\x01") # send for the password
	pType, data = recieveData(conn)# Get password
	if pType == "\x01" and sha256_crypt.verify(data, hash): return True
	else: return False


def connectionHandler(conn, addr, username): # Handle the connections
	conRunning = True
	global users #get users
	found = False

	for i, j, k, l in users: # loop though users
		if i == username: # if it is the user name
			found = True # set found
			if not checkPasswd(conn, j): # check password
				if not checkPasswd(conn, j): # check password
					if not checkPasswd(conn, j):
						conRunning = False # check password if rond stop
						conn.sendall("\x01"+"incorect")

	if not found:
		conn.sendall("\x03")
		pType, data = recieveData(conn)
		if data == "y" and pType == "\x03":
			conn.sendall("\x01") # send for the password
			passwd = conn.recv(1024) # Get password
			passh = sha256_crypt.encrypt(passwd)
			makeUser(username,passh,0,"none")
		else:
			conRunning = False
	if conRunning:
		global ftext # Get array with text
		conn.sendall("\x04"+("".join(ftext))) # send to client
		conns[username] = conn # Add to connections array
		broadcastData("\x05"+username+"@"+addr[0]+ " is now connected! \n") # Send connection msg to every one
		conn.sendall("\x05"+welcomeMsg) # Send welcome msg to new connection
	else:
		usersOn.remove(username)
	while running and conRunning: # keep looping till end or lose connection
		try:
			pType, data = recieveData(conn)# get data
			if pType == "\x05":
				if not data:
					removeConn(username) # remove connection
					conRunning = False #end loop
					break
				elif data == "quit": # if quit
					removeConn(username) # remove connection
					conRunning = False #end loop
				else:					#else
					addToFile(data) # save to file
					broadcastData("\x05"+data) # send to everyone
		except Exception, e: # if error
			removeConn(username) # remove connection
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
		if len(j) == 4: users.append((j[0],j[1],j[2],j[3]))
	ft = None # delate ft

def makeUser(username, passwd ,level,icon): # make user
	global users
	users.append((username,passwd,level,icon))
	f = open("users.csv","w")
	for i, j, k, l in users: f.write(i+","+j+","+str(k)+","+l+"\n")
	f.close()
