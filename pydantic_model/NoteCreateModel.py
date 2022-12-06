from pydantic import BaseModel
from pydantic_model.NoteModel import NoteModel


class NoteCreateModel(BaseModel):
    data: NoteModel
