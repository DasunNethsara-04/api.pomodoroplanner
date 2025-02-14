# # imports
import datetime
from typing import Any
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, DateTime
from database import Base


class User(Base):
    '''User model for the database. This model contains the user's information.'''
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(20), index=True)
    lastName = Column(String(30), index=True)
    username = Column(String(50), index=True)
    password = Column(String(75), index=True)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "username": self.username,
            "password": self.password
        }

    
class Todo(Base):
    '''Todo model for the database. This model contains the todo information.'''
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String(50), index=True)
    description = Column(String(100), index=True, nullable=True)
    completed = Column(Boolean, default=False)
    dueDate = Column(Date, default=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "dueDate": self.dueDate,
            "created_at": self.created_at,
        }

    
class Studies(Base):
    '''Studies model for the database. This model contains the studies information.'''
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(DateTime, index=True, default=datetime.datetime.utcnow)
    hours = Column(Integer, index=True, default=0)
