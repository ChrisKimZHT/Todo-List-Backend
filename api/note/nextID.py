from api.note import note_bp


@note_bp.route("/nextID", methods=["GET"])
def noteNextID():
    return "/note/nextID"
