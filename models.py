# # imports
# from datetime import datetime
# from sqlmodel import Field, SQLModel, Session, create_engine, select

# # database models
# class User(SQLModel, table=True):
#     '''User model for the database. This model contains the user's information.'''
#     id: int = Field(primary_key=True, default=None)
#     firstName: str = Field(max_length=100)
#     lastName: str = Field(max_length=100)
#     username: str = Field(max_length=100)
#     password: str = Field(max_length=100)

# class Todo(SQLModel, table=True):
#     '''Todo model for the database. This model contains the todo information.'''
#     id: int|None = Field(default=None, primary_key=True)
#     user_id: int = Field(foreign_key="user.id")
#     title: str = Field(max_length=100)
#     description: str = Field(max_length=100)
#     completed: bool = Field(default=False)
#     created_at: datetime = Field(default_factory=lambda: datetime.now())

# class Studies(SQLModel, table=True):
#     '''Studies model for the database. This model contains the studies information.'''
#     id: int|None = Field(default=None, primary_key=True)
#     user_id: int = Field(foreign_key="user.id")
#     date: datetime = Field(default_factory=lambda: datetime.now())
#     hours: int = Field(default=0)


import datetime
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
    
class Todo(Base):
    '''Todo model for the database. This model contains the todo information.'''
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String(50), index=True)
    description = Column(String(100), index=True, nullable=True)
    completed = Column(Boolean, default=False)
    dueDate = Column(Date, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
class Studies(Base):
    '''Studies model for the database. This model contains the studies information.'''
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(DateTime, index=True, default=datetime.datetime.utcnow)
    hours = Column(Integer, index=True, default=0)