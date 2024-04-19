import datetime
import json
import traceback

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QTextBrowser, QLineEdit, QPushButton, QComboBox, QMessageBox
import threading

import utils
import cryptography_techniques.shift as shift
import cryptography_techniques.vigenere as vigenere
import cryptography_techniques.rsa as RSA
import cryptography_techniques.difhel as difhel

TECHNIQUES_MAP = {
    "Shift": "shift",
    "Vigenere": "vigenere",
    "RSA": "RSA",
    "DifHel": "DifHel"
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

        self.server_message_technique_box.currentIndexChanged.connect(self.message_technique_on_change)
        self.send_server_message_button.clicked.connect(self.send_server_message)

        self.server_message_count = 0
        self.server_message = None
        self.processing_message = False
        self.message_queue = []
        self.queued_message = None



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
                if message and not self.processing_message:
                    print("Processing received message")
                    self.process_message(message)
                elif message:
                    self.message_queue.append(message)
                    print("Message queued")
                elif len(self.message_queue) > 0 and not self.processing_message:
                    self.queued_message = self.message_queue.pop(0)
                    print("Processing queued message")
                    self.process_message(self.queued_message)



        except Exception as e:
            print(traceback.format_exc())

    def process_message(self, message):
        self.processing_message = True
        header, message_type, length = utils.get_header_message_type_lenght_from_message(message)
        print(f"Header: {header}, Message type: {message_type}, Length: {length}")
        message = self.socket.recv(length * 4)
        if message_type == "t":
            print(f"Received public message bytes: {message}")
            try:
                try:
                    message_content = message.decode('utf-8')
                except UnicodeDecodeError as e:
                    message_content = message.decode('utf-32be')
            except Exception as e:
                message_content = "⚠️ The message couldn't be displayed ⚠️"
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
            print("Finished processing public message")
        elif message_type == "s":

            self.server_message = message
            self.server_message_count += 1

            print(f"Received server message bytes: {message}")
            try:
                try:
                    message_content = message.decode('utf-8')
                except UnicodeDecodeError as e:
                    message_content = message.decode('utf-32be')
            except Exception as e:
                message_content = "⚠️ The message couldn't be displayed ⚠️"

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
            print("Finished processing server message")
        self.processing_message = False


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
            if message_technique == "DifHel":
                message = f"task {TECHNIQUES_MAP[message_technique]}"
            else:
                if not message_operation:
                    QMessageBox.critical(self, "Server message Error", "Please select an operation")
                    return
                elif not message_length or not message_length.isdigit() or not int(message_length) > 0 or not int(message_length) < 10000:
                    QMessageBox.critical(self, "Server message Error", "Please enter a valide length (0 < length < 10000)")
                    return
                else:
                    message = f"task {TECHNIQUES_MAP[message_technique]} {message_operation.lower()} {message_length}"

            if message_technique == "Vigenere" and message_operation == "Decode":
                QMessageBox.critical(self, "Server message Error", "Vigenere decoding is currently not supported")
                return
            print(f"Sending server message : {message}")
            packet = utils.get_text_packet_from_message_string("s", message)
            print(f"Packet: {packet}")
            self.socket.send(packet)

            self.server_message_count = 0

            if message_technique == "Shift" or message_technique == "Vigenere":
                if message_operation == "Encode":
                    while self.server_message_count != 1:
                        pass

                    message_string = self.server_message.decode("utf-8")
                    message_string_striped = message_string.replace(chr(0), "")
                    print(f"Received message : {message_string_striped}")
                    encoding_key = message_string_striped[
                                   message_string_striped.find("shift-key ") + len("shift-key "):]
                    print(f"Received key : {encoding_key}")

                    while self.server_message_count != 2:
                        pass

                    message_to_encode = self.server_message

                    if message_technique == "Shift":
                        encoded_message_bytes = shift.encode_bytes_message(message_to_encode, int(encoding_key))
                    else:
                        encoded_message_bytes = vigenere.encode_bytes_message(message_to_encode, encoding_key)
                    packet = utils.get_text_packet_from_message_bytes("s", encoded_message_bytes)
                    self.socket.send(packet)
                elif message_operation == "Decode":
                    if message_technique == "Shift":
                        while self.server_message_count != 2:
                            pass
                        key_e, decrypted_message_e, key_space, decrypted_message_space = shift.decrypt(self.server_message)
                        print(f"Decrypted message e : {decrypted_message_e}")
                        print(f"Decrypted message space : {decrypted_message_space}")
                        if decrypted_message_e != "":
                            self.server_chat_message_browser.append(f"Decoded message : {decrypted_message_e}")
                            self.socket.send(utils.get_text_packet_from_message_string("s", str(key_e)))
                        elif decrypted_message_space != "":
                            self.server_chat_message_browser.append(f"Decoded message : {decrypted_message_space}")
                            self.socket.send(utils.get_text_packet_from_message_string("s", str(key_space)))
            elif message_technique == "RSA":
                if message_operation == "Encode":
                    while self.server_message_count != 1:
                        pass

                    message_string = self.server_message.decode("utf-8")
                    message_string_striped = message_string.replace(chr(0), "")

                    e = int(message_string_striped[message_string_striped.find("e=") + len("e="):])
                    n = message_string_striped[message_string_striped.find("n=") + len("n="):]
                    n = n.split(',')[0]
                    n = int(n)

                    while self.server_message_count != 2:
                        pass

                    encoded_message_bytes = RSA.encode_bytes_message(self.server_message, e, n)
                    packet = utils.get_text_packet_from_message_bytes("s", encoded_message_bytes)
                    self.socket.send(packet)
                elif message_operation == "Decode":
                    while self.server_message_count != 1:
                        pass
                    n, e, k = RSA.get_n_e_k()
                    print(f"Generated n : {n}, e : {e}, k : {k}")
                    packet = utils.get_text_packet_from_message_string("s", f"{n},{e}")
                    self.socket.send(packet)

                    while self.server_message_count != 2:
                        pass
                    decoded_message_bytes = RSA.decode(self.server_message, n, e, k)
                    packet = utils.get_text_packet_from_message_bytes("s", decoded_message_bytes)
                    self.socket.send(packet)
            elif message_technique == "DifHel":
                p, g = difhel.get_p_g()
                print(f"Generated p : {p}, g : {g}")
                packet = utils.get_text_packet_from_message_string("s", f"{p},{g}")
                self.socket.send(packet)
                while self.server_message_count != 3:
                    pass

                message_string = self.server_message.decode("utf-8")
                message_string_striped = message_string.replace(chr(0), "")
                server_half_key = int(message_string_striped)
                print(f"Received server half key : {server_half_key}")

                b, half_key = difhel.get_half_key(p, g)
                print(f"Generated half key : {half_key}")

                packet = utils.get_text_packet_from_message_string("s", str(half_key))
                self.socket.send(packet)

                while self.server_message_count != 4:
                    pass

                shared_key = difhel.get_shared_key(server_half_key, b, p)
                print(f"Computed shared key : {shared_key}")
                packet = utils.get_text_packet_from_message_string("s", str(shared_key))
                self.socket.send(packet)


        except Exception as e:
            print(traceback.format_exc())

    def message_technique_on_change(self):
        if self.server_message_technique_box.currentText() == "DifHel":
            self.server_message_operation_box.setEnabled(False)
            self.server_message_input.setEnabled(False)
        else:
            self.server_message_operation_box.setEnabled(True)
            self.server_message_input.setEnabled(True)



