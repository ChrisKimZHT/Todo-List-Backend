from api.todo import todo_bp


@todo_bp.route("/list", methods=["GET"])
def todoList():
    return "/todo/list"
