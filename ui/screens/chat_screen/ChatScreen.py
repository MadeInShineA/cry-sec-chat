import datetime
import json
import traceback

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTextBrowser, QLineEdit, QPushButton, QComboBox, QMessageBox
from cryptography_techniques.shift import server_message_encode
import threading

import utils

TECHNIQUES_MAP = {
    "Shift" : "shift",
    "Vigenere" : "vigenere",
    "RSA" : "RSA",
    "DifHel" : "DifHel"
}


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
        self.send_server_message_button = self.window.findChild(QPushButton, "sendServerMessageButton")

        self.server_message_technique_box = self.window.findChild(QComboBox, "serverMessageTechniqueBox")
        self.server_message_operation_box = self.window.findChild(QComboBox, "serverMessageOperationBox")

        self.send_public_message_button.clicked.connect(self.send_public_message)

        self.message_thread = threading.Thread(target=self.receive_message)
        self.message_thread.start()

        self.load_chat_messages()
        self.load_server_messages()

        self.send_server_message_button.clicked.connect(self.send_server_message)



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
                    header, message_type, length = utils.get_header_message_type_lenght_from_message(message)
                    print(f"Header: {header}, Message type: {message_type}, Length: {length}")
                    message = self.socket.recv(length * 4)
                    if message_type == "t":
                        print(f"Received public message bytes: {message}")
                        message_content = message.decode('utf-8')
                        message_datetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                        self.public_chat_message_browser.append(f"{message_datetime} : {message_content}")
                        with open("public_messages.json", "r+") as f:
                            f.seek(0, 2)
                            f.seek(f.tell() - 2, 0)
                            if f.read(1) == "[":
                                f.seek(f.tell() - 1, 0)
                                f.write("[\n")
                                json.dump({"datetime": message_datetime, "content": message_content}, f, indent=0)
                                f.write("\n]")
                            else:
                                f.seek(f.tell() - 2, 0)
                                f.write(",\n")
                                json.dump({"datetime": message_datetime, "content": message_content}, f, indent=0)
                                f.write("\n]")
                    elif message_type == "s":
                        # print(f"Received server message bytes: {message}")
                        message_content = message.decode('utf-8')
                        message_datetime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

                        self.server_chat_message_browser.append(f"{message_datetime} : {message_content}")

                        with open("server_messages.json", "r+") as f:
                            f.seek(0, 2)
                            f.seek(f.tell() - 2, 0)
                            if f.read(1) == "[":
                                f.seek(f.tell() - 1, 0)
                                f.write("[\n")
                                json.dump({"datetime": message_datetime, "content": message_content}, f, indent=0)
                                f.write("\n]")
                            else:
                                f.seek(f.tell() - 2, 0)
                                f.write(",\n")
                                json.dump({"datetime": message_datetime, "content": message_content}, f, indent=0)
                                f.write("\n]")

        except Exception as e:
            print(traceback.format_exc())


    def load_chat_messages(self):
        try:
            with open("public_messages.json", "r") as f:
                messages = json.load(f)
                for message in messages:
                    self.public_chat_message_browser.append(f"{message["datetime"]} : {message["content"]}")
        except Exception as e:
            print(traceback.format_exc())


    def load_server_messages(self):
        try:
            with open("server_messages.json", "r") as f:
                messages = json.load(f)
                for message in messages:
                    self.server_chat_message_browser.append(f"{message["datetime"]} : {message["content"]}")
        except Exception as e:
            print(traceback.format_exc())


    def send_server_message(self):
        try:
            message_technique = self.server_message_technique_box.currentText()
            message_operation = self.server_message_operation_box.currentText()
            message_length = self.server_message_input.text()

            if not message_technique:
                QMessageBox.critical(self, "Server message Error", "Please select a technique")
                return
            elif message_technique != "DifHel":
                if not message_operation:
                    QMessageBox.critical(self, "Server message Error", "Please select an operation")
                    return
                elif not message_length:
                    QMessageBox.critical(self, "Server message Error", "Please enter a length")
                    return

            message = f"task {TECHNIQUES_MAP[message_technique]} {str.lower(message_operation)} {message_length}"
            print(f"Sending server message : {message}")
            packet = utils.get_text_packet_from_message_string("s", message)
            self.socket.send(packet)

        except Exception as e:
            print(traceback.format_exc())




