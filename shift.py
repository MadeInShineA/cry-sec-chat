import math

import utils

MOST_FREQUENT_LANGUAGE_LETTER = 'e'
COUNTER = 0

# TODO encode_bytes_message
def encode(message, key):
    """
    :param message: Byte
    :param key: Int
    :return: String
    """
    res = ""
    for char in message:
        res += chr(ord(char) + key)
    return res


def decode_from_bytes(message, key):
    res = ""
    for byte in message:
        if byte != 0:
            res += chr(byte - key)
    return res


def decode_from_string(message, key):
    res = ""
    for char in message:
        if char != "":
            res += chr(ord(char) - key)
    return res


def decode_from_4_bytes_array(message_4_bytes_array, key):
    res = ""
    for four_bytes in message_4_bytes_array:
        decoded_char = int.from_bytes(four_bytes) - key
        res += decoded_char.to_bytes(math.ceil(decoded_char.bit_length() / 8), 'big').decode('utf-8')

    return res


def decode(message, key):
    if isinstance(message, bytes):
        return decode_from_bytes(message, key)
    elif isinstance(message, str):
        return decode_from_string(message, key)
    elif isinstance(message, list):
        return decode_from_4_bytes_array(message, key)


def decrypt(message):
    """
    :param message: bytes
    :return: int
    """

    frequency_map = {}
    message_4_bytes_array = utils.message_to_4_bytes_array(message)
    for four_bytes in message_4_bytes_array:
        if four_bytes in frequency_map.keys():
            frequency_map[four_bytes] += 1
        else:
            frequency_map[four_bytes] = 1
    frequency_map = {k: v for k, v in sorted(frequency_map.items(), key=lambda item: item[1], reverse=True)}
    most_frequent_4_bytes = list(frequency_map.keys())[0]

    key_e = int.from_bytes(most_frequent_4_bytes) - ord('e')
    print(f"The e key is : {key_e}")

    if key_e >= 0:
        try:
            message_e = decode(message_4_bytes_array, key_e)
        except UnicodeDecodeError as e:
            print(f"Unicode error while trying to decode message_e \n\t{e}")
            message_e = ""
            pass
        except OverflowError as e:
            print(f"OverflowError trying to decode message_e\n\t{e}\nThe message is probably too short to be decoded")
            message_e = ""

    else:
        message_e = ""

    key_space = int.from_bytes(most_frequent_4_bytes) - ord(' ')
    print(f"The space key is : {key_space}")

    if key_space >= 0:
        try:
            message_space = decode(message_4_bytes_array, key_space)
        except UnicodeDecodeError as e:
            print(f"Unicode error while trying to decode message_space\n\t{e}")
            message_space = ""
        except OverflowError as e:
            print(f"OverflowError trying to decode message_space\n\t{e}\nThe message is probably too short to be decoded")
            message_space = ""
    else:
        message_space = ""

    return key_e, message_e, key_space, message_space


if __name__ == '__main__':
    print(decode(encode("ñ", 1), 1))
    print(decode([b"\x00\xc3\xb4"], 3))

