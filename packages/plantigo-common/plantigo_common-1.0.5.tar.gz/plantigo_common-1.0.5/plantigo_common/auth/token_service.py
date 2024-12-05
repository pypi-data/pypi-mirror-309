from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from jose import jwt, JWTError


def verify_token(token: str, jwt_secret_key: str, jwt_algorithm: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])
        user_id: UUID = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
