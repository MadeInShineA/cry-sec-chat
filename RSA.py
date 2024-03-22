import math
import random

import numpy as np

from utils import message_to_4_bytes_array

PRIME_BYTE_SIZE = 6


def modular_pow(base, exponent, modulo):
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


def store_primes():
    """
    Store primes number between 1 to n number in a .bin file
    The bytes are stored in little endian

    :return: filname.bin
    """
    max_value = int(math.pow(2, 32))
    prime_numbers = get_primes(max_value)
    with open("primes.bin", "wb") as file:
        for prime in prime_numbers:
            prime_bytes = prime.tobytes()
            stripped_prime_bytes = prime_bytes[:PRIME_BYTE_SIZE]

            # Warning, the bytes are stored in little endian
            file.write(stripped_prime_bytes)


def get_primes(n):
    """
    :param n: Int
    :return: list
    """
    sieve = np.ones(n // 3 + (n % 6 == 2), dtype=bool)
    for i in range(1, int(n ** 0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[k * k // 3::2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = False
    return np.r_[2, 3, ((3 * np.nonzero(sieve)[0][1:] + 1) | 1)]


def get_n_e_k():
    """
    :return n: Int
    :return e: Int
    """
    with open("primes.bin", "rb") as file:
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
            e = int(primes_array[random.randint(0, p_index)])

        file.close()

    return n, e, k




def encode_bytes_message(message, key_e, key_n):
    res = bytearray()
    message_4_bytes_array = message_to_4_bytes_array(message)
    for four_bytes in message_4_bytes_array:
        z = modular_pow(int.from_bytes(four_bytes), key_e, key_n)
        encode_char_bytes = z.to_bytes(4, "big")
        res += encode_char_bytes
    return res

def extended_euclide_alg(e, k):
    if k == 0:
        return e, 1, 0
    else:
        d, u, v = extended_euclide_alg(k, e % k)
        return d, v, u - v * (e // k)




def decode(message, n, e, k):
    d, u, v = extended_euclide_alg(e, k)
    if u < 0:
        u += k
    res = bytearray()
    message_4_bytes_array = message_to_4_bytes_array(message)

    for four_byte in message_4_bytes_array:
        res += modular_pow(int.from_bytes(four_byte), u, n).to_bytes(4, byteorder="big")

    return res


if __name__ == '__main__':
    pass