"""
Tests for toolkit.encrypter
"""

import base64

import pytest

from toolkit import encrypter


class TestEncryptDecrypt:

    def test_roundtrip_simple(self):
        ct = encrypter.encrypt("hello world", "mypassword")
        assert encrypter.decrypt(ct, "mypassword") == "hello world"

    def test_roundtrip_unicode(self):
        msg = "नमस्ते दुनिया 🔐 こんにちは"
        ct = encrypter.encrypt(msg, "p@ss")
        assert encrypter.decrypt(ct, "p@ss") == msg

    def test_roundtrip_long_message(self):
        msg = "A" * 10_000
        ct = encrypter.encrypt(msg, "long")
        assert encrypter.decrypt(ct, "long") == msg

    def test_wrong_password_fails(self):
        ct = encrypter.encrypt("secret", "rightpass")
        with pytest.raises(Exception):
            encrypter.decrypt(ct, "wrongpass")

    def test_ciphertext_is_base64(self):
        ct = encrypter.encrypt("hello", "pw")
        decoded = base64.b64decode(ct)
        assert len(decoded) > 28

    def test_same_plaintext_differs(self):
        assert encrypter.encrypt("same", "pw") != encrypter.encrypt("same", "pw")

    def test_empty_string_roundtrip(self):
        ct = encrypter.encrypt("", "pw")
        assert encrypter.decrypt(ct, "pw") == ""

    def test_tampered_ciphertext_fails(self):
        ct = encrypter.encrypt("hello", "pw")
        blob = bytearray(base64.b64decode(ct))
        blob[-1] ^= 0x01
        tampered = base64.b64encode(bytes(blob)).decode()
        with pytest.raises(Exception):
            encrypter.decrypt(tampered, "pw")


class TestKeyDerivation:

    def test_derive_key_length(self):
        assert len(encrypter.derive_key("pw", b"salt" * 4)) == 32

    def test_same_inputs_same_key(self):
        k1 = encrypter.derive_key("pw", b"0123456789abcdef")
        k2 = encrypter.derive_key("pw", b"0123456789abcdef")
        assert k1 == k2

    def test_different_salt_different_key(self):
        k1 = encrypter.derive_key("pw", b"a" * 16)
        k2 = encrypter.derive_key("pw", b"b" * 16)
        assert k1 != k2
