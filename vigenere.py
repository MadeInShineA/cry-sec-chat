import math

from utils import message_to_4_bytes_array


def encode_bytes_message(message, key):
    """
    :param message: byte
    :param key: String
    :return: bytearray
    """
    res = bytearray()
    key_index = 0
    message_4_bytes_array = message_to_4_bytes_array(message)
    for four_bytes in message_4_bytes_array:
        encoded_char_int = int.from_bytes(four_bytes) + ord(key[key_index])

        # print(f"Encoded 4 bytes {four_bytes} ")
        # print(f"Encoded 4 bytes int {int.from_bytes(four_bytes)} ")
        # print(f"Key char {key[key_index]}")
        # print(f"Ord Key char {ord(key[key_index])}")

        encoded_char_bytes = encoded_char_int.to_bytes(4, byteorder="big")
        # print(f"Encoded char bytes {encoded_char_bytes}")


        res += encoded_char_bytes
        if key_index < len(key) - 1:
            key_index += 1
        else:
            key_index = 0
    return res



if __name__ == '__main__':
    pass