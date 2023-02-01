"""
Flask application for experience puposes
"""
from flask import Blueprint


# recommended to be named same as the file but not mandatory
second = Blueprint("second", __name__, static_folder= "static", template_folder="templates")

@second.route("/test")
def test():
    """
    Blueprint test route
    """
    return "<p>hola</p>"
