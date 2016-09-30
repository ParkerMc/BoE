import datetime
from os import path
from struct import pack

from passlib.hash import sha256_crypt

import settings
from webSocketServer import SSLWebSocketServer, WebSocket

usersOn = []
clients = []
users = []
Cfile = None
ftext = []

global clients
global users
global Cfile
global ftext
global users


class History:
    def __init__(self):
        pass

    @staticmethod
    def load(force_load):
        filename = "chat/Main/" + str(datetime.date.today()) + ".chat"
        global ftext
        global Cfile
        ftext = []  # Reset array
        if path.isfile(filename) and force_load:  # If it exists add the text to array
            Cfile = open(filename, "r")  # Open file
            ftext = Cfile.readlines()  # Read lines to array
            Cfile.close()  # Close the file
            Cfile = open(filename, "a")  # Opens that file in write mode

        elif not path.isfile(filename):  # If file dose not exist make it
            Cfile = open(filename, "w")  # open file

    @staticmethod
    def add(text):  # To add text to the history
        filename = "chat/Main/" + str(datetime.date.today()) + ".chat"
        if not path.isfile(filename):  # If file dose not exist make it
            global ftext
            global Cfile
            Cfile.close()  # Close old file
            ftext = []  # Reset Array
            Cfile = open(filename, "w")  # Open file

        ftext.append(text + "\n")  # Add text to string
        Cfile.write(text + "\n")  # Add t
        # ext to file


class User:
    def __init__(self):
        pass

    @staticmethod
    def loadusers():
        global users
        users = []  # reset array
        if not path.isfile("users.csv"):
            f = open("users.csv","w")
            f.write("username,password,level,icon")
            f.close()
        f = open("users.csv", "r")  # open file
        ft = f.readlines()  # readlines
        f.close()  # close file
        for i in ft:  # loop though lines
            j = i.replace("\n", "").split(",")  # remove EOL and split
            if len(j) == 4:
                users.append((j[0], j[1], j[2], j[3]))  # add data to array
        del ft  # delate ft

    @staticmethod
    def makeUser(username, passwd, level, icon):  # make user
        users.append((username, passwd, level, icon))  # add to user array
        f = open("users.csv", "w")  # open file to save
        for i, j, k, l in users:
            f.write(i + "," + j + "," + str(k) + "," + l + "\n")  # sve to file
        f.close()  # close the file


class Chat(WebSocket):
    def __init__(self, server, sock, address, mods):
        super(Chat, self).__init__(server, sock, address, mods)
        self.hash = ""
        self.loggedin = False
        self.makeingUser = False
        self.username = ""

    def connectionMsg(self, msg):
        self.sendall(pack(">i", 5) + self.username + "@" + self.address[0] + " - " + msg + "\n")

    @staticmethod
    def sendall(message):
        for client in clients:
            client.send(message)

    def afterLogin(self):
        History.load(False)
        self.send(pack(">i", 4) + ("".join(ftext)))
        clients.append(self)
        self.connectionMsg("Connected")
        self.send(pack(">i", 5) + settings.welcomeMsg + "\n")
        self.loggedin = True

    def handleMessage(self):
        self.mods.message(self, self.server)
        if self.data == "quit":
            self.close()
        elif self.loggedin and self.pId == pack(">i", 5):
            History.add(self.username + ' : ' + self.data)
            self.sendall(pack(">i", 5) + self.username + ' : ' + self.data)
        elif self.pId == pack(">i", 0):
            found = False
            for i, j, k, l in users:
                if i.lower() == self.data.lower():
                    found = True
                    self.hash = j
                    self.username = self.data
                    self.send(pack(">i", 1))
            if not found:
                self.username = self.data
                self.send(pack(">i", 3))
        elif self.pId == pack(">i", 1) and not self.makeingUser:
            right = sha256_crypt.verify(self.data, self.hash)
            if right:
                self.send(pack(">i", 1) + "Correct")
                self.afterLogin()
            else:
                self.send(pack(">i", 1) + "Incorrect")
        elif self.pId == pack(">i", 1):
            passh = sha256_crypt.encrypt(self.data)
            User.makeUser(self.username.lower(), passh, 0, "none")
            self.afterLogin()
            self.makeingUser = False
        elif self.pId == pack(">i", 3):
            if self.data == "y":
                self.makeingUser = True
                self.send(pack(">i", 1))
        elif self.pId == pack(">i", 6):
            if self.loggedin:
                self.username = ""
                self.loggedin = False
                self.connectionMsg("Disconnected")

                clients.remove(self)

        else:
            self.mods.newid(self, self.server)

    def handleConnected(self):
        print(self.address, 'connected')
        self.send(pack(">i", 0))

    def handleClose(self):
        self.mods.Cclose(self, self.server)
        if self.loggedin:
            self.connectionMsg("Disconnected")
            try:
                clients.remove(self)
            except:
                pass
        print self.address, 'closed'


def start():
    print "loading users..."
    User.loadusers()
    print "loading history..."
    History.load(True)
    server = SSLWebSocketServer(settings.host, settings.port, Chat, "ssl.pem", "ssl.pem")
    print "starting server..."
    server.serveforever()
