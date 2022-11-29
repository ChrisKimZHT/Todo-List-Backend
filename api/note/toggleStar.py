from api.note import note_bp


@note_bp.route("/toggleStar", methods=["GET"])
def noteToggleStar():
    return "/todo/toggleStar"
