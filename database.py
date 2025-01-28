from typing import Annotated, Any, Generator
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/pomodoro_planner"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[sessionmaker, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
SessionDep = Annotated[Session, Depends(get_db)]