import unittest
from Simple_tcpClient import miller_rabin_test, gcd, mod_inverse

class TestRabinMiller(unittest.TestCase):

    def test_small_primes(self):
        self.assertEqual(miller_rabin_test(2, 5), True)
        self.assertEqual(miller_rabin_test(3, 5), True)
        self.assertEqual(miller_rabin_test(5, 5), True)
        self.assertEqual(miller_rabin_test(7, 5), True)
        self.assertEqual(miller_rabin_test(11, 5), True)

    def test_small_composites(self):
        self.assertEqual(miller_rabin_test(4, 5), False)
        self.assertEqual(miller_rabin_test(6, 5), False)
        self.assertEqual(miller_rabin_test(8, 5), False)
        self.assertEqual(miller_rabin_test(9, 5), False)
        self.assertEqual(miller_rabin_test(10, 5), False)

    def test_large_primes(self):
        self.assertEqual(miller_rabin_test(104729, 5), True)  # 10000th prime
        self.assertEqual(miller_rabin_test(1299709, 5), True)  # 100000th prime

    def test_large_composites(self):
        self.assertEqual(miller_rabin_test(104728, 5), False)
        self.assertEqual(miller_rabin_test(1299708, 5), False)

    def test_very_large_primes(self):
        # Known very large prime numbers
        self.assertEqual(miller_rabin_test(32416190071, 5), True)  # 32416190071 is a prime
        self.assertEqual(miller_rabin_test(32416187567, 5), True)  # 32416187567 is a prime

    def test_very_large_composites(self):
        # Known very large composite numbers
        self.assertEqual(miller_rabin_test(32416190070, 5), False)  # 32416190070 is not a prime
        self.assertEqual(miller_rabin_test(32416187566, 5), False)  # 32416187566 is not a prime
    
    def test_gcd(self):
        self.assertEqual(gcd(2, 5), 1)
        self.assertEqual(gcd(3, 5), 1)
        self.assertEqual(gcd(5, 5), 5)
        self.assertEqual(gcd(7, 5), 1)
        self.assertEqual(gcd(11, 5), 1)


if __name__ == '__main__':
    unittest.main()