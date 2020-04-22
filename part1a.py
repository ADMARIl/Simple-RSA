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


def euclidean(a, b):
    print(a, b)


# Miller-Rabin as it is shown in the book
def mr_test(n, s):
    # print(n, s)
    for j in range(1, s):
        # random
        a = random.randint(1, n - 1)
        if witness(a, n):
            # This is supposed to return COMPOSITE but idk what that's supposed to be
            return False
    return PRIME


# adapted from the pseudo code from page 969 in the book
def witness(a, n):
    # calculate t
    t = 1
    sub_n = (n-1) >> 1
    while (sub_n & 1) != 0:
        sub_n = sub_n >> 1
        t += 1

    u = (n-1)//(2**t)
    # print("T and U are be", t, u)

    x = gmpy2.powmod(a, u, n)

    previous = x
    current = x
    for i in range(t):
        # current is x_i
        # previous is x_i - 1
        current = (previous ** 2) % n
        if current == 1 and previous != 1 and previous != n-1:
            return True
        previous = current
    if current != 1:
        return True
    return False


def main():
    print("#####   Part 1A   #####")
    bits = 2048 # int(input("Enter your desired modulus size: "))
    print("Modulus size of", bits, "bits selected.")

    # Generate RSA primes
    s = 10
    prime1 = random.randint(2, (2 ** bits) - 1)
    # print(prime1)
    if prime1 & 1 == 0:
        prime1 += 1
    while mr_test(prime1, s) != PRIME:
        # print("incrementing prime by 2")
        prime1 += 2
    print("Calculated", bits, "bit prime:")
    print(prime1)


if __name__ == "__main__":
    main()
