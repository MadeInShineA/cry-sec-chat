import math
import random

import numpy as np

import utils

def get_n_e_k():
    """
    Returns n e and k used for the decoding
    :return n: int
    :return e: int
    """
    with open("primes_to_2_32.bin", "rb") as file:
        primes = file.readlines()[0]
        primes_array = [primes[i:i+6] for i in range(0, len(primes), 6)]
        primes_array = [int.from_bytes(prime, "little") for prime in primes_array]

        p_index = random.randint(0, len(primes_array))

        p = primes_array[p_index]
        q = primes_array[random.randint(0, len(primes_array) - 1)]

        while p == 2 and q == 2:
            p = primes_array[p_index]
            q = primes_array[random.randint(0, len(primes_array) - 1)]

        n = p * q
        k = (p - 1) * (q - 1)

        e = primes_array[random.randint(0, p_index - 1)]
        while math.gcd(e, k) != 1:
            e = int(primes_array[random.randint(0, p_index - 1)])

        file.close()

    return n, e, k


def encode_bytes_message(message, e, n):
    """
    Encode the bytes message using the RSA encoding
    :param message: bytes
    :param e: int
    :param n: int
    :return: bytearray
    """
    res = bytearray()
    message_4_bytes_array = utils.message_to_4_bytes_array(message)
    for four_bytes in message_4_bytes_array:
        z = utils.modular_pow(int.from_bytes(four_bytes), e, n)
        encode_char_bytes = z.to_bytes(4, "big")
        res += encode_char_bytes
    return res


def extended_euclide_alg(e, k):
    """
    :param e: int
    :param k: int
    :return: int, int, int
    """
    if k == 0:
        return e, 1, 0
    else:
        d, u, v = extended_euclide_alg(k, e % k)
        return d, v, u - v * (e // k)


def decode(message, n, e, k):
    """

    :param message: bytes
    :param n: int
    :param e: int
    :param k: int
    :return: bytearray
    """
    d, u, v = extended_euclide_alg(e, k)
    if u < 0:
        u += k
    res = bytearray()
    message_4_bytes_array = utils.message_to_4_bytes_array(message)

    for four_byte in message_4_bytes_array:
        res += utils.modular_pow(int.from_bytes(four_byte), u, n).to_bytes(4, byteorder="big")

    return res


if __name__ == '__main__':
    pass