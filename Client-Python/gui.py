import sys
from PyQt4 import QtGui, uic

main_class = uic.loadUiType("ui/main.ui")[0]
server_list_class = uic.loadUiType("ui/serverList.ui")[0]
add_server_class = uic.loadUiType("ui/addServer.ui")[0]


class Main(QtGui.QMainWindow, main_class):

    def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)  # Run gui init
		self.setupUi(self)  # Setup Ui
		self.server_list = server_list(self)  # Load server list
		self.server_list.show()  # Show server list

    def chatUpdate(self):
        pass

    def send(self):
        pass

    def closeEvent(self, event):
        pass

    def connectToServer(self):
        pass


class server_list(QtGui.QDialog, server_list_class):

	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)  # Run gui init
		self.setupUi(self)  # Setup Ui
		# Create buttons
		self.addButton = QtGui.QPushButton()
		self.editButton = QtGui.QPushButton()
		self.cancelButton = QtGui.QPushButton()
		self.connectButton = QtGui.QPushButton()
		# Set button Text
		self.addButton.setText("Add New...")
		self.editButton.setText("Edit...")
		self.cancelButton.setText("Cancel")
		self.connectButton.setText("Connect")
		# Add buttons to box
		self.buttonBox.addButton(self.addButton, QtGui.QDialogButtonBox.ActionRole)
		self.buttonBox.addButton(self.editButton, QtGui.QDialogButtonBox.DestructiveRole)
		self.buttonBox.addButton(self.cancelButton, QtGui.QDialogButtonBox.RejectRole)
		self.buttonBox.addButton(self.connectButton, QtGui.QDialogButtonBox.AcceptRole)
		# Connect buttons
		self.addButton.clicked.connect(self.add)

	def add(self):
		self.add_server = add_server(self)  # Load GUI
		self.add_server.exec_()  # Run GUI


class add_server(QtGui.QDialog, add_server_class):

	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)  # Run gui init
		self.setupUi(self)  # Setup Ui
