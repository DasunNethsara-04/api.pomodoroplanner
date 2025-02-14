from schema import CreateUserRequest
from sqlalchemy.orm import Session
from models import User
from passlib.context import CryptContext


class UserController:

    def __init__(self) -> None:
        pass

    def get_users(self, session: Session):
        return session.query(User).all()
    
    def create_user(self, session: Session, user_req: CreateUserRequest, bcrypt_context: CryptContext) -> User:
        user: User = User(
            firstName=user_req.firstName,
            lastName=user_req.lastName,
            username=user_req.username,
            password=bcrypt_context.hash(user_req.password)
        )
        session.add(user)
        session.commit()
        return user
    
