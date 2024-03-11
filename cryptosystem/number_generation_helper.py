import random

# Miller-Rabin primality test for generating big prime numbers
def is_prime(n, k=128):
    # Test if n is not even
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, r, n)

        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
            
    return True

def generate_prime_candidate(length=1024):
    # generate random bits
    p = random.getrandbits(length)

    # modify least significant bit and most significant bit to be 1, ensuring the number is not even
    p |= (1 << length - 1) | 1

    return p

def binary_gcd(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    
    # find common factors of 2
    k = 0
    while a & 1 == 0 and b & 1 == 0:
        a >>= 1
        b >>= 1
        k += 1

    # Make a odd
    while a & 1 == 0:
        a >>= 1

    # Binary GCD algorithm
    while b:
        while b & 1 == 0:
            b >>= 1
        if a > b:
            a, b = b, a
        b -= a

    return a << k

def lcm(a, b):
    return a // binary_gcd(a, b) * b

# For modular inverse
def extended_gcd(a, b):
    x, y = 0, 1
    last_x, last_y = 1, 0
    while b != 0:
        quotient = a // b
        a, b = b, a % b
        x, last_x = last_x - quotient * x, x
        y, last_y = last_y - quotient * y, y
    return a, last_x, last_y
    
def modinv(a, m):
    d, x, y = extended_gcd(a, m)
    if d != 1:
        return False
    else:
        return x % m