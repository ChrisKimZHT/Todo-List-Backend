from api.note import note_bp


@note_bp.route("/get", methods=["GET"])
def noteGet():
    return "/note/get"
