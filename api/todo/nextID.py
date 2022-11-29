from api.todo import todo_bp


@todo_bp.route("/nextID", methods=["GET"])
def todoNextID():
    return "/todo/nextID"
