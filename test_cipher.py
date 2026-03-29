"""
Caesar Cipher — Test Suite
===========================
Run with:  python -m pytest tests/ -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from cipher import encrypt, decrypt, brute_force, _frequency_score


# ---------------------------------------------------------------------------
# encrypt()
# ---------------------------------------------------------------------------

class TestEncrypt:
    def test_basic_lowercase(self):
        assert encrypt("abc", 1) == "bcd"

    def test_basic_uppercase(self):
        assert encrypt("ABC", 1) == "BCD"

    def test_wrap_around(self):
        assert encrypt("xyz", 3) == "abc"

    def test_preserves_spaces(self):
        assert encrypt("hello world", 1) == "ifmmp xpsme"

    def test_preserves_punctuation(self):
        assert encrypt("Hello, World!", 3) == "Khoor, Zruog!"

    def test_shift_13_rot13(self):
        assert encrypt("Hello", 13) == "Uryyb"

    def test_shift_25(self):
        assert encrypt("b", 25) == "a"

    def test_numbers_unchanged(self):
        assert encrypt("abc123", 1) == "bcd123"

    def test_empty_string(self):
        assert encrypt("", 5) == ""

    def test_invalid_shift_zero(self):
        with pytest.raises(ValueError):
            encrypt("hello", 0)

    def test_invalid_shift_26(self):
        with pytest.raises(ValueError):
            encrypt("hello", 26)

    def test_invalid_shift_type(self):
        with pytest.raises(TypeError):
            encrypt("hello", "3")  # type: ignore


# ---------------------------------------------------------------------------
# decrypt()
# ---------------------------------------------------------------------------

class TestDecrypt:
    def test_basic_decrypt(self):
        assert decrypt("bcd", 1) == "abc"

    def test_roundtrip(self):
        original = "The Quick Brown Fox Jumps Over the Lazy Dog!"
        for shift in range(1, 26):
            assert decrypt(encrypt(original, shift), shift) == original

    def test_invalid_shift(self):
        with pytest.raises(ValueError):
            decrypt("test", 0)


# ---------------------------------------------------------------------------
# brute_force()
# ---------------------------------------------------------------------------

class TestBruteForce:
    def test_returns_25_candidates(self):
        results = brute_force("khoor")
        assert len(results) == 25

    def test_correct_shift_ranks_first(self):
        """Encrypt a full pangram with shift=3 — brute force should recover shift=3."""
        from cipher import encrypt as enc
        ciphertext = enc("The quick brown fox jumps over the lazy dog", 3)
        results = brute_force(ciphertext)
        assert results[0]["shift"] == 3

    def test_candidate_structure(self):
        results = brute_force("test")
        for c in results:
            assert "shift" in c
            assert "text" in c
            assert "score" in c

    def test_empty_string(self):
        results = brute_force("")
        assert len(results) == 25


# ---------------------------------------------------------------------------
# _frequency_score()
# ---------------------------------------------------------------------------

class TestFrequencyScore:
    def test_english_scores_high(self):
        english = "the quick brown fox jumps over the lazy dog"
        nonsense = "zzz qqq xxx yyy"
        assert _frequency_score(english) > _frequency_score(nonsense)

    def test_empty_string_returns_zero(self):
        assert _frequency_score("") == 0.0

    def test_score_range(self):
        score = _frequency_score("hello world")
        assert 0.0 <= score <= 1.0
