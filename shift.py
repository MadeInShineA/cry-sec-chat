import utils


def encode(message, key):
    res = ""
    for char in message:
        res += chr(ord(char) + key)
    return res


def decode(message, key):
    res = ""
    for char in message:
        res += chr(ord(char) - key)
    return res


def decrypt(message):
    """
    : param message: bytes
    : return: int
    """

    frequency_map = {}
    message_4_bytes_array = utils.message_to_4_bytes_array(message)
    for four_bytes in message_4_bytes_array:
        if four_bytes in frequency_map.keys():
            frequency_map[four_bytes] += 1
        else:
            frequency_map[four_bytes] = 1


if __name__ == '__main__':
    # print(decode(encode("ñ", 1), 1))
    decrypt(b'\x00\x00\x00U\x00\x00\x00n\x00\x00\x00i\x00\x00\x00c\x00\x00\x00o\x00\x00\x00d\x00\x00\x00e\x00\x00\x00D\x00\x00\x00e\x00\x00\x00c\x00\x00\x00o\x00\x00\x00d\x00\x00\x00e\x00\x00\x00E\x00\x00\x00r\x00\x00\x00r\x00\x00\x00o\x00\x00\x00r')


