import math
import random

import numpy as np

from utils import message_to_4_bytes_array


def get_primes():
    with open("../primes.bin", "rb") as file:
        primes = file.readlines()[0]
        primes_array = [primes[i:i + 6] for i in range(0, len(primes), 6)]
        primes_array = [int.from_bytes(prime, "little") for prime in primes_array]
        file.close()

    return primes_array, primes


primes_array = get_primes()[0]


def isPrime(g, t=0):
    if g == 0 or g == 1:
        return False
    if g == 3:
        return True
    if g % primes_array[t] == 0:
        return False
    isPrime(g, t + 1)


def get_random_p():
    """
    Returns the modular word
    :return: Int
    """
    p_index = random.randint(0, len(primes_array))

    p = primes_array[p_index]

    while p == 2 or p > 5000:
        p = primes_array[random.randint(0, len(primes_array))]
    return p


def get_line_primes(g):
    for i in primes_array:
        if primes_array[i] < g:
            p = primes_array[i]
            return p


def get_prime_factors(g):
    """
    Find all prime factors of g
    :param g: Int
    :return: Array of Int
    """
    dividend_array = []
    prime = get_line_primes(g)
    prime_array = []

    while prime >= g or g % prime != 0:
        prime = get_line_primes(g)

    for i in prime_array:
        if not isPrime(g):
            prime_array = prime_array.append(prime)
            get_prime_factors(g / prime)

        if prime_array[i] == prime_array[i + 1]:
            prime_array = prime_array.pop(i + 1)

        dividend_array = g / prime_array[i]

    return prime_array, dividend_array, prime


def test_prime(g):
    """
    test if g is primitive root
    :param g: Int
    :return: boolean
    """
    ret = []
    prime_array, dividends_array, primes = get_prime_factors(g)

    for i in prime_array:
        for j in dividends_array:
            if math.pow(prime_array[i], dividends_array[j] % primes != 1) and dividends_array[
                len(dividends_array) == dividends_array[j]]:
                ret.append(prime_array[i])

    return ret


def generate_g():
    """
    Generate primitive root modulo
    :return: Int
    """
    prime = get_random_p()
    g = prime - 1
    test_prime(g)


if __name__ == '__main__':
    print(generate_g())
