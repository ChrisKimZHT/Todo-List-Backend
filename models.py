from ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    todos = db.relationship("Todo", backref="user", lazy="dynamic")
    notes = db.relationship("Note", backref="user", lazy="dynamic")

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(255))
    detail = db.Column(db.Text)
    begin = db.Column(db.Integer)
    end = db.Column(db.Integer)
    isDeadLine = db.Column(db.Boolean)
    isFinished = db.Column(db.Boolean)

    def __init__(self, userID, title, detail, begin, end, isDeadLine, isFinished):
        self.userID = userID
        self.title = title
        self.detail = detail
        self.begin = begin
        self.end = end
        self.isDeadLine = isDeadLine
        self.isFinished = isFinished


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date = db.Column(db.Integer)
    isStared = db.Column(db.Boolean)

    def __init__(self, userID, title, content, date, isStared):
        self.userID = userID
        self.title = title
        self.content = content
        self.date = date
        self.isStared = isStared
