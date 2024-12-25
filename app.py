# imports
from typing import Annotated, Any, Generator, LiteralString
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from database import *

# database connection
sqlite_file_name: str = "database.db"
sqlite_uri: LiteralString = f"sqlite:///{sqlite_file_name}"
connect_args: dict[str, bool] = {"check_same_thread": False}
engine = create_engine(sqlite_uri, connect_args=connect_args, echo=True)

# create database and tables
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# FastAPI app
app: FastAPI = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

@app.on_event("startup")
async def on_startup() -> None:
    create_db_and_tables()

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
@app.get("/api/users")
async def get_users(session: SessionDep) -> list[dict]:
    users: Any = session.exec(select(User)).all()
    return users


# todos related endpoints
@app.get("/api/todos")
async def get_todos(session: SessionDep) -> list[dict]:
    todos: Any = session.exec(select(Todo)).all()
    return todos


# studies related endpoints
@app.get("/api/studies")
async def get_studies(session: SessionDep) -> list[dict]:
    studies: Any = session.exec(select(Studies)).all()
    return studies