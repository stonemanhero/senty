import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derives a Fernet key from the provided password and salt.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_text(plain_text: str, key: bytes) -> str:
    """
    Encrypts a plain text string using the provided key.
    """
    if plain_text is None:
        return ""
    f = Fernet(key)
    encrypted = f.encrypt(plain_text.encode())
    return encrypted.decode()

def decrypt_text(encrypted_text: str, key: bytes) -> str:
    """
    Decrypts an encrypted string using the provided key.
    """
    if not encrypted_text:
        return ""
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_text.encode())
    return decrypted.decode()
