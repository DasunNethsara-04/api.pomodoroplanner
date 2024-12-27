# imports
from datetime import datetime
from sqlmodel import Field, SQLModel, Session, create_engine, select

# database models
class User(SQLModel, table=True):
    '''User model for the database. This model contains the user's information.'''
    id: int = Field(primary_key=True, default=None)
    username: str = Field(max_length=100)
    email: str = Field(max_length=100)
    password: str = Field(max_length=100)

class Todo(SQLModel, table=True):
    '''Todo model for the database. This model contains the todo information.'''
    id: int|None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(max_length=100)
    description: str = Field(max_length=100)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now())

class Studies(SQLModel, table=True):
    '''Studies model for the database. This model contains the studies information.'''
    id: int|None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: datetime = Field(default_factory=lambda: datetime.now())
    hours: int = Field(default=0)