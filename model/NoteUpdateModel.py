from pydantic import BaseModel
from model.NoteModel import NoteModel


class NoteUpdateModel(BaseModel):
    data: NoteModel
