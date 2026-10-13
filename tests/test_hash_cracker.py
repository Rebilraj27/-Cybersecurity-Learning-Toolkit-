"""
Tests for toolkit.hash_cracker
"""

import hashlib

import pytest

from toolkit import hash_cracker


class TestHashWord:

    @pytest.mark.parametrize("algo,expected", [
        ("md5",    "5d41402abc4b2a76b9719d911017c592"),
        ("sha1",   "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"),
        ("sha256", "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"),
    ])
    def test_known_hashes(self, algo, expected):
        assert hash_cracker.hash_word("hello", algo) == expected

    def test_unsupported_algo_raises(self):
        with pytest.raises(ValueError):
            hash_cracker.hash_word("hello", "not-real")


class TestCrack:

    def test_crack_md5_success(self, sample_wordlist):
        target = hashlib.md5(b"password").hexdigest()
        result = hash_cracker.crack(target, sample_wordlist, algo="md5")
        assert result["found"] is True
        assert result["password"] == "password"

    def test_crack_sha256_success(self, sample_wordlist):
        target = hashlib.sha256(b"admin").hexdigest()
        result = hash_cracker.crack(target, sample_wordlist, algo="sha256")
        assert result["found"] is True
        assert result["password"] == "admin"

    def test_crack_sha1_success(self, sample_wordlist):
        target = hashlib.sha1(b"cyber").hexdigest()
        result = hash_cracker.crack(target, sample_wordlist, algo="sha1")
        assert result["found"] is True

    def test_crack_not_found(self, sample_wordlist):
        target = hashlib.md5(b"not-in-list").hexdigest()
        assert hash_cracker.crack(target, sample_wordlist)["found"] is False

    def test_crack_case_insensitive(self, sample_wordlist):
        target = hashlib.md5(b"hello").hexdigest().upper()
        assert hash_cracker.crack(target, sample_wordlist)["found"] is True

    def test_crack_missing_wordlist(self):
        with pytest.raises(FileNotFoundError):
            hash_cracker.crack("deadbeef", "/no/such/file.txt")

    def test_crack_bad_algo(self, sample_wordlist):
        with pytest.raises(ValueError):
            hash_cracker.crack("abc", sample_wordlist, algo="rot13")

    def test_supported_algos(self):
        assert set(hash_cracker.SUPPORTED) == {"md5", "sha1", "sha256", "sha512"}
