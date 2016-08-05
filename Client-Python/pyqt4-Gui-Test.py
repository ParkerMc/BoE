import sys
from PyQt4 import QtGui, uic

form_class = uic.loadUiType("qtgui.ui")[0]

class Main(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

   

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = Main()
    myWindow.show()
    app.exec_()