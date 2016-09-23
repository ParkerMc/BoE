#!/usr/bin/python2
import sys
from PyQt4 import QtGui

import gui

if __name__ == "__main__":
    # if "-t" in sys.argv: chat.bash()
    # else:
    app = QtGui.QApplication(sys.argv)
    mainWindow = gui.Main()
    mainWindow.show()
    app.exec_()
