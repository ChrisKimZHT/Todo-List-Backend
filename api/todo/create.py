from api.todo import todo_bp


@todo_bp.route("/create", methods=["POST"])
def todoCreate():
    return "/todo/create"
