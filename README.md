<h1 align="center">
   Simple RSA
</h1>
<p align="center">
   An implementation of the RSA encryption algorithm to generate a private key and a public key, along with methods that
   attempt to factor the private key. 
 </p>
 <p align="center">
  This project was for my Design and Analysis of Algorithms class at UMBC. The project outline can be found here:
  <a href="https://userpages.umbc.edu/~cmarron/cs441.s20/projects/rsa_proj.shtml" target="_blank">course website</a>,
  <a href="https://web.archive.org/web/20200527220344/https://userpages.umbc.edu/~cmarron/cs441.s20/projects/rsa_proj.shtml" target="_blank">web archive</a>
</p>

## Installation

1. Presuming you already have python3 the only non-standard package used is [gmpy2](https://gmpy2.readthedocs.io/en/latest/intro.html).
      * If you have windows you'll need to install [anaconda](https://www.anaconda.com/products/individual) to install gmpy2
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
    python2 part2.py [modulous]
    ```
  E.g.
    ```bash
    python2 part2.py 58853
    ```
  
## License

[MIT](https://choosealicense.com/licenses/mit/)