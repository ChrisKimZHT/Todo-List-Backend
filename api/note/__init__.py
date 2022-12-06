from flask import Blueprint

note_bp = Blueprint("note", __name__, url_prefix="/note")

from .create import noteCreate
from .delete import noteDelete
from .update import noteUpdate
from .list import noteList
from .get import noteGet
from .toggleStar import noteToggleStar
