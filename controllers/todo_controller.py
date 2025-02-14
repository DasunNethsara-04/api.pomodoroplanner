from models import Todo
from sqlalchemy.orm import Session
from schema import CreateTodoRequest
from exceptions import Exceptions


class TodoController:

    def __init__(self) -> None:
        pass

    def get_todos(self, session: Session, user_id: int | str):
        return session.query(Todo).filter(Todo.user_id == user_id).all()

    def get_todo_by_id(self, session: Session, todo_id: int | str) -> Todo | None:
        return session.query(Todo).filter(Todo.id == todo_id).first()

    def create_todo(self, session: Session, todo: CreateTodoRequest, user_id: int | str) -> Todo:
        new_todo: Todo = Todo(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            dueDate=todo.dueDate,
            created_at=todo.created_at,
            user_id=user_id,
        )
        session.add(new_todo)
        session.commit()
        return new_todo
    
    def update_todo(self, session: Session, todo_id: int | str, todo_req: CreateTodoRequest, user_id: int | str) -> Todo:
        todo: Todo = session.query(Todo).filter(Todo.id == todo_id).first()
        if todo is None:
            Exceptions().http_404_not_found_exception("Todo Not Found!")
        if todo.user_id != user_id:
            Exceptions().http_401_unauthorized_exception("Unauthorized User!")
        
        todo.title = todo_req.title
        todo.description = todo_req.description
        todo.completed = todo_req.completed
        todo.dueDate = todo_req.dueDate
        
        session.commit()
        session.refresh(todo)
        return todo
    
    def delete_todo(self, session: Session, todo_id: int | str):
        try:
            todo: Todo = session.query(Todo).filter(Todo.id == todo_id).first()

            if todo is None:
                Exceptions().http_404_not_found_exception("Todo not found!")
                return False
            session.delete(todo)
            session.commit()
            return True
        except Exception:
            return False
