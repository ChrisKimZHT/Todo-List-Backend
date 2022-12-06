from pydantic import BaseModel
from pydantic_model.TodoModel import TodoModel


class TodoUpdateModel(BaseModel):
    data: TodoModel
