from os import path

from PyQt4 import QtGui, uic, QtWebKit
from toHtml import toHtml

from ServerList import ServerList
from serverMGR import Socket

main_class = uic.loadUiType("ui/main.ui")[0]


def appendWeb(objectWeb, text):
    objectWeb.setHtml(objectWeb.page().mainFrame().toHtml() + text)


class Main(QtGui.QMainWindow, main_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)  # Run gui init
        self.setupUi(self)  # Setup Ui
        self.socket = Socket()
        self.servers = {}  # Array for servers
        if path.isfile("servers.csv"):  # If server file exists
            f = open("servers.csv", "r")  # Open file for reading
            data = f.readlines()  # Read file
            f.close()  # Close file
            for i in data:  # Loop though line
                if i != "":
                    j = i.replace("\n", "").split(",")  # Split at the ,'s
                    self.servers[j[0]] = (j[1], j[2], j[3])  # Add to array
        self.serverList = ServerList(self)  # Load server list
        self.serverList.show()  # Show server list
        # Connect buttons
        self.actionConnect.triggered.connect(self.connectToServer)
        self.actionDisconnect.triggered.connect(self.socket.disconnect)
        self.actionQuit.triggered.connect(self.close)
        self.socket.newMsg.connect(self.chatUpdate)
        self.sendB.clicked.connect(self.send)
        self.text.returnPressed.connect(self.send)
        self.chatBox.setHtml('<style>* {font-size:14px} code {border-radius: 4px;border: 1px solid;font-size: 14px;font-weight: 600;vertical-align: middle;word-wrap: break-word;text-align: left;white-space: pre-wrap;unicode-bidi: embed;direction: ltr;display: inline;padding: 0 .5em;margin: 0 .1em;line-height: 14px;font-family: "Source Code Pro", Monaco, monospace, Courier, "Lucida Console";background-color: #f8f8f8;border-color: #ccc;color: #333}</style>')

    def chatUpdate(self):
        ids, messages = self.socket.getMessages(4, 5)
        for i in messages:
            appendWeb(self.chatBox, toHtml(str(i)))

    def send(self):
        if self.text.text() == "quit":
            self.socket.disconnect()
        elif self.text.text() != "":
            self.socket.send(5, str(
                self.text.text().replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">",
                                                                                                           "&gt;")))
            self.text.setText("")

    def closeEvent(self, event):
        self.socket.disconnect()

    def connectToServer(self):
        self.serverList = ServerList(self)  # Load server list
        self.serverList.show()  # Show server list
