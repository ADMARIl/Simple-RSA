"""
File: part2.py
Created by Andrew Ingson (aings1@umbc.edu)
Date: 4/26/2020
CMSC 441 (Design and Analysis of Algorithms)

"""
import random
import gmpy2
import multiprocessing
import math

FOUND = 0
PROCESS_COUNT = 24
PROCESSES = []

processLock = multiprocessing.Lock()


# algorithm adapted from the pollard rho notes
def pollard_rho(n, process_id):
    i = 1
    processLock.acquire()
    initial = process_id + 2  # this could also be random.randomint(0, n - 1)
    print("CORE", process_id, "checking rho of", initial)
    processLock.release()
    y = initial
    k = 2
    previous = initial
    while True:
        i += 1
        current = ((pow(previous, 2)) - 1) % n  # gmpy2.powmod(previous, 2, n)
        d = gmpy2.gcd(y - current, n)
        if d != 1 and d != n:
            processLock.acquire()
            print(process_id, ":", d)
            processLock.release()
            return d
        if i == k:
            y = current
            k = 2 * k
        previous = current


# algorithm adapted from the p-1 notes
def pollard_p1(n, process_id):
    # choose a B to start with
    B = n ** (1 / 6)
    a = 2
    # break up how many things we have to check so we can split over cores
    process_range = (math.floor(B) // PROCESS_COUNT)
    start = process_range * process_id
    end = process_range * (process_id + 1) - 1
    # lock processes so we can print cleanly (thanks 421)
    processLock.acquire()
    print("CORE", process_id, "checking p1 from", start, "to", end)
    processLock.release()
    q1 = ((process_range // 4) * 1) + start
    q2 = ((process_range // 4) * 2) + start
    q3 = ((process_range // 4) * 3) + start
    for i in range(start, end):
        if i == q1:
            print("CORE", process_id, "p1 25%")
        elif i == q2:
            print("CORE", process_id, "p1 50%")
        elif i == q3:
            print("CORE", process_id, "p1 75%")
        a = gmpy2.powmod(a, i, n)
        d = gmpy2.gcd(a - 1, n)
        if d != 1 and d != n:
            return d
    return 1


def break_primes(n, process_id):
    # check to see if the primes were the same
    gmpy2.get_context().precision = 4096
    n_sqrt = gmpy2.sqrt(n)
    if n_sqrt % 1 == 0.0:
        print("Duplicate primes detected!")
        return n_sqrt

    p1_result = pollard_p1(n, process_id)
    if p1_result > 1:
        print("p1 factor found")
        for i in range(len(PROCESSES)):
            if i != process_id:
                PROCESSES[i].terminate()
        return p1_result

    rho_result = pollard_rho(n, process_id)
    print("rho factor found")
    for i in range(len(PROCESSES)):
        if i != process_id:
            PROCESSES[i].terminate()
    return rho_result


def main():
    print("#####   Part 2   #####")
    n = 537886363560496806725823490578687253
    gmpy2.get_context().precision = 4096
    print("Attempting to find factors of", n)

    for i in range(0, PROCESS_COUNT):
        process = multiprocessing.Process(target=break_primes, args=(n, i,))
        PROCESSES.append(process)
        process.start()

    for i in PROCESSES:
        i.join()


if __name__ == "__main__":
    main()
