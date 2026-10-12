import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=salt, iterations=200_000)
    return kdf.derive(password.encode())

def encrypt(plaintext: str, password: str) -> str:
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt)
    ct = AESGCM(key).encrypt(nonce, plaintext.encode(), None)
    blob = salt + nonce + ct
    return base64.b64encode(blob).decode()

def decrypt(token: str, password: str) -> str:
    blob = base64.b64decode(token)
    salt, nonce, ct = blob[:16], blob[16:28], blob[28:]
    key = derive_key(password, salt)
    return AESGCM(key).decrypt(nonce, ct, None).decode()
