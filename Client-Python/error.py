import cStringIO
import platform
import sys
import time
import traceback
import urllib

from PyQt4 import QtGui, uic

error_class = uic.loadUiType("ui/error.ui")[0]


def excepthook(exc_type, exc_value, tracebackobj):
    separator = '-' * 80
    log_file = "Error.log"
    version_info = "NR"
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S")

    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(exc_type), str(exc_value))
    sections = [separator, time_string, separator, errmsg, separator, tbinfo, separator, "Version: " + version_info,
                "Os: " + platform.system(), "Architecture: " + platform.architecture()[0], separator]
    msg = '\n'.join(sections)
    try:
        f = open(log_file, "w")
        f.write(msg)
        f.close()
    except IOError:
        pass
    app = QtGui.QApplication(sys.argv)
    main_window = Error(msg)
    main_window.show()
    app.exec_()


class Error(QtGui.QMainWindow, error_class):
    def __init__(self, msg, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
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
        except IOError:
            errorbox = QtGui.QMessageBox(self)
            errorbox.setWindowTitle("Error")
            errorbox.setText("Can not send email.")
            errorbox.exec_()


def excepthook2(exc_type, exc_value, tracebackobj):
    separator = '-' * 80
    log_file = "Error.log"
    version_info = "NR"
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S")

    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(exc_type), str(exc_value))
    sections = [separator, time_string, separator, errmsg, separator, tbinfo, separator, "Version: " + version_info,
                "Os: " + platform.system(), "Architecture: " + platform.architecture()[0], separator]
    msg = '\n'.join(sections)
    try:
        f = open(log_file, "w")
        f.write(msg)
        f.close()
    except IOError:
        pass
    main_window = Error2(msg)
    main_window.exec_()


class Error2(QtGui.QDialog, error_class):
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
