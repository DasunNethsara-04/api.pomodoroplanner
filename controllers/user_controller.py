from typing import List
from sqlalchemy.orm import Session
from models import User


class UserController:

    def __init__(self) -> None:
        pass

    def get_users(self, session: Session):
        return session.query(User).all()
    
