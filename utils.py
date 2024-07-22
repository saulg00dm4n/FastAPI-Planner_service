from fastapi import Depends
from fastapi import HTTPException
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, encode, decode
from hashlib import sha256
from sqlmodel import select, Session

from db import get_session
from models import User


SECRET_KEY = "krokodily_begayt_vkrasovkah"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_error = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}, )


def create_access_token(data: dict, exp: timedelta = None):
    to_encode = data.copy()
    if exp:
        expire = datetime.utcnow() + exp
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_error
        user = session.exec(select(User).where(User.id == user_id)).first()
        if user is None:
            raise credentials_error
        return user
    except PyJWTError:
        raise credentials_error


def hash_password(password: str):
    return sha256(password.encode()).hexdigest()    # хеширование паролей