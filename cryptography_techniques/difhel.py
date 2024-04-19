import math
import random

import numpy as np

import utils
from utils import modular_pow


def get_primes():
    with open("primes_to_5000.bin", "rb") as file:
        primes = file.readlines()[0]
        primes_array = [primes[i:i + 6] for i in range(0, len(primes), 6)]
        primes_array = [int.from_bytes(prime, "little") for prime in primes_array]
        file.close()

    return primes_array


def get_prime_factors(prime_array, n):
    """
    Find all prime factors of g
    :param n: Int
    :return: Set of Int
    """
    prime_factors = set()
    prime_index = 0

    while n != 1:
        if n % prime_array[prime_index] == 0:
            prime_factors.add(prime_array[prime_index])
            n = n / prime_array[prime_index]
        else:
            prime_index += 1

    return prime_factors


def get_p_g():
    """
    Generate the primitive root modulo of n
    :return: Int
    """
    prime_array = get_primes()
    p = random.choice(prime_array)
    prime_factors = get_prime_factors(prime_array, p-1)

    a_values = [(p-1) // prime for prime in prime_factors]

    g = 1
    while True:
        if all(modular_pow(g, a, p) != 1 for a in a_values):
            return p, g
        g += 1

def get_half_key(p, g):
    b = math.ceil(random.random() * 100)
    return b, utils.modular_pow(g, b, p)


def get_shared_key(server_half_key, b, p):
    return utils.modular_pow(server_half_key, b, p)

if __name__ == '__main__':
    print(get_prime_factors(97 - 1))
    # print(generate_g())