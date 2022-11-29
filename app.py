from flask import Flask
from api.todo import todo_bp
from api.note import note_bp

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.register_blueprint(todo_bp)
app.register_blueprint(note_bp)

if __name__ == '__main__':
    app.run()
