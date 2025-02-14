# imports
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from controllers import AuthController, UserController
from database import get_db
from models import User
import schema
from exceptions import Exceptions
from sqlalchemy.orm import Session

SECRET_KEY: str = "KEY"
ALGORITHM: str = "HS256"
bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="auth/token")

exception: Exceptions = Exceptions()
auth_controller: AuthController = AuthController()
user_controller: UserController = UserController

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict[str, str] | HTTPException:
    return auth_controller.get_current_user(token, SECRET_KEY, ALGORITHM)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(db: Annotated[Session, Depends(get_db)], create_user_request: schema.CreateUserRequest) -> dict[str, str]:
    return auth_controller.register_user(db, create_user_request, bcrypt_context, SECRET_KEY, ALGORITHM)


@router.post("/token", response_model=schema.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]) -> dict[str, str]:
    return auth_controller.login(form_data, db, bcrypt_context, SECRET_KEY, ALGORITHM)


@router.get("/verify-token/{token}")
def verify_user_token(token: str) -> dict[str, str]:
    if auth_controller.verify_token(token, SECRET_KEY, ALGORITHM) is None:
        exception.http_403_forbidden_exception("Token is invalid or expired")
    return {"message": "Token is valid"}
