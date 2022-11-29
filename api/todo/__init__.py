from flask import Blueprint

todo_bp = Blueprint("todo", __name__, url_prefix="/todo")

from .create import todoCreate
from .nextID import todoNextID
from .delete import todoDelete
from .update import todoUpdate
from .list import todoList
from .get import todoGet
from .toggleFinish import todoToggleFinish
