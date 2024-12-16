import select
from typing import Annotated, Any, Generator, LiteralString
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import User, Todo, Studies, SQLModel, Session, create_engine

sqlite_file_name: str = "database.db"
sqlite_uri: LiteralString = f"sqlite:///{sqlite_file_name}"
connect_args: dict[str, bool] = {"check_same_thread": False}
engine = create_engine(sqlite_uri, connect_args=connect_args, echo=True)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

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

@app.get("/api/author")
async def author() -> dict[str, str]:
    return {"message": "Pomodoro Planner API by Dasun Nethsara @DasunNethsara-04"}

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