import random

from utils import message_to_4_bytes_array


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


def primesInRange():
    prime_list = []
    for n in range(2**31, 2**32):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)
            print(prime_list)

    return prime_list


def keys_creation():
    prime_list = primesInRange()
    n = random.choice(prime_list)
    e = random.choice(prime_list)

    print(f"key n: {n}, key e: {e}")


def encode_bytes_message(message, key_e, key_n):
    res = bytearray()
    message_4_bytes_array = message_to_4_bytes_array(message)
    for four_bytes in message_4_bytes_array:
        z = modular_pow(int.from_bytes(four_bytes), key_e, key_n)
        encode_char_bytes = z.to_bytes(4, "big")
        res += encode_char_bytes
    return res


def decode():
    pass


if __name__ == '__main__':
    print(keys_creation())