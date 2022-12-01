from pydantic import BaseModel
from model.NoteModel import NoteModel


class NoteCreateModel(BaseModel):
    data: NoteModel
