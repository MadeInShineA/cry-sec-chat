from socket import *

SERVER_ADDRESS = "vlbelintrocrypto.hevs.ch"
SERVER_PORT = 6000
MAGIC_BYTES = bytearray("ISC", "utf-8")


def main():
    s = connect()
    connection_type = input("Enter you connection type t/i/s\n")
    while connection_type not in ["t", "s", "i"]:
        connection_type = input("Enter you connection type t/i/s\n")
    message = None
    match connection_type:
        case "t" | "s":
            message = get_text_message()
            packet = get_text_packet(connection_type, message )
        case "i":
            image = get_image_message()
            packet = get_image_packet(connection_type, image)



def connect():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((SERVER_ADDRESS, SERVER_PORT))
    return s


def get_image_message():
    return ""


def get_text_message():
    message = input("Enter your message\n")
    return message


def get_text_packet(connection_type, message):
    header = MAGIC_BYTES + bytearray(connection_type, "utf-8") + bytearray(message.len(), "utf-8").reverse()
    char_byte_array = []

    # TODO
    for char in bytearray(message, "utf-8"):
        pass

    return ""




def get_image_packet(connection_type, image):
    return ""


if __name__ == "__main__":
    main()

