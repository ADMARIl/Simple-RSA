"""
File: factor_calc.py
Created by Andrew Ingson (aings1@umbc.edu)
Date: 5/7/2020
CMSC 4-- (CLASS NAME)

"""

import gmpy2


def main():
    big = int(input("Big: "))
    small = int(input("Small: "))
    print("Sml Stat:", gmpy2.is_prime(small))

    result = gmpy2.div(big, small)
    print("Res Stat:", gmpy2.is_prime(result))

    print(result)


if __name__ == "__main__":
    main()