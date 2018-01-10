import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '.'))

# Test Suite

import orme.models

class TestModels(unittest.TestCase):

    def test_cipher(self):
        private_key = 'z3moYaHY9kf08oEw6W_oOnDdDNwhVAMukq_To3-BJ6Y='
        passphrase = 'What a beautiful day'

        ciphered_text = orme.models.Address.cipher_string(passphrase, private_key)
        deciphered_text = orme.models.Address.decipher_string(ciphered_text, private_key)

        self.assertEqual(passphrase, deciphered_text)
        self.assertNotEqual(passphrase, ciphered_text)

if __name__ == '__main__':
    unittest.main()