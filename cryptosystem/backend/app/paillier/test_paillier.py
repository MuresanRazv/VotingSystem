import pytest
from paillier_cryptosystem import generate_keys, encrypt, decrypt, add
from number_generation_helper import is_prime, generate_prime_candidate, binary_gcd
from time import perf_counter

class TestPaillierCryptosystem:

    @pytest.mark.asyncio
    async def test_key_length_and_type(self):
        key_sizes = [1024]
        for key_size in key_sizes:
            time_start = perf_counter()

            public_key, private_key = await generate_keys(key_size)
            n, _ = public_key
            l, mu = private_key

            time_end = perf_counter()
            print(f'KEY GENERATION BENCHMARK FOR {key_size}: {time_end - time_start}')
            assert isinstance(n, int)
            assert isinstance(l, int)
            assert isinstance(mu, int)
            assert n.bit_length() >= key_size

    @pytest.mark.asyncio
    async def test_prime_numbers(self):
        p = generate_prime_candidate(1024)
        q = generate_prime_candidate(1024)
        
        assert is_prime(p, 1024)
        assert is_prime(q, 1024)
        assert p != q

    @pytest.mark.asyncio
    async def test_n_divides_order_of_g(self):
        public_key, private_key = await generate_keys()
        n, g = public_key

        assert binary_gcd(g, n ** 2) == 1

    @pytest.mark.asyncio
    async def test_public_key_validity(self):
        public_key, private_key = await generate_keys()
        g, n = public_key
        assert g > 0
        assert n > 0

    @pytest.mark.asyncio
    async def test_private_key_validity(self):
        public_key, private_key = await generate_keys()
        l, mu = private_key
        assert l > 0
        assert mu > 0

    @pytest.mark.asyncio
    async def test_randomness(self):
        public_key1, private_key1 = await generate_keys()
        public_key2, private_key2 = await generate_keys()
        assert public_key1 != public_key2
        assert private_key1 != private_key2

    @pytest.mark.asyncio
    async def test_encryption_and_decryption(self):
        public_key, private_key = await generate_keys(1024)
        message = 42
        ciphertext = await encrypt(public_key, message)
        decrypted_message = await decrypt(public_key, private_key, ciphertext)
        assert message == decrypted_message

    @pytest.mark.asyncio
    async def test_addition(self):
        public_key, private_key = await generate_keys(1024)

        first_number = 12345678901234567890
        second_number = 98765432109876543210

        first_cipher = await encrypt(public_key, first_number)
        second_cipher = await encrypt(public_key, second_number)

        time_start = perf_counter()

        sum = await add(public_key, first_cipher, second_cipher)

        time_end = perf_counter()
        print(f"ADDITION OPERATION BENCHMARK: {(time_end - time_start):10f}")
        sum = await decrypt(public_key, private_key, sum)
        assert 1 == 0
        assert sum == first_number + second_number

if __name__ == '__main__':
    pytest.main()
