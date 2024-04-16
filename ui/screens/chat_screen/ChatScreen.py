import traceback

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTextBrowser, QLineEdit, QPushButton
import threading

import utils


class ChatScreen(QWidget):
    def __init__(self, socket):
        super().__init__()
        self.window = uic.loadUi('ui/screens/chat_screen/ChatScreen.ui')

        self.socket = socket
        self.public_chat_message_browser = self.window.findChild(QTextBrowser, "publicChatBrowser")
        self.public_message_input = self.window.findChild(QLineEdit, "publicMessageInput")
        self.send_public_message_button = self.window.findChild(QPushButton, "sendPublicMessageButton")

        self.server_chat_message_browser = self.window.findChild(QTextBrowser, "serverChatBrowser")
        self.server_message_input = self.window.findChild(QLineEdit, "serverMessageInput")
        self.server_public_message_button = self.window.findChild(QPushButton, "sendServerMessageButton")

        self.send_public_message_button.clicked.connect(self.send_public_message)

        # Start the thread for receiving messages
        self.message_thread = threading.Thread(target=self.receive_message)
        self.message_thread.start()




    def send_public_message(self):
        try:
            message = self.public_message_input.text()
            packet = utils.get_text_packet_from_message_string("t", message)
            self.socket.send(packet)
            self.public_message_input.clear()
        except Exception as e:
            print(traceback.format_exc())

    def receive_message(self):
        try:
            while True:
                message = self.socket.recv(6)
                if message:
                    print(f"Received message : {message}")
                    header, message_type, length = utils.get_header_message_type_lenght_from_message(message)
                    print(f"Header: {header}, Message type: {message_type}, Length: {length}")
                    if message_type == "t":
                        message = self.socket.recv(length * 4)
                        print(f"Received message bytes: {message}")
                        self.public_chat_message_browser.append(f"Received message : {message.decode('utf-8')}")
        except Exception as e:
            print(traceback.format_exc())




