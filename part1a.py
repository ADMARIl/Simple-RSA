"""
File: part1a.py
Created by Andrew Ingson (aings1@umbc.edu)
Date: 4/22/2020
CMSC 441 Intro to Algorithms
Notes: The pdf on the RSA steps seems to be very helpful

"""
import random
import gmpy2

PRIME = True
COMPOSITE = False
E_EXPO = 65537


def euclidean(a, b):
    # check for base case
    if b == 0:
        return a, 1, 0
    else:
        d_p, x_p, y_p = euclidean(b, a % b)
        d, x, y = d_p, y_p, x_p - (a // b) * y_p
        return d, x, y


# Miller-Rabin as it is shown in the book (pg 970)
def mr_test(n, s):
    # print(n, s)
    for j in range(1, s):
        # random
        a = random.randint(1, n - 1)
        if witness(a, n):
            # This is supposed to return COMPOSITE but idk what that's supposed to be
            return COMPOSITE
    return PRIME


# adapted from the pseudo code from page 969 in the book
def witness(a, n):
    # calculate t
    t = 1
    sub_n = (n - 1) >> 1
    while (sub_n & 1) != 0:
        sub_n = sub_n >> 1
        t += 1

    u = (n - 1) // (2 ** t)
    # print("T and U are be", t, u)

    x = gmpy2.powmod(a, u, n)

    previous = x
    current = x
    for i in range(t):
        # current is x_i
        # previous is x_i - 1
        current = (previous ** 2) % n
        if current == 1 and previous != 1 and previous != n - 1:
            return True
        previous = current
    if current != 1:
        return True
    return False


def getPrime(size, s):
    # Generate RSA primes
    curr_prime = random.randint((2 ** (size - 1)), (2 ** size) - 1)
    # print(prime1)
    if curr_prime & 1 == 0:
        curr_prime += 1
    while mr_test(curr_prime, s) != PRIME:
        # print("incrementing prime by 2")
        curr_prime += 2

    return curr_prime


def publicKey(size):
    s = 50
    primeP = getPrime(size // 2, s)
    primeQ = getPrime(size // 2, s)
    print("---- BEGIN PUBLIC KEY ----")
    print(E_EXPO, end="")
    print(", ", end='')
    print(primeP * primeQ)
    print("---- END PUBLIC KEY ----")


def main():
    print("#####   Part 1A   #####")
    bits = int(input("Enter your desired modulus size: "))
    print("Modulus size of", bits, "bits selected.")

    # Generate RSA primes
    publicKey(bits)


if __name__ == "__main__":
    main()
