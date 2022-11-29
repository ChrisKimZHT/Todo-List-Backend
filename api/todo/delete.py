from api.todo import todo_bp


@todo_bp.route("/delete", methods=["DELETE"])
def todoDelete():
    return "/todo/delete"
