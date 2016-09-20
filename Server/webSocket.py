import datetime
import settings
from os import path

from passlib.hash import sha256_crypt

from webSocketServer import SSLWebSocketServer, WebSocket


global clients
global users
global Cfile
global ftext
global users

usersOn = []
clients = []
users = []
Cfile = None
ftext = []

class History():
	def __init__(self):
		pass

	@staticmethod
	def load():
		global ftext
		global Cfile
		ftext = [] # Reset array
		if path.isfile("chat/Main/"+str(datetime.date.today())+".chat"): # If it exists add the text to array
			Cfile = open("chat/Main/"+str(datetime.date.today())+".chat","r") # Open file
			ftext = Cfile.readlines() # Read lines to array
			Cfile.close() # Close the file
			Cfile = open("chat/Main/"+str(datetime.date.today())+".chat","w") # Opens that file in write mode
			Cfile.write("".join(ftext)) # Write the same lines to the file or else they will get overiden

		else: # If file dose not exist make it
			Cfile = open("chat/Main/"+str(datetime.date.today())+".chat","w") # open file

	@staticmethod
	def add(text): # To add text to the history
		if not path.isfile("chat/Main/"+str(datetime.date.today())+".chat"): # If file dose not exist make it
			global ftext
			global Cfile
			Cfile.close() # Close old file
			ftext = [] # Reset Array
			Cfile = open("chat/Main/"+str(datetime.date.today())+".chat","w") # Open file

		ftext.append(text+"\n") # Add text to string
		Cfile.write(text+"\n") # Add text to file


class User():
	def __init__(self):
		pass

	@staticmethod
	def loadusers():
		global users
		users = [] #reset array
		f = open("users.csv","r") # open file
		ft = f.readlines() # readlines
		f.close() # close file
		for i in ft:# loop though lines
			j = i.replace("\n","").split(",") # remove EOL and split
			if len(j) == 4: users.append((j[0],j[1],j[2],j[3])) # add data to array
		ft = None # delate ft

	@staticmethod
	def makeUser(username, passwd ,level,icon): # make user
		users.append((username,passwd,level,icon))#add to user array
		f = open("users.csv","w")# open file to save
		for i, j, k, l in users: f.write(i+","+j+","+str(k)+","+l+"\n") #sve to file
		f.close()# close the file

class Chat(WebSocket):

	def handleMessage(self):
		print self.data
		self.mods.message(self, self.server)
		if self.data == "quit":
			self.close()
		elif self.loggedin and self.pId == "\x05":
			History.add(self.data)
			for client in clients:
				client.send("\x05"+self.username + ' : ' + self.data)
		elif self.pId == "\x00":
			found = False
			for i, j, k, l in users:
				if i == self.data:
					found = True
					self.hash = j
					self.username = self.data
					self.send("\x01")
			if not found:
				self.username = self.data
				self.send("\x03")
		elif self.pId == "\x01" and not self.makeingUser:
			right = sha256_crypt.verify(self.data, self.hash)
			if right:
				self.send("\x03"+"correct")
				self.send("\x04"+("".join(ftext)))
				clients.append(self)
				for client in clients:
					client.send("\x05"+self.username+"@"+self.address[0]+ " - connected \n")
				self.send("\x05"+settings.welcomeMsg)
				self.loggedin = True
			else: self.send("\x01"+"incorect")
		elif self.pId == "\x01" and self.makeingUser:
			passh = sha256_crypt.encrypt(self.data)
			User.makeUser(self.username,passh,0,"none")
			self.send("\x04"+("".join(ftext)))
			clients.append(self)
			for client in clients:
				client.send("\x05"+self.username+"@"+self.address[0]+ " - connected \n")
			self.send("\x05"+settings.welcomeMsg)
			self.loggedin = True
			self.makeingUser = False
		elif self.pId == "\x03":
			if self.data == "y":
				self.makeingUser = True
				self.send("\x01")
		elif self.pId == "\x06":
			if self.loggedin:
				self.username = ""
				self.loggedin = False
				for client in clients:
					client.send("\x05"+self.username + "@" + self.address[0] + ' - disconnected')


				clients.remove(self)

		else: self.mods.newid(self, self.server)

	def handleConnected(self):
		self.hash = ""
		self.loggedin = False
		self.makeingUser = False
		self.username = ""
		print self.address, 'connected'
		self.send("\x00")

	def handleClose(self):
		self.mods.Cclose(self, self.server)
		try: clients.remove(self)
		except: None
		print self.address, 'closed'
		if self.loggedin:
			for client in clients:
				client.send("\x05"+self.username + ' - disconnected')


def start():
	print "loading users..."
	User.loadusers()
	print "loading history..."
	History.load()
	server = SSLWebSocketServer(settings.host, settings.port, Chat,"ssl.pem","ssl.pem")
	print "starting server..."
	server.serveforever()