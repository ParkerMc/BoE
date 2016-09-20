import settings
from PyQt4 import QtGui, QtCore, uic
from socket import *
from socket import ssl as sslc
from threading import Thread, RLock
from re import sub

global chatText_queue
global chatText_queue_lock

main_class = uic.loadUiType("ui/qtgui.ui")[0]
login_class = uic.loadUiType("ui/login.ui")[0]
createuser_class = uic.loadUiType("ui/createuser.ui")[0]

chatText_queue = []
chatText_queue_lock = RLock()

class Main(QtGui.QMainWindow, main_class):
    updateChat = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        global updateChat
        updateChat = self.updateChat
        self.sendB.clicked.connect(self.send)
        self.text.returnPressed.connect(self.send)
        self.updateChat.connect(self.chatUpdate)

    def chatUpdate(self):
        chatText_queue_lock.acquire()
        for i in chatText_queue:
            chatText_queue.remove(i)
            self.chatBox.append(str(i))
        chatText_queue_lock.release()


    def send(self):
        text = sub('\W+', ' ', str(self.text.text()))
        if text == "quit":
            s.write("\x05quit")
            uws.close()
            running = False
        elif self.text.text() != "":
            s.write("\x05"+text)
    def closeEvent(self, event):
        s.write("\x05quit")
        uws.close()
    def connect(self):
        self.login = login(self)
        self.login.exec_()

class login(QtGui.QDialog, login_class):
    def __init__(self, parent=None):
        global uws
        uws = socket(AF_INET, SOCK_STREAM)
        uws.connect((settings.host, settings.port))
        global s
        s = sslc(uws)
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.Login.clicked.connect(self.login)

    def login(self):
        s.write("\x06")
        user = sub('\W+', ' ', str(self.user.text()))
        passwd = sub('\W+', ' ', str(self.passwd.text()))
        s.write("\x00"+user)
        pType, data = recv(s)
        if pType == "\x03":
            self.make = createuser(user, passwd, self.parent())
            self.make.exec_()
            self.accept()
        elif pType == "\x01":
            s.write("\x01"+passwd)
            pType, data = recv(s)
            if pType == "\x03" and data == "correct":
                global rthread
                try: rthread.kill()
                except: None
                rthread = Thread(target = recive, args = ( ))
                rthread.start()
                global username
                username = user
                self.accept()

            else:
                msgbox = QtGui.QMessageBox(self)
                msgbox.setText(data)
                msgbox.exec_()
                uws.close()
        else:
            msgbox = QtGui.QMessageBox(self)
            msgbox.setText(data)
            msgbox.exec_()
            uws.close()

class createuser(QtGui.QDialog, createuser_class):
    def __init__(self, username, passwd,parent=None):
        self.username = username
        self.passwd = passwd
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.yes.clicked.connect(self.make)
        self.no.clicked.connect(self.close)

    def close(self):
        s.write("\x03"+"n")
        uws.close()
        self.accept()

    def make(self):
        s.write("\x03"+"y")
        pType, data = recv(s)
        s.write("\x01"+str(self.passwd))
        global rthread
        try: rthread.kill()
        except: None
        rthread = Thread(target = recive, args = ( ))
        rthread.start()
        global username
        username = str(self.username)
        self.accept()

def recv(s):
    data = s.read(1024)
    try:
        return data[:1], data[1:]; # return data
    except:
        return None;

def recive():
    global running
    running = True
    while running:
        try:
            pType, data = recv(s)
            if not data and not pType: break
        except Exception, e:
            running = False
        if pType == "\x04" or pType == "\x05":
            chatText_queue_lock.acquire()
            chatText_queue.append(data)
            chatText_queue_lock.release()
            updateChat.emit()
