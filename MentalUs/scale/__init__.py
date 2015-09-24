from flask import Blueprint

scale = Blueprint('scale', __name__)

from . import views