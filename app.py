# imports
from typing import Annotated, Any, List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import auth
from auth import get_current_user
from models import User, Todo, Studies
from base_models import CreateTodoRequest

# FastAPI app
app: FastAPI = FastAPI()
app.include_router(auth.router)

app.add_middleware(CORSMiddleware,
                    allow_origins=['*'],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                   )

@app.on_event("startup")
async def on_startup() -> None:
    models.Base.metadata.create_all(bind=engine)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
SessionDep = Annotated[Session, Depends(get_db)]
    
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
async def get_user(user: Annotated[dict, Depends(get_current_user)], session: SessionDep) -> dict[str, dict[str, str]]:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return {"User": user}

@app.get("/api/users")
async def get_users(user: Annotated[dict, Depends(get_current_user)], session: SessionDep) -> list[str, User]:
    users: list[User] = session.query(User).all()
    return {"User": user}

# todos related endpoints
@app.get("/api/todos")
async def get_todos(session: SessionDep, user: dict = Depends(get_current_user)) -> dict[str, list[dict[str, Any]]]:
    todos: List[Todo] = session.query(Todo).filter(Todo.user_id == user["id"]).all()
    return {"todos": [todo.to_dict() for todo in todos]}


@app.post("/api/todo/")
async def create_todo(todo: CreateTodoRequest, session: SessionDep, user: Annotated[dict, Depends(get_current_user)])-> dict[str, str|bool]:
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

# studies related endpoints
@app.get("/api/studies")
async def get_studies(user: Annotated[dict, Depends(get_current_user)], session: SessionDep) -> dict:
    studies: list[Studies] = session.query(Studies).filter(Studies.user_id == user["id"]).all()
    return {"studies": studies}