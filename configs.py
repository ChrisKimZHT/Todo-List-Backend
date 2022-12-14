from dotenv import load_dotenv
import os

load_dotenv()

FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_EXP_DELTA = 86400

USERNAME_LEN_MIN = 3
USERNAME_LEN_MAX = 16
PASSWORD_LEN_MIN = 6
PASSWORD_LEN_MAX = 16
