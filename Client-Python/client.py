#!/usr/bin/python2
from PyQt4 import QtGui

import chat
import gui
import sys

if __name__ == "__main__":
    if "-t" in sys.argv: chat.bash()
    else:
        app = QtGui.QApplication(sys.argv)
        mainWindow = gui.Main()
        mainWindow.show()
        app.exec_()
