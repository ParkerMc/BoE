from PyQt4 import QtGui, uic
from os import path

main_class = uic.loadUiType("ui/main.ui")[0]
serverList_class = uic.loadUiType("ui/serverList.ui")[0]
addServer_class = uic.loadUiType("ui/addServer.ui")[0]


class Main(QtGui.QMainWindow, main_class):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)  # Run gui init
		self.setupUi(self)  # Setup Ui
		self.servers = {}  # Array for servers
		if path.isfile("servers.csv"):  # If server file exists
			f = open("servers.csv", "r")  # Open file for reading
			data = f.readlines()  # Read file
			f.close()  # Close file
			for i in data:  # Loop though line
				j = i.split(",")  # Split at the ,'s

				self.servers[j[0]] = (j[1], j[2], j[3])  # Add to array
		self.serverList = ServerList(self)  # Load server list
		self.serverList.show()  # Show server list

	def chatUpdate(self):
		pass

	def send(self):
		pass

	def closeEvent(self, event):
		pass

	def connectToServer(self):
		pass


class ServerList(QtGui.QDialog, serverList_class):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)  # Run gui init
		self.setupUi(self)  # Setup Ui
		# Defining variables
		self.addServer = None
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
		# Load servers from array
		for i, j in self.parent().servers.items():
			self.servers.addTopLevelItems([QtGui.QTreeWidgetItem((i, "", ""))])

	def add(self):
		self.addServer = AddServer("", "", "", "", self)  # Load GUI
		self.addServer.exec_()  # Run GUI
		if self.addServer.saved:  # If save
			self.servers.addTopLevelItems([QtGui.QTreeWidgetItem((self.addServer.data[0], "", ""))])  # Add to list
			self.parent().servers[self.addServer.data[0]] = (self.addServer.data[1], self.addServer.data[2], self.addServer.data[3])  # Add to array
			f = open("servers.csv", "w")  # Open file for writing
			for i, j in self.parent().servers.items():  # Loop though array
				f.write(str(i) + "," + str(j[0]) + "," + str(j[1]) + "," + str(j[2]) + "\n")  # Save to file
			f.close()  # Close file


class AddServer(QtGui.QDialog, addServer_class):
	def __init__(self, server_name, address, port, username, parent=None):
		QtGui.QDialog.__init__(self, parent)  # Run gui init
		self.setupUi(self)  # Setup Ui
		# Defining variables
		self.data = None
		self.saved = False  # If user clicks ok
		# Set fields
		self.name.setText(server_name)
		self.ip.setText(address)
		self.port.setText(port)
		self.username.setText(username)
		self.buttonBox.accepted.connect(self.save)  # Connect button to return data

	def save(self):
		self.saved = True  # Save data on return
		# noinspection PyPep8
		self.data = (str(self.name.text()), str(self.ip.text()), str(self.port.text()),
					str(self.username.text()))  # Get data for saving
		self.close()
