# imports
from datetime import timedelta, datetime
from typing import Annotated, Any, Generator
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from database import Session, User, create_engine
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from database import *
# sql


# base models
class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

SECRET_KEY: str = "KEY"
ALGORITHM: str = "HS256"
bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: SessionDep, create_user_request: CreateUserRequest):
    create_user_model: User = User(
        username= create_user_request.username,
        email=create_user_request.email,
        password=bcrypt_context.hash(create_user_request.password),
    )
    
    db.add(create_user_model)
    db.commit()
    
