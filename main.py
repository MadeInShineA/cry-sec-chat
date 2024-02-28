from socket import *
import inspect

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
    connection_type = input("Enter you connection type t/i/s\n")
    while connection_type not in CONNECTION_TYPES:
        connection_type = input("Enter you connection type t/i/s\n")
    message = None
    packet = None
    match connection_type:
        case "t" | "s":
            # Handle the case when the connection type is t => text
            if connection_type == "t":
                message = get_text_message()
            else:
                # Handle the case when the connection type is s => server
                # We need to ask the user for the command and the arguments as long as they are not conformed to what the server expects
                while connection_type == "s" and message is None:
                    print("Here are the allowed commands for the s type :")
                    # Print the allowed commands and their arguments (using the inspect module to get the source code of the lambda functions)
                    for(allowed_command, allowed_arguments) in ALLOWED_COMMANDS_ARGUMENTS.items():
                        print(f"\t{allowed_command}", end=" ")
                        for arg in allowed_arguments:
                            if callable(arg):
                                # Print the source code of the lambda function without the new line character and the comma in case it's not the last argument
                                print(inspect.getsourcelines(arg)[0][0].strip(" ").replace("\n", "").replace(",", ""), end=" ")
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
            packet = get_text_packet(connection_type, message)
        case "i":
            image = get_image_message()
            packet = get_image_packet(connection_type, image)
    s.send(packet)
    print("Message sent")
    while True:
        message = s.recv(1024)
        if message:
            print("Message received")
            header, type, length, message = split_received_message(message)
            print(f"Received header : {header}")
            print(f"Received type : {type}")
            print(f"Received length : {length}")
            print(f"Received message : {message}")


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
        # char_bytes = char.encode("utf-32be")
        char_bytes = char.encode("utf-8")
        padding_needed = 4 - len(char_bytes)
        char_bytes = b"\x00" * padding_needed + char_bytes
        packet += char_bytes

    return packet


def get_image_packet(connection_type, image):
    packet = bytearray()
    packet += MAGIC_BYTES
    packet += connection_type.encode("utf-8")

    return packet


def split_received_message(message):
    # message = message.decode("utf-8")
    header = message[:3].decode("utf-8")
    type = chr(message[3])
    length = int.from_bytes(message[4:6])
    message = message[6:].decode("utf-8")
    return header, type, length, message



if __name__ == "__main__":
    main()

