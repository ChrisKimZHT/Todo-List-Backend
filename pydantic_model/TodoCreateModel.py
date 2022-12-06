from pydantic import BaseModel
from pydantic_model.TodoModel import TodoModel


class TodoCreateModel(BaseModel):
    data: TodoModel
