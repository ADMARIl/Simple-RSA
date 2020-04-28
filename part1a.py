"""
File: part1a.py
Created by Andrew Ingson (aings1@umbc.edu)
Date: 4/22/2020
CMSC 441 (Design and Analysis of Algorithms)
Notes: Run the program in a python 3 environment in order to build

"""
import random
import gmpy2
import math

PRIME = True
COMPOSITE = False
E_EXPO = 65537


# extended euclidean from class notes
def euclidean(a, b):
    # check for base case
    if b == 0:
        return a, 1, 0
    else:
        # swap things around recursively
        d_p, x_p, y_p = euclidean(b, a % b)
        d, x, y = d_p, y_p, x_p - (a // b) * y_p
        return d, x, y


# Miller-Rabin as it is shown in the book (pg 970)
def mr_test(n, s):
    # check for primality s number of times
    for j in range(1, s):
        # random
        a = random.randint(1, n - 1)
        if witness(a, n):
            # Return this is a isn't prime
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
    # calculate U
    u = (n - 1) // (2 ** t)
    # print("T and U are be", t, u)
    # modular exponentiation
    x = gmpy2.powmod(a, u, n)
    # calculate prime likely hood
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


# algorithm adapted from the p-1 notes
def pollard_p1(n):
    B = n ** (1/6)
    a = 2
    for i in range(2, math.floor(B)):
        a = gmpy2.powmod(a, i, n)
        d = gmpy2.gcd(a - 1, n)
        if d > 1:
            return d
    return 1


def getPrime(size, s):
    # Generate RSA primes
    curr_prime = random.randint((2 ** (size - 1)), (2 ** size) - 1)
    # print(prime1)
    # check if its even
    if curr_prime & 1 == 0:
        curr_prime += 1
    # keep incrementing by 2 till we reach a prime
    while not gmpy2.is_prime(curr_prime) or mr_test(curr_prime, s) != PRIME:
        # print("incrementing prime by 2")
        curr_prime += 2
    # poll = pollard_p1(curr_prime)
    # if ((curr_prime - 1) // poll) < poll:
      #  return getPrime(size, s)

    return curr_prime


def getKeys(size):
    # calculate primes
    s = 50
    primeP = getPrime(size // 2, s)
    primeQ = getPrime(size // 2, s)
    # check that primes aren't equal
    while primeP == primeQ:
        primeQ = getPrime(size // 2, s)
    # calculate public key
    n = primeP * primeQ
    phi = (primeP - 1) * (primeQ - 1)
    print("---- BEGIN PUBLIC KEY ----")
    print("(", E_EXPO, end="")
    print(", ", end='')
    print(n, ")")
    print("---- END PUBLIC KEY ----")
    # calculate private key
    calc_gcd, ex, ny = euclidean(E_EXPO, (primeP - 1) * (primeQ - 1))
    # make sure d is positive
    d = ex % phi
    print("---- BEGIN PRIVATE KEY ----")
    print("(", d, end="")
    print(", ", end='')
    print(n, ")")
    print("---- END PRIVATE KEY ----")

    return n, d


def main():
    print("#####   Part 1A   #####")
    bits = int(input("Enter your desired modulus size (has to be greater than size of message): "))
    print("Modulus size of", bits, "bits selected.")

    # Generate RSA primes
    n, d = getKeys(bits)

    # numberify message
    message = "I deserve an A"
    print("Before encrypt:", message)

    x = 0
    for c in message:
        x = x << 8
        x = x ^ ord(c)
    print("Message int:", x)

    # encrypt the message
    c = gmpy2.powmod(x, E_EXPO, n)
    print("Encrypted signature:", c)
    # decrypt the message
    m = gmpy2.powmod(c, d, n)
    # print("M:", m)

    # print(x)
    # print(m)
    if m == x:
        print("RSA Successful!")
    else:
        print("This shouldn't ever be reached")
        if bits < 112:
            print("Error likely because", bits, "is less than the size of the message")


if __name__ == "__main__":
    main()
