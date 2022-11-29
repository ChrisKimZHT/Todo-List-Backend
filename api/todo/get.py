from api.todo import todo_bp


@todo_bp.route("/get", methods=["GET"])
def todoGet():
    return "/todo/get"
