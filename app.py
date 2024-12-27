# imports
from typing import Annotated, Any
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from database import *
import auth
from auth import get_current_user

SessionDep = Annotated[Session, Depends(get_session)]

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
@app.get("/api/user", status_code=status.HTTP_200_OK)
async def get_user(user: Annotated[dict, Depends(get_current_user)], session: SessionDep) -> dict:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return {"User": user}

@app.get("/api/users")
async def get_users(user: Annotated[dict, Depends(get_current_user)], session: SessionDep) -> list[User]:
    users: Any = session.exec(select(User)).all()
    return users


# todos related endpoints
@app.get("/api/todos")
async def get_todos(user: Annotated[dict, Depends(get_current_user)], session: SessionDep) -> list[User]:
    todos: Any = session.exec(select(Todo)).all()
    return todos


# studies related endpoints
@app.get("/api/studies")
async def get_studies(user: Annotated[dict, Depends(get_current_user)], session: SessionDep) -> list[User]:
    studies: Any = session.exec(select(Studies)).all()
    return studies