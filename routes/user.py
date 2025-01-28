from typing import Annotated
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from models import User
from .auth import get_current_user
from starlette import status
from exceptions import Exceptions

exception: Exceptions = Exceptions()


router: APIRouter = APIRouter(
    prefix="/user",
    tags=['user'],
)


# users related endpoints
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: Annotated[dict, Depends(get_current_user)], session: Annotated[Session, Depends[get_db]]) -> dict[str, dict[str, str]]:
    if user is None:
        exception.http_401_unauthorized_exception("Unauthorized User!")
    return {"User": user}

@router.get("/all")
async def get_users(user: Annotated[dict, Depends(get_current_user)], session: Annotated[Session, Depends[get_db]]) -> list[str, User]:
    users: list[User] = session.query(User).all()
    return {"User": users}
