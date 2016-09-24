from PyQt4 import QtGui, uic

addServer_class = uic.loadUiType("ui/addServer.ui")[0]


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
