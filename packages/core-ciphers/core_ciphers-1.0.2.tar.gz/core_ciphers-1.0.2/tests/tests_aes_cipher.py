# -*- coding: utf-8 -*-

from unittest import TestCase

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from core_ciphers.aes_cipher import AESCipher


class AESCipherTestCases(TestCase):
    def test_default_cipher(self):
        data, cipher = "SomeData", AESCipher()

        encrypted = cipher.encrypt(data)
        decrypted = cipher.decrypt(encrypted)
        self.assertEqual(data, decrypted)

    def test_cipher_mode_eax(self):
        cipher = AESCipher(
            key=get_random_bytes(16),
            mode=AES.MODE_EAX
        )

        data = "SomeOtherData"
        encrypted = cipher.encrypt(data)
        decrypted = cipher.decrypt(encrypted)
        self.assertEqual(data, decrypted)

    def test_cipher_mode_ecb(self):
        cipher = AESCipher(
            key=get_random_bytes(16),
            mode=AES.MODE_ECB
        )

        data = "SomeOtherECBData"
        encrypted = cipher.encrypt(data)
        decrypted = cipher.decrypt(encrypted)
        self.assertEqual(data, decrypted)
