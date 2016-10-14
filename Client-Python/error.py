import cStringIO
import platform
import sys
import time
import traceback
import urllib

from PyQt4 import QtGui, uic

error_class = uic.loadUiType("ui/error.ui")[0]


def excepthook(excType, excValue, tracebackobj):
    separator = '-' * 80
    logFile = "Error.log"
    versionInfo = "NR"
    timeString = time.strftime("%m/%d/%Y, %H:%M:%S")

    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, timeString, separator, errmsg, separator, tbinfo, separator, "Version: " + versionInfo,
                "Os: " + platform.system(), "Architecture: " + platform.architecture()[0], separator]
    msg = '\n'.join(sections)
    try:
        f = open(logFile, "w")
        f.write(msg)
        f.close()
    except IOError:
        pass
    app = QtGui.QApplication(sys.argv)
    mainWindow = error(msg)
    mainWindow.show()
    app.exec_()


class error(QtGui.QMainWindow, error_class):
    def __init__(self, msg, parent=None):
        QtGui.QDialog.__init__(self, parent)
        super(error, self).__init__()
        self.setupUi(self)
        self.msg = msg
        self.emsg.setText(msg)
        self.send.clicked.connect(self.sende)

    def sende(self):
        try:
            urllib.urlretrieve(
                """https://parkermc.ddns.net/boebugs.php?msg=%s""" % (
                    "From: " + self.email.text() + "\n\n" + self.de.toPlainText() + "\n" + self.msg), "temp.html")
            errorbox = QtGui.QMessageBox(self)
            errorbox.setWindowTitle("Sent")
            errorbox.setText("Email sent thank you :)")
            errorbox.exec_()
        except:
            errorbox = QtGui.QMessageBox(self)
            errorbox.setWindowTitle("Error")
            errorbox.setText("Can not send email.")
            errorbox.exec_()


def excepthook2(excType, excValue, tracebackobj):
    separator = '-' * 80
    logFile = "Error.log"
    versionInfo = "NR"
    timeString = time.strftime("%m/%d/%Y, %H:%M:%S")

    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, timeString, separator, errmsg, separator, tbinfo, separator, "Version: " + versionInfo,
                "Os: " + platform.system(), "Architecture: " + platform.architecture()[0], separator]
    msg = '\n'.join(sections)
    try:
        f = open(logFile, "w")
        f.write(msg)
        f.close()
    except IOError:
        pass
    mainWindow = error2(msg)
    mainWindow.exec_()


class error2(QtGui.QDialog, error_class):
    def __init__(self, msg, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.msg = msg
        self.emsg.setText(msg)
        self.send.clicked.connect(self.sende)

    def sende(self):
        try:
            urllib.urlretrieve(
                """https://parkermc.ddns.net/boebugs.php?msg=%s""" % (
                    "From: " + self.email.text() + "\n\n" + self.de.toPlainText() + "\n" + self.msg), "temp.html")
            errorbox = QtGui.QMessageBox(self)
            errorbox.setWindowTitle("Sent")
            errorbox.setText("Email sent thank you :)")
            errorbox.exec_()
        except:
            errorbox = QtGui.QMessageBox(self)
            errorbox.setWindowTitle("Error")
            errorbox.setText("Can not send email.")
            errorbox.exec_()
