from pydantic import BaseModel
from model.TodoModel import TodoModel


class TodoUpdateModel(BaseModel):
    data: TodoModel
