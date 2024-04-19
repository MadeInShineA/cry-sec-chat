import math
from socket import *

import numpy as np
from PIL import Image


SERVER_ADDRESS = "vlbelintrocrypto.hevs.ch"
SERVER_PORT = 6000
MAGIC_BYTES = "ISC".encode("utf-8")
PRIME_BYTE_SIZE = 6


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

def modular_pow(base, exponent, modulo):
    """

    :param base: int
    :param exponent: int
    :param modulo: int
    :return: int
    """
    if modulo == 1:
        return 0
    base = base % modulo
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulo
        exponent = exponent >> 1
        base = (base * base) % modulo
    return result

def store_primes(   ):
    """
    Store primes number between 1 to n number in a .bin file
    The bytes are stored in little endian

    :return: none
    """
    max_value = int(math.pow(2, 32))
    prime_numbers = get_primes(max_value)
    with open("primes_to_2_32.bin", "wb") as file:
        for prime in prime_numbers:
            prime_bytes = prime.tobytes()
            stripped_prime_bytes = prime_bytes[:PRIME_BYTE_SIZE]

            # Warning, the bytes are stored in little endian
            file.write(stripped_prime_bytes)


def get_primes(n):
    """
    Returns an array of primes from 1 to 2^n
    :param n: int
    :return: array
    """
    sieve = np.ones(n // 3 + (n % 6 == 2), dtype=bool)
    for i in range(1, int(n ** 0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[k * k // 3::2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
    return np.r_[2, 3, ((3 * np.nonzero(sieve)[0][1:] + 1) | 1)]


if __name__ == '__main__':
    with open("primes_to_5000.txt", "r") as file:
        primes = file.readlines()
        primes_array = [int(prime) for prime in primes]
        file.close()
    print(primes_array)
    with open("primes_to_5000.bin", "wb") as file:
        for prime in primes_array:
            prime_bytes = prime.to_bytes(PRIME_BYTE_SIZE, "little")
            stripped_prime_bytes = prime_bytes[:PRIME_BYTE_SIZE]

            # Warning, the bytes are stored in little endian
            file.write(stripped_prime_bytes)