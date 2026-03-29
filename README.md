# ⚔ Caesar Cipher — Classical Cryptography Tool

> A production-grade implementation of the Caesar cipher with a polished web interface, REST API, brute-force analysis, and a comprehensive test suite.

![Python](https://img.shields.io/badge/Python-3.9%2B-gold?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-gold?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-gold?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=flat-square)

---

## Overview

The **Caesar Cipher** is one of history's earliest known encryption techniques, used by Julius Caesar to protect sensitive military correspondence. Each letter in the plaintext is shifted a fixed number of positions along the alphabet.

This project transforms a basic Python script into a **professional, full-stack application** featuring:

- 🔒 **Encrypt** — Shift plaintext by a secret key (1–25)
- 🗝 **Decrypt** — Recover plaintext with the correct key
- 🔍 **Brute-Force Analysis** — Rank all 25 possible keys using frequency analysis
- 🌐 **Web Interface** — Elegant, responsive frontend with live alphabet visualiser
- 🛠 **REST API** — Clean Flask endpoints for programmatic access
- ✅ **Test Suite** — Full pytest coverage of all core logic

---

## Project Structure

```
caesar-cipher/
├── backend/
│   ├── cipher.py          # Core cryptography module (encrypt, decrypt, brute-force)
│   └── app.py             # Flask REST API server
├── frontend/
│   └── index.html         # Standalone web interface (works with or without Flask)
├── tests/
│   └── test_cipher.py     # pytest test suite
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/your-username/caesar-cipher.git
cd caesar-cipher
pip install -r requirements.txt
```

### 2. Run the Web App

```bash
python backend/app.py
```

Then open your browser at → **http://localhost:5000**

### 3. Use the Standalone Frontend (no server required)

Simply open `frontend/index.html` directly in your browser. All cipher logic runs in JavaScript with no dependencies.

---

## REST API Reference

All endpoints accept and return `application/json`.

### POST `/api/encrypt`

Encrypt a plaintext string with a given shift.

**Request**
```json
{ "text": "Hello, World!", "shift": 3 }
```

**Response**
```json
{ "status": "success", "result": "Khoor, Zruog!", "shift": 3, "original": "Hello, World!" }
```

---

### POST `/api/decrypt`

Decrypt a ciphertext string with the correct shift.

**Request**
```json
{ "text": "Khoor, Zruog!", "shift": 3 }
```

**Response**
```json
{ "status": "success", "result": "Hello, World!", "shift": 3, "original": "Khoor, Zruog!" }
```

---

### POST `/api/brute-force`

Try all 25 shifts and return candidates ranked by English-language likelihood using letter-frequency analysis.

**Request**
```json
{ "text": "Khoor zruog" }
```

**Response**
```json
{
  "status": "success",
  "candidates": [
    { "shift": 3, "text": "Hello world", "score": 0.412 },
    { "shift": 16, "text": "Wtaad ldgas", "score": 0.198 },
    ...
  ]
}
```

---

## Python API

The `cipher.py` module can be used directly in your own code:

```python
from backend.cipher import encrypt, decrypt, brute_force

# Encrypt
ciphertext = encrypt("Hello, World!", shift=3)
# → "Khoor, Zruog!"

# Decrypt
plaintext = decrypt("Khoor, Zruog!", shift=3)
# → "Hello, World!"

# Brute-force analysis
candidates = brute_force("Khoor zruog")
print(candidates[0])
# → {'shift': 3, 'text': 'Hello world', 'score': 0.412}
```

### `encrypt(text, shift)`
| Parameter | Type | Description |
|-----------|------|-------------|
| `text`    | str  | Plaintext to encrypt |
| `shift`   | int  | Key: integer in [1, 25] |

Returns the encrypted string. Raises `ValueError` for invalid shift, `TypeError` for non-integer shift.

### `decrypt(text, shift)`
Same signature as `encrypt`. Returns the decrypted string.

### `brute_force(ciphertext)`
Returns a list of 25 dicts sorted by likelihood score (descending):
```python
[{"shift": int, "text": str, "score": float}, ...]
```

---

## Running Tests

```bash
python -m pytest tests/ -v
```

Expected output:

```
tests/test_cipher.py::TestEncrypt::test_basic_lowercase       PASSED
tests/test_cipher.py::TestEncrypt::test_wrap_around           PASSED
tests/test_cipher.py::TestEncrypt::test_preserves_punctuation PASSED
tests/test_cipher.py::TestDecrypt::test_roundtrip             PASSED
tests/test_cipher.py::TestBruteForce::test_correct_shift_ranks_first PASSED
...
```

---

## How It Works

### Encryption

Each alphabetic character is shifted forward by the key `k`:

```
E(x) = (x + k) mod 26
```

Non-alphabetic characters (spaces, punctuation, digits) are preserved unchanged. Case is maintained.

**Example — Shift 3:**
```
Plain:  A B C D E F ... X Y Z
Cipher: D E F G H I ... A B C
```

### Decryption

Reverse the shift:

```
D(x) = (x − k) mod 26
```

### Brute-Force Analysis

All 25 possible shifts are tried. Each candidate is scored by comparing its letter frequency distribution against standard English letter frequencies (`etaoinshrdlcumwfgypbvkjxqz`). The highest-scoring candidate is most likely to be the correct plaintext.

---

## Security Note

The Caesar cipher is a **classical educational cipher only** — it provides no meaningful modern security. With only 25 possible keys, it can be broken in milliseconds. For real-world encryption, use established standards such as **AES-256** via Python's [`cryptography`](https://cryptography.io/) library.

---

## License

MIT © 2026 — Caesar Cipher Project

---

*"If he had anything confidential to say, he wrote it in cipher — shifting each letter by three positions in the alphabet."*
— Suetonius, **De Vita Caesarum**, c. 121 AD
