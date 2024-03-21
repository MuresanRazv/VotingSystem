import number_generation_helper as ngh
import serialize_helper as sh
import random

ALPHABET = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    " \t\n\r"
)

BIT_LENGTH = 1024

def L(x, n):
    return (x - 1) // n

class Paillier:
    #constructor
    def __init__(self, bit_length=BIT_LENGTH):
        self.p = ngh.generate_prime_candidate(bit_length)
        self.q = ngh.generate_prime_candidate(bit_length)
        print(self.p, self.q)
        # check p and q are relatively prime
        while ngh.binary_gcd(self.p*self.q, (self.p-1)*(self.q-1)) != 1:
            self.p = ngh.generate_prime_candidate(bit_length)
            self.q = ngh.generate_prime_candidate(bit_length)

    def generate_keys(self):
        n = self.p * self.q
        lbd = ngh.lcm(self.p - 1, self.q - 1)
        g = random.randint(2, n ** 2 - 1)
        # ensure n divides the order of g
        u = ngh.modinv(L(pow(g, lbd, n ** 2), n), n)
        while u == False or ngh.binary_gcd(g, n ** 2) != 1:
            g = random.randint(1, n ** 2)
            u = ngh.modinv(L(pow(g, lbd, n ** 2), n), n)

        return (n, g), (lbd, u)
    
    def encrypt(self, public_key, plaintext):
        # Serialize plaintext
        # m = sh.serialize(plaintext)
        m = plaintext
        n, g = public_key

        if (m > n):
            raise ValueError("Plaintext is too large")
        
        # Select random r where 0 < r < n and gcd(r, n) = 1
        r = random.SystemRandom().randrange(1, n - 1)
        while ngh.binary_gcd(r, n) != 1:
            r = random.SystemRandom().randrange(1, n - 1)

        # Encrypt plaintext
        return (pow(g, m, n**2) * pow(r, n, n**2)) % (n**2)
    
    def decrypt(self, public_key, private_key, ciphertext):
        n, g = public_key
        lbd, u = private_key

        if (ciphertext > n**2):
            raise ValueError("Ciphertext is too large")
        
        return L(pow(ciphertext, lbd, n**2), n) * u % n
    
    # works only for numbers
    def add(self, public_key, first_plaintext, second_plaintext):
        n, _ = public_key
        return ((first_plaintext % n**2) * (second_plaintext % n**2)) % n**2