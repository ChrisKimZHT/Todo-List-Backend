from api.note import note_bp


@note_bp.route("/list", methods=["GET"])
def noteList():
    return "/note/list"
