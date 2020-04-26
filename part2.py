"""
File: part2.py
Created by Andrew Ingson (aings1@umbc.edu)
Date: 4/26/2020
CMSC 4-- (CLASS NAME)

"""
import random
import math
import gmpy2


# algorithm adapted from the pollard rho notes
def pollard_rho(n):
    i = 1
    initial = random.randint(0, n - 1)
    y = initial
    k = 2
    previous = initial
    while True:
        i += 1
        current = gmpy2.powmod(previous, 2, n)
        d = math.gcd(y - current, n)
        if d != 1 and d != n:
            return d
        if i == k:
            y = current
            k = 2 * k
        previous = current


def break_primes(n):
    # check to see if the primes were the same
    n_sqrt = math.sqrt(n)
    if n_sqrt % 1 == 0.0:
        print("Duplicate primes detected")
        return n_sqrt

    return pollard_rho(n)


def main():
    print("#####   Part 2   #####")
    n = 1504522304890037877025707358625209
    print("Attempting to find factors of", n)
    pol_res = break_primes(n)
    print("Factor of n:")
    print(pol_res)


if __name__ == "__main__":
    main()
