from PyQt4 import QtGui, uic
from os import path 

createUser_class = uic.loadUiType(path.join(path.dirname(path.realpath(__file__))[:-10], "ui/createuser.ui"))[0]


class CreateUser(QtGui.QDialog, createUser_class):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.yes.clicked.connect(self.make)
        self.no.clicked.connect(self.close)
        self.makeUser = False

    def make(self):
        self.makeUser = True
        self.close()
