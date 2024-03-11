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

def L(x, n):
    return (x - 1) // n

class Paillier:
    def generate_keys(self, bit_length=2048):
        p = ngh.generate_prime_candidate(bit_length)
        q = ngh.generate_prime_candidate(bit_length)
        n = p * q
        lbd = ngh.lcm(p - 1, q - 1)
        g = random.randint(1, n ** 2)
        # ensure n divides the order of g
        u = ngh.modinv(L(pow(g, lbd, n ** 2), n), n)
        while ngh.binary_gcd(g, pow(n, 2)) != 1 and u != False:
            g = random.randint(1, n ** 2)
            u = ngh.modinv(L(pow(g, lbd, n ** 2), n), n)

        return (n, g), (lbd, u)
    
    # Generate keys using a faster method (p, q are of similar length)
    def generate_keys_fast(self, bit_length=2048):
        p = ngh.generate_prime_candidate(bit_length)
        q = ngh.generate_prime_candidate(bit_length)

        n = p * q
        g = n + 1
        lbd = (p - 1) * (q - 1)
        u = ngh.modinv((p - 1) * (q - 1), n)

        return (n, g), (lbd, u)
    
    def encrypt(self, public_key, plaintext):
        # Serialize plaintext
        m = sh.serialize(plaintext)
        n, g = public_key

        if (m > n):
            raise ValueError("Plaintext is too large")
        
        # Select random r where 0 < r < n and gcd(r, n) = 1
        r = random.randint(1, n - 1)
        while ngh.binary_gcd(r, n) != 1:
            r = random.randint(1, n)

        # Encrypt plaintext
        return (pow(g, m, n**2) * pow(r, n, n**2)) % (n**2)
    
    def decrypt(self, public_key, private_key, ciphertext):
        n, _ = public_key
        lbd, u = private_key

        # Decrypt ciphertext
        return (L(pow(ciphertext, lbd, n**2), n) * u) % n
        



paellier = Paellier()
public, private = paellier.generate_keys_fast()
encrypted = paellier.encrypt(public, {"key": "Hello, World!"})
decrypted = paellier.decrypt(public, private, encrypted)
print(decrypted)
print(sh.deserialize({"key": "Hello, World!"}))