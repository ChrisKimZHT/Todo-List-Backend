from api.todo import todo_bp


@todo_bp.route("/toggleFinish", methods=["GET"])
def todoToggleFinish():
    return "/todo/toggleFinish"
