# imports
from datetime import timedelta, datetime
from typing import Annotated, Any, Generator
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from database import Session, User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from database import *


SECRET_KEY: str = "KEY"
ALGORITHM: str = "HS256"
bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="auth/token")

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

SessionDep = Annotated[Session, Depends(get_session)]

def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session

def authenticate_user(username: str, password: str, db: SessionDep) -> dict[User] | bool :
    user = db.exec(select(User).filter(User.username == username)).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, id: int|str, expires_delta: timedelta) -> dict[str, Any]:
    encode: dict = {"sub": username, "id": id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict[str, str] | HTTPException:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int|str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: SessionDep, create_user_request: CreateUserRequest) -> None:
    create_user_model: User = User(
        username= create_user_request.username,
        email=create_user_request.email,
        password=bcrypt_context.hash(create_user_request.password),
    )
    
    db.add(create_user_model)
    db.commit()
    
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep) -> dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    token = create_access_token(user.username, user.id, timedelta(minutes=15))
    return {"access_token": token, "token_type": "bearer"}
    