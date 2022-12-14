from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

from .register import authRegister
from .login import authLogin
from .check import authCheck
