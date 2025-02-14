# imports
from typing import Annotated, Any, List
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from database import engine, get_db
from sqlalchemy.orm import Session
import models
import auth
from models import User, Todo, Studies
import schema
from auth import get_current_user
from exceptions import Exceptions
from controllers import TodoController, UserController, StudiesController

# FastAPI app
app: FastAPI = FastAPI()
app.include_router(auth.router)

app.add_middleware(CORSMiddleware,
                    allow_origins=['*'],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                   )

# required classes
exception: Exceptions = Exceptions()
todo_controller: TodoController = TodoController()
user_controller: UserController = UserController()
studies_controller: StudiesController = StudiesController()


@app.on_event("startup")
async def on_startup() -> None:
    models.Base.metadata.create_all(bind=engine)

    
@app.get("/api/")
async def index() -> dict[str, str]:
    return {"message": "This is a Response from FastAPI from Vercel"}


@app.get("/api/info")
async def info() -> dict[str, str]:
    return {
        "app_name": "Pomodoro Planner",
        "app_version": "1.0.0",
        "app_description": "Pomodoro Planner API for Pomodoro Planner App",
        "app_author": "Dasun Nethsara",
        "app_author_website": "http://techsaralk.epizy.com/",
        "app_author_github": "https://github.com/DasunNethsara-04/"
    }


# users related endpoints
@app.get("/api/user", status_code=status.HTTP_200_OK)
async def get_user(user: Annotated[dict, Depends(get_current_user)],
                   session: Annotated[Session, Depends(get_db)]
                   ) -> dict:
    if user is None:
        exception.http_401_unauthorized_exception("Unauthorized User!")
    return {"User": user}


@app.get("/api/users")
async def get_users(user: Annotated[dict, Depends(get_current_user)],
                    session: Annotated[Session, Depends(get_db)]
                    ) -> dict:
    if user is None:
        exception.http_401_unauthorized_exception("Unauthorized User!")
    users: List[User] = user_controller.get_users(session)
    return {"users": [user.to_dict() for user in users]}


# todos related endpoints
@app.get("/api/todos")
async def get_todos(session: Annotated[Session, Depends(get_db)],
                    user: dict=Depends(get_current_user)
                    ) -> dict[str, list[dict[str, Any]]]:
    todos: List[Todo] = session.query(Todo).filter(Todo.user_id == user["id"]).all()
    return {"todos": [todo.to_dict() for todo in todos]}


@app.get("/api/todo/{todo_id}")
async def get_todo_by_id(todo_id: str | int, session: Annotated[Session, Depends(get_db)], user: Annotated[dict, Depends(get_current_user)]) -> dict[str, dict[str, Any]]:
    todo: Todo = session.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        exception.http_404_not_found_exception("Todo Not Found!")
    return {"todo": todo.to_dict()}


@app.post("/api/todo/")
async def create_todo(todo: schema.CreateTodoRequest, session: Annotated[Session, Depends(get_db)], user: Annotated[dict, Depends(get_current_user)]) -> dict[str, str | bool]:
    new_todo: Todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        dueDate=todo.dueDate,
        created_at=todo.created_at,
        user_id=user["id"]
    )
    session.add(new_todo)
    session.commit()
    return {"success": True, "message": "New Todo Created Successfully!"}


@app.put("/api/todo/{todo_id}")
async def update_todo(todo_id: int | str, todo_req: schema.CreateTodoRequest, session: Annotated[Session, Depends(get_db)], user: Annotated[dict, Depends(get_current_user)]) -> dict[str, str | bool | dict[str, Any]]:
    todo: Todo = session.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        exception.http_404_not_found_exception("Todo Not Found!")
    if todo.user_id != user["id"]:
        exception.http_401_unauthorized_exception("Unauthorized User!")
        
    todo.title = todo_req.title
    todo.description = todo_req.description
    todo.completed = todo_req.completed
    todo.dueDate = todo_req.dueDate
    
    session.commit()
    session.refresh(todo)
    return {"success": True, "message": "Todo Updated Successfully!", "todo": todo.to_dict()}


@app.delete("/api/todo/{todo_id}")
async def delete_todo(todo_id: int | str, session: Annotated[Session, Depends(get_db)], user: Annotated[dict, Depends(get_current_user)]) -> dict[str, str | bool]:
    todo: Todo = session.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        exception.http_404_not_found_exception("Todo not found!")
    session.delete(todo)
    session.commit()
    return {"success":True, "message":"Todo deleted successfully!"}


# studies related endpoints
@app.get("/api/studies")
async def get_studies(user: Annotated[dict, Depends(get_current_user)], session: Annotated[Session, Depends(get_db)]) -> dict:
    studies: list[Studies] = session.query(Studies).filter(Studies.user_id == user["id"]).all()
    return {"studies": studies}
