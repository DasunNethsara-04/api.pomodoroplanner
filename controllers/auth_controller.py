from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import timedelta, datetime
from exceptions import Exceptions
from fastapi import HTTPException
from schema import CreateUserRequest
from .user_controller import UserController


class AuthController:

    def __init__(self) -> None:
        pass
    
    def authenticate_user(self, username: str, password: str, db:Session, bcrypt_context: CryptContext):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.password):
            return False
        return user

    def create_access_token(self, username: str, id: int | str, expires_delta, ALGORITHM:str, SECRET_KEY: str) -> dict[str]:
        encode: dict = {"sub": username, "id": id}
        expires = datetime.utcnow() + expires_delta
        encode.update({"exp": expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str, SECRET_KEY: str, ALGORITHM: str) -> dict[str, str] | HTTPException:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                Exceptions().http_403_forbidden_exception("Token is invalid or expired")
            return payload

        except JWTError:
            Exceptions().http_403_forbidden_exception("Token is invalid or expired")

    def get_user_by_username(self, db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()

    def get_current_user(self, token: str, SECRET_KEY: str, ALGORITHM: str) -> dict[str, str] | HTTPException:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int | str = payload.get("id")
            if username is None or user_id is None:
                Exceptions().http_401_unauthorized_exception("Could not validate credentials")
            return {"username": username, "id": user_id}

        except JWTError:
            Exceptions().http_401_unauthorized_exception("Could not validate credentials")

    def register_user(self, db: Session, create_user_request:CreateUserRequest, bcrypt_context: CryptContext, SECRET_KEY: str, ALGORITHM: str):
        db_user = self.get_user_by_username(db, create_user_request.username)
        if db_user:
            Exceptions().http_400_bad_request_exception("Username already registered")
        user = UserController().create_user(db, create_user_request, bcrypt_context)
        token = self.create_access_token(create_user_request.username, user.id, timedelta(minutes=60), ALGORITHM, SECRET_KEY)
        return {"access_token": token, "token_type": "bearer"}
    
    def login(self, form_data: dict, db: Session, bcrypt_context: CryptContext, SECRET_KEY: str, ALGORITHM: str):
        user = self.authenticate_user(form_data.username, form_data.password, db, bcrypt_context)
        if not user:
            Exceptions().http_401_unauthorized_exception("Could not validate credentials")
        token = self.create_access_token(user.username, user.id, timedelta(minutes=60), ALGORITHM, SECRET_KEY)
        return {"access_token": token, "token_type": "bearer"}
