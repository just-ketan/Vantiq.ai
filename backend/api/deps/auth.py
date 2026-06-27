## Auth dependency

from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.config import settings
from api.deps.db import get_db
from models.user import User
from uuid import UUID

from uuid import UUID
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.deps.db import get_db
from core.config import settings
from models.user import User
from core.logger import logger

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)

from uuid import UUID

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    logger.debug("JWT received")

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        logger.debug("JWT decoded successfully")

        user_id = payload.get("sub")
        print("USER ID:", user_id)

        if user_id is None:
            raise credentials_exception

    except JWTError as e:
        print("JWT ERROR:", e)
        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.id == UUID(user_id))
        .first()
    )

    logger.info(
        "Authenticated user %s",
        user.email,
    )

    if user is None:
        raise credentials_exception

    return user

