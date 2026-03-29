"""
Caesar Cipher — Core Cryptography Module
=========================================
A production-ready implementation of the Caesar cipher with support for
full Unicode-safe Latin alphabet shifting, brute-force analysis, and
frequency-analysis hints.

Author : Caesar Cipher Project
License: MIT
"""

from __future__ import annotations

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_SIZE = len(ALPHABET)

# English letter frequency table (most → least common)
ENGLISH_FREQ = "etaoinshrdlcumwfgypbvkjxqz"


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def _validate_shift(shift: int) -> None:
    """Raise ValueError if *shift* is outside the valid range [1, 25]."""
    if not isinstance(shift, int):
        raise TypeError(f"Shift must be an integer, got {type(shift).__name__!r}.")
    if not (1 <= shift <= 25):
        raise ValueError(f"Shift must be between 1 and 25 (inclusive), got {shift}.")


# ---------------------------------------------------------------------------
# Core transform
# ---------------------------------------------------------------------------

def _caesar_transform(text: str, shift: int) -> str:
    """
    Apply a Caesar shift to *text*, preserving case and non-alpha characters.

    Parameters
    ----------
    text  : The string to transform.
    shift : A positive or negative integer offset.

    Returns
    -------
    str : The transformed text.
    """
    result: list[str] = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % ALPHABET_SIZE
            result.append(chr(base + shifted))
        else:
            result.append(char)
    return "".join(result)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def encrypt(text: str, shift: int) -> str:
    """
    Encrypt *text* using a Caesar cipher with the given *shift*.

    Parameters
    ----------
    text  : Plaintext string (any case; non-alpha chars are preserved).
    shift : Integer in [1, 25] representing the cipher key.

    Returns
    -------
    str : The encrypted ciphertext.

    Raises
    ------
    TypeError  : If *shift* is not an integer.
    ValueError : If *shift* is outside [1, 25].

    Examples
    --------
    >>> encrypt("Hello, World!", 3)
    'Khoor, Zruog!'
    """
    _validate_shift(shift)
    return _caesar_transform(text, shift)


def decrypt(text: str, shift: int) -> str:
    """
    Decrypt *text* that was encrypted with the given Caesar *shift*.

    Parameters
    ----------
    text  : Ciphertext string.
    shift : The original encryption shift in [1, 25].

    Returns
    -------
    str : The recovered plaintext.

    Raises
    ------
    TypeError  : If *shift* is not an integer.
    ValueError : If *shift* is outside [1, 25].

    Examples
    --------
    >>> decrypt("Khoor, Zruog!", 3)
    'Hello, World!'
    """
    _validate_shift(shift)
    return _caesar_transform(text, -shift)


def brute_force(ciphertext: str) -> list[dict]:
    """
    Try all 25 possible shifts and return ranked candidates.

    A simple frequency-analysis score is computed for each candidate by
    comparing the decoded text's most-common letter against the English
    frequency table.

    Parameters
    ----------
    ciphertext : The text to analyse.

    Returns
    -------
    list[dict] : List of dicts ordered by *score* (best first).
        Each dict contains:
          - ``shift``   (int)  : The shift value tried.
          - ``text``    (str)  : The decoded candidate.
          - ``score``   (float): Frequency-analysis score (higher = more likely).
    """
    candidates = []
    for shift in range(1, ALPHABET_SIZE):
        candidate = _caesar_transform(ciphertext, -shift)
        score = _frequency_score(candidate)
        candidates.append({"shift": shift, "text": candidate, "score": score})

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates


def _frequency_score(text: str) -> float:
    """
    Score *text* using a weighted dot-product against English letter frequencies.

    Uses empirical English unigram probabilities so that genuine English text
    scores significantly higher than random ciphertext.

    Returns a float; higher means more English-like.
    """
    # Empirical English letter frequencies (source: Lewand, 2000)
    ENGLISH_PROBS: dict[str, float] = {
        'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
        'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
        'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
        'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
        'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
        'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
        'y': 0.01974, 'z': 0.00074,
    }

    from collections import Counter
    letters = [c.lower() for c in text if c.isalpha()]
    if not letters:
        return 0.0

    freq = Counter(letters)
    total = len(letters)

    score = 0.0
    for letter, prob in ENGLISH_PROBS.items():
        observed = freq.get(letter, 0) / total
        score += observed * prob          # dot product — higher when distributions align

    return score
