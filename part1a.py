"""
File: part1a.py
Created by Andrew Ingson (aings1@umbc.edu)
Date: 4/22/2020
CMSC 441 Intro to Algorithms
Notes: Run the program in a python 3 environment in order to build

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


def getKeys(size):
    # calculate primes
    s = 50
    primeP = getPrime(size // 2, s)
    primeQ = getPrime(size // 2, s)
    # calculate public key
    n = primeP * primeQ
    print("---- BEGIN PUBLIC KEY ----")
    print("(", E_EXPO, end="")
    print(", ", end='')
    print(n, ")")
    print("---- END PUBLIC KEY ----")
    # calculate private key
    calc_gcd, ex, ny = euclidean(E_EXPO, (primeP-1)*(primeQ-1))
    d = ex
    # d = int(d)
    print("---- BEGIN PRIVATE KEY ----")
    print("(", d, end="")
    print(", ", end='')
    print(n, ")")
    print("---- END PRIVATE KEY ----")
#    print("\n\n")
#    print(d*E_EXPO)
#    print(1 % ((primeP-1) * (primeQ - 1)))

    return n, d


def main():
    print("#####   Part 1A   #####")
    bits = int(input("Enter your desired modulus size: "))
    print("Modulus size of", bits, "bits selected.")

    # Generate RSA primes
    n, d = getKeys(bits)

    message = "I deserve an A"
    print("Before encrypt:", message)
    x = 0
    for c in message:
        x = x << 8
        x = x ^ ord(c)

    # message_num = 4
    #  print(x)
    c = gmpy2.powmod(x, E_EXPO, n)
    print("C:", c)
    m = gmpy2.powmod(c, d, n)
    # print("M:", m)

    print(x)
    print(m)
    if m == x:
        print("RSA Successful!")


if __name__ == "__main__":
    main()
