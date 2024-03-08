from socket import *
import inspect
from PIL import Image

import shift
import vigenere

# from skimage.transform import resize
# import matplotlib.pyplot as plt

SERVER_ADDRESS = "vlbelintrocrypto.hevs.ch"
SERVER_PORT = 6000
MAGIC_BYTES = "ISC".encode("utf-8")
CONNECTION_TYPES = ["t", "s", "i"]
ALLOWED_COMMANDS_ARGUMENTS = {
    "task": [
        ["shift", "vigenere", "RSA"],
        ["encode", "decode"],
        lambda x: 0 < int(x) < 10000,
    ]
}


def main():
    s = connect()
    message_counter = 0
    message_type = input("Enter you connection type t/i/s\n")
    while message_type not in CONNECTION_TYPES:
        message_type = input("Enter you connection type t/i/s\n")
    message = None
    packet = None
    match message_type:
        case "t" | "s":
            # Handle the case when the connection type is t => text
            if message_type == "t":
                message = get_text_message()
            else:
                # Handle the case when the connection type is s => server
                """
                We need to ask the user for the command and the arguments
                as long as they are not conformed to what the server expects
                """
                while message_type == "s" and message is None:
                    print("Here are the allowed commands for the s type :")
                    """
                    Print the allowed commands and their arguments
                    (using the inspect module to get the source code of the lambda functions)
                    """
                    for (allowed_command, allowed_arguments) in ALLOWED_COMMANDS_ARGUMENTS.items():
                        print(f"\t{allowed_command}", end=" ")
                        for arg in allowed_arguments:
                            if callable(arg):
                                """
                                # Print the source code of the lambda function without the new line character
                                and the comma in case it's not the last argument
                                """
                                print(inspect.getsourcelines(arg)[0][0].strip(" ").replace("\n", "").replace(",", ""),
                                      end=" ")
                            else:
                                print(f"{arg}", end=" ")
                        # Print a new line character to break the " " end argument and go to the next line
                        print()
                    # Ask the user for the command and the arguments
                    message = get_text_message()
                    command = message.split(" ")[0]
                    # Check if the command is allowed
                    if command not in ALLOWED_COMMANDS_ARGUMENTS.keys():
                        print("Command not allowed")
                        message = None
                    else:
                        arguments = message.split(" ")[1:]
                        # Check if the number of arguments is correct
                        if len(arguments) != len(ALLOWED_COMMANDS_ARGUMENTS[command]):
                            print("Wrong number of arguments")
                            message = None
                        else:
                            for i, arg in enumerate(arguments):
                                # Check if the argument is callable (a lambda function)
                                if callable(ALLOWED_COMMANDS_ARGUMENTS[command][i]):
                                    if not ALLOWED_COMMANDS_ARGUMENTS[command][i](arg):
                                        print(f"Argument not allowed : {arg}")
                                        message = None
                                # Check if the argument is in the allowed arguments
                                elif arg not in ALLOWED_COMMANDS_ARGUMENTS[command][i]:
                                    print(f"Argument not allowed : {arg}")
                                    message = None
            packet = get_text_packet(message_type, message)
        case "i":
            image = get_image_message()
            packet = get_image_packet(message_type, image)
    s.send(packet)
    print("Message sent")
    while True:
        message = s.recv(1024)
        if message:
            print("Message received")
            header, message_type, length, message_bytes = split_received_message(message)
            print(f"Received header : {header}")
            print(f"Received type : {message_type}")
            print(f"Received length : {length}")
            print(f"Received message bytes: {message_bytes}")

            # TODO Upgrade the way of handling server's messages handling (atm only works for s shift decrypt
            if message_counter == 0 and message_type == "s":
                message_string = message_bytes.decode("utf-8")
                message_string_striped = message_string.replace(chr(0), "")
                print(f"Received message : {message_string_striped}")
                message_counter += 1

                encoding_key = message_string_striped[message_string_striped.find("shift-key ") + len("shift-key "):]
                print(f"Received key : {encoding_key}")
            elif message_counter == 1:

                # Shift decode
                # key_e, decrypted_message_e, key_space, decrypted_message_space = shift.decrypt(message_bytes)
                # print(f"Decrypted message e : {decrypted_message_e}")
                # print(f"Decrypted message space : {decrypted_message_space}")
                # if decrypted_message_e != "":
                #     s.send(get_text_packet("s", str(key_e)))
                # elif decrypted_message_space != "":
                #     s.send(get_text_packet("s", str(key_space)))

                # Shift encode
                #
                # encoded_message_bytes = shift.encode_bytes_message(message_bytes, int(encoding_key))
                # packet = get_text_packet_from_message_bytes("s", encoded_message_bytes)
                # print(packet)
                # s.send(packet)


                # Vigenere encode
                encoded_message_bytes = vigenere.encode_bytes_message(message_bytes, encoding_key)
                packet = get_text_packet_from_message_bytes("s", encoded_message_bytes)
                print(packet)
                s.send(packet)
                message_counter = 0





def connect():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((SERVER_ADDRESS, SERVER_PORT))
    return s


def get_image_message():
    message = input("Enter your image path\n")
    return message


def get_text_message():
    message = input("Enter your message\n")
    return message


def get_text_packet(connection_type, message):
    packet = bytearray()
    packet += MAGIC_BYTES
    packet += connection_type.encode("utf-8")
    packet += len(message).to_bytes(2, byteorder="big")

    for char in message:
        # Encode the char in utf-8 on 4 bytes in big endian
        char_bytes = char.encode("utf-8")
        padding_needed = 4 - len(char_bytes)
        char_bytes = b"\x00" * padding_needed + char_bytes
        packet += char_bytes
        """
        # packet += len(char_bytes).to_bytes(4, byteorder="big")
        # le serveur se sert de la taille des charactères pour décoder le message
        # il va lire les 4 bytes du premier char et en se basant sur le len du char,
        # il reconnait le char, en gros, ça facilite le décryptage du côté du serveur
        """
    return packet


def get_text_packet_from_message_bytes(connection_type, message):
    packet = bytearray()
    packet += MAGIC_BYTES
    packet += connection_type.encode("utf-8")
    packet += (len(message) // 4).to_bytes(2, byteorder="big")

    packet += message
    return packet


def get_image_packet(connection_type, image):
    packet = bytearray()
    packet += MAGIC_BYTES
    packet += connection_type.encode("utf-8")
    # reading of an image from the path
    im = Image.open(image)
    # resizing of the image while keeping dimensions
    im.thumbnail((128, 128))
    width, height = im.size
    packet += width.to_bytes(2, "little")
    packet += height.to_bytes(2, "little")
    # recupering RGB code for each pixels
    # pixels = im.load()
    rgb_im = im.convert('RGB')
    for line in range(width):
        for col in range(height):
            red, green, blue = rgb_im.getpixel((line, col))
            """
            Divmod divise les valeurs de rouge, vert et bleu par 256, le résultat devient le byte de point fort
                et le reste devient le byte de point faible.
            Le résultat est ensuite transformer en bytearray via une boucle for qui convertit chaques
                valeurs en byte.
            """
            r, g1 = divmod(red, 256)
            r, g2 = divmod(green, 256)
            packet = bytes([int(b) for b in (r, g2, g1, blue)])

    return packet


def split_received_message(message):
    try:
        header = message[:3].decode("utf-8")
        message_type = chr(message[3])
        length = int.from_bytes(message[4:6])
        message_bytes = message[6:]

        return header, message_type, length, message_bytes
    except Exception as e:
        print(f"Erreur lors du décodage du message {message} \n {e}")


if __name__ == "__main__":
    main()

