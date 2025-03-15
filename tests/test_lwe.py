import unittest
import numpy as np
from src.lwe import LWE


class TestLWE(unittest.TestCase):

        
    def test_encrypt_bit(self):
        pk, sk = LWE.keygen()
        
        for _ in range(10000):
            ct = LWE.encrypt_bit(pk, 1)
            self.assertEqual(LWE.decrypt_bit(sk, ct), 1)
            ct = LWE.encrypt_bit(pk, 0)
            self.assertEqual(LWE.decrypt_bit(sk, ct), 0)
        
    def test_encrypt_string(self):
        pk, sk = LWE.keygen()
        
        for _ in range(10000):
            characters = '01'
            s = ''.join([characters[i] for i in np.random.randint(0, len(characters), 10)])
            print(s)
            ct = LWE.encrypt_string(pk, s)
            self.assertEqual(LWE.decrypt_string(sk, ct), s)
        

if __name__ == '__main__':
    unittest.main()