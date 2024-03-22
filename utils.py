def message_to_4_bytes_array(message):
    """
    :param message: bytes
    :return: byte array
    """
    return [message[i:i+4] for i in range(0, len(message), 4)]
