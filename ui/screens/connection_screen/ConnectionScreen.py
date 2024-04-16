from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton


class ConnectionScreen(QWidget):
    def __init__(self, address, port):
        super().__init__()
        self.window = uic.loadUi('ui/screens/connection_screen/ConnectionScreen.ui')
        self.server_address = self.window.findChild(QLineEdit, "serverAddress")
        self.server_port = self.window.findChild(QLineEdit, "serverPort")

        self.server_address.setText(address)
        self.server_port.setText(port)

        self.connection_button = self.window.findChild(QPushButton, "connectionButton")

    def set_connect_function(self, function):
        self.connection_button.clicked.connect(function)




