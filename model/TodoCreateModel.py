from pydantic import BaseModel
from model.TodoModel import TodoModel


class TodoCreateModel(BaseModel):
    data: TodoModel
