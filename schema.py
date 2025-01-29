from pydantic import BaseModel
import datetime


# base models
class CreateUserRequest(BaseModel):
    firstName: str
    lastName: str
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    

# base models
class CreateTodoRequest(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool | None = False
    dueDate: str
    created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
