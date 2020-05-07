"""
File: part2.py
Created by Andrew Ingson (aings1@umbc.edu)
Date: 4/26/2020
CMSC 441 (Design and Analysis of Algorithms)
Notes: The only non-standard library used for this project would gmpy2. On windows you can use anaconda to get gmpy2
        otherwise you'll need to run this program on linux so you can install gmpy2 with pip.
Build/Run Instructions: Run this program with the modulo as a command line argument. E.g. python3 part2.py 58853

"""
import random
import gmpy2
import multiprocessing
import math
import sys
from datetime import datetime

# this constant defines that amount of threads that are generated to crack a modulo
PROCESS_COUNT = 2
PROCESSES = []
# if this flag is set to true program will print more status info
DEBUG = False
# pollard rho can be faster for smaller numbers if you give it a constant to work from instead of letting it randomly
# choose things. Change this constant to change the threshold for at what bit size it switches over to random
RHO_CONSTANT = 150

# short list of trivial primes
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
          109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
          367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
          499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
          643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
          797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
          947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063,
          1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201,
          1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319,
          1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471,
          1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597,
          1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723,
          1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873,
          1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011,
          2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141,
          2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293,
          2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417,
          2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591,
          2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711,
          2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843,
          2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001,
          3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169,
          3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319,
          3323, 3329, 3331, 3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 3449, 3457, 3461, 3463,
          3467, 3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571, 3581, 3583, 3593,
          3607, 3613, 3617, 3623, 3631, 3637, 3643, 3659, 3671, 3673, 3677, 3691, 3697, 3701, 3709, 3719, 3727, 3733,
          3739, 3761, 3767, 3769, 3779, 3793, 3797, 3803, 3821, 3823, 3833, 3847, 3851, 3853, 3863, 3877, 3881, 3889,
          3907, 3911, 3917, 3919, 3923, 3929, 3931, 3943, 3947, 3967, 3989, 4001, 4003, 4007, 4013, 4019, 4021, 4027,
          4049, 4051, 4057, 4073, 4079, 4091, 4093, 4099, 4111, 4127, 4129, 4133, 4139, 4153, 4157, 4159, 4177, 4201,
          4211, 4217, 4219, 4229, 4231, 4241, 4243, 4253, 4259, 4261, 4271, 4273, 4283, 4289, 4297, 4327, 4337, 4339,
          4349, 4357, 4363, 4373, 4391, 4397, 4409, 4421, 4423, 4441, 4447, 4451, 4457, 4463, 4481, 4483, 4493, 4507,
          4513, 4517, 4519, 4523, 4547, 4549, 4561, 4567, 4583, 4591, 4597, 4603, 4621, 4637, 4639, 4643, 4649, 4651,
          4657, 4663, 4673, 4679, 4691, 4703, 4721, 4723, 4729, 4733, 4751, 4759, 4783, 4787, 4789, 4793, 4799, 4801,
          4813, 4817, 4831, 4861, 4871, 4877, 4889, 4903, 4909, 4919, 4931, 4933, 4937, 4943, 4951, 4957, 4967, 4969,
          4973, 4987, 4993, 4999, 5003, 5009, 5011, 5021, 5023, 5039, 5051, 5059, 5077, 5081, 5087, 5099, 5101, 5107,
          5113, 5119, 5147, 5153, 5167, 5171, 5179, 5189, 5197, 5209, 5227, 5231, 5233, 5237, 5261, 5273, 5279, 5281,
          5297, 5303, 5309, 5323, 5333, 5347, 5351, 5381, 5387, 5393, 5399, 5407, 5413, 5417, 5419, 5431, 5437, 5441,
          5443, 5449, 5471, 5477, 5479, 5483, 5501, 5503, 5507, 5519, 5521, 5527, 5531, 5557, 5563, 5569, 5573, 5581,
          5591, 5623, 5639, 5641, 5647, 5651, 5653, 5657, 5659, 5669, 5683, 5689, 5693, 5701, 5711, 5717, 5737, 5741,
          5743, 5749, 5779, 5783, 5791, 5801, 5807, 5813, 5821, 5827, 5839, 5843, 5849, 5851, 5857, 5861, 5867, 5869,
          5879, 5881, 5897, 5903, 5923, 5927, 5939, 5953, 5981, 5987, 6007, 6011, 6029, 6037, 6043, 6047, 6053, 6067,
          6073, 6079, 6089, 6091, 6101, 6113, 6121, 6131, 6133, 6143, 6151, 6163, 6173, 6197, 6199, 6203, 6211, 6217,
          6221, 6229, 6247, 6257, 6263, 6269, 6271, 6277, 6287, 6299, 6301, 6311, 6317, 6323, 6329, 6337, 6343, 6353,
          6359, 6361, 6367, 6373, 6379, 6389, 6397, 6421, 6427, 6449, 6451, 6469, 6473, 6481, 6491, 6521, 6529, 6547,
          6551, 6553, 6563, 6569, 6571, 6577, 6581, 6599, 6607, 6619, 6637, 6653, 6659, 6661, 6673, 6679, 6689, 6691,
          6701, 6703, 6709, 6719, 6733, 6737, 6761, 6763, 6779, 6781, 6791, 6793, 6803, 6823, 6827, 6829, 6833, 6841,
          6857, 6863, 6869, 6871, 6883, 6899, 6907, 6911, 6917, 6947, 6949, 6959, 6961, 6967, 6971, 6977, 6983, 6991,
          6997, 7001, 7013, 7019, 7027, 7039, 7043, 7057, 7069, 7079, 7103, 7109, 7121, 7127, 7129, 7151, 7159, 7177,
          7187, 7193, 7207, 7211, 7213, 7219, 7229, 7237, 7243, 7247, 7253, 7283, 7297, 7307, 7309, 7321, 7331, 7333,
          7349, 7351, 7369, 7393, 7411, 7417, 7433, 7451, 7457, 7459, 7477, 7481, 7487, 7489, 7499, 7507, 7517, 7523,
          7529, 7537, 7541, 7547, 7549, 7559, 7561, 7573, 7577, 7583, 7589, 7591, 7603, 7607, 7621, 7639, 7643, 7649,
          7669, 7673, 7681, 7687, 7691, 7699, 7703, 7717, 7723, 7727, 7741, 7753, 7757, 7759, 7789, 7793, 7817, 7823]
# lock to for multi threading so the processes don't step on each others toes
processLock = multiprocessing.Lock()


# algorithm adapted from the pollard rho notes
def pollard_rho(n, process_id):
    i = 1
    # set the point in which rho starts
    if gmpy2.bit_length(gmpy2.mpz(n)) < RHO_CONSTANT:
        # small value modulo so we are better off starting with small value
        if DEBUG:
            print("bit size", gmpy2.bit_length(gmpy2.mpz(n)), "less than", RHO_CONSTANT, "so non ran")
        initial = process_id + 2
        re_rand = False
    else:
        # small value modulo so we are better off starting with a random value
        if DEBUG:
            print("ran")
        # set a flag so we can re rand rho at a latter point
        re_rand = True
        # process_id + 2  # this could also be random.randomint(0, n - 1)
        initial = random.randint(primes[len(primes) - 1], n // (process_id + 2))
    if DEBUG:
        processLock.acquire()
        print("CORE", process_id, "checking rho of", initial)
        processLock.release()
    y = initial
    k = 2
    previous = initial
    count = 0
    while True:
        i += 1
        count += 1
        # alt methods
        # gmpy2.powmod(pow(previous, 2) - 1, 1, n)  # ((pow(previous, 2)) - 1) % n  #
        current = (((previous ** 2) - 1) % n)
        d = gmpy2.gcd(y - current, n)
        if d != 1 and d != n:
            return d
        if i == k:
            y = current
            k = 2 * k
        previous = current
        if re_rand and count > 100000:  # (gmpy2.sqrt(n) // primes[len(primes)-1]):
            # print("RE-RAN")
            count = 0
            previous = random.randint(primes[len(primes) - 1], int(gmpy2.sqrt(n)))


# algorithm adapted from the p-1 notes
def pollard_p1(n, process_id):
    # choose a B to start with
    work_limit = pow(n, (1 / 6))
    a = 2
    # break up how many things we have to check so we can split over cores
    process_range = (math.floor(work_limit) // PROCESS_COUNT)
    start = process_range * process_id
    end = process_range * (process_id + 1) - 1

    # assign default values here so we are an excellent, coding standard following coder
    q1, q2, q3 = 0, 0, 0
    if DEBUG:
        # lock processes so we can print cleanly (thanks 421)
        processLock.acquire()
        print("CORE", process_id, "checking p1 from", start, "to", end)
        processLock.release()
        q1 = ((process_range // 4) * 1) + start
        q2 = ((process_range // 4) * 2) + start
        q3 = ((process_range // 4) * 3) + start
    for i in range(start, end):
        # print informative debug statements
        if DEBUG:
            if i == q1:
                print("CORE", process_id, "p1 25%")
            elif i == q2:
                print("CORE", process_id, "p1 50%")
            elif i == q3:
                print("CORE", process_id, "p1 75%")

        # check to see if we've found the terminating conditions for p - 1
        a = gmpy2.powmod(a, i, n)
        d = gmpy2.gcd(a - 1, n)
        if d != 1 and d != n:
            return d
    return 1


def william_p1(n, process_id):
    # this algorithm technically works but literally none of the modulos were p+1 so idk
    work_limit = pow(n, (1 / 6))
    threshold = 3
    previous_sub2 = 2
    # A needs to be greater than 2 to start with so we therefore start with 3
    A = process_id + 3
    previous = A

    counter = 0
    # if the counter ever reaches m, terminate
    while counter != threshold:
        counter += 1
        # current = (a^(current-1) - current-2) % n)
        current = (((A ** previous) - previous_sub2) % n)
        # move the previous variables forward
        previous_sub2 = previous
        previous = current

        d = gmpy2.gcd(current - 2, n)
        if d != 1 and d != n:
            # calculate the factorial of m
            mult = gmpy2.fac(threshold)
            if DEBUG:
                print(d, mult)
            # check to see if we've found the terminating conditions for p + 1
            if gmpy2.f_mod(mult, d):
                return d
        else:
            # increment threshold by 1 if we haven't found anything
            threshold += 1
        if threshold > work_limit:
            return 1

    return 1


def elliptical_curve(n, process_id):
    # I decided not to finish the implementation of this algo as the learning curve for implementation was steep
    # and not worth it. I left this code here to show that I tried though.

    print("Pollard p-1 Part 2: The Lenstra Boogolo")
    print(process_id, "ECM Called")
    # vars to maintain the generation loop
    coor_x, coor_y = 0, 0
    # generate curve
    # TODO: Not sure if these random ranges are correct
    coor_x, coor_y = gmpy2.mpz_random(gmpy2.random_state(), n), gmpy2.mpz_random(gmpy2.random_state(), n)
    a = gmpy2.mpz_random(gmpy2.random_state(), n)
    # b = y^2 - ax - x^3
    b = gmpy2.f_mod((coor_y * coor_y - a * coor_x - coor_x * coor_x * coor_x), n)
    # TODO: The wikipedia says there's checks you can do for the curve at this point by I don't want to put in the
    #  effort, however this note is here as a reminder in case things aren't working
    #  (while loop to check this stuff?)
    # is this the right check? (delta)

    # generate point
    curr_x = coor_x
    curr_y = coor_y

    # range to loop to
    current = 2
    limit = random.randint(1000000, 100000000)

    # loop to do the monster math
    # TODO: loop to do the actual ECM stuff
    # return value since this is broken and un finished
    return 1


# function to handle the factoring of the provided modulo
def break_primes(n, process_id, sync, output):
    # check to see if the primes were the same
    gmpy2.get_context().precision = 4096
    n_sqrt = gmpy2.sqrt(n)
    # check to see if the modulo is a perfect square root of itself
    if n_sqrt % 1 == 0.0:
        processLock.acquire()
        if output.empty():
            output.put(n_sqrt)
            sync.set()
            print("Duplicate primes detected! Prime is", n_sqrt)
        processLock.release()
        return n_sqrt

    # trial division
    processLock.acquire()
    # loop through the trivial primes
    for i in range(len(primes)):
        # check if we've haven't found anything yet
        if output.empty():
            # the smaller of any factors of modulo has to be less than the sqrt of that modulo so we can give up if we
            # haven't found anything by then
            if primes[i] > gmpy2.sqrt(n):
                break
            elif gmpy2.f_mod(n, primes[i]) == 0.0:
                # share the result and handle the multiprocessing cleanup
                print("Trial Division Success! Divisible by", primes[i])
                print("Result is", n // primes[i])
                output.put(primes[i])
                sync.set()
                # processLock.release()
                return primes[i]
    processLock.release()
    # informative statements
    if DEBUG:
        print("No Trivial")
        print("nothing easy :(")

    # check to see if the modulo is vulnerable to pollard p - 1
    p1_result = pollard_p1(n, process_id)
    processLock.acquire()
    if p1_result > 1 and output.empty():
        # share the result and handle the multiprocessing cleanup
        print(process_id, "p1 factor found:", p1_result)
        output.put(p1_result)
        sync.set()
        return p1_result
    if DEBUG:
        print(process_id, ": p1 no factors")
    processLock.release()

    # check to see if the modulo is vulnerable to william p + 1
    william = 1  # william_p1(n, process_id)
    processLock.acquire()
    if william > 1 and output.empty():
        # share the result and handle the multiprocessing cleanup
        print("William factor found:", william)
        output.put(william)
        sync.set()
        return william
    if DEBUG:
        print(process_id, ": william no factors")
    processLock.release()

    # if all else fails try pollard rho on it
    rho_result = pollard_rho(n, process_id)
    processLock.acquire()
    if output.empty():
        # share the result and handle the multiprocessing cleanup
        print(process_id, "rho factor found:", rho_result)
        output.put_nowait(rho_result)
        sync.set()
    # processLock.release()
    return rho_result


def main():
    print("#####   Part 2   #####")
    # get the modulo we want to factor from the command line
    n = int(sys.argv[1])
    gmpy2.get_context().precision = 4096
    # variable to monitor when any process finishes
    sync = multiprocessing.Event()
    # Queue to hold the return value of the function so we can use it again in the main process
    output_q = multiprocessing.Queue()

    # check the factors of all numbers in batch
    modulo = n  # 412327469960708624240573

    print("Attempting to find factors of", modulo)
    bit_size = gmpy2.bit_length(gmpy2.mpz(modulo))
    print("Modulo size:", bit_size)

    curr_time = datetime.now().time()
    print("Start Time:", curr_time)

    # check if n is prime
    if gmpy2.is_prime(modulo):
        print("This probably shouldn't happen but n is prime", modulo)
        return 0

    # start PROCESS_COUNT amount of processes
    for i in range(0, PROCESS_COUNT):
        process = multiprocessing.Process(target=break_primes, args=(modulo, i, sync, output_q))
        PROCESSES.append(process)
        process.start()

    # wait until any of the processes find something then kill the others
    sync.wait()
    # kill the remaining processes once the factor has been found
    for i in PROCESSES:
        if DEBUG:
            print("Killing processes")
        i.terminate()
    # join processes back to spawning process
    for i in PROCESSES:
        i.join()
    output_q.put('extra value to make the queue happy')
    if DEBUG:
        print("Queue Size", output_q.qsize())
    # get the value back from the process
    result = output_q.get()
    if DEBUG:
        print("Queue Size", output_q.qsize())
    # clean up the queue
    while not output_q.empty():
        if DEBUG:
            print("Cleaning")
        output_q.get_nowait()
    sync.clear()
    # print ending time
    curr_time = datetime.now().time()
    print("End Time:", curr_time)
    if DEBUG:
        print("Factor of n is:", result)


if __name__ == "__main__":
    main()
