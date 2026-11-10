# # regret/backend/security/hashing.py
# backend/security/hashing.py

from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Accepts a plain password and returns its secure hash.
    """

    hashed_password = password_hash.hash(password)

    return hashed_password