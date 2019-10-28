import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from cs411_project.db import get_db

index_blueprint = Blueprint("index", __name__ ,template_folder='templates')

@index_blueprint.route("/")
def test1():
    db = get_db()
    db.execute(
        'INSERT INTO User(Id, FirstName, LastName, Email, Password) VALUES (?, ?, ?, ?, ?)',
        (1, "Bob", "Smith", "bob@smith.com", "password")
    )
    db.commit()

    return render_template("hello.html")


@index_blueprint.route("/woo")
def test2():
    db = get_db()
    db.execute(
        'SELECT * FROM User'
    )
    

    return render_template("hello.html")


