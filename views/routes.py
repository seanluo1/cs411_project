from flask import render_template, Flask, Blueprint
from models import User

index_blueprint = Blueprint("index", __name__ ,template_folder='templates')

@index_blueprint.route("/")
def test1():
    return render_template("hello.html")

