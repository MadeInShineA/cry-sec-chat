from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTextBrowser, QLineEdit, QPushButton


class ChatScreen(QWidget):
    def __init__(self, socket):
        super().__init__()
        self.window = uic.loadUi('ui/screens/chat_screen/ChatScreen.ui')

        self.socket = socket
        self.public_chat_message_browser = self.window.findChild(QTextBrowser, "publicChatBrowser")
        self.public_message_input = self.window.findChild(QLineEdit, "publicMessageInput")
        self.send_public_message_button = self.window.findChild(QPushButton, "sendPublicMessageButton")

        self.private_chat_message_browser = self.window.findChild(QTextBrowser, "privateChatBrowser")
        self.private_message_input = self.window.findChild(QLineEdit, "privateMessageInput")
        self.private_public_message_button = self.window.findChild(QPushButton, "sendPrivateMessageButton")


