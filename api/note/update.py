from api.note import note_bp


@note_bp.route("/update", methods=["POST"])
def noteUpdate():
    return "/note/update"
