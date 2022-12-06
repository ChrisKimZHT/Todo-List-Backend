from pydantic import BaseModel
from pydantic_model.NoteModel import NoteModel


class NoteUpdateModel(BaseModel):
    data: NoteModel
