from api.note import note_bp


@note_bp.route("/delete", methods=["DELETE"])
def noteDelete():
    return "/note/delete"
