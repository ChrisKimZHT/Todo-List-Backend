from pydantic import BaseModel
from request_model.TodoModel import TodoModel


class TodoCreateModel(BaseModel):
    data: TodoModel
