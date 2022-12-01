from pydantic import BaseModel


class TodoModel(BaseModel):
    id: int
    title: str
    detail: str
    begin: int
    end: int
    isDeadLine: bool
    isFinished: bool
