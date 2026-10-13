"""
Tests for toolkit.password_strength
"""

import pytest

from toolkit import password_strength


class TestEntropy:

    def test_empty_password_zero(self):
        assert password_strength.entropy("") == 0.0

    def test_lowercase_only(self):
        e = password_strength.entropy("abcdefgh")
        assert 37 < e < 39

    def test_mixed_charset_higher(self):
        weak = password_strength.entropy("aaaaaaaa")
        strong = password_strength.entropy("Aa1!Aa1!")
        assert strong > weak

    def test_longer_password_higher(self):
        assert password_strength.entropy("Ab1!Ab1!Ab1!") > password_strength.entropy("Ab1!")


class TestAnalyze:

    def test_very_weak_password(self):
        result = password_strength.analyze("123")
        assert result["strength"] in ("Very Weak", "Weak")
        assert result["score"] <= 2

    def test_strong_password(self):
        result = password_strength.analyze("MyS3cur3P@ssw0rd!2024")
        assert result["score"] >= 4

    def test_common_password_flagged(self):
        result = password_strength.analyze("password123")
        assert result["score"] == 0
        assert any("common" in f.lower() for f in result["feedback"])

    def test_qwerty_flagged(self):
        assert password_strength.analyze("qwerty")["score"] == 0

    def test_short_password_feedback(self):
        result = password_strength.analyze("Aa1!")
        assert any("12" in f or "characters" in f.lower() for f in result["feedback"])

    def test_returns_all_keys(self):
        result = password_strength.analyze("Test123!")
        for key in ("score", "strength", "entropy_bits", "feedback"):
            assert key in result

    def test_score_never_exceeds_5(self):
        result = password_strength.analyze("A" * 100 + "a1!@#$%^&*")
        assert result["score"] <= 5

    def test_feedback_is_list(self):
        assert isinstance(password_strength.analyze("abc")["feedback"], list)
