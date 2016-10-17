from PyQt4 import QtGui, uic

from AddServer import AddServer
from CreateUser import CreateUser
from Login import Login
from os import path

serverList_class = uic.loadUiType(path.join(path.dirname(path.realpath(__file__)), "ui/serverList.ui"))[0]


class ServerList(QtGui.QDialog, serverList_class):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)  # Run gui init
        self.setupUi(self)  # Setup Ui
        # Defining variables
        self.socket = parent.socket
        self.onMsgFound = None
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
        self.socket.msgFound.connect(self.msg_found)
        # Load servers from array
        for i, _ in self.servers.items():
            self.items[i] = QtGui.QTreeWidgetItem((i, "", ""))
            self.serversL.addTopLevelItems([self.items[i]])

    def msg_found(self):
        self.onMsgFound()

    def runInMain(self):
        for command, args in self.thread2.commands:
            command(*args)
            self.thread2.commands.remove((command, args))

    def cancel(self):
        self.close()

    def connectToServer(self):
        if len(self.serversL.selectedItems()) > 0:  # If item is selected
            key = str(self.serversL.selectedItems()[0].text(0))  # Get the key
            self.socket.connect(str(self.servers[key][0]), str(self.servers[key][1]))  # Try to connect
            self.socket.waitTillMessage(0)
            self.onMsgFound = self._after_connect
            self.username = str(self.servers[key][2])

    def _after_connect(self):
        self.socket.send(0, self.username)
        self.onMsgFound = self._new_vs_non
        self.socket.waitTillMessage(3, 1)

    def _login(self):
        self.login = Login(self.username, self)  # Load GUI
        self.login.exec_()  # Run GUI
        if self.login.tryPass:
            self.socket.send(0, self.login.username)
            self.onMsgFound = self._send_login_pass
            self.username = self.login.username
            self.socket.waitTillMessage(1, 3)

    def _send_login_pass(self):
        if self.socket.waited_for[0][0] == 1:
            if self.login.password:
                self.socket.send(1, self.login.password)
                self.onMsgFound = self._cheking_pass
                self.socket.waitTillMessage(1)
        else:
            self.makeUser = CreateUser(self)
            self.makeUser.exec_()
            if self.makeUser.makeUser:
                self._make_user()

    def _cheking_pass(self):
        if self.socket.waited_for[1][0] == "Correct":
            self.close()
        else:
            msgbox = QtGui.QMessageBox(self)
            msgbox.setText("Incorrect Username or Password.")
            msgbox.exec_()
            self._login()

    def _new_vs_non(self):
        if self.socket.waited_for[0][0] == 1:
            self._login()
        else:
            self.makeUser = CreateUser(self)
            self.makeUser.exec_()
            if self.makeUser.makeUser:
                self._make_user()

    def _make_user(self):
        self.login = Login(self.username, self)  # Load GUI
        self.login.exec_()  # Run GUI
        if self.login.tryPass:
            self.socket.send(0, self.login.username)
            self.onMsgFound = self._send_yes_make
            self.socket.waitTillMessage(3)

    def _send_yes_make(self):
        self.close()
        self.socket.send(3, "y")
        self.onMsgFound = self._send_pass_make
        self.socket.waitTillMessage(1)

    def _send_pass_make(self):
        self.socket.send(1, self.login.password)

    def add(self):
        self.addServer = AddServer("", "", "8000", "", False, self)  # Load GUI
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
        f = open("~/servers.csv", "w")  # Open file for writing
        for i, j in self.servers.items():  # Loop though array
            f.write(str(i) + "," + str(j[0]) + "," + str(j[1]) + "," + str(j[2]) + "\n")  # Save to file
        f.close()  # Close file
