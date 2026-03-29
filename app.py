"""
Caesar Cipher — Flask REST API
================================
Exposes /api/encrypt, /api/decrypt, and /api/brute-force endpoints
that the frontend communicates with.

Usage (development):
    pip install flask flask-cors
    python app.py
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Make sure the backend package is importable when run from project root
sys.path.insert(0, os.path.dirname(__file__))
from cipher import encrypt, decrypt, brute_force

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_json_field(data: dict, field: str):
    value = data.get(field)
    if value is None:
        raise ValueError(f"Missing required field: '{field}'.")
    return value


def _success(payload: dict):
    return jsonify({"status": "success", **payload})


def _error(message: str, code: int = 400):
    return jsonify({"status": "error", "message": message}), code


# ---------------------------------------------------------------------------
# Routes — static frontend
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ---------------------------------------------------------------------------
# Routes — API
# ---------------------------------------------------------------------------

@app.route("/api/encrypt", methods=["POST"])
def api_encrypt():
    """
    POST /api/encrypt
    Body (JSON): { "text": str, "shift": int }
    Returns    : { "status": "success", "result": str, "shift": int }
    """
    data = request.get_json(silent=True) or {}
    try:
        text = _get_json_field(data, "text")
        shift = int(_get_json_field(data, "shift"))
        result = encrypt(str(text), shift)
    except (TypeError, ValueError) as exc:
        return _error(str(exc))

    return _success({"result": result, "shift": shift, "original": text})


@app.route("/api/decrypt", methods=["POST"])
def api_decrypt():
    """
    POST /api/decrypt
    Body (JSON): { "text": str, "shift": int }
    Returns    : { "status": "success", "result": str, "shift": int }
    """
    data = request.get_json(silent=True) or {}
    try:
        text = _get_json_field(data, "text")
        shift = int(_get_json_field(data, "shift"))
        result = decrypt(str(text), shift)
    except (TypeError, ValueError) as exc:
        return _error(str(exc))

    return _success({"result": result, "shift": shift, "original": text})


@app.route("/api/brute-force", methods=["POST"])
def api_brute_force():
    """
    POST /api/brute-force
    Body (JSON): { "text": str }
    Returns    : { "status": "success", "candidates": list[dict] }
    """
    data = request.get_json(silent=True) or {}
    try:
        text = _get_json_field(data, "text")
        candidates = brute_force(str(text))
    except (TypeError, ValueError) as exc:
        return _error(str(exc))

    return _success({"candidates": candidates[:10]})  # Return top 10


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    print(f"  Caesar Cipher API running → http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
