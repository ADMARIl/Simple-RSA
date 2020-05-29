<h1 align="center">
   Simple RSA
</h1>
<p align="center">
   An implementation of the RSA encryption algorithm to generate a private key and a public key, along with various methods to
   attempt to factor the modulus of the private key. 
 </p>
 <p align="center">
  This project was for my Design and Analysis of Algorithms class at UMBC (CMSC 441). The project outline can be found here:
  <a href="https://userpages.umbc.edu/~cmarron/cs441.s20/projects/rsa_proj.shtml" target="_blank">course website</a>,
  <a href="https://web.archive.org/web/20200527220344/https://userpages.umbc.edu/~cmarron/cs441.s20/projects/rsa_proj.shtml" target="_blank">web archive</a>
</p>

## Installation

1. Presuming you already have python3 the only non-standard package used is [gmpy2](https://gmpy2.readthedocs.io/en/latest/intro.html).
      * If you're on windows you'll need to install [anaconda](https://www.anaconda.com/products/individual) to get gmpy2
          ```bash
          conda install gmpy2  
          ```
      * If you're on linux/mac you can just use pip
          ```bash
          pip3 install gmpy2
          ```

## Building and Running

* To generate a public/private key pair you can run part1a
    ```bash
    python3 part1a.py
    ```
  
* To factor a modulus, run part2 with the modulus as an argument
    ```bash
    python3 part2.py [modulus]
    ```
  E.g.
    ```bash
    python3 part2.py 21421376143373
    ```
  Will return:
    ```bash
    #####   Part 2   #####
    Attempting to find factors of 21421376143373
    Modulo size: 45
    Start Time: 20:49:42.451780
    1 p1 factor found: 5071501
    End Time: 20:49:42.620936
    ```
  
## License

[MIT](https://choosealicense.com/licenses/mit/)
