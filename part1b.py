"""
File: part1b.py
Created by Andrew Ingson (aings1@umbc.edu)
Date: 4/26/2020
CMSC 4-- (CLASS NAME)

"""
import random


def euclidean(a, b):
    # check for base case
    if b == 0:
        return a, 1, 0
    else:
        # swap things around recursively
        d_p, x_p, y_p = euclidean(b, a % b)
        d, x, y = d_p, y_p, x_p - (a // b) * y_p
        return d, x, y


def pollard_rho(n):
    i = 1
    initial = random.randint(0, n - 1)
    y = initial
    k = 2
    previous = initial
    while True:
        i += 1
        current = (previous ** 2) % n
        d, x_1, y_1 = euclidean(y - current, n)
        if d != 1 and d != n:
            return d
        if i == k:
            y = current
            k = 2 * k
        previous = current


def main():
    print("#####   Part 1B   #####")
    n = 23701
    pol_res = pollard_rho(n)
    print("Factor of n:")
    print(pol_res)


if __name__ == "__main__":
    main()
