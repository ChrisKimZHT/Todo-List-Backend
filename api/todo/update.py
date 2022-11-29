from api.todo import todo_bp


@todo_bp.route("/update", methods=["POST"])
def todoUpdate():
    return "/todo/update"
