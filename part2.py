"""
File: part2.py
Created by Andrew Ingson (aings1@umbc.edu)
Date: 4/26/2020
CMSC 441 (Design and Analysis of Algorithms)

"""
import random
import gmpy2
import threading


class WorkThread(threading.Thread):
    def __init__(self, ID, n):
        threading.Thread.__init__(self)
        self.threadID = ID
        self.n = n

    def run(self):
        print(self.threadID, ":", break_primes(self.n))


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
        d = gmpy2.gcd(y - current, n)
        if d != 1 and d != n:
            return d
        if i == k:
            y = current
            k = 2 * k
        previous = current


# algorithm adapted from the p-1 notes
def pollard_p1(n):
    i = 1
    bound = 2
    while True:
        i += 1
        bound = gmpy2.powmod(bound, i, n)
        d = gmpy2.gcd(bound - 1, n)
        if d != 1 and d != n:
            return d


def break_primes(n):
    # check to see if the primes were the same
    gmpy2.get_context().precision = 4096
    n_sqrt = gmpy2.sqrt(n)
    if n_sqrt % 1 == 0.0:
        print("Duplicate primes detected!")
        return n_sqrt

    return pollard_p1(n)


def main():
    print("#####   Part 2   #####")
    n = 14421421868825429441
    gmpy2.get_context().precision = 4096
    print("Attempting to find factors of", n)

    thread1 = WorkThread(1, n)
    thread2 = WorkThread(2, n)

    thread1.start()
    thread2.start()

    # pol_res = break_primes(n)
    # print("Factor of n:")
    # print(pol_res)


if __name__ == "__main__":
    main()
