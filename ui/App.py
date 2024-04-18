from socket import socket
import traceback

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

from ui.screens.connection_screen.ConnectionScreen import ConnectionScreen
from ui.screens.chat_screen.ChatScreen import ChatScreen

SERVER_ADDRESS = "vlbelintrocrypto.hevs.ch"
SERVER_PORT = "6000"


class App(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.connectionScreen = ConnectionScreen(SERVER_ADDRESS, SERVER_PORT)
        self.connectionScreen.set_connect_function(self.connectToServer)
        self.window = self.connectionScreen.window
        self.window.show()

        self.socket = socket()
        self.chatScreen = None

    def connectToServer(self):
        try:
            print("Connecting to server")
            server_address = self.connectionScreen.server_address.text()
            port = int(self.connectionScreen.server_port.text())
            self.socket.connect((server_address, port))
            print("Connected to server")
            self.window.close()

            self.chatScreen = ChatScreen(socket=self.socket)
            self.window = self.chatScreen.window
            self.window.show()

        except ValueError as e:
            QMessageBox.critical(self.connectionScreen, "Connection Error", "Invalid IP Address or Port")
            self.connectionScreen.server_address.setFocus()

        except Exception as e:
            print(traceback.format_exc())
            QMessageBox.critical(self.connectionScreen, "Connection Error", "Could not connect to the server")
            self.connectionScreen.server_address.setFocus()
