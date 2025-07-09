# utils/encryption.py

from cryptography.fernet import Fernet
import os

KEY_FILE = "utils/secret.key"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_note(note: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(note.encode()).decode()

def decrypt_note(encrypted_note: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_note.encode()).decode()
