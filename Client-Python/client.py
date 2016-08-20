import chat, sys, gui
from PyQt4 import QtGui

if __name__ == "__main__":
    if "-t" in sys.argv: chat.bash()
    else:
        app = QtGui.QApplication(sys.argv)
        mainWindow = gui.Main()
        mainWindow.show()
        app.exec_()
