from typing import Annotated, Any, Generator, LiteralString
from models import *

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