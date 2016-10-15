import re
import sys
import webbrowser
from os import path
from threading import Thread

from PyQt4 import QtGui, uic, QtCore, Qt
from PyQt4.QtWebKit import QWebSettings

import error
from ServerList import ServerList
from serverMGR import Socket
from toHtml import toHtml

main_class = uic.loadUiType("ui/main.ui")[0]


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
        self.resetWeb()
        self.last = None
        sys.excepthook = error.excepthook2

    def resetWeb(self):
        self.chatBox.setHtml(
            '<style>'
            '* {font-size:14px}'
            'code {border-radius: 4px;border: 1px solid;display: inline;padding: 0 .5em;margin: 0 .1em;'
            'line-height: 14px;background-color: #f8f8f8;border-color: #ccc;color: #333}'
            '</style>'
            '<script>'
            'window.onscroll = function() {RunOnPython.loadMore()};'
            '</script>')
        self.chatBox.page().mainFrame().addToJavaScriptWindowObject('RunOnPython', self)
        self.chatBox.page().settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

    def appendWeb(self, object_web, text):
        pos = object_web.page().mainFrame().scrollPosition()
        if object_web.page().mainFrame().scrollBarMaximum(Qt.Qt.Vertical) is pos.y():
            max_scroll = True
        else:
            max_scroll = False
        object_web.setHtml(object_web.page().mainFrame().toHtml() + text)
        if max_scroll:
            pos.setY(object_web.page().mainFrame().scrollBarMaximum(Qt.Qt.Vertical))
        object_web.page().mainFrame().setScrollPosition(pos)
        object_web.page().mainFrame().addToJavaScriptWindowObject('RunOnPython', self)

    def prependWeb(self, object_web, text):
        object_web.setHtml(
            re.sub("(.*?)<body>(.*?)</body>(.*?)", r"\1<body>" + text + '<a id="goto"></a>' + r"\2</body>\3",
                   str(object_web.page().mainFrame().toHtml()).replace('<a id="goto"></a>', "")))
        object_web.page().mainFrame().addToJavaScriptWindowObject('RunOnPython', self)
        object_web.page().mainFrame().evaluateJavaScript("document.getElementById('goto').scrollIntoView();")

    def chatUpdate(self):
        ids, messages = self.socket.getMessages(4, 5)
        for i, j in zip(messages, ids):
            if j == 4:
                self.last = str(i).split("<")[0]
                self.prependWeb(self.chatBox, toHtml((str(i).split("<")[1])))
            else:
                self.appendWeb(self.chatBox, toHtml(str(i)))

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

    @staticmethod
    @QtCore.pyqtSlot(str)
    def openUrl(self, url):
        thread = Thread(target=webbrowser.open, args=[url], name="web")
        thread.start()

    @QtCore.pyqtSlot()
    def loadMore(self):
        if str(self.last) != "all" and self.chatBox.page().mainFrame().scrollPosition().y() < 30:
            self.socket.send(4, self.last)
