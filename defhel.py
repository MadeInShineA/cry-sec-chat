import math
import random

import numpy as np

from utils import message_to_4_bytes_array


def get_p():
    """
    Returns the modular word
    :return: Int
    """
    with open("primes.bin", "rb") as file:
        primes = file.readlines()[0]
        primes_array = [primes[i:i + 6] for i in range(0, len(primes), 6)]
        primes_array = [int.from_bytes(prime, "little") for prime in primes_array]

        p_index = random.randint(0, len(primes_array))

        p = primes_array[p_index]

        while p == 2 or p > 5000:
            p = primes_array[p_index]

        file.close()

    return p


def g_prime_factors(g):
    """
    Find all prime factors of g
    :param g: Int
    :return: Array of Int
    """
    global divident_array
    prime = get_p()
    prime_array = np.empty()
    if g % prime == 0:
        prime_array = np.append(prime_array, prime)
        g_prime_factors(g / prime)
    for i in prime_array:
        if prime_array[i] == prime_array[i + 1]:
            prime_array = np.delete(prime_array, ([i + 1]))
        divident_array = g / prime_array[i]
    return prime_array, divident_array


def test_prime(g):
    """
    test if g is primitive root
    :param g: Int
    :return: boolean
    """
    prime = get_p()
    prime_array, dividents_array = g_prime_factors(g)
    for i in prime_array:
        for j in dividents_array:
            if math.pow(prime_array[i], dividents_array[j] % prime != 1):
                j+1

            else: i+1


def generate_g():
    """
    Generate primitive root modulo
    :return: Int
    """
    prime = get_p()
    g = prime - 1


if __name__ == '__main__':
    print(get_p())
