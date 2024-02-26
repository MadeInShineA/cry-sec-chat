from socket import *

SERVER_ADDRESS = "vlbelintrocrypto.hevs.ch"
SERVER_PORT = 6000
MAGIC_BYTES = "ISC".encode("utf-8")
CONNECTION_TYPES = ["t", "s", "i"]
ALLOWED_COMMANDS = ["task", "pipi"]


def main():
    s = connect()
    connection_type = input("Enter you connection type t/i/s\n")
    while connection_type not in CONNECTION_TYPES:
        connection_type = input("Enter you connection type t/i/s\n")
    message = None
    packet = None
    match connection_type:
        case "t" | "s":
            if connection_type == "t":
                message = get_text_message()
            else:
                while connection_type == "s" and message not in ALLOWED_COMMANDS:
                    print(f"Here are the allowed commands for the s type :\n\t- {"\n\t- ".join(ALLOWED_COMMANDS)}")
                    message = get_text_message()
            packet = get_text_packet(connection_type, message)
        case "i":
            image = get_image_message()
            packet = get_image_packet(connection_type, image)
    s.send(packet)
    print("Message sent")
    # while True:
    #     message = s.recv
    #     if message:
    #        header, type, message = split_received_message(message)




def connect():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((SERVER_ADDRESS, SERVER_PORT))
    return s


def get_image_message():
    return ""


def get_text_message():
    message = input("Enter your message\n")
    return message

# def split_received_message(message):
#     header = message
# TODO faire fonction pour recevoir messages serveurs


def get_text_packet(connection_type, message):

    packet = bytearray()
    packet += MAGIC_BYTES
    packet += connection_type.encode("utf-8")
    packet += len(message).to_bytes(2, byteorder="big")

    for char in message:
        char_bytes = char.encode("utf-32be")
        packet += char_bytes
#regarder pour faire utf-8 big endian
    print(packet)
    return packet




def get_image_packet(connection_type, image):
    return ""


if __name__ == "__main__":
    main()

