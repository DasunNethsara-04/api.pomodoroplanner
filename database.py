from datetime import datetime
from sqlmodel import Field, SQLModel, Session, create_engine

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    username: str = Field(max_length=100)
    email: str = Field(max_length=100)
    password: str = Field(max_length=100)

class Todo(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(max_length=100)
    description: str = Field(max_length=100)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now())

class Studies(SQLModel, table=True):
    # This table contains how many hours a user worked in the particular date.
    id: int|None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: datetime = Field(default_factory=lambda: datetime.now())
    hours: int = Field(default=0)