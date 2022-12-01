from pydantic import BaseModel


class NoteModel(BaseModel):
    id: int
    title: str
    content: str
    date: int
    star: bool
