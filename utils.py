from socket import *
from PIL import Image


SERVER_ADDRESS = "vlbelintrocrypto.hevs.ch"
SERVER_PORT = 6000
MAGIC_BYTES = "ISC".encode("utf-8")

def message_to_4_bytes_array(message):
    """
    :param message: bytes
    :return: byte array
    """
    return [message[i:i+4] for i in range(0, len(message), 4)]


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


def get_text_packet_from_message_string(connection_type, message):
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

def get_header_message_type_lenght_from_message(message):
    print(f"Message {message}")
    header = message[:3].decode("utf-8")
    message_type = chr(message[3])
    length = int.from_bytes(message[4:6])
    return header, message_type, length

def get_message_bytes_from_message(message, length):
    return message[6:6+length]

def split_received_message(message):
    try:
        header = message[:3].decode("utf-8")
        message_type = chr(message[3])
        length = int.from_bytes(message[4:6])
        message_bytes = message[6:]

        return header, message_type, length, message_bytes
    except Exception as e:
        print(f"Erreur lors du décodage du message {message} \n {e}")