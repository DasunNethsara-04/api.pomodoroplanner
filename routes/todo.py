from fastapi import APIRouter, Depends
from .auth import get_current_user
from database import SessionDep
from models import Todo
from typing import Annotated, List, Any
from exceptions import Exceptions
import schema

exception: Exceptions = Exceptions()

router: APIRouter = APIRouter(
    prefix="/todo",
    tags=['todo'],
)


@router.get("/")
async def get_todos(session: SessionDep, user: dict = Depends(get_current_user)) -> dict[str, list[dict[str, Any]]]:
    todos: List[Todo] = session.query(Todo).filter(Todo.user_id == user["id"]).all()
    return {"todos": [todo.to_dict() for todo in todos]}

@router.get("/{todo_id}")
async def get_todo_by_id(todo_id: str|int, session: SessionDep, user: Annotated[dict, Depends(get_current_user)]) -> dict[str, dict[str, Any]]:
    todo: Todo = session.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        exception.http_404_not_found_exception("Todo Not Found!")
    return {"todo": todo.to_dict()}

@router.post("/")
async def create_todo(todo: schema.CreateTodoRequest, session: SessionDep, user: Annotated[dict, Depends(get_current_user)])-> dict[str, str|bool]:
    new_todo: Todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        dueDate = todo.dueDate,
        created_at = todo.created_at,
        user_id=user["id"]
    )
    session.add(new_todo)
    session.commit()
    return {"success": True, "message": "New Todo Created Successfully!"}