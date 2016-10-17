from PyQt4 import QtGui, uic
from os import path

login_class = uic.loadUiType(path.join(path.dirname(path.realpath(__file__)), "ui/login.ui"))[0]


class Login(QtGui.QDialog, login_class):
    def __init__(self, username, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.password = None
        self.username = username
        self.user.setText(username)
        self.Login.clicked.connect(self.login)
        self.tryPass = False

    def login(self):
        self.tryPass = True
        self.password = str(self.passwd.text())
        self.username = str(self.user.text())
        self.close()
