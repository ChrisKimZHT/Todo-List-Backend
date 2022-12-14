from flask import Flask, jsonify
from api.todo import todo_bp
from api.note import note_bp
from api.auth import auth_bp
from flask_cors import CORS
from flask_migrate import Migrate
from ext import db
import configs

app = Flask(__name__)
app.config.from_object(configs)
app.secret_key = app.config["FLASK_SECRET_KEY"]
CORS(app, supports_credentials=True)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.errorhandler(400)
def internal_server_error(e):  # 400 Bad Request
    return jsonify(status=1, message=str(e)), 400


@app.errorhandler(401)
def internal_server_error(e):  # 401 Unauthorized
    return jsonify(status=1, message=str(e)), 401


@app.errorhandler(500)
def internal_server_error(e):  # 500 Internal Server Error
    return jsonify(status=1, message=str(e)), 500


app.register_blueprint(todo_bp)
app.register_blueprint(note_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run()
