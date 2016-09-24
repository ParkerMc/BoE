from os import path

from PyQt4 import QtGui, uic

from serverMGR import Socket

main_class = uic.loadUiType("ui/main.ui")[0]
serverList_class = uic.loadUiType("ui/serverList.ui")[0]
addServer_class = uic.loadUiType("ui/addServer.ui")[0]
login_class = uic.loadUiType("ui/login.ui")[0]
createUser_class = uic.loadUiType("ui/createuser.ui")[0]


class Main(QtGui.QMainWindow, main_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)  # Run gui init
        self.setupUi(self)  # Setup Ui
        self.socket = Socket()
        self.servers = {}  # Array for servers
        if path.isfile("servers.csv"):  # If server file exists
            f = open("servers.csv", "r")  # Open file for reading
            data = f.readlines()  # Read file
            f.close()  # Close file
            for i in data:  # Loop though line
                if i != "":
                    j = i.replace("\n", "").split(",")  # Split at the ,'s
                    self.servers[j[0]] = (j[1], j[2], j[3])  # Add to array
        self.serverList = ServerList(self)  # Load server list
        self.serverList.show()  # Show server list
        # Connect buttons
        self.actionConnect.triggered.connect(self.connectToServer)
        self.actionDisconnect.triggered.connect(self.socket.disconnect)
        self.actionQuit.triggered.connect(self.close)
        self.socket.newMsg.connect(self.chatUpdate)
        self.sendB.clicked.connect(self.send)
        self.text.returnPressed.connect(self.send)

    def chatUpdate(self):
        ids, messages = self.socket.getMessages(5)
        for i in messages:
            self.chatBox.append(str(i))

    def send(self):
        if self.text.text() == "quit":
            self.socket.disconnect()
        elif self.text.text() != "":
            self.socket.send(5, str(self.text.text()))
            self.text.setText("")

    def closeEvent(self, event):
        self.socket.disconnect()

    def connectToServer(self):
        self.serverList = ServerList(self)  # Load server list
        self.serverList.show()  # Show server list


class ServerList(QtGui.QDialog, serverList_class):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)  # Run gui init
        self.setupUi(self)  # Setup Ui
        # Defining variables
        self.socket = parent.socket
        self.addServer = None
        self.login = None
        self.makeUser = None
        self.servers = parent.servers
        self.items = {}
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
        self.editButton.clicked.connect(self.edit)
        self.connectButton.clicked.connect(self.connectToServer)
        self.cancelButton.clicked.connect(self.cancel)
        # Load servers from array
        for i, j in self.servers.items():
            self.items[i] = QtGui.QTreeWidgetItem((i, "", ""))
            self.serversL.addTopLevelItems([self.items[i]])

    def cancel(self):
        self.close()

    def connectToServer(self):
        if len(self.serversL.selectedItems()) > 0:  # If item is selected
            key = str(self.serversL.selectedItems()[0].text(0))  # Get the key
            self.socket.connect(str(self.servers[key][0]), str(self.servers[key][1]))  # Try to connect
            ids, messages = self.socket.waitTillMessage(0)
            self.socket.send(0, str(self.servers[key][2]))
            ids, messages = self.socket.waitTillMessage(3, 1)
            if ids[0] == 1:
                while True:
                    self.login = Login(str(self.servers[key][2]), False, self)  # Load GUI
                    self.login.exec_()  # Run GUI
                    if self.login.tryPass:
                        self.socket.send(0, self.login.username)
                        ids, messages = self.socket.waitTillMessage(1)
                        self.socket.send(1, self.login.password)
                        ids, messages = self.socket.waitTillMessage(1)
                        if messages[0] == "Correct":
                            self.close()
                            ids, messages = self.socket.waitTillMessage(4)
                            for i in messages:
                                self.parent().chatBox.append(str(i))
                            break
                        else:
                            msgbox = QtGui.QMessageBox(self)
                            msgbox.setText("Incorrect Username or Password.")
                            msgbox.exec_()
                    else:
                        break
            else:
                self.makeUser = CreateUser(self)
                self.makeUser.exec_()
                if self.makeUser.makeUser:
                    while True:
                        self.login = Login(str(self.servers[key][2]), True, self)  # Load GUI
                        self.login.exec_()  # Run GUI
                        if self.login.tryPass:
                            self.socket.send(0, self.login.username)
                            ids, messages = self.socket.waitTillMessage(3)
                            self.close()
                            self.socket.send(3, "y")
                            ids, messages = self.socket.waitTillMessage(1)
                            self.socket.send(1, self.login.password)
                            ids, messages = self.socket.waitTillMessage(4)
                            for i in messages:
                                self.parent().chatBox.append(str(i))
                            break


    def add(self):
        self.addServer = AddServer("", "", "", "", False, self)  # Load GUI
        self.addServer.exec_()  # Run GUI
        if self.addServer.saved:  # If save
            self.items[self.addServer.data[0]] = QtGui.QTreeWidgetItem((self.addServer.data[0], "", ""))  # Set item
            self.serversL.addTopLevelItems([self.items[self.addServer.data[0]]])  # add Item
            self.save()

    def edit(self):
        if len(self.serversL.selectedItems()) > 0:  # If item is selected
            key = str(self.serversL.selectedItems()[0].text(0))  # Get the key
            self.addServer = AddServer(key, self.servers[key][0], self.servers[key][1], self.servers[key][2], True,
                                       self)  # Load GUI
            self.addServer.exec_()  # Run GUI
            if self.addServer.saved:  # If save
                if key != self.addServer.data[0]:
                    del self.servers[key]
                    self.items[self.addServer.data[0]] = self.items[key]
                    del self.items[key]
                    self.items[self.addServer.data[0]].setText(0, self.addServer.data[0])
                self.save()

    def save(self):
        self.servers[self.addServer.data[0]] = (
            self.addServer.data[1], self.addServer.data[2], self.addServer.data[3])  # Add to array
        f = open("servers.csv", "w")  # Open file for writing
        for i, j in self.servers.items():  # Loop though array
            f.write(str(i) + "," + str(j[0]) + "," + str(j[1]) + "," + str(j[2]) + "\n")  # Save to file
        f.close()  # Close file


class AddServer(QtGui.QDialog, addServer_class):
    def __init__(self, server_name, address, port, username, edit, parent=None):
        QtGui.QDialog.__init__(self, parent)  # Run gui init
        self.setupUi(self)  # Setup Ui
        # Defining variables
        self.servers = parent.servers
        self.oldName = server_name
        self.data = None
        self.saved = False  # If user clicks ok
        # Set fields
        self.name.setText(server_name)
        self.ip.setText(address)
        self.port.setText(port)
        self.username.setText(username)
        self.buttonBox.accepted.connect(self.save)  # Connect button to return data
        # Connect Text change
        self.name.textChanged.connect(self.change)
        self.ip.textChanged.connect(self.change)
        self.port.textChanged.connect(self.change)
        self.username.textChanged.connect(self.change)
        self.buttonBox.buttons()[0].setEnabled(edit)  # Turn off button ot leave on

    def change(self):
        if str(self.name.text()).strip() != "" and str(self.ip.text()).strip() != "" and str(
                self.port.text()).strip() != "" and str(self.username.text()).strip() != "":  # If all fields are filled
            if str(self.name.text()) not in self.servers.keys() or str(
                    self.name.text()) == self.oldName:  # If new name or not used name
                self.buttonBox.buttons()[0].setEnabled(True)  # Turn on button
            else:
                self.buttonBox.buttons()[0].setEnabled(False)  # Turn off button
        else:
            self.buttonBox.buttons()[0].setEnabled(False)  # Turn off button

    def save(self):
        self.saved = True  # Save data on return
        # noinspection PyPep8
        self.data = (str(self.name.text()), str(self.ip.text()), str(self.port.text()),
                     str(self.username.text()))  # Get data for saving
        self.close()  # Close dialog


class Login(QtGui.QDialog, login_class):
    def __init__(self, username, enabled, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.password = None
        self.username = username
        self.user.setText(username)
        self.user.setEnabled(enabled)
        self.Login.clicked.connect(self.login)
        self.tryPass = False

    def login(self):
        self.tryPass = True
        self.password = str(self.passwd.text())
        self.username = str(self.user.text())
        self.close()


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
