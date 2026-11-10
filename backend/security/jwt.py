# # regret/backend/security/jwt.py




import os
import uuid

from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv




load_dotenv("backend/.env")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is missing from .env")

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
)

REFRESH_TOKEN_EXPIRE_HOURS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_HOURS", "24")
)


# creating access token


def create_access_token(user_id: int) :

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "jti": str(uuid.uuid4())
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# refresh token

def create_refresh_token(user_id: int) :

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(
            hours=REFRESH_TOKEN_EXPIRE_HOURS
        ),
        "jti": str(uuid.uuid4())
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


#  decoding and verifying tken

def decode_token(token: str) :

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={
            "require": [
                "sub",
                "type",
                "iat",
                "exp",
                "jti"
            ]
        }
    )

    return payload


# ==================================
# VERIFY TOKEN TYPE
# ==================================

def verify_token_type(
    payload: dict,
    expected_type: str
) -> bool:

    if payload.get("type") != expected_type:
        raise ValueError("Invalid token type")

    return True















