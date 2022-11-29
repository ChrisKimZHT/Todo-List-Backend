from api.note import note_bp


@note_bp.route("/create", methods=["POST"])
def noteCreate():
    return "/note/create"
