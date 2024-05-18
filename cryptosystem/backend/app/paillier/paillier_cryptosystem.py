from app.paillier.number_generation_helper import generate_prime_candidate, binary_gcd, lcm, modinv
import random

BIT_LENGTH = 2048

def L(x, n):
    return (x - 1) // n

async def generate_keys():
    p = generate_prime_candidate(BIT_LENGTH)
    q = generate_prime_candidate(BIT_LENGTH)
    
    # check p and q are relatively prime
    while binary_gcd(p*q, (p-1)*(q-1)) != 1:
        p = generate_prime_candidate(BIT_LENGTH)
        q = generate_prime_candidate(BIT_LENGTH)

    n = p * q
    lbd = lcm(p - 1, q - 1)
    g = random.randint(2, n ** 2 - 1)
    # ensure n divides the order of g
    u = modinv(L(pow(g, lbd, n ** 2), n), n)
    while u == False or binary_gcd(g, n ** 2) != 1:
        g = random.randint(1, n ** 2)
        u = modinv(L(pow(g, lbd, n ** 2), n), n)

    return (n, g), (lbd, u)

async def encrypt(public_key, plaintext):
    # Serialize plaintext
    # m = sh.serialize(plaintext)
    m = plaintext
    n, g = public_key

    if (m > n):
        raise ValueError("Plaintext is too large")
    
    # Select random r where 0 < r < n and gcd(r, n) = 1
    r = random.SystemRandom().randrange(1, n - 1)
    while binary_gcd(r, n) != 1:
        r = random.SystemRandom().randrange(1, n - 1)

    # Encrypt plaintext
    return (pow(g, m, n**2) * pow(r, n, n**2)) % (n**2)

async def decrypt(public_key, private_key, ciphertext):
    n, g = public_key
    lbd, u = private_key

    if (ciphertext > n**2):
        raise ValueError("Ciphertext is too large")
    
    return L(pow(ciphertext, lbd, n**2), n) * u % n

# works only for numbers
async def add(public_key, first_plaintext, second_plaintext):
    n, _ = public_key
    return ((first_plaintext % n**2) * (second_plaintext % n**2)) % n**2
